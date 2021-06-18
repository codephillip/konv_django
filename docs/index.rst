======================
Konv Documentation
======================

Introduction
============
Konv Server that provides data to the dashboard and mobile app

Tools
============
#. Django
#. Django Rest Framework
#. Python3
#. Swagger
#. Wagtail

Resources
============

* Deployment

https://medium.com/techkylabs/django-deployment-on-linux-ubuntu-16-04-with-postgresql-nginx-ssl-e6504a02f224

https://www.humankode.com/ssl/how-to-set-up-free-ssl-certificates-from-lets-encrypt-using-docker-and-nginx

https://simpleisbetterthancomplex.com/tutorial/2016/10/14/how-to-deploy-to-digital-ocean.html


Links
============

* Django admin - https://konvdemo.herokuapp.com/admin/
* Swagger - https://konvdemo.herokuapp.com/swagger
* CMS - https://konvdemo.herokuapp.com/


Bugs
-----
#. Error; "relation wagtailcore_locale does not exist" on heroku

.. code-block:: console

    $ heroku run python manage.py makemigrations -a konvdemo
    $ heroku run python manage.py migrate -a konvdemo

#. Static files error: "/app/myProjectManager/settings.py/staticfiles/staticfiles.json". Change project root from ``PROJECT_ROOT = os.path.join(os.path.abspath(__file__))`` to ``PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))``

#. Error: "whitenoise 4.0 incompatible with...". Change ``STATICFILES_STORAGE = ' whitenoise.django.GzipManifestStaticFilesStorage`` to ``STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'``

