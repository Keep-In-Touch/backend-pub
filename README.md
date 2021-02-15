# backend

## Requirements

Python 3.7.

**pip-tools** is used for the management of requirements: https://github.com/jazzband/pip-tools.

#### How to add a new dependency?

1. Add new requirements in `requirements.in`.
2. Run ``pip-compile``, requirements.txt is updated automatically
3. Run ``pip-sync``, new packages are installed

## Run local server in docker
To run local server for test run this command:
`docker-compose up -d --build`

Server will be launched on `localhost:8000`

## Remote test server
**`10.90.137.154:1337`**


## Remote server
You can send requests to remote server: **`64.225.94.45`** or **`keep-in-touch.tk`**


## Endpoints description
* `http://64.225.94.45/swagger/`
* `keep-in-touch.tk/swagger/`

## Admin panel
* `http://64.225.94.45/admin/`
* `keep-in-touch.tk/admin/`



## Deploy instruction

### Turn off containers
`sudo docker-compose down --remove-orphans`

### Update code
`git pull`

### Run containers (It will take several minutes)
`sudo docker-compose up -d --build`

### Run migrations(migrate)
`sudo docker-compose exec web python manage.py migrate --noinput`

### Collect static files 
`sudo docker-compose exec web python manage.py collectstatic --no-input --clear`

## UML generation
`python manage.py graph_models -a -g -o myapp_models.png` to generate UML of all packages  
`python manage.py graph_models package -o myapp_models.png` to generate UML only of package named _package_