=======================================
Django Rest Framework auth microservice
=======================================

Out-of-the-box solution for AAA services accessible through REST API.

Detailed documentation is in the README.md in main folder.

Quick start
-----------

1. Add "drf-micro-auth" to INSTALLED_APPS ::

    INSTALLED_APPS = [
        ...
        'drf-micro-auth',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('drf_micro_auth/', include('drf_micro_auth.urls')),

3. Run ``python manage.py migrate`` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/drf_micro_auth/docs/ to explore endpoints.