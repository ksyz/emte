# TODO, maybe sometime:
# * F18 systemd macros, when EL6 reaches EOL
# * Do something about mutex errors sometimes occurring when init scripts'
#   restart is invoked; something like "sleep 2" between stop and start?
# * Use "Include" in zabbix_{agentd,proxy,server}.conf, point to corresponding
#   /etc/zabbix/zabbix_*.conf.d/ dir; needs patching in order to not load
#   various backup files (*.rpm{orig,new,save}, *~ etc) in that dir.
#   https://support.zabbix.com/browse/ZBXNEXT-497 -- Scheduled for 2.2
# * zabbixsrv could be member of the groups zabbixsrv and zabbix
# * Consider using systemd's ReadWriteDirectories
# * Consider mod_proxy patch from Debian
#   https://support.zabbix.com/browse/ZBX-4986

#TODO: systemctl reload seems to be necessary after switching with Alternatives
#TODO: If the DB path for a Sqlite proxy is configured wrong, it requires systemctl restart. Start doesn't work.

# Some info on SELinux that should go to our README

# Allow to connect the frontend to a database
# setsebool -P httpd_can_network_connect_db 1

# Allow the frontend to check whether Zabbix server is reachable
#echo "avc:  denied  { name_connect } for  pid=20619 comm="httpd" dest=10051 scontext=system_u:system_r:httpd_t:s0 tcontext=system_u:object_r:zabbix_port_t:s0 tclass=tcp_socket" | audit2allow -M myhttpd; sudo semodule -i myhttpd.pp

#TODO: Consider filing a bug for selinux-policy
# Allow ping from the frontend
#echo "avc:  denied  { setpgid } for  pid=31880 comm="zabbix_server_p" scontext=system_u:system_r:zabbix_t:s0 tcontext=system_u:system_r:zabbix_t:s0 tclass=process" | audit2allow -M myzab; sudo semodule -i myzab.pp

# Allow host list for pings in /tmp
#echo "avc:  denied  { read } for  pid=3427 comm="fping6" path="/tmp/zabbix_server_pgsql_3002.pinger" dev=dm-1 ino=20 scontext=system_u:system_r:ping_t:s0 tcontext=system_u:object_r:initrc_tmp_t:s0 tclass=file" | audit2allow -M myzab; sudo semodule -i myzab2.pp

#type=AVC msg=audit(1346965425.718:65127): avc:  denied  { getattr } for  pid=3427 comm="fping6" path="/tmp/zabbix_server_pgsql_3002.pinger" dev=dm-1 ino=20 scontext=system_u:system_r:ping_t:s0 tcontext=system_u:object_r:initrc_tmp_t:s0 tclass=file


%global srcname zabbix

Name:           zabbix20
Version:        2.0.3
Release:        3%{?dist}
Summary:        Open-source monitoring solution for your IT infrastructure

Group:          Applications/Internet
License:        GPLv2+
URL:            http://www.zabbix.com
#Source0:        http://downloads.sourceforge.net/%{srcname}/%{srcname}-%{version}.tar.gz
# upstream tarball minus src/zabbix_java/lib/org-json-2010-12-28.jar
Source0:        %{srcname}-%{version}-free.tar.gz
Source1:        %{srcname}-web.conf
Source2:        %{srcname}-server.init
Source3:        %{srcname}-agent.init
Source4:        %{srcname}-proxy.init
Source5:        %{srcname}-logrotate.in
Source9:        %{srcname}-tmpfiles.conf
# systemd units -- Alternatives switches between them (they state their dependencies)
#TODO: Submit upstream
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
%if 0%{?fedora}
BuildRequires:   systemd-units
%endif

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
%if 0%{?fedora}
Requires(post):      systemd-units
Requires(preun):     systemd-units
Requires(postun):    systemd-units
%else
Requires(post):      /sbin/chkconfig
Requires(preun):     /sbin/chkconfig
Requires(preun):     /sbin/service
Requires(postun):    /sbin/service
%endif

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
%if 0%{?fedora}
Requires(post):      systemd-units
Requires(preun):     systemd-units
Requires(postun):    systemd-units
%else
Requires(post):      /sbin/chkconfig
Requires(preun):     /sbin/chkconfig
Requires(preun):     /sbin/service
Requires(postun):    /sbin/service
%endif

%description agent
The Zabbix client agent, to be installed on monitored systems.

%package proxy
Summary:             Zabbix Proxy
Group:               Applications/Internet
Requires:            %{name} = %{version}-%{release}
Requires:            %{name}-proxy-implementation = %{version}-%{release}
Requires(pre):       shadow-utils
%if 0%{?fedora}
Requires(post):      systemd-units
Requires(preun):     systemd-units
Requires(postun):    systemd-units
%else
Requires(post):      /sbin/chkconfig
Requires(preun):     /sbin/chkconfig
Requires(preun):     /sbin/service
Requires(postun):    /sbin/service
%endif
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
Requires:        php-gd
Requires:        php-bcmath
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
%patch3 -p1

# remove flash applet
# https://support.zabbix.com/browse/ZBX-4794
%patch2 -p1
rm -f frontend/php/images/flash/zbxclock.swf

# remove bundled java libs
rm -rf src/zabbix_java/lib/*.jar

# remove prebuilt Windows binaries
rm -rf bin

# remove included fonts
rm -rf frontends/php/fonts

# remove executable permissions
chmod a-x upgrades/dbpatches/*/mysql/upgrade

# All libraries are expected in /usr/lib or /usr/local/lib
# https://support.zabbix.com/browse/ZBXNEXT-1296
sed -i.orig -e 's|_LIBDIR=/usr/lib|_LIBDIR=%{_libdir}|g' \
    configure

# kill off .htaccess files, options set in SOURCE1
rm -f frontends/php/include/.htaccess
rm -f frontends/php/api/.htaccess
rm -f frontends/php/conf/.htaccess

# Remove dispensable COPYING
# https://support.zabbix.com/browse/ZBX-5568
# Solved for releases after 2.0.3
rm -rf frontends/php/conf/COPYING

# set timestamp on modified config file and directories
touch -r frontends/php/css.css frontends/php/include/config.inc.php \
    frontends/php/include/defines.inc.php \
    frontends/php/include \
    frontends/php/include/classes

# fix config file options
sed -i \
    -e 's|# PidFile=.*|PidFile=%{_localstatedir}/run/%{srcname}/zabbix_agentd.pid|g' \
    -e 's|^LogFile=.*|LogFile=%{_localstatedir}/log/%{srcname}/zabbix_agentd.log|g' \
    -e 's|# LogFileSize=.*|LogFileSize=0|g' \
    conf/zabbix_agentd.conf

sed -i \
    -e 's|# PidFile=.*|PidFile=%{_localstatedir}/run/%{srcname}/zabbix_server.pid|g' \
    -e 's|^LogFile=.*|LogFile=%{_localstatedir}/log/%{srcname}/zabbix_server.log|g' \
    -e 's|# LogFileSize=.*|LogFileSize=0|g' \
    -e 's|# AlertScriptsPath=${datadir}/zabbix/|AlertScriptsPath=%{_sharedstatedir}/zabbixsrv/|g' \
    -e 's|^DBUser=root|DBUser=zabbix|g' \
    -e 's|# DBSocket=/tmp/mysql.sock|DBSocket=%{_sharedstatedir}/mysql/mysql.sock|g' \
    -e 's|# ExternalScripts=\${datadir}/zabbix/externalscripts|ExternalScripts=%{_sharedstatedir}/zabbixsrv/externalscripts|' \
    conf/zabbix_server.conf

sed -i \
    -e 's|# PidFile=.*|PidFile=%{_localstatedir}/run/%{srcname}/zabbix_proxy.pid|g' \
    -e 's|^LogFile=.*|LogFile=%{_localstatedir}/log/%{srcname}/zabbix_proxy.log|g' \
    -e 's|# LogFileSize=.*|LogFileSize=0|g' \
    -e 's|^DBUser=root|DBUser=zabbix|g' \
    -e 's|# DBSocket=/tmp/mysql.sock|DBSocket=%{_sharedstatedir}/mysql/mysql.sock|g' \
    -e 's|# ExternalScripts=\${datadir}/zabbix/externalscripts|ExternalScripts=%{_sharedstatedir}/zabbixsrv/externalscripts|' \
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
    --datadir=%{_sharedstatedir}/zabbixsrv
"

# Frontend doesn't work for Sqlite, thus don't build server
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
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/%{srcname}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/%{srcname}
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
%if 0%{?rhel}
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
%endif

# Frontend
mkdir -p $RPM_BUILD_ROOT%{_datadir}

# Home directories
#TODO: Duplicate directory exists for unknown reason
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/zabbix
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/zabbixsrv
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/zabbixsrv/externalscripts
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/zabbixsrv/alertscripts

# Install binaries
make DESTDIR=$RPM_BUILD_ROOT install
install -m 0755 -p src/zabbix_server/zabbix_server_* $RPM_BUILD_ROOT%{_sbindir}/
install -m 0755 -p src/zabbix_proxy/zabbix_proxy_* $RPM_BUILD_ROOT%{_sbindir}/

# Install the frontend after removing backup files from patching
find frontends/php -name '*.orig' -exec rm {} \;
cp -a frontends/php $RPM_BUILD_ROOT%{_datadir}/%{srcname}

# prepare ghosted config file
#TODO: Simplify that? Like /etc/zabbix_web/zabbix.conf.php?
touch $RPM_BUILD_ROOT%{_sysconfdir}/%{srcname}/web/zabbix.conf.php

# This file is used to switch the frontend to maintenance mode
mv $RPM_BUILD_ROOT%{_datadir}/%{srcname}/conf/maintenance.inc.php $RPM_BUILD_ROOT%{_sysconfdir}/%{srcname}/web/maintenance.inc.php

# drop Apache config file in place
install -m 0644 -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/%{srcname}.conf

# install log rotation
cat %{SOURCE5} | sed -e 's|COMPONENT|agentd|g' > \
     $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zabbix-agent
cat %{SOURCE5} | sed -e 's|COMPONENT|server|g' > \
     $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zabbix-server
cat %{SOURCE5} | sed -e 's|COMPONENT|proxy|g' > \
     $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zabbix-proxy

%if 0%{?fedora}
# Install different systemd units because of the requirements for DBMS daemons
install -m 0644 -p %{SOURCE10} $RPM_BUILD_ROOT%{_unitdir}/zabbix-agent.service
install -m 0644 -p %{SOURCE11} $RPM_BUILD_ROOT%{_unitdir}/zabbix-proxy-mysql.service
install -m 0644 -p %{SOURCE12} $RPM_BUILD_ROOT%{_unitdir}/zabbix-proxy-pgsql.service
install -m 0644 -p %{SOURCE13} $RPM_BUILD_ROOT%{_unitdir}/zabbix-proxy-sqlite3.service
install -m 0644 -p %{SOURCE14} $RPM_BUILD_ROOT%{_unitdir}/zabbix-server-mysql.service
install -m 0644 -p %{SOURCE15} $RPM_BUILD_ROOT%{_unitdir}/zabbix-server-pgsql.service
# PrivateTmp available from F17 on
%if 0%{?fedora} < 17
sed -i '/^PrivateTmp/d' $RPM_BUILD_ROOT%{_unitdir}/zabbix-agent.service
sed -i '/^PrivateTmp/d' $RPM_BUILD_ROOT%{_unitdir}/zabbix-proxy-mysql.service
sed -i '/^PrivateTmp/d' $RPM_BUILD_ROOT%{_unitdir}/zabbix-proxy-pgsql.service
sed -i '/^PrivateTmp/d' $RPM_BUILD_ROOT%{_unitdir}/zabbix-proxy-sqlite3.service
sed -i '/^PrivateTmp/d' $RPM_BUILD_ROOT%{_unitdir}/zabbix-server-mysql.service
sed -i '/^PrivateTmp/d' $RPM_BUILD_ROOT%{_unitdir}/zabbix-server-pgsql.service
%endif
%else
# init scripts
install -m 0755 -p %{SOURCE3} $RPM_BUILD_ROOT%{_initrddir}/zabbix-agent
install -m 0755 -p %{SOURCE4} $RPM_BUILD_ROOT%{_initrddir}/zabbix-proxy
install -m 0755 -p %{SOURCE2} $RPM_BUILD_ROOT%{_initrddir}/zabbix-server
%endif

# Ghosted alternatives 
touch $RPM_BUILD_ROOT%{_unitdir}/zabbix-server.service
touch $RPM_BUILD_ROOT%{_unitdir}/zabbix-proxy.service

# install compatibility links for config files
ln -sf %{_sysconfdir}/zabbix_agent.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{srcname}/zabbix_agent.conf
ln -sf %{_sysconfdir}/zabbix_agentd.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{srcname}/zabbix_agentd.conf
ln -sf %{_sysconfdir}/zabbix_server.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{srcname}/zabbix_server.conf
ln -sf %{_sysconfdir}/zabbix_proxy.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{srcname}/zabbix_proxy.conf
ln -sf %{_sharedstatedir}/zabbixsrv/externalscripts $RPM_BUILD_ROOT%{_sysconfdir}/%{srcname}/externalscripts
ln -sf %{_sharedstatedir}/zabbixsrv/alertscripts $RPM_BUILD_ROOT%{_sysconfdir}/%{srcname}/alertscripts
#TODO: What does that do to existing directories?

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

%if 0%{?fedora}
# systemd must create /var/run/%{srcname}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d
install -m 0644 %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/tmpfiles.d/zabbix.conf
%endif


%post server
%if 0%{?fedora}
if [ $1 -eq 1 ] ; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%else
/sbin/chkconfig --add zabbix-server
%endif

if [ $1 -gt 1 ]
then
  # Apply permissions also in *.rpmnew upgrades from old permissive ones
  chmod 0600 %{_sysconfdir}/zabbix_server.conf
  chown zabbixsrv:zabbix %{_sysconfdir}/zabbix_server.conf
fi
:

%post server-mysql
%if 0%{?fedora}
%{_sbindir}/update-alternatives --install %{_sbindir}/%{srcname}_server \
    %{srcname}-server %{_sbindir}/%{srcname}_server_mysql 10 \
        --slave %{_unitdir}/zabbix-server.service %{srcname}-server-systemd \
            %{_unitdir}/zabbix-server-mysql.service
%else
%{_sbindir}/update-alternatives --install %{_sbindir}/%{srcname}_server \
    %{srcname}-server %{_sbindir}/%{srcname}_server_mysql 10
%endif

%post server-pgsql
%if 0%{?fedora}
%{_sbindir}/update-alternatives --install %{_sbindir}/%{srcname}_server \
    %{srcname}-server %{_sbindir}/%{srcname}_server_pgsql 10 \
        --slave %{_unitdir}/zabbix-server.service %{srcname}-server-systemd \
            %{_unitdir}/zabbix-server-pgsql.service
%else
%{_sbindir}/update-alternatives --install %{_sbindir}/%{srcname}_server \
    %{srcname}-server %{_sbindir}/%{srcname}_server_pgsql 10
%endif

%post proxy
%if 0%{?fedora}
if [ $1 -eq 1 ] ; then
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%else
/sbin/chkconfig --add zabbix-proxy
%endif

if [ $1 -gt 1 ]
then
  # Apply permissions also in *.rpmnew upgrades from old permissive ones
  chmod 0600 %{_sysconfdir}/zabbix_proxy.conf
  chown zabbixsrv:zabbix %{_sysconfdir}/zabbix_proxy.conf
fi
:

%post proxy-mysql
%if 0%{?fedora}
%{_sbindir}/update-alternatives --install %{_sbindir}/%{srcname}_proxy \
    %{srcname}-proxy %{_sbindir}/%{srcname}_proxy_mysql 10 \
        --slave %{_unitdir}/zabbix-proxy.service %{srcname}-proxy-systemd \
            %{_unitdir}/zabbix-proxy-mysql.service
%else
%{_sbindir}/update-alternatives --install %{_sbindir}/%{srcname}_proxy \
    %{srcname}-proxy %{_sbindir}/%{srcname}_proxy_mysql 10
%endif

%post proxy-pgsql
%if 0%{?fedora}
%{_sbindir}/update-alternatives --install %{_sbindir}/%{srcname}_proxy \
    %{srcname}-proxy %{_sbindir}/%{srcname}_proxy_pgsql 10 \
        --slave %{_unitdir}/zabbix-proxy.service %{srcname}-proxy-systemd \
            %{_unitdir}/zabbix-proxy-pgsql.service
%else
%{_sbindir}/update-alternatives --install %{_sbindir}/%{srcname}_proxy \
    %{srcname}-proxy %{_sbindir}/%{srcname}_proxy_pgsql 10
%endif

%post proxy-sqlite3
%if 0%{?fedora}
%{_sbindir}/update-alternatives --install %{_sbindir}/%{srcname}_proxy \
    %{srcname}-proxy %{_sbindir}/%{srcname}_proxy_sqlite3 10 \
        --slave %{_unitdir}/zabbix-proxy.service %{srcname}-proxy-systemd \
            %{_unitdir}/zabbix-proxy-sqlite3.service
%else
%{_sbindir}/update-alternatives --install %{_sbindir}/%{srcname}_proxy \
    %{srcname}-proxy %{_sbindir}/%{srcname}_proxy_sqlite3 10
%endif

%pre agent
getent group zabbix > /dev/null || groupadd -r zabbix
getent passwd zabbix > /dev/null || \
    useradd -r -g zabbix -d %{_sharedstatedir}/zabbix -s /sbin/nologin \
    -c "Zabbix Monitoring System" zabbix
:

%post agent
if [ $1 -eq 1 ] ; then
%if 0%{?fedora}
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%else
    /sbin/chkconfig --add zabbix-agent || :
%endif
fi

%pre server
getent group zabbix > /dev/null || groupadd -r zabbix
getent passwd zabbixsrv > /dev/null || \
    useradd -r -g zabbix -d %{_sharedstatedir}/zabbixsrv -s /sbin/nologin \
    -c "Zabbix Monitoring System -- Proxy or server" zabbixsrv
:

%preun server
if [ "$1" = 0 ]
then
%if 0%{?fedora}
  /bin/systemctl --no-reload disable zabbix-server.service > /dev/null 2>&1 || :
  /bin/systemctl stop zabbix-server.service > /dev/null 2>&1 || :
%else
  /sbin/service zabbix-server stop >/dev/null 2>&1
  /sbin/chkconfig --del zabbix-server
%endif
fi
:

#TODO: Update path from 1.8.6 with wrongly set home dir?
%pre proxy
getent group zabbix > /dev/null || groupadd -r zabbix
getent passwd zabbixsrv > /dev/null || \
    useradd -r -g zabbix -d %{_sharedstatedir}/zabbixsrv -s /sbin/nologin \
    -c "Zabbix Monitoring System -- Proxy or server" zabbixsrv
:

%preun proxy
if [ "$1" = 0 ]
then
%if 0%{?fedora}
  /bin/systemctl --no-reload disable zabbix-proxy.service > /dev/null 2>&1 || :
  /bin/systemctl stop zabbix-proxy.service > /dev/null 2>&1 || :
%else
  /sbin/service zabbix-proxy stop >/dev/null 2>&1
  /sbin/chkconfig --del zabbix-proxy
%endif
fi
:

%preun agent
%if 0%{?fedora}
if [ $1 -eq 0 ] ; then
  /bin/systemctl --no-reload disable zabbix-agent.service > /dev/null 2>&1 || :
  /bin/systemctl stop zabbix-agent.service > /dev/null 2>&1 || :
fi
%endif

%postun server
%if 0%{?fedora}
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%endif

if [ $1 -ge 1 ] ; then
%if 0%{?fedora}
  /bin/systemctl try-restart zabbix-server.service >/dev/null 2>&1 || :
%else
  /sbin/service zabbix-server try-restart >/dev/null 2>&1 || :
%endif
fi

%postun server-mysql
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove %{srcname}-server %{_sbindir}/%{srcname}_server_mysql
fi

%postun server-pgsql
if [ $1 -eq 0 ] ; then
    %{_sbindir}/update-alternatives --remove %{srcname}-server %{_sbindir}/%{srcname}_server_pgsql
fi

%postun proxy
%if 0%{?fedora}
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%endif

if [ $1 -ge 1 ] ; then
%if 0%{?fedora}
    /bin/systemctl try-restart zabbix-proxy.service >/dev/null 2>&1 || :
%else
    /sbin/service zabbix-proxy try-restart >/dev/null 2>&1 || :
%endif
fi

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
%if 0%{?fedora}
  /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%endif

if [ $1 -ge 1 ] ; then
%if 0%{?fedora}
    /bin/systemctl try-restart zabbix-agent.service >/dev/null 2>&1 || :
%else
    /sbin/service zabbix-agent try-restart >/dev/null 2>&1 || :
%endif
fi


%files
#TODO: Arrange get/sender plus agent config differently
%doc AUTHORS ChangeLog COPYING NEWS README %{srcname}-fedora.README
%dir %{_sysconfdir}/%{srcname}
%config(noreplace) %{_sysconfdir}/zabbix_agentd.conf
%config(noreplace) %{_sysconfdir}/%{srcname}/zabbix_agentd.conf
%if 0%{?fedora}
%config(noreplace) %{_sysconfdir}/tmpfiles.d/zabbix.conf
%endif
%{_bindir}/zabbix_get
%{_bindir}/zabbix_sender
%{_mandir}/man1/zabbix_get.1*
%{_mandir}/man1/zabbix_sender.1*

%files server
%doc misc/snmptrap/zabbix_trap_receiver.pl
%attr(0775,root,zabbix) %dir %{_localstatedir}/log/zabbix
%attr(0775,root,zabbix) %dir %{_localstatedir}/run/zabbix
%attr(0400,zabbixsrv,zabbix) %config(noreplace) %{_sysconfdir}/zabbix_server.conf
%config(noreplace) %{_sysconfdir}/%{srcname}/zabbix_server.conf
%config(noreplace) %{_sysconfdir}/%{srcname}/externalscripts
%config(noreplace) %{_sysconfdir}/%{srcname}/alertscripts
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-server
%ghost %{_sbindir}/zabbix_server
%attr(0755,zabbixsrv,zabbix) %{_sharedstatedir}/%{srcname}srv
%if 0%{?fedora}
%ghost %{_unitdir}/zabbix-server.service
%else
%{_initrddir}/zabbix-server
%endif
%{_mandir}/man8/zabbix_server.8*

%files server-mysql
%{_datadir}/%{srcname}-mysql
%{_sbindir}/zabbix_server_mysql
%if 0%{?fedora}
%{_unitdir}/zabbix-server-mysql.service
%endif

%files server-pgsql
%{_datadir}/%{srcname}-postgresql
%{_sbindir}/zabbix_server_pgsql
%if 0%{?fedora}
%{_unitdir}/zabbix-server-pgsql.service
%endif

%files agent
%doc conf/zabbix_agentd/*.conf
%attr(0775,root,zabbix) %dir %{_localstatedir}/log/zabbix
%attr(0775,root,zabbix) %dir %{_localstatedir}/run/zabbix
%config(noreplace) %{_sysconfdir}/zabbix_agent.conf
%config(noreplace) %{_sysconfdir}/%{srcname}/zabbix_agent.conf
%config(noreplace) %{_sysconfdir}/zabbix_agentd.conf
%config(noreplace) %{_sysconfdir}/%{srcname}/zabbix_agentd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-agent
%attr(0755,zabbix,zabbix) %dir %{_sharedstatedir}/%{srcname}
%if 0%{?fedora}
%{_unitdir}/zabbix-agent.service
%else
%{_initrddir}/zabbix-agent
%endif
%{_sbindir}/zabbix_agent
%{_sbindir}/zabbix_agentd
%{_mandir}/man8/zabbix_agentd.8*

%files proxy
%doc misc/snmptrap/zabbix_trap_receiver.pl
%attr(0775,root,zabbix) %dir %{_localstatedir}/log/zabbix
%attr(0775,root,zabbix) %dir %{_localstatedir}/run/zabbix
%attr(0600,zabbixsrv,zabbix) %config(noreplace) %{_sysconfdir}/zabbix_proxy.conf
%config(noreplace) %{_sysconfdir}/%{srcname}/zabbix_proxy.conf
%attr(0755,zabbixsrv,zabbix) %dir %{_sysconfdir}/%{srcname}/externalscripts
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-proxy
%ghost %{_sbindir}/zabbix_proxy
%attr(0755,zabbixsrv,zabbix) %{_sharedstatedir}/%{srcname}srv
%if 0%{?fedora}
%ghost %{_unitdir}/zabbix-proxy.service
%else
%{_initrddir}/zabbix-proxy
%endif
%{_bindir}/zabbix_get
%{_mandir}/man1/zabbix_get.1*
%{_mandir}/man8/zabbix_proxy.8*

%files proxy-mysql
%{_datadir}/%{srcname}-mysql
%{_sbindir}/zabbix_proxy_mysql
%if 0%{?fedora}
%{_unitdir}/zabbix-proxy-mysql.service
%endif

%files proxy-pgsql
%{_datadir}/%{srcname}-postgresql
%{_sbindir}/zabbix_proxy_pgsql
%if 0%{?fedora}
%{_unitdir}/zabbix-proxy-pgsql.service
%endif

%files proxy-sqlite3
%{_datadir}/%{srcname}-sqlite3
%{_sbindir}/zabbix_proxy_sqlite3
%if 0%{?fedora}
%{_unitdir}/zabbix-proxy-sqlite3.service
%endif

%files web
%dir %attr(0750,apache,apache) %{_sysconfdir}/%{srcname}/web
%ghost %attr(0644,apache,apache) %config(noreplace) %{_sysconfdir}/%{srcname}/web/zabbix.conf.php
%attr(0644,apache,apache) %config(noreplace) %{_sysconfdir}/%{srcname}/web/maintenance.inc.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/zabbix.conf
%{_datadir}/%{srcname}

%files web-mysql

%files web-pgsql

%changelog
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

* Thu Jun 28 2012 Dan Horák <dan[at]danny.cz> - 1.8.14-1
- update to 1.8.14

* Sat May 12 2012 Dan Horák <dan[at]danny.cz> - 1.8.13-1
- update to 1.8.13

* Tue Apr 24 2012 Dan Horák <dan[at]danny.cz> - 1.8.12-1
- update to 1.8.12

* Wed Mar 21 2012 Dan Horák <dan[at]danny.cz> - 1.8.11-1
- update to 1.8.11

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 28 2011 Dan Horák <dan[at]danny.cz> - 1.8.10-1
- update to 1.8.10 (fixes CVE-2011-4615)

* Thu Nov 24 2011 Dan Horák <dan[at]danny.cz> - 1.8.9-1
- update to 1.8.9
- switch to systemd units (#720065)
- drop empty docs subpackage
- drop spec compatibility with sysv-based systems

* Wed Oct  5 2011 Dan Horák <dan[at]danny.cz> - 1.8.8-1
- Update for 1.8.8
- Drop the ZBX-4099 patch, that's now obsolete
- Remove two further htaccess files and put the configuration in
  the main configuration file
- thanks to Volker Fröhlich for the changes above
- move zabbix_get to the server and proxy subpackages (#734512)
- remove prebuilt Windows binaries (#737341)
- remove flash clock applet (#737337)

* Fri Sep  9 2011 Dan Horák <dan[at]danny.cz> - 1.8.7-2
- fix server crash (ZBX-4099)

* Mon Sep  5 2011 Dan Horák <dan[at]danny.cz> - 1.8.7-1
- updated to 1.8.7

* Tue Aug  9 2011 Dan Horák <dan[at]danny.cz> - 1.8.6-1
- updated to 1.8.6 (#729164, #729165)
- updated user/group adding scriptlet

* Fri Jul  8 2011 Dan Horák <dan[at]danny.cz> - 1.8.5-5
- rebuilt with net-snmp 5.7

* Mon Jun 13 2011 Dan Horák <dan[at]danny.cz> - 1.8.5-4
- generalize the spec so creating packages like zabbix18 will be much easier

* Fri Jun  3 2011 Dan Horák <dan[at]danny.cz> - 1.8.5-3
- fix path to the traceroute utility
- add tmpfiles.d support for /var/run/zabbix (#656726)

* Mon May 23 2011 Dan Horák <dan[at]danny.cz> - 1.8.5-2
- include /var/lib/zabbix and /etc/zabbix/externalscripts dirs in package (#704181)
- add snmp trap receiver script in package (#705331)

* Wed Apr 20 2011 Dan Horák <dan[at]danny.cz> - 1.8.5-1
- updated to 1.8.5

* Wed Mar 23 2011 Dan Horák <dan[at]danny.cz> - 1.8.4-4
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Dan Horák <dan[at]danny.cz> - 1.8.4-2
- enable libcurl detection (#670500)

* Tue Jan  4 2011 Dan Horák <dan[at]danny.cz> - 1.8.4-1
- updated to 1.8.4
- fixes zabbix_agent fail to start on IPv4-only host (#664639)

* Tue Nov 23 2010 Dan Horák <dan[at]danny.cz> - 1.8.3-5
- zabbix emailer doesn't handle multiline responses (#656072)

* Mon Nov  1 2010 Dan Horák <dan[at]danny.cz> - 1.8.3-4
- rebuilt with net-snmp 5.6

* Wed Sep 29 2010 jkeating - 1.8.3-3
- Rebuilt for gcc bug 634757

* Mon Sep  6 2010 Dan Horák <dan[at]danny.cz> - 1.8.3-2
- fix font path in patch2 (#630500)

* Tue Aug 17 2010 Dan Horák <dan[at]danny.cz> - 1.8.3-1
- updated to 1.8.3

* Wed Aug 11 2010 Dan Horák <dan[at]danny.cz> - 1.8.2-3
- added patch for XSS in triggers page (#620809, ZBX-2326)

* Thu Apr 29 2010 Dan Horák <dan[at]danny.cz> - 1.8.2-2
- DejaVu fonts doesn't exist on EL <= 5

* Tue Mar 30 2010 Dan Horák <dan[at]danny.cz> - 1.8.2-1
- Update to 1.8.2

* Sat Mar 20 2010 Dan Horák <dan[at]danny.cz> - 1.8.1-7
- web interface needs php-xml (#572413)
- updated defaults in config files (#573325)
- built with libssh2 support (#575279)

* Wed Feb 24 2010 Dan Horák <dan[at]danny.cz> - 1.8.1-6
- use system fonts

* Sun Feb 13 2010 Dan Horák <dan[at]danny.cz> - 1.8.1-5
- fixed linking with the new --no-add-needed default (#564932)

* Mon Feb  1 2010 Dan Horák <dan[at]danny.cz> - 1.8.1-4
- enable dependency tracking

* Mon Feb  1 2010 Dan Horák <dan[at]danny.cz> - 1.8.1-3
- updated the web-config patch

* Mon Feb  1 2010 Dan Horák <dan[at]danny.cz> - 1.8.1-2
- close fd on exec (#559221)

* Fri Jan 29 2010 Dan Horák <dan[at]danny.cz> - 1.8.1-1
- Update to 1.8.1

* Tue Jan 26 2010 Dan Horák <dan[at]danny.cz> - 1.8-1
- Update to 1.8

* Thu Dec 31 2009 Dan Horák <dan[at]danny.cz> - 1.6.8-1
- Update to 1.6.8
- Upstream changelog: http://www.zabbix.com/rn1.6.8.php
- fixes 2 issues from #551331

* Wed Nov 25 2009 Dan Horák <dan[at]danny.cz> - 1.6.6-2
- rebuilt with net-snmp 5.5

* Sat Aug 29 2009 Dan Horák <dan[at]danny.cz> - 1.6.6-1
- Update to 1.6.6
- Upstream changelog: http://www.zabbix.com/rn1.6.6.php

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.6.5-3
- rebuilt with new openssl

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun  8 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6.5-1
- Update to 1.6.5, see http://sourceforge.net/mailarchive/message.php?msg_name=4A37A2CA.8050503%40zabbix.com for the full release notes.
- 
- It is recommended to create the following indexes in order to speed up
- performance of Zabbix front-end as well as server side (ignore it if the
- indexes already exist):
- 
- CREATE UNIQUE INDEX history_log_2 on history_log (itemid,id);
- CREATE UNIQUE INDEX history_text_2 on history_text (itemid,id);
- CREATE INDEX graphs_items_1 on graphs_items (itemid);
- CREATE INDEX graphs_items_2 on graphs_items (graphid);
- CREATE INDEX services_1 on services (triggerid);

* Mon Jun  8 2009 Ville Skyttä <ville.skytta at iki.fi> - 1.6.4-4
- Start agent after and shut down before proxy and server by default.
- Include database schemas also in -proxy-* docs.
- Make buildable on EL-4 (without libcurl, OpenIPMI).
- Reformat description.

* Fri Apr 17 2009 Ville Skyttä <ville.skytta at iki.fi> - 1.6.4-3
- Tighten configuration file permissions.
- Ensure zero exit status from scriptlets.
- Improve init script LSB compliance.
- Restart running services on package upgrades.

* Thu Apr  9 2009 Dan Horák <dan[at]danny.cz> - 1.6.4-2
- make the -docs subpackage noarch

* Thu Apr  9 2009 Dan Horák <dan[at]danny.cz> - 1.6.4-1
- update to 1.6.4
- remove the cpustat patch, it was integreated into upstream
- use noarch subpackage for the web interface
- database specific web subpackages conflicts with each other
- use common set of option for the configure macro
- enable IPMI support
- sqlite web subpackage must depend on local sqlite
- reorganize the docs and the sql scripts
- change how the web interface config file is created
- updated scriptlet for adding the zabbix user
- move the documentation in PDF to -docs subpackage
- most of the changes were submitted by Ville Skyttä in #494706 
- Resolves: #489673, #493234, #494706

* Mon Mar  9 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6.2-5
- Update pre patch due to incomplete fix for security problems.

* Wed Mar  4 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6.2-4
- Update to a SVN snapshot of the upstream 1.6 branch to fix security
  issue (BZ#488501)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 23 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6.2-2
- Rebuild for MySQL 5.1.X

* Fri Jan 16 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6.2-1
- Update to 1.6.2: http://www.zabbix.com/rn1.6.2.php

* Thu Dec  4 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6.1-1
- Fix BZ#474593 by adding a requires.

* Wed Nov  5 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6.1-1
- Update to 1.6.1

* Tue Sep 30 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6-1.1
- Bump release because forgot to add some new files.

* Thu Sep 30 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.6-1
- Update to final 1.6

* Mon Aug 11 2008 Jason L Tibbitts III <tibbs@math.uh.edu> - 1.4.6-2
- Fix license tag.

* Fri Jul 25 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.6-1
- Update to 1.4.6

* Mon Jul 07 2008 Dan Horak <dan[at]danny.cz> - 1.4.5-4
- add LSB headers into init scripts
- disable internal log rotation

* Fri May 02 2008 Jarod Wilson <jwilson@redhat.com> - 1.4.5-3
- Seems the zabbix folks replaced the original 1.4.5 tarball with
  an updated tarball or something -- it actually does contain a
  tiny bit of additional code... So update to newer 1.4.5.

* Tue Apr 08 2008 Jarod Wilson <jwilson@redhat.com> - 1.4.5-2
- Fix building w/postgresql (#441456)

* Tue Mar 25 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.5-1
- Update to 1.4.5

* Thu Feb 14 2008 Jarod Wilson <jwilson@redhat.com> - 1.4.4-2
- Bump and rebuild with gcc 4.3

* Mon Dec 17 2007 Jarod Wilson <jwilson@redhat.com> - 1.4.4-1
- New upstream release
- Fixes two crasher bugs in 1.4.3 release

* Wed Dec 12 2007 Jarod Wilson <jwilson@redhat.com> - 1.4.3-1
- New upstream release

* Thu Dec 06 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.4.2-5
- Rebuild for deps

* Sat Dec 01 2007 Dan Horak <dan[at]danny.cz> 1.4.2-4
- add security fix (#407181)

* Thu Sep 20 2007 Dan Horak <dan[at]danny.cz> 1.4.2-3
- Add a patch to clean a warning during compile
- Add a patch to fix cpu load computations

* Tue Aug 21 2007 Jarod Wilson <jwilson@redhat.com> 1.4.2-2
- Account for binaries moving from %%_bindir to %%_sbindir

* Tue Aug 21 2007 Jarod Wilson <jwilson@redhat.com> 1.4.2-1
- New upstream release

* Mon Jul 02 2007 Jarod Wilson <jwilson@redhat.com> 1.4.1-1
- New upstream release

* Fri Jun 29 2007 Jarod Wilson <jwilson@redhat.com> 1.4-3
- Install correct sql init files (#244991)
- Add Requires: php-bcmath to zabbix-web (#245767)

* Wed May 30 2007 Jarod Wilson <jwilson@redhat.com> 1.4-2
- Add placeholder zabbix.conf.php

* Tue May 29 2007 Jarod Wilson <jwilson@redhat.com> 1.4-1
- New upstream release

* Fri Mar 30 2007 Jarod Wilson <jwilson@redhat.com> 1.1.7-1
- New upstream release

* Wed Feb 07 2007 Jarod Wilson <jwilson@redhat.com> 1.1.6-1
- New upstream release

* Thu Feb 01 2007 Jarod Wilson <jwilson@redhat.com> 1.1.5-1
- New upstream release

* Tue Jan 02 2007 Jarod Wilson <jwilson@redhat.com> 1.1.4-5
- Add explicit R:php to zabbix-web (#220676)

* Wed Dec 13 2006 Jarod Wilson <jwilson@redhat.com> 1.1.4-4
- Fix snmp polling buffer overflow (#218065)

* Wed Nov 29 2006 Jarod Wilson <jwilson@redhat.com> 1.1.4-3
- Rebuild for updated libnetsnmp

* Thu Nov 16 2006 Jarod Wilson <jwilson@redhat.com> 1.1.4-2
- Fix up pt_br
- Add Req-pre on useradd

* Wed Nov 15 2006 Jarod Wilson <jwilson@redhat.com> 1.1.4-1
- Update to 1.1.4

* Tue Nov 14 2006 Jarod Wilson <jwilson@redhat.com> 1.1.3-3
- Add BR: gnutls-devel, R: net-snmp-libs

* Tue Nov 14 2006 Jarod Wilson <jwilson@redhat.com> 1.1.3-2
- Fix php-pgsql Requires

* Tue Nov 14 2006 Jarod Wilson <jwilson@redhat.com> 1.1.3-1
- Update to 1.1.3

* Mon Oct 02 2006 Jarod Wilson <jwilson@redhat.com> 1.1.2-1
- Update to 1.1.2
- Enable alternate building with postgresql support

* Thu Aug 17 2006 Jarod Wilson <jwilson@redhat.com> 1.1.1-2
- Yank out Requires: mysql-server
- Add Requires: for php-gd and fping

* Tue Aug 15 2006 Jarod Wilson <jwilson@redhat.com> 1.1.1-1
- Update to 1.1.1
- More macroification
- Fix up zabbix-web Requires:
- Prep for enabling postgres support

* Thu Jul 27 2006 Jarod Wilson <jwilson@redhat.com> 1.1-2
- Add Requires: on chkconfig and service
- Remove openssl-devel from BR, mysql-devel pulls it in
- Alter scriptlets to match Fedora conventions

* Tue Jul 11 2006 Jarod Wilson <jwilson@redhat.com> 1.1-1
- Initial build for Fedora Extras
