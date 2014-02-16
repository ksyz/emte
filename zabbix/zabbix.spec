# TODO, maybe sometime:
# * F18 systemd macros, when EL6 reaches EOL
# * Do something about mutex errors sometimes occurring when init scripts'
#   restart is invoked; something like "sleep 2" between stop and start?
#   "Include" statement in config files needs patching in order to not load
#   various backup files (*.rpm{orig,new,save}, *~ etc) in that dir.
#   https://support.zabbix.com/browse/ZBXNEXT-497
# * Consider using systemd's ReadWriteDirectories

#TODO: systemctl reload seems to be necessary after switching with Alternatives
#TODO: If the DB path for a Sqlite proxy is configured wrong, it requires systemctl restart. Start doesn't work.

# Allow pinger lists in /var/lib/zabbixsrv/tmp
#echo "avc:  denied  { read } for  pid=3427 comm="fping6" path="/var/lib/zabbixsrv/tmp/zabbix_server_pgsql_3002.pinger" dev=dm-1 ino=20 scontext=system_u:system_r:ping_t:s0 tcontext=system_u:object_r:initrc_tmp_t:s0 tclass=file" | audit2allow -M myzab; sudo semodule -i myzab2.pp

#type=AVC msg=audit(1346965425.718:65127): avc:  denied  { getattr } for  pid=3427 comm="fping6" path="/var/lib/zabbixsrv/tmp/zabbix_server_pgsql_3002.pinger" dev=dm-1 ino=20 scontext=system_u:system_r:ping_t:s0 tcontext=system_u:object_r:initrc_tmp_t:s0 tclass=file

%global srcname zabbix

Name:           zabbix
Version:        2.0.11
Release:        2%{?dist}
Summary:        Open-source monitoring solution for your IT infrastructure

Group:          Applications/Internet
License:        GPLv2+
URL:            http://www.zabbix.com
#Source0:        http://downloads.sourceforge.net/%{srcname}/%{srcname}-%{version}.tar.gz
# upstream tarball minus src/zabbix_java/lib/org-json-2010-12-28.jar
Source0:        %{srcname}-%{version}-free.tar.gz
Source1:        %{srcname}-web.conf
Source5:        %{srcname}-logrotate.in
Source9:        %{srcname}-tmpfiles.conf
# systemd units -- Alternatives switches between them (they state their dependencies)
# https://support.zabbix.com/browse/ZBXNEXT-1593
Source10:       %{srcname}-agent.service
Source11:       %{srcname}-proxy-mysql.service
Source12:       %{srcname}-proxy-pgsql.service
Source13:       %{srcname}-proxy-sqlite3.service
Source14:       %{srcname}-server-mysql.service
Source15:       %{srcname}-server-pgsql.service

Source16:       %{srcname}-fedora.README

# local rules for config files
Patch0:         %{srcname}-2.0.2-config.patch
# local rules for config files - fonts
Patch1:         %{srcname}-2.0.3-fonts-config.patch
# remove flash content (#737337)
# https://support.zabbix.com/browse/ZBX-4794
Patch2:         %{srcname}-2.0.1-no-flash.patch
# adapt for fping3 - https://support.zabbix.com/browse/ZBX-4894
Patch3:         %{srcname}-1.8.12-fping3.patch

BuildRequires:   mysql-devel
BuildRequires:   postgresql-devel
BuildRequires:   sqlite-devel
BuildRequires:   net-snmp-devel
BuildRequires:   openldap-devel
BuildRequires:   gnutls-devel
BuildRequires:   iksemel-devel
BuildRequires:   unixODBC-devel
BuildRequires:   curl-devel
BuildRequires:   OpenIPMI-devel
BuildRequires:   libssh2-devel
BuildRequires:   systemd

Requires:        logrotate
# Could alternatively be conditional on Fedora/EL
%if %{srcname} != %{name}
Conflicts:       %{srcname}
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

%package server
Summary:             Zabbix server common files
Group:               Applications/Internet
Requires:            %{name} = %{version}-%{release}
Requires:            %{name}-server-implementation = %{version}-%{release}
Requires:            fping
Requires:            traceroute
Requires(pre):       shadow-utils
Requires(post):      systemd
Requires(preun):     systemd
Requires(postun):    systemd

%description server
Zabbix server common files

%package server-mysql
Summary:             Zabbix server compiled to use MySQL
Group:               Applications/Internet
Requires:            %{name} = %{version}-%{release}
Requires:            %{name}-server = %{version}-%{release}
Requires(post):      %{_sbindir}/update-alternatives
Requires(preun):     %{_sbindir}/alternatives
Requires(postun):    %{_sbindir}/update-alternatives
Provides:            %{name}-server-implementation = %{version}-%{release}

%description server-mysql
Zabbix server compiled to use MySQL

%package server-pgsql
Summary:             Zabbix server compiled to use PostgresSQL
Group:               Applications/Internet
Requires:            %{name} = %{version}-%{release}
Requires:            %{name}-server = %{version}-%{release}
Requires(post):      %{_sbindir}/update-alternatives
Requires(preun):     %{_sbindir}/alternatives
Requires(postun):    %{_sbindir}/update-alternatives
Provides:            %{name}-server-implementation = %{version}-%{release}

%description server-pgsql
Zabbix server compiled to use PostgresSQL

%package agent
Summary:             Zabbix Agent
Group:               Applications/Internet
Requires:            %{name} = %{version}-%{release}
Requires(pre):       shadow-utils
Requires(post):      systemd
Requires(preun):     systemd
Requires(postun):    systemd

%description agent
The Zabbix client agent, to be installed on monitored systems.

%package proxy
Summary:             Zabbix Proxy
Group:               Applications/Internet
Requires:            %{name} = %{version}-%{release}
Requires:            %{name}-proxy-implementation = %{version}-%{release}
Requires(pre):       shadow-utils
Requires(post):      systemd
Requires(preun):     systemd
Requires(postun):    systemd
Requires:            fping

%description proxy
The Zabbix proxy

%package proxy-mysql
Summary:             Zabbix proxy compiled to use MySQL
Group:               Applications/Internet
Requires:            %{name}-proxy = %{version}-%{release}
Provides:            %{name}-proxy-implementation = %{version}-%{release}
Requires(post):      %{_sbindir}/update-alternatives
Requires(preun):     %{_sbindir}/alternatives
Requires(postun):    %{_sbindir}/update-alternatives

%description proxy-mysql
The Zabbix proxy compiled to use MySQL

%package proxy-pgsql
Summary:             Zabbix proxy compiled to use PostgreSQL
Group:               Applications/Internet
Requires:            %{name}-proxy = %{version}-%{release}
Provides:            %{name}-proxy-implementation = %{version}-%{release}
Requires(post):      %{_sbindir}/update-alternatives
Requires(preun):     %{_sbindir}/alternatives
Requires(postun):    %{_sbindir}/update-alternatives

%description proxy-pgsql
The Zabbix proxy compiled to use PostgreSQL

%package proxy-sqlite3
Summary:             Zabbix proxy compiled to use SQLite
Group:               Applications/Internet
Requires:            %{name}-proxy = %{version}-%{release}
Provides:            %{name}-proxy-implementation = %{version}-%{release}
Requires(post):      %{_sbindir}/update-alternatives
Requires(preun):     %{_sbindir}/alternatives
Requires(postun):    %{_sbindir}/update-alternatives

%description proxy-sqlite3
The Zabbix proxy compiled to use SQLite

%package web
Summary:         Zabbix Web Frontend
Group:           Applications/Internet
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
Requires:        dejavu-sans-fonts
Requires:        %{name} = %{version}-%{release}
Requires:        %{name}-web-database = %{version}-%{release}

%description web
The php frontend to display the Zabbix web interface.

%package web-mysql
Summary:         Zabbix web frontend for MySQL
Group:           Applications/Internet
BuildArch:       noarch
Requires:        %{name}-web = %{version}-%{release}
Requires:        php-mysql
Provides:        %{name}-web-database = %{version}-%{release}
Obsoletes:       %{name}-web <= 1.5.3-0.1

%description web-mysql
Zabbix web frontend for MySQL

%package web-pgsql
Summary:         Zabbix web frontend for PostgreSQL
Group:           Applications/Internet
BuildArch:       noarch
Requires:        %{name}-web = %{version}-%{release}
Requires:        php-pgsql
Provides:        %{name}-web-database = %{version}-%{release}

%description web-pgsql
Zabbix web frontend for PostgreSQL


%prep
%setup0 -q -n %{srcname}-%{version}
%patch0 -p1
%patch1 -p1

# Remove flash applet
# https://support.zabbix.com/browse/ZBX-4794
%patch2 -p1
rm -f frontends/php/images/flash/zbxclock.swf

%patch3 -p1

# Logrotate's su option is only available in Fedora and EL 7
sed -i '/su zabbix zabbix/d' %{SOURCE5}

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
rm -f frontends/php/include/.htaccess
rm -f frontends/php/api/.htaccess
rm -f frontends/php/conf/.htaccess

# Adapt configuration file options
sed -i \
    -e 's|# PidFile=.*|PidFile=%{_localstatedir}/run/zabbix/zabbix_agentd.pid|g' \
    -e 's|^LogFile=.*|LogFile=%{_localstatedir}/log/zabbix/zabbix_agentd.log|g' \
    -e 's|# LogFileSize=.*|LogFileSize=0|g' \
    -e 's|/usr/local||g' \
    conf/zabbix_agentd.conf

sed -i \
    -e 's|/usr/local||g' \
    conf/zabbix_agent.conf

#TODO: It'd be better to leave the defaults in a commment and just override them, as they are still hard-coded!
sed -i \
    -e 's|# PidFile=.*|PidFile=%{_localstatedir}/run/zabbix/zabbix_server.pid|g' \
    -e 's|^LogFile=.*|LogFile=%{_localstatedir}/log/zabbix/zabbix_server.log|g' \
    -e 's|# LogFileSize=.*|LogFileSize=0|g' \
    -e 's|# AlertScriptsPath=${datadir}/zabbix/|AlertScriptsPath=%{_sharedstatedir}/zabbixsrv/|g' \
    -e 's|^DBUser=root|DBUser=zabbix|g' \
    -e 's|# DBSocket=/tmp/mysql.sock|DBSocket=%{_sharedstatedir}/mysql/mysql.sock|g' \
    -e 's|# ExternalScripts=\${datadir}/zabbix/externalscripts|ExternalScripts=%{_sharedstatedir}/zabbixsrv/externalscripts|' \
    -e 's|# TmpDir=\/tmp|TmpDir=%{_sharedstatedir}/zabbixsrv/tmp|' \
    -e 's|/usr/local||g' \
    conf/zabbix_server.conf

#TODO: It'd be better to leave the defaults in a commment and just override them, as they are still hard-coded!
sed -i \
    -e 's|# PidFile=.*|PidFile=%{_localstatedir}/run/zabbix/zabbix_proxy.pid|g' \
    -e 's|^LogFile=.*|LogFile=%{_localstatedir}/log/zabbix/zabbix_proxy.log|g' \
    -e 's|# LogFileSize=.*|LogFileSize=0|g' \
    -e 's|^DBUser=root|DBUser=zabbix|g' \
    -e 's|# DBSocket=/tmp/mysql.sock|DBSocket=%{_sharedstatedir}/mysql/mysql.sock|g' \
    -e 's|# ExternalScripts=\${datadir}/zabbix/externalscripts|ExternalScripts=%{_sharedstatedir}/zabbixsrv/externalscripts|' \
    -e 's|# TmpDir=\/tmp|TmpDir=%{_sharedstatedir}/zabbixsrv/tmp|' \
    -e 's|/usr/local||g' \
    conf/zabbix_proxy.conf

#TODO: Ticket
# Adapt man pages and SQL patches
sed -i 's|/usr/local||g;s| (if not modified during compile time).||' man/*.man
sed -i 's|/usr/local||g' \
    upgrades/dbpatches/2.0/mysql/patch.sql \
    upgrades/dbpatches/2.0/postgresql/patch.sql

# Install README file
install -m0644 %{SOURCE16} .


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
    --with-jabber
    --with-unixodbc
    --with-ssh2
"

# Frontend doesn't work for SQLite, thus don't build server
%configure $common_flags --with-sqlite3
make %{?_smp_mflags}
mv src/zabbix_proxy/zabbix_proxy src/zabbix_proxy/zabbix_proxy_sqlite3

%configure $common_flags --with-mysql --enable-server
make %{?_smp_mflags}
mv src/zabbix_server/zabbix_server src/zabbix_server/zabbix_server_mysql
mv src/zabbix_proxy/zabbix_proxy src/zabbix_proxy/zabbix_proxy_mysql

%configure $common_flags --with-postgresql --enable-server
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
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/zabbix
mkdir -p $RPM_BUILD_ROOT%{_unitdir}

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

# This file is used to switch the frontend to maintenance mode
mv $RPM_BUILD_ROOT%{_datadir}/%{srcname}/conf/maintenance.inc.php $RPM_BUILD_ROOT%{_sysconfdir}/%{srcname}/web/maintenance.inc.php

# Drop Apache config file in place
install -m 0644 -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/%{srcname}.conf

# Install log rotation
sed -e 's|COMPONENT|agentd|g' %{SOURCE5} > \
     $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zabbix-agent
sed -e 's|COMPONENT|server|g' %{SOURCE5} > \
     $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zabbix-server
sed -e 's|COMPONENT|proxy|g' %{SOURCE5} > \
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
ln -sf %{_sysconfdir}/zabbix_agent.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{srcname}/zabbix_agent.conf
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
    install -dm 755 $datadir/upgrades/{1.6,1.8,2.0}
    cp -p database/$db/* $datadir
    cp -pR upgrades/dbpatches/1.6/$db/* $datadir/upgrades/1.6
    cp -pR upgrades/dbpatches/1.8/$db/* $datadir/upgrades/1.8
    cp -pR upgrades/dbpatches/2.0/$db/* $datadir/upgrades/2.0
done

install -dm 755 $RPM_BUILD_ROOT%{_datadir}/%{srcname}-sqlite3
cp -p database/sqlite3/schema.sql $RPM_BUILD_ROOT%{_datadir}/%{srcname}-sqlite3

# systemd must create /var/run/%{srcname}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d
install -m 0644 %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d/zabbix.conf


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
getent group zabbix > /dev/null || groupadd -r zabbix
getent passwd zabbixsrv > /dev/null || \
    useradd -r -g zabbix -d %{_sharedstatedir}/zabbixsrv -s /sbin/nologin \
    -c "Zabbix Monitoring System -- Proxy or server" zabbixsrv
:

%preun server
  %systemd_preun zabbix-server.service

%pre proxy
getent group zabbix > /dev/null || groupadd -r zabbix
getent passwd zabbixsrv > /dev/null || \
    useradd -r -g zabbix -d %{_sharedstatedir}/zabbixsrv -s /sbin/nologin \
    -c "Zabbix Monitoring System -- Proxy or server" zabbixsrv
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
%doc AUTHORS ChangeLog COPYING NEWS README %{srcname}-fedora.README
%dir %{_sysconfdir}/%{srcname}
%config(noreplace) %{_sysconfdir}/zabbix_agentd.conf
%config(noreplace) %{_sysconfdir}/%{srcname}/zabbix_agentd.conf
%config(noreplace) %{_sysconfdir}/tmpfiles.d/zabbix.conf
%{_bindir}/zabbix_get
%{_bindir}/zabbix_sender
%{_mandir}/man1/zabbix_get.1*
%{_mandir}/man1/zabbix_sender.1*

%files server
%doc misc/snmptrap/zabbix_trap_receiver.pl
%attr(0775,root,zabbix) %dir %{_localstatedir}/log/zabbix
%attr(0600,zabbixsrv,zabbix) %config(noreplace) %{_sysconfdir}/zabbix_server.conf
%config(noreplace) %{_sysconfdir}/%{srcname}/zabbix_server.conf
%config(noreplace) %{_sysconfdir}/%{srcname}/externalscripts
%config(noreplace) %{_sysconfdir}/%{srcname}/alertscripts
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-server
%ghost %{_sbindir}/zabbix_server
%attr(0755,zabbixsrv,zabbix) %{_sharedstatedir}/zabbixsrv
%ghost %{_unitdir}/zabbix-server.service
%{_mandir}/man8/zabbix_server.8*

%files server-mysql
%{_datadir}/%{srcname}-mysql
%{_sbindir}/zabbix_server_mysql
%{_unitdir}/zabbix-server-mysql.service

%files server-pgsql
%{_datadir}/%{srcname}-postgresql
%{_sbindir}/zabbix_server_pgsql
%{_unitdir}/zabbix-server-pgsql.service

%files agent
%doc conf/zabbix_agentd/*.conf
%attr(0775,root,zabbix) %dir %{_localstatedir}/log/zabbix
%config(noreplace) %{_sysconfdir}/zabbix_agent.conf
%config(noreplace) %{_sysconfdir}/%{srcname}/zabbix_agent.conf
%config(noreplace) %{_sysconfdir}/zabbix_agentd.conf
%config(noreplace) %{_sysconfdir}/%{srcname}/zabbix_agentd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-agent
%attr(0755,zabbix,zabbix) %dir %{_sharedstatedir}/zabbix
%{_unitdir}/zabbix-agent.service
%{_sbindir}/zabbix_agent
%{_sbindir}/zabbix_agentd
%{_mandir}/man8/zabbix_agentd.8*

%files proxy
%doc misc/snmptrap/zabbix_trap_receiver.pl
%attr(0775,root,zabbix) %dir %{_localstatedir}/log/zabbix
%attr(0600,zabbixsrv,zabbix) %config(noreplace) %{_sysconfdir}/zabbix_proxy.conf
%config(noreplace) %{_sysconfdir}/%{srcname}/zabbix_proxy.conf
%config(noreplace) %{_sysconfdir}/%{srcname}/externalscripts
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-proxy
%ghost %{_sbindir}/zabbix_proxy
%attr(0755,zabbixsrv,zabbix) %{_sharedstatedir}/zabbixsrv
%ghost %{_unitdir}/zabbix-proxy.service
%{_mandir}/man8/zabbix_proxy.8*

%files proxy-mysql
%{_datadir}/%{srcname}-mysql
%{_sbindir}/zabbix_proxy_mysql
%{_unitdir}/zabbix-proxy-mysql.service

%files proxy-pgsql
%{_datadir}/%{srcname}-postgresql
%{_sbindir}/zabbix_proxy_pgsql
%{_unitdir}/zabbix-proxy-pgsql.service

%files proxy-sqlite3
%{_datadir}/%{srcname}-sqlite3
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

* Thu Oct  3 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.8-3
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

* Mon Apr 22 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.6-1
- New upstream release

* Tue Feb 12 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.5-1
- New upstream release
- Drop now-included patches

* Tue Jan 22 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.4-5
- Remove zabbix_get plus manpage from the proxy files section
- Solve conflict for externalscripts symlink between proxy and
  server package

* Sun Jan 20 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.4-4
- Remove origin of directories BZ#867159, comment 14 and 16

* Thu Jan 17 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.4-3
- Patch for CVE-2013-1364

* Mon Jan 14 2013 Volker Fröhlich <volker27@gmx.at> - 2.0.4-2
- New upstream release
- Synchronized spec file with zabbix20
- Apply patch for ZBX-6101
- Add forgotten chkconfig and service commands on agent preun script
- Add SNMP source IP address patch
- Apply fping 3 patch only for Fedora

* Fri Nov 30 2012 Volker Fröhlich <volker27@gmx.at> - 2.0.3-7
- Correct and complete conditionals for /var/run/zabbix
- su line only works in Fedora

* Fri Nov 30 2012 Orion Poplawski <orion@cora.nwra.com> - 2.0.3-6
- Add su line to logrotate config file
- Do not own /var/run/zabbix on Fedora, systemd manages it

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
