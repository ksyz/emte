%global commit0 606764598106b1851cdb724e807a7e2088578c13
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global package_name pg_prometheus

%global debug_package %{nil}

Name:		%{package_name}
Version:	1.2.0
Release:	2.%{shortcommit0}%{?dist}
Summary:	PostgreSQL plugin for prometheus data model

License:	ASL 2.0

URL:		https://github.com/timescale/%{package_name}
Source0:	https://github.com/timescale/%{package_name}/archive/%{commit0}.tar.gz#/%{package_name}-%{shortcommit0}.tar.gz

BuildRequires: gcc

%if 0%{?rhel} > 7 || 0%{?fedora}

%if 0%{?fedora} > 29
Requires:	postgresql-server-devel = %(eval "rpm -q postgresql-server-devel --qf '%%{version}-%%{release}'")
BuildRequires: postgresql-server-devel >= 10
BuildRequires: libpq-devel
%else
Requires:	postgresql-devel = %(eval "rpm -q postgresql-devel --qf '%%{version}-%%{release}'")
BuildRequires: postgresql-devel >= 10
%endif

%else
# requires https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-$releasever-$basearch
Requires:	postgresql10-devel = %(eval "rpm -q postgresql10-devel --qf '%%{version}-%%{release}'")
BuildRequires: postgresql10-devel
%endif

%description
An extension for PostgreSQL that defines a Prometheus metric samples 
data type and provides several storage formats for storing Prometheus 
data.

%prep
%setup -q -n %{package_name}-%{commit0}

%if 0%{?rhel} && 0%{?rhel} < 8
sed -e 's|^PG_CONFIG =.*|PG_CONFIG = /usr/pgsql-10/bin/pg_config|g' -i Makefile
%endif

%build
make %{?_smp_mflags}

%install
# % make_install
make install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE

%if 0%{?rhel} > 7 || 0%{?fedora} > 0
%{_libdir}/pgsql/pg_prometheus.so
%{_datarootdir}/pgsql/extension/
%else
%{_usr}/pgsql-10/lib/pg_prometheus.so
%{_usr}/pgsql-10/share/extension
%endif

%changelog

* Fri Jul 26 2019 Michal Ingeli <mi@v3.sk> 1.2.0-2
- Fixed fc30 BR

* Fri Jul 26 2019 Michal Ingeli <mi@v3.sk> 1.2.0-1
- New HEAD release

* Fri Jul 26 2019 Michal Ingeli <mi@v3.sk> 0.2-3
- Added Fedora>=29 build target compatibility

* Wed Feb 20 2019 Michal Ingeli <mi@v3.sk> 0.2-2
- Postgresql10 rebuild

* Tue Jul 10 2018 Michal Ingeli <mi@v3.sk> 0.2-1
- Initial package.
