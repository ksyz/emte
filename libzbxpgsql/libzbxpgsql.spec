%global curdatetime %(date +%%Y%%m%%d%%H%%M%%S)

# alexrj»
%global commit0  66aa0d0f7e7e5658971dfcf6484557bc80831879
# %global gittag0 GIT-TAG
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           libzbxpgsql
Version:        1.1.0
Release:        5.%{curdatetime}.%{shortcommit0}%{?dist}

Summary:		Comprehensive monitoring of PostgreSQL servers via native Zabbix agent module

Group:          Applications/Databases
License:		GPLv2+
URL:			https://github.com/cavaliercoder/libzbxpgsql
Source0:		https://github.com/cavaliercoder/libzbxpgsql/archive/%{commit0}.tar.gz#/%{name}-%{version}.git_%{shortcommit0}.tar.gz

BuildRequires:	libpqxx-devel
BuildRequires:	rpm
BuildRequires:	rpm-build
BuildRequires:	rpmdevtools
BuildRequires:	libtool
BuildRequires:	postgresql-devel
BuildRequires:	libconfig-devel
BuildRequires:	zabbix-devel > 3.0.0

# same as zabbix package, as we include its headers
BuildRequires:	elfutils-libelf-devel
BuildRequires:	curl-devel
BuildRequires:	mysql-devel
BuildRequires:	postgresql-devel
BuildRequires:	sqlite-devel
BuildRequires:	net-snmp-devel
BuildRequires:	openldap-devel
BuildRequires:	openssl-devel
BuildRequires:	gnutls-devel
BuildRequires:	iksemel-devel
BuildRequires:	unixODBC-devel
BuildRequires:	curl-devel
BuildRequires:	OpenIPMI-devel
BuildRequires:	libssh2-devel
BuildRequires:	libxml2-devel

# name%{?isa} >= %{?epoch:%{epoch}:}%{version}-%{release}'
Requires:		zabbix-agent = %(eval "rpm -q zabbix-devel --qf '%%{version}-%%{release}'")

%description
provides detailed and granular monitoring of PostgreSQL servers using 
a native Zabbix agent module, with highly configurable item keys and 
a complimentary monitoring Template.

Native Zabbix agent modules are advantageous over User Parameters and 
scripts in that no process forking, code interpreter or complex 
configuration are required. This significantly reduces the impact of 
monitoring on the agent system, particularly when monitoring hundreds 
or thousands of checks.

%prep
%setup -qn %{name}-%{commit0}

%build
autoreconf -if
# %configure  --libdir=%{_libdir}/libzbxpgsql --enable-dependency-tracking --with-zabbix=%{_includedir}/zabbix/
%configure  --libdir=%{_libdir}/zabbix/agent/modules/ --enable-dependency-tracking --with-zabbix=%{_includedir}/zabbix/
make %{?_smp_mflags}

%install
%make_install

install -dm755 %{buildroot}%{_datadir}/%{name}
install -m644 templates/*.xml %{buildroot}%{_datadir}/%{name}
install -m644 conf/libzbxpgsql.conf %{buildroot}%{_sysconfdir}/zabbix/libzbxpgsql.conf

%files
%doc README.md ChangeLog COPYING
%{_libdir}/zabbix/agent/modules/*
%{_datadir}/%{name}
%{_sysconfdir}/zabbix/*

%changelog
* Thu Nov 30 2017 Michal Ingeli <mi@v3.sk> - 1.1.0-5
- Added stub/test configuration file

* Mon Nov 20 2017 Michal Ingeli <mi@v3.sk> - 1.1.0-4
- Include only templates into datadir

* Mon Nov 20 2017 Michal Ingeli <mi@v3.sk> - 1.1.0-3
- Adjsuted libdir to module load path
- Added zabbix-agent runtime = build time requirement

* Fri Nov 10 2017 Michal Ingeli <mi@v3.sk> - 1.1.0-2
- Included all zabbix BR

* Fri Nov 10 2017 Michal Ingeli <mi@v3.sk> - 1.1.0-1
- Initial package

