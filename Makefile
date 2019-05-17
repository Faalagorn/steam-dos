.PHONY: lint test coverage install uninstall clean version

# major.minor part of version of this release
# TODO inject it into .vdf files, so manual tweak won't be
# needed. Also, make sure it's compatible with the latest tag.
version_major_minor = 0.1

tool_dir = steam-dos-$(version_major_minor)

files = run_dosbox \
	confgen.py \
	midi.py \
	settings.py \
	toolbox.py \
	tweaks.py \
	compatibilitytool.vdf \
	toolmanifest.vdf \
	LICENSE \
	version

steam_dir = ${HOME}/.local/share/Steam
install_dir = $(steam_dir)/compatibilitytools.d/$(tool_dir)

lint:
	shellcheck $(shell find . -name *.sh)
	pylint --rcfile=.pylint run_dosbox *.py tests/*.py
	pycodestyle-3 run_dosbox *.py tests/*.py

test:
	python3 -m unittest discover -v -s tests

coverage:
	./tests/coverage-report.sh

version:
	git describe --tags --dirty --long > version

$(tool_dir).zip: $(files)
	mkdir -p $(tool_dir)
	cp --reflink=auto -t $(tool_dir) $^
	zip $@ $(tool_dir)/*
	rm -rf $(tool_dir)

$(tool_dir).tar.xz: $(files)
	mkdir -p $(tool_dir)
	cp --reflink=auto -t $(tool_dir) $^
	tar -cJf $@ $(tool_dir)
	rm -rf $(tool_dir)

install: $(files)
	mkdir -p $(install_dir)
	cp --reflink=auto -t $(install_dir) $^

clean:
	rm -f $(tool_dir).tar.xz
	rm -f $(tool_dir).zip

uninstall:
	rm -rf $(install_dir)
