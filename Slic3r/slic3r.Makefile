# $ENV{BOOST_DIR}
# $ENV{BOOST_INCLUDEDIR}
# $ENV{BOOST_LIBRARYPATH}
# $ENV{CPANM}
# $ENV{LC_NUMERIC}
# $ENV{LD_RUN_PATH}
# $ENV{SLIC3R_DEBUG}
# $ENV{SLIC3R_FILAMENT_DIAMETER}
# $ENV{SLIC3R_GIT_VERSION}
# $ENV{SLIC3R_NO_AUTO}
# $ENV{'SLIC3R_SINGLETHREADED'}
# $ENV{SLIC3R_STATIC}
# $ENV{SLIC3R_TESTS_GCODE}
# $ENV{SLIC3R_VAR_ABS_PATH}
# $ENV{SLIC3R_VAR_REL}
# $ENV{TRAVIS}

_version := $(shell git rev-parse --short HEAD)

.PHONY: all build.pl check-deps xs test

build.pl:
	export SLIC3R_GIT_VERSION=$(_version)
	perl ./Build2.PL --vendor --no-auto --all-deps
	perl ./Build2.PL --vendor --no-auto --all-deps --gui

check-deps:
	perl ./Build2.PL --check-deps --all-deps --vendor --no-auto --gui

cpanm-xs:
	export SLIC3R_GIT_VERSION=$(_version)
	cpanm --skip-satisfied --local-lib local-lib --reinstall --verbose ./xs

test:
	export SLIC3R_GIT_VERSION=$(_version)
	perl -MApp::Prove -e "App::Prove->new->run(); 1;"

all: check-desp cpanm-xs test
