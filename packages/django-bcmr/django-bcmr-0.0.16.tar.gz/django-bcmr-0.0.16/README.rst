=====
BCMR
=====

BCMR or Bitcoin Cash Metadata Registry is a Django app for storing, accessing and managing CashToken BCMRs.

Quick start
-----------

1. Add the following to your requirements.txt::
    
    Pillow==9.4.0
    django-bcmr==x.x.x

2. Add "bcmr" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'bcmr',
    ]

3. Include the bcmr URLconf in your project urls.py like this::

    path('bcmr/', include('bcmr.urls')),

4. Add media and DRF (to restrict access on root API auth token filter) config on settings.py::

    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

    REST_FRAMEWORK = {
        ...
        'DEFAULT_RENDERER_CLASSES': [
            'rest_framework.renderers.JSONRenderer'
        ]
    }

5. (upon deployment) Add media location path on nginx configuration file::

    location /media {
        proxy_pass http://127.0.0.1:8000;
        root /root/<project_name>;
    }

    location /bcmr {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }

6. Start the development server and visit http://localhost:8000/admin/
   to access the DB (you'll need the Admin app enabled).

7. Visit http://localhost:8000/bcmr/ to check API endpoints for BCMRs and tokens.


REST API
-----------

Registries and tokens created by a user can only be modified/deleted by that user (owner).

All endpoints are restricted on its usage for prevention of users tampering other user's registries and tokens.
An auth token generated upon creation of either a registry or token helps impose this restriction.
This token is used as a header for identification if the user modifying BCMR data is the owner.
Header name is `Bcmr-Auth`.

The endpoints are restricted as follows::

    GET = no header required
    POST = if header is supplied, created token/registry will belong to that auth token owner
         = if header is not supplied, a new auth token will be generated (new owner)
    PUT/PATCH = header required
    DELETE = header required


Create Fungible Token Form
-----------------------------

Creating a token from the REST API can be a hassle as one needs to process the image before passing it
as payload. This special route helps ease that burden by simply providing users to create a token and
upload an image without having to login to the admin: `create_token/fungible/`
