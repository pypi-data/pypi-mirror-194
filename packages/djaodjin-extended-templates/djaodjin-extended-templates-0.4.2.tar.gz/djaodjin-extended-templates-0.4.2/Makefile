# -*- Makefile -*-

-include $(buildTop)/share/dws/prefix.mk

srcDir        ?= $(realpath .)
installTop    ?= $(VIRTUAL_ENV)
binDir        ?= $(installTop)/bin
CONFIG_DIR    ?= $(srcDir)
# XXX CONFIG_DIR should really be $(installTop)/etc/testsite
LOCALSTATEDIR ?= $(installTop)/var

installDirs   ?= install -d
installFiles  := install -p -m 644
NPM           ?= npm
PYTHON        := $(binDir)/python

ASSETS_DIR    := $(srcDir)/htdocs/static
RUN_DIR       ?= $(srcDir)
DB_NAME       ?= $(RUN_DIR)/db.sqlite

MANAGE        := TESTSITE_SETTINGS_LOCATION=$(CONFIG_DIR) RUN_DIR=$(RUN_DIR) $(PYTHON) manage.py

# Django 1.7,1.8 sync tables without migrations by default while Django 1.9
# requires a --run-syncdb argument.
# Implementation Note: We have to wait for the config files to be installed
# before running the manage.py command (else missing SECRECT_KEY).
RUNSYNCDB     = $(if $(findstring --run-syncdb,$(shell cd $(srcDir) && $(MANAGE) migrate --help 2>/dev/null)),--run-syncdb,)

install::
	cd $(srcDir) && $(PYTHON) ./setup.py --quiet \
		build -b $(CURDIR)/build install


install-conf:: $(DESTDIR)$(CONFIG_DIR)/credentials \
                $(DESTDIR)$(CONFIG_DIR)/gunicorn.conf
	$(installDirs) $(DESTDIR)$(LOCALSTATEDIR)/db
	$(installDirs) $(DESTDIR)$(LOCALSTATEDIR)/run
	$(installDirs) $(DESTDIR)$(LOCALSTATEDIR)/log/gunicorn


build-assets: vendor-assets-prerequisites


clean:: clean-dbs
	[ ! -f $(srcDir)/package-lock.json ] || rm $(srcDir)/package-lock.json
	find $(srcDir) -name '__pycache__' -exec rm -rf {} +
	find $(srcDir) -name '*~' -exec rm -rf {} +

clean-dbs:
	[ ! -f $(DB_NAME) ] || rm $(DB_NAME)
	[ ! -f $(srcDir)/testsite-app.log ] || rm $(srcDir)/testsite-app.log
	rm -rf $(RUN_DIR)/themes $(srcDir)/htdocs/media


vendor-assets-prerequisites: $(srcDir)/testsite/package.json


$(DESTDIR)$(CONFIG_DIR)/credentials: $(srcDir)/testsite/etc/credentials
	$(installDirs) $(dir $@)
	[ -f $@ ] || \
		sed -e "s,\%(SECRET_KEY)s,`$(PYTHON) -c 'import sys ; from random import choice ; sys.stdout.write("".join([choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^*-_=+") for i in range(50)]))'`," $< > $@


$(DESTDIR)$(CONFIG_DIR)/gunicorn.conf: $(srcDir)/testsite/etc/gunicorn.conf
	$(installDirs) $(dir $@)
	[ -f $@ ] || sed \
		-e 's,%(LOCALSTATEDIR)s,$(LOCALSTATEDIR),' $< > $@


initdb: clean-dbs install-conf $(ASSETS_DIR)/vendor/bootstrap.css
	$(installDirs) $(dir $(DB_NAME))
	cd $(srcDir) && $(MANAGE) migrate $(RUNSYNCDB) --noinput
	cd $(srcDir) && $(MANAGE) loaddata testsite/fixtures/default-db.json
	$(installDirs) $(RUN_DIR)/themes/djaodjin-extended-templates
	$(installDirs) $(srcDir)/htdocs/media/vendor
	$(installFiles) $(ASSETS_DIR)/vendor/bootstrap.css $(srcDir)/htdocs/media/vendor

doc:
	$(installDirs) build/docs
	cd $(srcDir) && sphinx-build -b html ./docs $(PWD)/build/docs

vendor-assets-prerequisites: $(ASSETS_DIR)/vendor/bootstrap.css

$(ASSETS_DIR)/vendor/bootstrap.css: $(srcDir)/testsite/package.json
	$(installFiles) $^ $(installTop)
	$(NPM) install --loglevel verbose --cache $(installTop)/.npm --tmp $(installTop)/tmp --prefix $(installTop)
	$(installDirs) -d $(ASSETS_DIR)/fonts $(ASSETS_DIR)/../media/fonts $(ASSETS_DIR)/vendor/bootstrap/mixins $(ASSETS_DIR)/img/bootstrap-colorpicker
	$(installFiles) $(installTop)/node_modules/ace-builds/src/ace.js $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/ace-builds/src/ext-language_tools.js $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/ace-builds/src/ext-modelist.js $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/ace-builds/src/ext-emmet.js $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/ace-builds/src/theme-monokai.js $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/ace-builds/src/mode-html.js $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/ace-builds/src/mode-css.js $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/ace-builds/src/mode-javascript.js $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/ace-builds/src/worker-html.js $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/bootstrap/dist/css/bootstrap.css $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/bootstrap/dist/js/bootstrap.js $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/bootstrap-colorpicker/dist/img/bootstrap-colorpicker/*.png $(ASSETS_DIR)/img/bootstrap-colorpicker
	$(installFiles) $(installTop)/node_modules/bootstrap-colorpicker/dist/css/bootstrap-colorpicker.css $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/bootstrap-colorpicker/dist/js/bootstrap-colorpicker.js $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/dropzone/dist/dropzone.css $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/dropzone/dist/dropzone.js $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/font-awesome/css/font-awesome.css $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/font-awesome/fonts/* $(ASSETS_DIR)/fonts
	$(installFiles) $(installTop)/node_modules/hallo/dist/hallo.js $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/jquery/dist/jquery.js $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/jquery-ui-touch-punch/jquery.ui.touch-punch.js $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/jquery.selection/dist/jquery.selection.js $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/less/dist/less.js $(ASSETS_DIR)/vendor
	[ -f $(binDir)/lessc ] || (cd $(binDir) && ln -s ../node_modules/less/bin/lessc)
	$(installFiles) $(installTop)/node_modules/pagedown/Markdown.Converter.js $(installTop)/node_modules/pagedown/Markdown.Sanitizer.js $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/rangy/lib/rangy-core.js $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/textarea-autosize/dist/jquery.textarea_autosize.js $(ASSETS_DIR)/vendor
	$(installFiles) $(installTop)/node_modules/vue/dist/vue.js $(ASSETS_DIR)/vendor

#	$(installFiles) $(srcDir)/testsite/static/vendor/* $(ASSETS_DIR)/vendor
