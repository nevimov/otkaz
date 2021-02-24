# TODO.md

* Consider setting `unique=False` for `Seller.public_name`

* Fill `about.html` with actual content.

* Write terms of placement for `signup.html`.

* Replace copy-paste inside `pii_agreement.html` with the actual agreement text.

* Localize django-allauth templates used on this project. The list includes,
  but not limited to the following:
  - email confirmation
  - email password reset

* settings/production:
  `STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'`

* settings/production: Set appropriate `CONN_MAX_AGE`
  https://docs.djangoproject.com/en/3.1/ref/databases/#persistent-connections

* docker-compose: Update postgres image version to 13

* Consider upgrading Bootstrap to the new major release (v4 -> v5).

* Comment out unused Bootstrap modules in `core/static/css/src/_bootstrap.scss`.

* Use partial indexes for `catalog.models.Window` (condition: sold = True).

* Configure logging in production settings.

* Protect the main admin site from bruteforce attacks:
  https://django-allauth.readthedocs.io/en/latest/advanced.html#admin
