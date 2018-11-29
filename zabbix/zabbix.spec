# TODO, maybe sometime:
# * Allow for nginx?
# * Consider using systemd's ReadWriteDirectories

#TODO: systemctl reload seems to be necessary after switching with Alternatives
#TODO: If the DB path for a Sqlite proxy is configured wrong, it requires systemctl restart. Start doesn't work.

%global srcname zabbix
#%%global prerelease rc2
%if ! 0%{?patchver}
%define patchver 24
%endif

Name:           zabbix
Version:        3.0.%{patchver}
Release:        2%{?prerelease:.%{prerelease}.1}%{?dist}
Summary:        Open-source monitoring solution for your IT infrastructure

License:        GPLv2+
URL:            http://www.zabbix.com
Source0:        http://downloads.sourceforge.net/%{srcname}/%{srcname}-%{version}%{?prerelease:%{prerelease}}.tar.gz
Source1:        %{srcname}-web.conf
Source5:        %{srcname}-logrotate.in
Source9:        %{srcname}-tmpfiles-zabbix.conf
# systemd units -- Alternatives switches between them (they state their dependencies)
# https://support.zabbix.com/browse/ZBXNEXT-1593
Source10:       %{srcname}-agent.service
Source11:       %{srcname}-proxy-mysql.service
Source12:       %{srcname}-proxy-pgsql.service
Source13:       %{srcname}-proxy-sqlite3.service
Source14:       %{srcname}-server-mysql.service
Source15:       %{srcname}-server-pgsql.service
Source16:       %{srcname}-fedora-epel.README
Source17:       %{srcname}-tmpfiles-zabbixsrv.conf

Source9000:     README.zabbix-web-ro-database.txt

# local rules for config files
Patch0:         %{srcname}-3.0.24-4-config.patch

# local rules for config files - fonts
Patch10:         %{srcname}-3.0.13-fonts-config.patch

# * Remove fping3 options detection
# 
# adapt for fping3 - https://support.zabbix.com/browse/ZBX-4894
# "zabbix tries to detect whether fping help output contains -I or -S flag (in that order)",
# and the order ... changed. this patch hardcodes '-S' option
# https://github.com/schweikert/fping/commit/66909a30c5a18fbee1078ff4ebd8b44c2b74b236
# this is now fixed in zabbix get_source_ip_option(), which will continue 
# to search for -S option, even after -I was found.
# 
# right now, this patch is applied on to skip flag detection altogether, 
# because we dont need to detect stuff that don't change.
Patch3:         %{srcname}-1.8.12-fping3.patch

# * Adds proxy performance to API
# 
# this could be calculated from several API requests. this patch exposes 
# stuff from Frontend UI to API.
Patch4:          zabbix-3.0.13-api-proxyperf.patch

# * Add R/O Frontend UI option
# 
# to be able to use zabbix on read/only database, we need to skip all 
# change SQL queries (for now, only for mysql/mariadb). We still need 
# to write some data for sessions, eferenced from users table and auditlog 
# tables. Also, casual frontend browsing updates profile table, which we 
# also skip, when RW database is defined.
# add $DB['DATABASE_RW'] = 'whateber'; into standard config
Patch9000:     %{srcname}-web-ro-database.patch
Patch9001:     %{srcname}-3.0.13-web-ro-database.patch

# Fix build with MariaDB 10.2+
# See https://support.zabbix.com/browse/ZBX-12232 ; this is the patch
# I submitted there, but applied to configure because running autoreconf
# results in different paths in some build scripts, and breaks the build
Patch1:         zabbix-3.0.13-mariadb-detect.patch

%if 0%{?fedora} >= 28
BuildRequires:   mariadb-connector-c-devel
%else
BuildRequires:   mysql-devel
%endif

%if 0%{?fedora} >= 29
BuildRequires:   libpq-devel
%else
BuildRequires:   postgresql-devel
%endif

BuildRequires:   sqlite-devel
BuildRequires:   net-snmp-devel
BuildRequires:   openldap-devel
BuildRequires:   openssl-devel
BuildRequires:   gnutls-devel
BuildRequires:   unixODBC-devel
BuildRequires:   curl-devel
BuildRequires:   OpenIPMI-devel
BuildRequires:   libssh2-devel
BuildRequires:   libxml2-devel
BuildRequires:   systemd
BuildRequires:   gcc

Requires:        logrotate
Provides:        bundled(md5-deutsch)
# Could alternatively be conditional on Fedora/EL
%if %{srcname} != %{name}
Provides:        %{srcname} = %{version}-%{release}
Conflicts:       %{srcname} < 3.0
Conflicts:       %{srcname}20
Conflicts:       %{srcname}22
%else
Obsoletes:       %{srcname}-docs < 1.8.15-2
Obsoletes:       %{srcname}-web-sqlite3 < 2.0.3-3
Obsoletes:       %{srcname}-server-sqlite3 < 2.0.3-3
%endif

%description
Zabbix is software that monitors numerous parameters of a network and the
health and integrity of servers. Zabbix uses a flexible notification mechanism
that allows users to configure e-mail based alerts for virtually any event.
This allows a fast reaction to server problems. Zabbix offers excellent
reporting and data visualization features based on the stored data.
This makes Zabbix ideal for capacity planning.

Zabbix supports both polling and trapping. All Zabbix reports and statistics,
as well as configuration parameters are accessed through a web-based front end.
A web-based front end ensures that the status of your network and the health of
your servers can be assessed from any location. Properly configured, Zabbix can
play an important role in monitoring IT infrastructure. This is equally true
for small organizations with a few servers and for large companies with a
multitude of servers.

%package devel
Summary:			Zabbix header files
Requires:			%{name} = %{version}-%{release}
BuildArch:			noarch

%description devel
Development files to build zabbix loadable modules

%package dbfiles-mysql
Summary:             Zabbix database schemas, images, data and patches
BuildArch:           noarch

%description dbfiles-mysql
Zabbix database schemas, images, data and patches necessary for creating
and/or updating MySQL databases

%package dbfiles-pgsql
Summary:             Zabbix database schemas, images, data and patches
BuildArch:           noarch

%description dbfiles-pgsql
Zabbix database schemas, images, data and patches necessary for creating
and/or updating PostgreSQL databases

%package dbfiles-sqlite3
Summary:             Zabbix database schemas and patches
BuildArch:           noarch

%description dbfiles-sqlite3
Zabbix database schemas and patches necessary for creating
and/or updating SQLite databases

%package server
Summary:             Zabbix server common files
BuildArch:           noarch
Requires:            %{name} = %{version}-%{release}
Requires:            %{name}-server-implementation = %{version}-%{release}
Requires:            fping >= 3
Requires:            traceroute
Requires(pre):       shadow-utils
Requires(post):      systemd
Requires(preun):     systemd
Requires(postun):    systemd

%description server
Zabbix server common files

%package server-mysql
Summary:             Zabbix server compiled to use MySQL/MariaDB
Requires:            %{name} = %{version}-%{release}
Requires:            %{name}-dbfiles-mysql
Requires:            %{name}-server = %{version}-%{release}
Requires(post):      %{_sbindir}/update-alternatives
Requires(preun):     %{_sbindir}/alternatives
Requires(postun):    %{_sbindir}/update-alternatives
Provides:            %{name}-server-implementation = %{version}-%{release}

%description server-mysql
Zabbix server compiled to use MySQL

%package server-pgsql
Summary:             Zabbix server compiled to use PostgreSQL
Requires:            %{name} = %{version}-%{release}
Requires:            %{name}-server = %{version}-%{release}
Requires:            %{name}-dbfiles-pgsql
Requires(post):      %{_sbindir}/update-alternatives
Requires(preun):     %{_sbindir}/alternatives
Requires(postun):    %{_sbindir}/update-alternatives
Provides:            %{name}-server-implementation = %{version}-%{release}

%description server-pgsql
Zabbix server compiled to use PostgreSQL

%package agent
Summary:             Zabbix agent
Requires:            %{name} = %{version}-%{release}
Requires(pre):       shadow-utils
Requires(post):      systemd
Requires(preun):     systemd
Requires(postun):    systemd

%description agent
Zabbix agent, to be installed on monitored systems

%package proxy
Summary:             Zabbix proxy common files
BuildArch:           noarch
Requires:            %{name} = %{version}-%{release}
Requires:            %{name}-proxy-implementation = %{version}-%{release}
Requires(pre):       shadow-utils
Requires(post):      systemd
Requires(preun):     systemd
Requires(postun):    systemd
Requires:            fping >= 3

%description proxy
Zabbix proxy commmon files

%package proxy-mysql
Summary:             Zabbix proxy compiled to use MySQL
Requires:            %{name}-proxy = %{version}-%{release}
Requires:            %{name}-dbfiles-mysql
Provides:            %{name}-proxy-implementation = %{version}-%{release}
Requires(post):      %{_sbindir}/update-alternatives
Requires(preun):     %{_sbindir}/alternatives
Requires(postun):    %{_sbindir}/update-alternatives

%description proxy-mysql
Zabbix proxy compiled to use MySQL

%package proxy-pgsql
Summary:             Zabbix proxy compiled to use PostgreSQL
Requires:            %{name}-proxy = %{version}-%{release}
Requires:            %{name}-dbfiles-pgsql
Provides:            %{name}-proxy-implementation = %{version}-%{release}
Requires(post):      %{_sbindir}/update-alternatives
Requires(preun):     %{_sbindir}/alternatives
Requires(postun):    %{_sbindir}/update-alternatives

%description proxy-pgsql
Zabbix proxy compiled to use PostgreSQL

%package proxy-sqlite3
Summary:             Zabbix proxy compiled to use SQLite
Requires:            %{name}-proxy = %{version}-%{release}
Requires:            %{name}-dbfiles-sqlite3
Provides:            %{name}-proxy-implementation = %{version}-%{release}
Requires(post):      %{_sbindir}/update-alternatives
Requires(preun):     %{_sbindir}/alternatives
Requires(postun):    %{_sbindir}/update-alternatives

%description proxy-sqlite3
Zabbix proxy compiled to use SQLite

%package web
Summary:         Zabbix Web Frontend
BuildArch:       noarch
# Don't remove "php". Everything else only depends on php-common
# and you'll end up with no module for Apache!
Requires:        php
Requires:        php-gd
Requires:        php-bcmath
Requires:        php-ldap
Requires:        php-mbstring
Requires:        php-xml
Requires:        php-gettext
Requires:        web-assets-httpd
# jquery 1.10.2 and jquery-ui 1.10.3 in the sources
# jquery-ui's review is stalled, so we can't replace it:
# https://bugzilla.redhat.com/show_bug.cgi?id=858027
Requires:        js-jquery1 
# prototype 1.6.1 in the sources
#TODO: Das landet in /usr/share/prototype!
#Requires:        prototype
Requires:        dejavu-sans-fonts
Requires:		 dejavu-sans-mono-fonts
Requires:        %{name} = %{version}-%{release}
Requires:        %{name}-web-database = %{version}-%{release}

%description web
The php frontend to display the Zabbix web interface.

%package web-mysql
Summary:         Zabbix web frontend for MySQL
BuildArch:       noarch
Requires:        %{name}-web = %{version}-%{release}
Requires:        php-mysqli
Provides:        %{name}-web-database = %{version}-%{release}
Obsoletes:       %{name}-web <= 1.5.3-0.1

%description web-mysql
Zabbix web frontend for MySQL

%package web-pgsql
Summary:         Zabbix web frontend for PostgreSQL
BuildArch:       noarch
Requires:        %{name}-web = %{version}-%{release}
Requires:        php-pgsql
Provides:        %{name}-web-database = %{version}-%{release}

%description web-pgsql
Zabbix web frontend for PostgreSQL


%prep
%setup0 -q -n %{srcname}-%{version}%{?prerelease:.%{prerelease}}
%patch0 -p1 -b .backup-config
%patch10 -p1
## % patch1 -p1
%patch4 -p1
%patch9001 -p1

# Remove bundled java libs
rm -rf src/zabbix_java/lib/*.jar

# Remove prebuilt Windows binaries
rm -rf bin

# Remove included fonts
rm -rf frontends/php/fonts

# Remove executable permissions
chmod a-x upgrades/dbpatches/*/mysql/upgrade

# Override statically named directory for alertscripts and externalscripts
# https://support.zabbix.com/browse/ZBX-6159
sed -i 's|$(DESTDIR)@datadir@/zabbix|$(DESTDIR)/var/lib/zabbixsrv|' \
    src/zabbix_server/Makefile.in \
    src/zabbix_proxy/Makefile.in

# Kill off .htaccess files, options set in SOURCE1
find frontends/php -name .htaccess -a -delete

# remove translation source files and scripts
find frontends/php/locale \( -name '*.po' -o -name '*.sh' \) -a -delete

# Fix path to traceroute utility
find database -name 'data.sql' -exec sed -i 's|/usr/bin/traceroute|/bin/traceroute|' {} \;


# Common
# Settings with hard-coded defaults that are not suitable for Fedora
# are explicitly set, leaving the comment with the default value in place.
# Settings without hard-coded defaults are simply replaced -- be they
# comments or explicit settings!

# Also replace the datadir placeholder that is not expanded, but effective
sed -i \
    -e '\|^# LogFileSize=.*|a LogFileSize=0' \
    -e 's|^DBUser=root|DBUser=zabbix|' \
    -e 's|^# DBSocket=.*|# DBSocket=%{_sharedstatedir}/mysql/mysql.sock|' \
    -e '\|^# ExternalScripts=.*|a ExternalScripts=%{_sharedstatedir}/zabbixsrv/externalscripts' \
    -e '\|^# AlertScripts=.*|a AlertScripts=%{_sharedstatedir}/zabbixsrv/externalscripts' \
    -e '\|^# TmpDir=.*|a TmpDir=%{_sharedstatedir}/zabbixsrv/tmp' \
    -e 's|/usr/local||' \
    -e 's|\${datadir}|/usr/share|' \
    conf/zabbix_agentd.conf conf/zabbix_proxy.conf conf/zabbix_server.conf

# Specific
sed -i \
    -e '\|^# PidFile=.*|a PidFile=%{_rundir}/zabbix/zabbix_agentd.pid' \
    -e 's|^LogFile=.*|LogFile=%{_localstatedir}/log/zabbix/zabbix_agentd.log|' \
    -e 's|LoadModulePath=.*|LoadModulePath=%{_libdir}/%{srcname}/agent/modules|g' \
    conf/zabbix_agentd.conf

sed -i \
    -e '\|^# PidFile=.*|a PidFile=%{_rundir}/zabbixsrv/zabbix_proxy.pid' \
    -e 's|^LogFile=.*|LogFile=%{_localstatedir}/log/zabbixsrv/zabbix_proxy.log|' \
    -e 's|LoadModulePath=.*|LoadModulePath=%{_libdir}/%{srcname}/server/modules|g' \
    conf/zabbix_proxy.conf

sed -i \
    -e '\|^# PidFile=.*|a PidFile=%{_rundir}/zabbixsrv/zabbix_server.pid' \
    -e 's|^LogFile=.*|LogFile=%{_localstatedir}/log/zabbixsrv/zabbix_server.log|' \
    -e 's|LoadModulePath=.*|LoadModulePath=%{_libdir}/%{srcname}/server/modules|g' \
    conf/zabbix_server.conf

# Adapt man pages and SQL patches
# These SQL files allow users to upgrade from 1.8
sed -i 's|/usr/local||g;s| (if not modified during compile time).||' man/*.man
sed -i 's|/usr/local||g' \
    upgrades/dbpatches/2.0/mysql/patch.sql \
    upgrades/dbpatches/2.0/postgresql/patch.sql

# Install README file
install -m 0644 -p %{SOURCE16} .
install -m 0644 -p %{SOURCE9000} .


%build

common_flags="
    --enable-dependency-tracking
    --enable-agent
    --enable-proxy
    --enable-ipv6
    --disable-java
    --with-net-snmp
    --with-ldap
    --with-libcurl
    --with-openipmi
    --with-openssl
    --with-unixodbc
    --with-ssh2
    --with-libxml2
"

# Frontend doesn't work for SQLite, thus don't build server
%configure $common_flags --with-sqlite3
make %{?_smp_mflags}
mv src/zabbix_proxy/zabbix_proxy src/zabbix_proxy/zabbix_proxy_sqlite3

%configure $common_flags --with-mysql --enable-server
make clean
make %{?_smp_mflags}
mv src/zabbix_server/zabbix_server src/zabbix_server/zabbix_server_mysql
mv src/zabbix_proxy/zabbix_proxy src/zabbix_proxy/zabbix_proxy_mysql

%configure $common_flags --with-postgresql --enable-server
make clean
make %{?_smp_mflags}
mv src/zabbix_server/zabbix_server src/zabbix_server/zabbix_server_pgsql
mv src/zabbix_proxy/zabbix_proxy src/zabbix_proxy/zabbix_proxy_pgsql

# Ghosted alternatives
touch src/zabbix_server/zabbix_server
touch src/zabbix_proxy/zabbix_proxy


%install
# Configuration, runtime and start-up
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{srcname}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{srcname}/web
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/zabbix
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/zabbixsrv
mkdir -p $RPM_BUILD_ROOT%{_unitdir}

# systemd tmpfiles
mkdir -p $RPM_BUILD_ROOT%{_tmpfilesdir}
install -m 0644 -p %{SOURCE9} $RPM_BUILD_ROOT%{_tmpfilesdir}/zabbix.conf
install -m 0644 -p %{SOURCE17} $RPM_BUILD_ROOT%{_tmpfilesdir}/zabbixsrv.conf
mkdir -p $RPM_BUILD_ROOT%{_rundir}
install -d -m 0755 $RPM_BUILD_ROOT%{_rundir}/zabbix/
install -d -m 0755 $RPM_BUILD_ROOT%{_rundir}/zabbixsrv/

# Frontend
mkdir -p $RPM_BUILD_ROOT%{_datadir}

# Home directory for the agent;
# The other home directory is created during installation
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/zabbix

# Install binaries
make DESTDIR=$RPM_BUILD_ROOT install
install -m 0755 -p src/zabbix_server/zabbix_server_* $RPM_BUILD_ROOT%{_sbindir}/
install -m 0755 -p src/zabbix_proxy/zabbix_proxy_* $RPM_BUILD_ROOT%{_sbindir}/

# Install the frontend after removing backup files from patching
find frontends/php -name '*.orig' -exec rm {} \;
cp -a frontends/php $RPM_BUILD_ROOT%{_datadir}/%{srcname}

# Prepare ghosted config file
#TODO: Simplify that? Like /etc/zabbix_web/zabbix.conf.php?
touch $RPM_BUILD_ROOT%{_sysconfdir}/%{srcname}/web/zabbix.conf.php

# Replace bundled font and JS libraries
# There is no jquery-ui package yet
rm frontends/php/fonts/DejaVuSans.ttf && ln -sf %{_datadir}/fonts/dejavu/DejaVuSans.ttf $RPM_BUILD_ROOT%{_datadir}/%{srcname}/fonts/DejaVuSans.ttf
rm frontends/php/js/vendor/jquery.js && ln -sf %{_datadir}/web-assets/jquery/1/jquery.js $RPM_BUILD_ROOT%{_datadir}/%{srcname}/js/vendor/jquery.js 
rm frontends/php/js/vendor/prototype.js && ln -sf %{_datadir}/prototype/prototype.js $RPM_BUILD_ROOT%{_datadir}/%{srcname}/js/vendor/prototype.js 

# Move MVC override directory out; We are not owning or creating this directory!
#TODO: README dort
rm -r frontends/php/local/ && ln -sf %{_usr}/local/share/zabbix/local $RPM_BUILD_ROOT%{_datadir}/%{srcname}/local
#TODO: local vielleicht doch unter /etc/zabbix/web?

# This file is used to switch the frontend to maintenance mode
mv $RPM_BUILD_ROOT%{_datadir}/%{srcname}/conf/maintenance.inc.php $RPM_BUILD_ROOT%{_sysconfdir}/%{srcname}/web/maintenance.inc.php

# Drop Apache config file in place
install -m 0644 -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/%{srcname}.conf

# Install log rotation
sed -e 's|COMPONENT|agentd|g; s|USER|zabbix|g' %{SOURCE5} > \
     $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zabbix-agent
sed -e 's|COMPONENT|server|g; s|USER|zabbixsrv|g' %{SOURCE5} > \
     $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zabbix-server
sed -e 's|COMPONENT|proxy|g; s|USER|zabbixsrv|g' %{SOURCE5} > \
     $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zabbix-proxy

# Install different systemd units because of the requirements for DBMS daemons
install -m 0644 -p %{SOURCE10} $RPM_BUILD_ROOT%{_unitdir}/zabbix-agent.service
install -m 0644 -p %{SOURCE11} $RPM_BUILD_ROOT%{_unitdir}/zabbix-proxy-mysql.service
install -m 0644 -p %{SOURCE12} $RPM_BUILD_ROOT%{_unitdir}/zabbix-proxy-pgsql.service
install -m 0644 -p %{SOURCE13} $RPM_BUILD_ROOT%{_unitdir}/zabbix-proxy-sqlite3.service
install -m 0644 -p %{SOURCE14} $RPM_BUILD_ROOT%{_unitdir}/zabbix-server-mysql.service
install -m 0644 -p %{SOURCE15} $RPM_BUILD_ROOT%{_unitdir}/zabbix-server-pgsql.service

# Ghosted alternatives 
touch $RPM_BUILD_ROOT%{_unitdir}/zabbix-server.service
touch $RPM_BUILD_ROOT%{_unitdir}/zabbix-proxy.service

# Install compatibility links for config files
#TODO: Switch to .wants files instead!
ln -sf %{_sysconfdir}/zabbix_agentd.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{srcname}/zabbix_agentd.conf
ln -sf %{_sysconfdir}/zabbix_server.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{srcname}/zabbix_server.conf
ln -sf %{_sysconfdir}/zabbix_proxy.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{srcname}/zabbix_proxy.conf
ln -sf %{_sharedstatedir}/zabbixsrv/externalscripts $RPM_BUILD_ROOT%{_sysconfdir}/%{srcname}/externalscripts
ln -sf %{_sharedstatedir}/zabbixsrv/alertscripts $RPM_BUILD_ROOT%{_sysconfdir}/%{srcname}/alertscripts
#TODO: What does that do to existing directories?

# Directory for fping spooling files 
mkdir $RPM_BUILD_ROOT%{_sharedstatedir}/zabbixsrv/tmp

# Install sql files
for db in postgresql mysql; do
    datadir=$RPM_BUILD_ROOT%{_datadir}/%{srcname}-$db
    install -dm 0755 $datadir/upgrades/{1.6,1.8,2.0}
    cp -p database/$db/* $datadir
    cp -pR upgrades/dbpatches/1.6/$db/* $datadir/upgrades/1.6
    cp -pR upgrades/dbpatches/1.8/$db/* $datadir/upgrades/1.8
    cp -pR upgrades/dbpatches/2.0/$db/* $datadir/upgrades/2.0
done

install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{srcname}-sqlite3
cp -p database/sqlite3/schema.sql $RPM_BUILD_ROOT%{_datadir}/%{srcname}-sqlite3

# Don't include include/config.h
# * https://github.com/cavaliercoder/libzbxpgsql/issues/68#issuecomment-309274698
# * https://support.zabbix.com/browse/ZBXNEXT-3157
mkdir -p $RPM_BUILD_ROOT%{_includedir}/zabbix/
mv include/config.h include/zbx_config.h
# sed -i include/sysinc.h -e 's/"config.h"/"zbx_config.h"/g'
install -m 644 include/*.h $RPM_BUILD_ROOT%{_includedir}/%{srcname}/

install -m 755 -d $RPM_BUILD_ROOT%{_libdir}/%{srcname}/agent/modules
install -m 755 -d $RPM_BUILD_ROOT%{_libdir}/%{srcname}/server/modules

sed -e 's|^MODULES_DIR.*|MODULES_DIR = $(DESTDIR)/%{_libdir}/%{srcname}/agent/modules|g' -i src/zabbix_agent/Makefile.in
sed -e 's|^MODULES_DIR.*|MODULES_DIR = $(DESTDIR)/%{_libdir}/%{srcname}/server/modules|g' -i src/zabbix_server/Makefile.in
sed -e 's|^MODULES_DIR.*|MODULES_DIR = $(DESTDIR)/%{_libdir}/%{srcname}/server/modules|g' -i src/zabbix_proxy/Makefile.in


%post server
%systemd_post zabbix-server.service

if [ $1 -gt 1 ] ; then
  # Apply permissions also in *.rpmnew upgrades from old permissive ones
  chmod 0600 %{_sysconfdir}/zabbix_server.conf
  chown zabbixsrv:zabbix %{_sysconfdir}/zabbix_server.conf
fi
:

%post server-mysql
%{_sbindir}/update-alternatives --install %{_sbindir}/%{srcname}_server \
    %{srcname}-server %{_sbindir}/%{srcname}_server_mysql 10 \
        --slave %{_unitdir}/zabbix-server.service %{srcname}-server-systemd \
            %{_unitdir}/zabbix-server-mysql.service

%post server-pgsql
%{_sbindir}/update-alternatives --install %{_sbindir}/%{srcname}_server \
    %{srcname}-server %{_sbindir}/%{srcname}_server_pgsql 10 \
        --slave %{_unitdir}/zabbix-server.service %{srcname}-server-systemd \
            %{_unitdir}/zabbix-server-pgsql.service

%post proxy
%systemd_post zabbix-proxy.service

if [ $1 -gt 1 ] ; then
  # Apply permissions also in *.rpmnew upgrades from old permissive ones
  chmod 0600 %{_sysconfdir}/zabbix_proxy.conf
  chown zabbixsrv:zabbix %{_sysconfdir}/zabbix_proxy.conf
fi
:

%post proxy-mysql
%{_sbindir}/update-alternatives --install %{_sbindir}/%{srcname}_proxy \
    %{srcname}-proxy %{_sbindir}/%{srcname}_proxy_mysql 10 \
        --slave %{_unitdir}/zabbix-proxy.service %{srcname}-proxy-systemd \
            %{_unitdir}/zabbix-proxy-mysql.service

%post proxy-pgsql
%{_sbindir}/update-alternatives --install %{_sbindir}/%{srcname}_proxy \
    %{srcname}-proxy %{_sbindir}/%{srcname}_proxy_pgsql 10 \
        --slave %{_unitdir}/zabbix-proxy.service %{srcname}-proxy-systemd \
            %{_unitdir}/zabbix-proxy-pgsql.service

%post proxy-sqlite3
%{_sbindir}/update-alternatives --install %{_sbindir}/%{srcname}_proxy \
    %{srcname}-proxy %{_sbindir}/%{srcname}_proxy_sqlite3 10 \
        --slave %{_unitdir}/zabbix-proxy.service %{srcname}-proxy-systemd \
            %{_unitdir}/zabbix-proxy-sqlite3.service

%pre agent
getent group zabbix > /dev/null || groupadd -r zabbix
getent passwd zabbix > /dev/null || \
    useradd -r -g zabbix -d %{_sharedstatedir}/zabbix -s /sbin/nologin \
    -c "Zabbix Monitoring System" zabbix
:

%post agent
%systemd_post zabbix-agent.service

%pre server
getent group zabbixsrv > /dev/null || groupadd -r zabbixsrv
# The zabbixsrv group is introduced by 2.2 packaging
# The zabbixsrv user was a member of the zabbix group in 2.0
if getent passwd zabbixsrv > /dev/null; then
    if [[ $(id -gn zabbixsrv) == "zabbix" ]]; then
        usermod -c "Zabbix Monitoring System -- Proxy or server" -g zabbixsrv zabbixsrv
    fi
else
    useradd -r -g zabbixsrv -d %{_sharedstatedir}/zabbixsrv -s /sbin/nologin \
    -c "Zabbix Monitoring System -- Proxy or server" zabbixsrv
fi
:

%preun server
  %systemd_preun zabbix-server.service

%pre proxy
getent group zabbixsrv > /dev/null || groupadd -r zabbixsrv
# The zabbixsrv group is introduced by 2.2 packaging
# The zabbixsrv user was a member of the zabbix group in 2.0
if getent passwd zabbixsrv > /dev/null; then
    if [[ $(id -gn zabbixsrv) == "zabbix" ]]; then
        usermod -c "Zabbix Monitoring System -- Proxy or server" -g zabbixsrv zabbixsrv
    fi
else
    useradd -r -g zabbixsrv -d %{_sharedstatedir}/zabbixsrv -s /sbin/nologin \
    -c "Zabbix Monitoring System -- Proxy or server" zabbixsrv
fi
:

%preun proxy
%systemd_preun zabbix-proxy.service

%preun agent
%systemd_preun zabbix-agent.service

%postun server
%systemd_postun_with_restart zabbix-server.service

%postun server-mysql
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove %{srcname}-server %{_sbindir}/%{srcname}_server_mysql
fi

%postun server-pgsql
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove %{srcname}-server %{_sbindir}/%{srcname}_server_pgsql
fi

%postun proxy
%systemd_postun_with_restart zabbix-proxy.service

%postun proxy-mysql
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove %{srcname}-proxy %{_sbindir}/%{srcname}_proxy_mysql
fi

%postun proxy-pgsql
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove %{srcname}-proxy %{_sbindir}/%{srcname}_proxy_pgsql
fi

%postun proxy-sqlite3
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove %{srcname}-proxy %{_sbindir}/%{srcname}_proxy_sqlite3
fi

%postun agent
%systemd_postun_with_restart zabbix-agent.service


%files
%doc AUTHORS ChangeLog COPYING NEWS README zabbix-fedora-epel.README README.zabbix-web-ro-database.txt
%dir %{_sysconfdir}/%{srcname}
%config(noreplace) %{_sysconfdir}/zabbix_agentd.conf
%config(noreplace) %{_sysconfdir}/%{srcname}/zabbix_agentd.conf
%{_bindir}/zabbix_get
%{_bindir}/zabbix_sender
%{_mandir}/man1/zabbix_get.1*
%{_mandir}/man1/zabbix_sender.1*

%files devel
%{_includedir}/%{name}/

%files dbfiles-mysql
%doc COPYING
%{_datadir}/%{srcname}-mysql/

%files dbfiles-pgsql
%doc COPYING
%{_datadir}/%{srcname}-postgresql/

%files dbfiles-sqlite3
%doc COPYING
%{_datadir}/%{srcname}-sqlite3/

%files server
%doc misc/snmptrap/zabbix_trap_receiver.pl
%attr(0755,zabbixsrv,zabbixsrv) %dir %{_rundir}/zabbixsrv/
%{_tmpfilesdir}/zabbixsrv.conf
%attr(0640,root,zabbixsrv) %config(noreplace) %{_sysconfdir}/zabbix_server.conf
%attr(0775,root,zabbixsrv) %dir %{_localstatedir}/log/zabbixsrv
%config(noreplace) %{_sysconfdir}/%{srcname}/zabbix_server.conf
%config(noreplace) %{_sysconfdir}/%{srcname}/externalscripts
%config(noreplace) %{_sysconfdir}/%{srcname}/alertscripts
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-server
%ghost %{_sbindir}/zabbix_server
%attr(0750,zabbixsrv,zabbixsrv) %dir %{_sharedstatedir}/zabbixsrv
%attr(0750,zabbixsrv,zabbixsrv) %dir %{_sharedstatedir}/zabbixsrv/tmp
%attr(0750,zabbixsrv,zabbixsrv) %dir %{_sharedstatedir}/zabbixsrv/alertscripts
%attr(0750,zabbixsrv,zabbixsrv) %dir %{_sharedstatedir}/zabbixsrv/externalscripts
%ghost %{_unitdir}/zabbix-server.service
%{_mandir}/man8/zabbix_server.8*
%{_libdir}/%{srcname}/server/modules

%files server-mysql
%{_sbindir}/zabbix_server_mysql
%{_unitdir}/zabbix-server-mysql.service

%files server-pgsql
%{_sbindir}/zabbix_server_pgsql
%{_unitdir}/zabbix-server-pgsql.service

%files agent
%doc conf/zabbix_agentd/*.conf
%attr(0755,zabbix,zabbix) %dir %{_rundir}/zabbix/
%{_tmpfilesdir}/zabbix.conf
%attr(0775,root,zabbix) %dir %{_localstatedir}/log/zabbix
%config(noreplace) %{_sysconfdir}/zabbix_agentd.conf
%config(noreplace) %{_sysconfdir}/%{srcname}/zabbix_agentd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-agent
%attr(750,zabbix,zabbix) %dir %{_sharedstatedir}/zabbix
%{_unitdir}/zabbix-agent.service
%{_sbindir}/zabbix_agentd
%{_mandir}/man8/zabbix_agentd.8*
%{_libdir}/%{srcname}/agent/modules

%files proxy
%doc misc/snmptrap/zabbix_trap_receiver.pl
%attr(0755,zabbixsrv,zabbixsrv) %dir %{_rundir}/zabbixsrv/
%{_tmpfilesdir}/zabbixsrv.conf
%attr(0640,root,zabbixsrv) %config(noreplace) %{_sysconfdir}/zabbix_proxy.conf
%attr(0775,root,zabbixsrv) %dir %{_localstatedir}/log/zabbixsrv
%config(noreplace) %{_sysconfdir}/%{srcname}/zabbix_proxy.conf
%config(noreplace) %{_sysconfdir}/%{srcname}/externalscripts
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-proxy
%ghost %{_sbindir}/zabbix_proxy
%attr(0750,zabbixsrv,zabbixsrv) %dir %{_sharedstatedir}/zabbixsrv
%attr(0750,zabbixsrv,zabbixsrv) %dir %{_sharedstatedir}/zabbixsrv/tmp
%attr(0750,zabbixsrv,zabbixsrv) %dir %{_sharedstatedir}/zabbixsrv/alertscripts
%attr(0750,zabbixsrv,zabbixsrv) %dir %{_sharedstatedir}/zabbixsrv/externalscripts
%ghost %{_unitdir}/zabbix-proxy.service
%{_mandir}/man8/zabbix_proxy.8*

%files proxy-mysql
%{_sbindir}/zabbix_proxy_mysql
%{_unitdir}/zabbix-proxy-mysql.service

%files proxy-pgsql
%{_sbindir}/zabbix_proxy_pgsql
%{_unitdir}/zabbix-proxy-pgsql.service

%files proxy-sqlite3
%{_sbindir}/zabbix_proxy_sqlite3
%{_unitdir}/zabbix-proxy-sqlite3.service

%files web
%dir %attr(0750,apache,apache) %{_sysconfdir}/%{srcname}/web
%ghost %attr(0644,apache,apache) %config(noreplace) %{_sysconfdir}/%{srcname}/web/zabbix.conf.php
%attr(0644,apache,apache) %config(noreplace) %{_sysconfdir}/%{srcname}/web/maintenance.inc.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/zabbix.conf
%{_datadir}/%{srcname}

%files web-mysql

%files web-pgsql

%changelog
* Thu Nov 29 2018 Michal Ingeli <mi@v3.sk> - 3.0.24-2
- Fixed PidFile path

* Wed Nov 28 2018 Michal Ingeli <mi@v3.sk> - 3.0.24-1
- New upstream release 3.0.24
- Removed redundant changes from zabbix-3.0.24-config.patch 
  to only modify php code. Rest is done by spec file anyway.
- Changed path lib/tmpfiles.d to _tmpfilesdir macro

* Thu Nov 15 2018 Michal Ingeli <mi@v3.sk> - 3.0.23-1
- New upstream release 3.0.23

* Mon Sep 17 2018 Michal Ingeli <mi@v3.sk> - 3.0.22-1
- New upstream release 3.0.22

* Thu Sep  6 2018 Michal Ingeli <mi@v3.sk> - 3.0.21-1
- New upstream release 3.0.21
- Added BR gcc

* Thu Aug 16 2018 Michal Ingeli <mi@v3.sk> - 3.0.20-1
- New upstream release 3.0.20

* Thu Jul 19 2018 Michal Ingeli <mi@v3.sk> - 3.0.19-1
- New upstream release 3.0.19

* Tue Jul 17 2018 Michal Ingeli <mi@v3.sk> - 3.0.16-2
- Removed jabber media, due to lib iksemel EOL. May be re-enabled 
  in the future.
- Removed "group" tags.

* Mon Jun 25 2018 Michal Ingeli <mi@v3.sk> - 3.0.16-1
- New upstream relase 3.0.16

* Thu Feb 08 2018 Volker Fröhlich <volker27@gmx.at> - 3.0.14-2
- Remove group keyword

* Thu Dec 28 2017 Volker Fröhlich <volker27@gmx.at> - 3.0.14-1
  Remove mariadb-connector patch

* Mon Nov 20 2017 Michal Ingeli <mi@v3.sk> - 3.0.13-4
- Adjusted LoadModulePath to %libdir/%srcname/

* Mon Nov 20 2017 Michal Ingeli <mi@v3.sk> - 3.0.13-3
- Included config.h as zbx_config.h

* Mon Nov 20 2017 Michal Ingeli <mi@v3.sk> - 3.0.13-2
- New upstream release
- Adjusted patches
- Added Requireed zabbix version = BR
- Don't include include/config.h in zabbix-devel
  https://github.com/cavaliercoder/libzbxpgsql/issues/68#issuecomment-309274698
  https://support.zabbix.com/browse/ZBXNEXT-3157

* Wed Nov 15 2017 Michal Ingeli <mi@v3.sk> - 3.0.12-1
- New upstream release
- merged spec file from fedora repository

* Fri Nov 10 2017 Michal Ingeli <mi@v3.sk> - 3.0.7-5
- Added devel package

* Wed Nov  8 2017 Michal Ingeli <mi@v3.sk> - 3.0.7-4
- Fixed profile updates on R/O database

* Wed Oct 18 2017 Volker Fröhlich <volker27@gmx.at> - 3.0.12-1
- New upstream release

* Mon Sep 25 2017 Volker Fröhlich <volker27@gmx.at> - 3.0.11-1
- New upstream release

* Fri Sep 22 2017 Volker Fröhlich <volker27@gmx.at> - 3.0.10-4
- Replace mysql-devel with mariadb-connector-c-devel, resolves BZ #1493663

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Volker Fröhlich <volker27@gmx.at> - 3.0.10-1
- New upstream release


* Tue Feb  7 2017 michal Ingeli <mi@v3.sk> - 3.0.7-3
- Added patch option to run on MySQL/MariaDB R/O database e.g. replication slave

* Tue Feb  7 2017 michal Ingeli <mi@v3.sk> - 3.0.7-2
- Added proxy performance patch

* Mon Feb  6 2017 michal Ingeli <mi@v3.sk> - 3.0.7-1
- Version bump

* Wed Sep  7 2016 michal Ingeli <mi@v3.sk> - 3.0.4-2
- Backported/merged fedora SPEC file

* Sat Jul 23 2016 Volker Fröhlich <volker27@gmx.at> - 3.0.4-1
- New upstream release

* Mon Jul 11 2016 Orion Poplawski <orion@cora.nwra.com> - 3.0.3-2
- Fix php mysql requires

* Mon Jul 04 2016 Volker Fröhlich <volker27@gmx.at> - 3.0.3-1
- New upstream release

* Mon May 09 2016 Volker Fröhlich <volker27@gmx.at> - 3.0.2-1
- New upstream release
- Remove now-obsolete fping3 patch

* Tue Mar 29 2016 Volker Fröhlich <volker27@gmx.at> - 3.0.1-1
- Un-bundle jquery and prototype; remove the font patch and use a symlink instead
- Add PHP configuration to Apache config file (BZ#1074292)
- Fix the duplicate definition of a pidfile (BZ#1220392)
- Change logrotate mode to truncate

* Tue Mar  1 2016 Michal Ingeli <mi@v3.sk> 3.0.1-1
- New release

* Thu Feb 18 2016 Michal Ingeli <mi@v3.sk> 3.0.0-1
- New release
- Removed zabbix_agent binary and configuration (inet service).
- Added openssl BR
- Added version check for fping >= 3
- Backported removal of translation sources from upstream
- Removed flash removals, as there is no flash anymore
- Changed .htaccess clean-up to use search instead of direct entries

* Thu Nov 12 2015 Volker Fröhlich <volker27@gmx.at> - 2.4.7-1
- New release

* Mon Aug 10 2015 Volker Fröhlich <volker27@gmx.at> - 2.4.6-1
- New release

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 22 2015 Volker Fröhlich <volker27@gmx.at> - 2.4.5-1
- New release

* Tue Feb 24 2015 Volker Fröhlich <volker27@gmx.at> - 2.4.4-1
- New release

* Sat Dec 20 2014 Volker Fröhlich <volker27@gmx.at> - 2.4.3-1
- New release

* Wed Oct  8 2014 Volker Fröhlich <volker27@gmx.at> - 2.4.1-1
- New release

* Thu Sep 11 2014 Volker Fröhlich <volker27@gmx.at> - 2.4.0-1
- New major version release

* Mon Sep  1 2014 Volker Fröhlich <volker27@gmx.at> - 2.2.6-2
- Install tmpfiles configuration in the proper location per guidelines,
  thus solving the startup trouble due to missing directories
  (respectively BZ 1115251, 1081584, 982001, 1135696)
- Clean between builds, otherwise zabbix_{proxy,server} are compiled
  again on install; make server and proxy package noarch now
- Set the service type to forking in unit files (BZ 1132437),
  add PIDFile entry, remove RemainAfterExit, change /var/run to /run
- Correct path to traceroute in DB dumps again
- Leave database-specific datadir subdirectories to the dbfiles sub-packages
- Harmonize package descriptions and summaries

* Wed Aug 27 2014 Volker Fröhlich <volker27@gmx.at> - 2.2.6-1
- New upstream release
- Use the upstream tarball, now that non-free json was replaced with android-json

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Volker Fröhlich <volker27@gmx.at> - 2.2.5-1
- New upstream release

* Tue Jun 24 2014 Volker Fröhlich <volker27@gmx.at> - 2.2.4-1
- New upstream release
- Remove obsolete patches

* Fri Jun 20 2014 Volker Fröhlich <volker27@gmx.at> - 2.2.3-4
- Patch for ZBX-8151 (Local file inclusion via XXE attack) -- CVE-2014-3005

* Sun Jun  8 2014 Volker Fröhlich <volker27@gmx.at> - 2.2.3-3
- Patch for ZBX-8238 (logrt may continue reading an old file repeatedly)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Volker Fröhlich <volker27@gmx.at> - 2.2.3-1
- New upstream release

* Sun Feb 16 2014 Volker Fröhlich <volker27@gmx.at> - 2.2.2-1
- New major release
- Preserve timestamp on all install commands
- Provide bundled md5-deutsch
- Add noarch sub-packages for DB files
- Correct directory permissions
- Correct Conflicts directives
- Correct /var/lib/zabbixsrv owner and permissions
- Use dir directive for home directories and their sub-directories
- Update config patch
- Provide "zabbix"
- Add libxml2-devel as BR for VMware monitoring and --with-libxml2 flag
- Move user zabbixsrv to his own group
  - Split tmpfiles.d, thus solve BZ#982001 
  - Split lock, log and run locations
  - Adapt ownership and permissions
- Update README

* Sun Feb 16 2014 Volker Fröhlich <volker27@gmx.at> - 2.0.11-2
- Remove if clauses for Fedora/RHEL as they are obsolete in EL 7
- Use systemd scriplet macros (BZ#850378)
- Remove init scripts

* Wed Feb 12 2014 Volker Fröhlich <volker27@gmx.at> - 2.0.11-1
- New upstream release
- Truncate changelog

* Sun Dec 15 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.10-2
- The start function of the proxy init script had a typo causing failure
- Improved the section on running multiple instances in the README

* Fri Dec 13 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.10-1
- New upstream release
- Drop obsolete patch ZBX-7479
- Improve init scripts to not kill other instances (BZ#1018293)
- General overhaul of init scripts and documentation in README
- Harmonize scriptlet if-clause style

* Sun Nov  3 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.9-2
- Fix vulnerability for remote command execution injection
  (ZBX-7479, CVE-2013-6824)

* Wed Oct  9 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.9-1
- New upstream release
- Drop obsolete patches ZBX-6804, ZBX-7091, ZBX-6922, ZBX-6992

* Mon Sep 23 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.8-3
- Add SQL speed-up patch (ZBX-6804)
- Add SQL injection vulnerability patch (ZBX-7091, CVE-2013-5743)
- Add patch for failing XML host import (ZBX-6922)

* Fri Sep 13 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.8-2
- Add php-ldap as a requirement for the frontend
- Add patch for ZBX-6992

* Fri Aug 23 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.8-1
- New upstream release
- Create and configure a spooling directory for fping files outside of /tmp
- Update README to reflect that and add a SELinux section
- Drop PrivateTmp from systemd unit files
- Drop patch for ZBX-6526 (solved upstream)
- Drop patch for CVE-2012-6086 (solved upstream)
- Correct path for the flash applet when removing
- Truncate changelog

* Tue Jul 30 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.6-3
- Backport fix for CVE-2012-6086

* Tue May 07 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.6-2
- Add patch for ZBX-6526
- Solve permission problem with /var/run/zabbix in Fedora (BZ#904041)
- Remove origin of directories BZ#867159, comment 14 and 16

* Mon Apr 22 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.6-1
- New upstream release
- Drop ZBX-6290 and ZBX-6318 patches

* Tue Mar 19 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.5-3
- Include patch for ZBX-6318

* Tue Feb 12 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.5-2
- Include patch for ZBX-6290

* Tue Feb 12 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.5-1
- New upstream release
- Drop now-included patches
- Init file comments point to the actual configuration files now

* Sat Feb  9 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.4-5
- Dispensable version of COPYING is no more
- Correct path to traceroute in DB dumps again

* Tue Jan 22 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.4-4
- Remove zabbix_get plus manpage from the proxy files section
- Solve conflict for externalscripts symlink between proxy and
  server package

* Thu Jan 17 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.4-3
- Patch for CVE-2013-1364

* Mon Jan 14 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.4-2
- Apply patch for ZBX-6101
- Add su line to logrotate config file
- Do not own /var/run/zabbix on Fedora, systemd manages it
- Add forgotten chkconfig and service commands on agent preun script

* Sat Dec  8 2012 Volker Fröhlich <volker27@gmx.at> - 2.0.4-1
- New upstream release

* Fri Dec  7 2012 Volker Fröhlich <volker27@gmx.at> - 2.0.3-7
- Add SNMP source IP address patch

* Mon Nov 26 2012 Volker Fröhlich <volker27@gmx.at> - 2.0.3-6
- Apply fping 3 patch only for Fedora

* Tue Nov 13 2012 Volker Fröhlich <volker27@gmx.at> - 2.0.3-5
- Adapt httpd configuration file for Apache 2.4 (BZ#871498)

* Thu Nov  8 2012 Volker Fröhlich <volker27@gmx.at> - 2.0.3-4
- Require php explicitly again
- Remove traces of /usr/local in configuration files
- Improve Fedora README file

* Sun Oct 14 2012 Volker Fröhlich <volker27@gmx.at> - 2.0.3-3
- Correct capitalization in unit files, init scripts and package description
- Improve sysconfig sourcing in init scripts
- Correct post-script permissions and owner on rpmnew files
- Obsolete sqlite web and server sub-package

* Sun Oct 14 2012 Volker Fröhlich <volker27@gmx.at> - 2.0.3-2
- Include agent configuration file in base package for zabbix_sender
- Stricter permissions for server config file
- Adapt DB patches to our file layout
- Remove conditional around Source9
- doc-sub-package obsolete only for Fedora, where the package keeps
  the name "zabbix"
- Add missing requirement for proxy scriplet
- Remove Requires php because the PHP modules serve this purpose
- Use systemd's PrivateTmp only for F17 and up
- Correct proxy and server pre-scriplet (usergroup)

* Fri Oct  5 2012 Volker Fröhlich <volker27@gmx.at> - 2.0.3-1
- New upstream release
- Add Fedora specific README

* Mon Aug 27 2012 Volker Fröhlich <volker27@gmx.at> - 2.0.2-3
- Eliminate Sqlite server and web sub-package
  They never worked and are considered experimental by upstream
- Harmonize conditionals
- Put maintenance configuration in web configuration directory
- Adapt man pages to file layout
- Remove backup files from frontend
- Move maintenance configuration file to /etc/...
- Move ExternalScripts and AlertScripts to daemon home directory
- Don't ship SQL scripts as documentation

* Sun Aug 26 2012 Volker Fröhlich <volker27@gmx.at> - 2.0.2-2
- Use separate daemon users, so the agent can not parse the 
  database password
- Use PrivateTmp in unit files

* Wed Aug 15 2012 Volker Fröhlich <volker27@gmx.at> - 2.0.2-1
- New upstream release
- Unified specfile for sys-v-init scripts and systemd
- Switch to Alternatives system
- Source from systemconfig in init scripts

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Dan Horák <dan[at]danny.cz> - 2.0.1-1
- update to 2.0.1
- rebased patches
- upstream location (/etc) for config files is used with symlinks to the old /etc/zabbix
- dropped our own SNMP trap processor, upstream one running directly under net-snmp daemon is used instead
- moved zabbix_get and zabbix_sender tools to the main package
