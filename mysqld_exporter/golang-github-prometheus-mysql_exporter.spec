# If any of the following macros should be set otherwise,
# you can wrap any of them with the following conditions:
# - %%if 0%%{centos} == 7
# - %%if 0%%{?rhel} == 7
# - %%if 0%%{?fedora} == 23
# Or just test for particular distribution:
# - %%if 0%%{centos}
# - %%if 0%%{?rhel}
# - %%if 0%%{?fedora}
#
# Be aware, on centos, both %%rhel and %%centos are set. If you want to test
# rhel specific macros, you can use %%if 0%%{?rhel} && 0%%{?centos} == 0 condition.
# (Don't forget to replace double percentage symbol with single one in order to apply a condition)

# Generate devel rpm
%global with_devel 1
# Build project from bundled dependencies
%global with_bundled 1
# Build with debug info rpm
%global with_debug 0
# Run tests in check section
%global with_check 1
# Generate unit-test rpm
%global with_unit_test 0

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif


%global provider        github
%global provider_tld    com
%global project         prometheus
%global repo            mysqld_exporter
# https://github.com/prometheus/mysqld_exporter
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          5d7179615695a61ecc3b5bf90a2a7c76a9592cdd
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           golang-%{provider}-%{project}-%{repo}
Version:        0.11.0
Release:        3%{?dist}
Summary:        Exporter for machine metrics
License:        ASL 2.0
URL:            https://%{provider_prefix}
#Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source0:        https://%{provider_prefix}/archive/v%{version}.tar.gz
Source1:        sysconfig.mysqld_exporter
Source2:        mysqld_exporter.service

Provides:       mysqld_exporter = %{version}-%{release}

BuildRequires:  systemd
# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%description
%{summary}

%if 0%{?with_devel}
%package devel
Summary:       %{summary}
BuildArch:     noarch

%if 0%{?with_check} && ! 0%{?with_bundled}
# ;
%endif
# ;

%description devel
%{summary}

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test-devel
Summary:         Unit tests for %{name} package
%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/prometheus/client_golang/prometheus/promhttp)
%endif

Requires:      golang(github.com/prometheus/client_golang/prometheus/promhttp)

%description unit-test-devel
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n %{repo}-%{version}

%build
mkdir -p _build/src/%{provider}.%{provider_tld}/%{project}
ln -s $(pwd) _build/src/%{provider_prefix}

%if ! 0%{?with_bundled}
export GOPATH=$(pwd)/_build:%{gopath}
%else
# Since we aren't packaging up the vendor directory we need to link
# back to it somehow. Hack it up so that we can add the vendor
# directory from BUILD dir as a gopath to be searched when executing
# tests from the BUILDROOT dir.
ln -s ./ ./vendor/src # ./vendor/src -> ./vendor
export GOPATH=$(pwd)/_build:$(pwd)/vendor:%{gopath}
%endif

%if ! 0%{?gobuild:1}
function _gobuild { go build -a -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" -v -x "$@"; }
%global gobuild _gobuild
%endif

%gobuild -o _build/mysqld_exporter %{provider_prefix}

%install
install -d -p   %{buildroot}%{_sbindir} \
                %{buildroot}%{_defaultdocdir}/mysqld_exporter \
                %{buildroot}%{_sysconfdir}/sysconfig \
                %{buildroot}%{_unitdir}

install -p -m 0644 %{_sourcedir}/sysconfig.mysqld_exporter %{buildroot}%{_sysconfdir}/sysconfig/mysqld_exporter
install -p -m 0644 %{_sourcedir}/mysqld_exporter.service %{buildroot}%{_unitdir}/mysqld_exporter.service

install -p -m 0755 ./_build/mysqld_exporter %{buildroot}%{_sbindir}/mysqld_exporter

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . \( -iname "*.go" -or -iname "*.s" \) \! -iname "*_test.go" | grep -v "vendor") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test-devel.file-list
for file in $(find . -iname "*_test.go" | grep -v "vendor") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test-devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
# Since we aren't packaging up the vendor directory we need to link
# back to it somehow. Hack it up so that we can add the vendor
# directory from BUILD dir as a gopath to be searched when executing
# tests from the BUILDROOT dir.
ln -s ./ ./vendor/src # ./vendor/src -> ./vendor

export GOPATH=%{buildroot}/%{gopath}:$(pwd)/vendor:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}
%gotest %{import_path}/collector
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%if 0%{?with_devel}
%files devel -f devel.file-list
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test-devel -f unit-test-devel.file-list
%endif

%files
%{_unitdir}/mysqld_exporter.service
%config(noreplace) %{_sysconfdir}/sysconfig/mysqld_exporter
%license LICENSE
%doc *.md
%{_sbindir}/*

%pre
getent group mysqld_exporter > /dev/null || groupadd -r mysqld_exporter
getent passwd mysqld_exporter > /dev/null || \
    useradd -rg mysqld_exporter -d /var/lib/mysqld_exporter -s /sbin/nologin \
            -c "Prometheus node exporter" mysqld_exporter
mkdir -p /var/lib/mysqld_exporter/textfile_collector

%post
%systemd_post mysqld_exporter.service

%preun
%systemd_preun mysqld_exporter.service

%postun
%systemd_postun

%changelog
* Fri Oct  5 2018 Michal Ingeli <mi@v3.sk> - 0.11.0-3
- Fixed my.cnf location in sysconfig

* Thu Oct  4 2018 Michal Ingeli <mi@v3.sk> - 0.11.0-2
- Fixed sysconfig file

* Mon Jul 16 2018 Michal Ingeli <mi@v3.sk> - 0.11.0-1
- New upstream release

* Tue Apr  4 2017 Michal Ingeli <mi@v3.sk> - 0.9.0-2
- Added sysconfig file
- Fixed service unit

* Tue Apr  4 2017 Michal Ingeli <mi@v3.sk> - 0.9.0-1
- Based on node_exporter specfile by Tobias Florek <tob@butter.sh>

