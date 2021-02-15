from rest_framework import serializers

from firebase_auth.models import FCMToken


class FCMTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMToken
        fields = '__all__'
        extra_kwargs = {"user": {"read_only": True}}

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(FCMTokenSerializer, self).create(validated_data)
