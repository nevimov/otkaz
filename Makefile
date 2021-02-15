STATIC_DIR=./core/static
CSS_DIR=$(STATIC_DIR)/css
SCSS_DIR=$(CSS_DIR)/src


# ***********
# *** CSS ***
# ***********

PHONY: css css-compile css-watch css-minify css-prefix

css-prefix:
	npx postcss --use autoprefixer --no-map --replace $(CSS_DIR)/**/*.css

css-minify:
	npx postcss --use cssnano --no-map --replace $(CSS_DIR)/**/*.css

css-watch:
	watchmedo shell-command --recursive --patterns="*.scss" --command="make css-compile" $(SCSS_DIR)

css-compile:
	sass --load-path=. $(SCSS_DIR):$(CSS_DIR)
	make css-prefix

css:
	make css-compile
	make css-prefix
	make css-minify


# ******************
# *** JavaScript ***
# ******************

PHONY: js js-compile js-watch js-lint

js:
	make js-lint
	make js-compile

js-compile:
	npx rollup --config

js-watch:
	npx rollup --config --watch

js-lint:
	npx eslint ./core/static/js/src


# **************
# *** Django ***
# **************

PHONY: run-msk run-msk-dt run-nk run-nk-dt run-sm run-sm-dt run run-dt static check-deploy check-migrations

run-msk:
	./waitforit.sh ${POSTGRES_HOST}:${POSTGRES_PORT} -- ./manage.py runserver --settings=core.settings.dev_moscow 0.0.0.0:8000

run-msk-dt:
	DEBUG_TOOLBAR=yes make run-msk

run-nk:
	./waitforit.sh ${POSTGRES_HOST}:${POSTGRES_PORT} -- ./manage.py runserver --settings=core.settings.dev_novokuznetsk 0.0.0.0:8001

run-nk-dt:
	DEBUG_TOOLBAR=yes make run-nk

run-sm:
	./waitforit.sh ${POSTGRES_HOST}:${POSTGRES_PORT} -- ./manage.py runserver --settings=core.settings.dev_samara 0.0.0.0:8002

run-sm-dt:
	DEBUG_TOOLBAR=yes make run-sm

run:
	(trap "exit" INT TERM; trap 'kill 0' EXIT; make run-msk & make run-nk & make run-sm)

run-dt:
	DEBUG_TOOLBAR=yes make run

static:
	./manage.py collectstatic --no-input --clear

check-deploy:
	./manage.py check --deploy --settings=core.settings.production

check-migrations:
	./manage.py makemigrations --check --dry-run
