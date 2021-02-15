from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, fields

from kit_people.models import Role, KitPerson, Interaction, WEEK_DAYS, Regularity


class RoleSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(RoleSerializer, self).create(validated_data)

    class Meta:
        model = Role
        fields = '__all__'
        extra_kwargs = {"user": {"read_only": True}}


class RegularitySerializer(serializers.ModelSerializer):
    week_days = fields.MultipleChoiceField(choices=WEEK_DAYS, required=False)

    class Meta:
        model = Regularity
        fields = '__all__'


class KitPersonSerializer(serializers.ModelSerializer):
    regularity = RegularitySerializer(required=False)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        regularity_data = validated_data.pop('regularity', None)
        kit_person = KitPerson.objects.create(**validated_data)
        regularity = Regularity.objects.create(**regularity_data, kit_person=kit_person)
        return kit_person

    def update(self, instance, validated_data):

        instance.role = validated_data.get('role', instance.role)
        instance.name = validated_data.get('name', instance.name)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.contact = validated_data.get('contact', instance.contact)
        instance.user = validated_data.get('user', instance.user)
        instance.birthday = validated_data.get('birthday', instance.birthday)
        instance.chatApp = validated_data.get('chatApp', instance.chatApp)
        instance.save()

        regularity_data = validated_data.get('regularity', None)
        try:
            regularity = instance.regularity
        except ObjectDoesNotExist:
            regularity = None

        if regularity_data is not None:
            if regularity is None:
                regularity = Regularity()
            regularity.notification_type = regularity_data.get('notification_type')
            regularity.week_days = regularity_data.get('week_days')
            regularity.times_a_week = regularity_data.get('times_a_week')
            regularity.time_of_month = regularity_data.get('time_of_month')
            regularity.reminder = regularity_data.get('reminder')
            regularity.kit_person = instance
            regularity.save()

        return instance

    def validate(self, data):
        """
        Check that there are only required fields for particular notification type.
        """
        if data.get('regularity') is not None:
            regularity = data['regularity']
            notification_type = regularity['notification_type']
            if notification_type == 'D':
                if regularity.get('times_a_week') is not None or regularity.get('time_of_month') is not None:
                    raise serializers.ValidationError(
                        'You chose daily notification type. It does not have times_a_week or time_of_month field')
                if regularity.get('week_days') is None:
                    raise serializers.ValidationError('week_days field can not be empty for this notification type')
            if notification_type == 'W':
                if regularity.get('week_days') is not None or regularity.get('time_of_month') is not None:
                    raise serializers.ValidationError(
                        'You chose weekly notification type. It does not have week_days or time_of_month field')
                if regularity.get('times_a_week') is None:
                    raise serializers.ValidationError('times_a_week field can not be empty for this notification type')
            if notification_type == 'M':
                if regularity.get('week_days') is not None or regularity.get('times_a_week') is not None:
                    raise serializers.ValidationError(
                        'You chose monthly notification type. It does not have week_days or times_a_week field')
                if regularity.get('time_of_month') is None:
                    raise serializers.ValidationError('time_of_month field can not be empty for this notification type')
        return data

    class Meta:
        model = KitPerson
        fields = '__all__'
        extra_kwargs = {"user": {"read_only": True}}


class InteractionSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(InteractionSerializer, self).create(validated_data)

    class Meta:
        model = Interaction
        fields = '__all__'
        extra_kwargs = {"user": {"read_only": True}}
