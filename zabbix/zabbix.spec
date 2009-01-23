Name:           zabbix
Version:        1.6.2
Release:        2%{?dist}
Summary:        Open-source monitoring solution for your IT infrastructure

Group:          Applications/Internet
License:        GPL
URL:            http://www.zabbix.com/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:        zabbix-web.conf
Source2:        zabbix-server.init
Source3:        zabbix-agent.init
Source4:        zabbix-proxy.init
Source5:        zabbix-logrotate.in

Patch0:         zabbix-1.6.2-cpustats.patch

Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:   mysql-devel
BuildRequires:   postgresql-devel
BuildRequires:   net-snmp-devel
BuildRequires:   openldap-devel
BuildRequires:   gnutls-devel
BuildRequires:   iksemel-devel
BuildRequires:   curl-devel
BuildRequires:   sqlite-devel
BuildRequires:   unixODBC-devel

Requires:        logrotate
Requires(pre):   /usr/sbin/useradd

%description
ZABBIX is software that monitors numerous parameters of a
network and the health and integrity of servers. ZABBIX
uses a flexible notification mechanism that allows users
to configure e-mail based alerts for virtually any event.
This allows a fast reaction to server problems. ZABBIX
offers excellent reporting and data visualisation features
based on the stored data. This makes ZABBIX ideal for
capacity planning.

ZABBIX supports both polling and trapping. All ZABBIX
reports and statistics, as well as configuration
parameters are accessed through a web-based front end. A
web-based front end ensures that the status of your network
and the health of your servers can be assessed from any
location. Properly configured, ZABBIX can play an important
role in monitoring IT infrastructure. This is equally true
for small organisations with a few servers and for large
companies with a multitude of servers.

%package server
Summary:         Zabbix server common files
Group:           Applications/Internet
Requires:	 zabbix = %{version}-%{release}
Requires:        zabbix-server-implementation = %{version}-%{release}
Requires:        fping
Requires:	 net-snmp
Requires(post):  /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service

%description server
Zabbix server common files

%package server-mysql
Summary:         Zabbix server compiled to use MySQL
Group:           Applications/Internet
Requires:        zabbix = %{version}-%{release}
Requires:	 zabbix-server = %{version}-%{release}
Provides:        zabbix-server-implementation = %{version}-%{release}
Obsoletes:       zabbix <= 1.5.3-0.1
Conflicts:       zabbix-server-pgsql
Conflicts:       zabbix-server-sqlite3

%description server-mysql
Zabbix server compiled to use MySQL

%package server-pgsql
Summary:         Zabbix server compiled to use PostgresSQL
Group:           Applications/Internet
Requires:        zabbix = %{version}-%{release}
Requires:	 zabbix-server = %{version}-%{release}
Provides:        zabbix-server-implementation = %{version}-%{release}
Conflicts:       zabbix-server-mysql
Conflicts:       zabbix-server-sqlite3

%description server-pgsql
Zabbix server compiled to use PostgresSQL

%package server-sqlite3
Summary:         Zabbix server compiled to use SQLite
Group:           Applications/Internet
Requires:        zabbix = %{version}-%{release}
Requires:	 zabbix-server = %{version}-%{release}
Provides:        zabbix-server-implementation = %{version}-%{release}
Conflicts:       zabbix-server-mysql
Conflicts:	 zabbix-server-pgsql

%description server-sqlite3
Zabbix server compiled to use SQLite

%package agent
Summary:         Zabbix Agent
Group:           Applications/Internet
Requires:	 zabbix = %{version}-%{release}
Requires(post):  /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service

%description agent
The Zabbix client agent, to be installed on monitored systems.

%package proxy
Summary:         Zabbix Proxy
Group:           Applications/Internet
Requires:	 zabbix = %{version}-%{release}
Requires:        zabbix-proxy-implementation = %{version}-%{release}
Requires(post):  /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires:        fping

%description proxy
The Zabbix proxy

%package proxy-mysql
Summary:         Zabbix proxy compiled to use MySQL
Group:           Applications/Internet
Requires:	 zabbix-proxy = %{version}-%{release}
Provides:        zabbix-proxy-implementation = %{version}-%{release}

%description proxy-mysql
The Zabbix proxy compiled to use MySQL

%package proxy-pgsql
Summary:         Zabbix proxy compiled to use PostgreSQL
Group:           Applications/Internet
Requires:	 zabbix-proxy = %{version}-%{release}
Provides:        zabbix-proxy-implementation = %{version}-%{release}

%description proxy-pgsql
The Zabbix proxy compiled to use PostgreSQL

%package proxy-sqlite3
Summary:         Zabbix proxy compiled to use SQLite
Group:           Applications/Internet
Requires:	 zabbix-proxy = %{version}-%{release}
Provides:        zabbix-proxy-implementation = %{version}-%{release}

%description proxy-sqlite3
The Zabbix proxy compiled to use SQLite

%package web
Summary:         Zabbix Web Frontend
Group:           Applications/Internet
Requires:        php
Requires:	 php-gd
Requires:	 php-bcmath
Requires:        zabbix = %{version}-%{release}
Requires:	 zabbix-web-database = %{version}-%{release}

%description web
The php frontend to display the zabbix web interface.

%package web-mysql
Summary:         Zabbix web frontend for MySQL
Group:           Applications/Internet
Requires:	 zabbix-web = %{version}-%{release}
Requires:	 php-mysql
Provides:	 zabbix-web-database = %{version}-%{release}
Obsoletes:	 zabbix-web <= 1.5.3-0.1

%description web-mysql
Zabbix web frontend for MySQL

%package web-pgsql
Summary:         Zabbix web frontend for PostgreSQL
Group:           Applications/Internet
Requires:	 zabbix-web = %{version}-%{release}
Requires:	 php-pgsql
Provides:	 zabbix-web-database = %{version}-%{release}

%description web-pgsql
Zabbix web frontend for PostgreSQL

%package web-sqlite3
Summary:         Zabbix web frontend for SQLite
Group:           Applications/Internet
Requires:	 zabbix-web = %{version}-%{release}
Provides:	 zabbix-web-database = %{version}-%{release}

%description web-sqlite3
Zabbix web frontend for SQLite

%prep
%setup0 -q
%patch0 -p1 -b .cpustats

chmod -R a+rX .

# nuke erronious executable permissions
#chmod -x src/zabbix_agent/eventlog.c

# fix up some lib64 issues
%{__perl} -pi.orig -e 's|_LIBDIR=/usr/lib|_LIBDIR=%{_libdir}|g' \
    configure

%build

%configure \
    --enable-server \
    --enable-agent \
    --enable-proxy \
    --enable-ipv6 \
    --with-mysql \
    --with-net-snmp \
    --with-ldap \
    --with-libcurl \
    --with-jabber \
    --with-unixodbc

make %{?_smp_mflags}

mv src/zabbix_server/zabbix_server src/zabbix_server/zabbix_server_mysql
mv src/zabbix_proxy/zabbix_proxy src/zabbix_proxy/zabbix_proxy_mysql

%configure \
    --enable-server \
    --enable-agent \
    --enable-proxy \
    --enable-ipv6 \
    --with-pgsql \
    --with-net-snmp \
    --with-ldap \
    --with-libcurl \
    --with-jabber \
    --with-unixodbc

make %{?_smp_mflags}
mv src/zabbix_server/zabbix_server src/zabbix_server/zabbix_server_pgsql
mv src/zabbix_proxy/zabbix_proxy src/zabbix_proxy/zabbix_proxy_pgsql

%configure \
    --enable-server \
    --enable-agent \
    --enable-proxy \
    --enable-ipv6 \
    --with-sqlite3 \
    --with-net-snmp \
    --with-ldap \
    --with-libcurl \
    --with-jabber \
    --with-unixodbc

make %{?_smp_mflags}
mv src/zabbix_server/zabbix_server src/zabbix_server/zabbix_server_sqlite3
mv src/zabbix_proxy/zabbix_proxy src/zabbix_proxy/zabbix_proxy_sqlite3

touch src/zabbix_server/zabbix_server
touch src/zabbix_proxy/zabbix_proxy

%install
rm -rf $RPM_BUILD_ROOT
# set up some required directories
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/init.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
mkdir -p $RPM_BUILD_ROOT%{_datadir}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log/%{name}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/%{name}

#rm create/Makefile*
#rm create/data/images_oracle.sql
#rm create/schema/oracle.sql
#rm -r upgrades/dbpatches/1.6/oracle

#pushd %{name}-%{version}-mysql
# php frontend
cp -a frontends/php $RPM_BUILD_ROOT%{_datadir}/%{name}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/include/db.inc.php \
    $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/
ln -s ../../../..%{_sysconfdir}/%{name}/db.inc.php \
    $RPM_BUILD_ROOT%{_datadir}/%{name}/include/db.inc.php
cat << __EOF__ >> $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/zabbix.conf.php
# This file is a place-holder. When you run through the zabbix
# web setup, a proper configuration file should be generated
# for you to drop in this location.
__EOF__
ln -s ../../../..%{_sysconfdir}/%{name}/zabbix.conf.php \
    $RPM_BUILD_ROOT%{_datadir}/%{name}/conf/zabbix.conf.php
# kill off .htaccess files, options set in SOURCE1
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/include/.htaccess
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/include/classes/.htaccess
# drop config files in place
install -m 0644 -p misc/conf/zabbix_agent.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
cat misc/conf/zabbix_agentd.conf | sed \
    -e 's|PidFile=.*|PidFile=%{_localstatedir}/run/zabbix/zabbix_agentd.pid|g' \
    -e 's|LogFile=.*|LogFile=%{_localstatedir}/log/zabbix/zabbix_agentd.log|g' \
    -e 's|#LogFileSize=.*|LogFileSize=0|g' \
    > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/zabbix_agentd.conf
cat misc/conf/zabbix_server.conf | sed \
    -e 's|PidFile=.*|PidFile=%{_localstatedir}/run/zabbix/zabbix.pid|g' \
    -e 's|LogFile=.*|LogFile=%{_localstatedir}/log/zabbix/zabbix_server.log|g' \
    -e 's|#LogFileSize=.*|LogFileSize=0|g' \
    -e 's|AlertScriptsPath=/home/zabbix/bin/|AlertScriptsPath=%{_localstatedir}/lib/zabbix/|g' \
    -e 's|DBUser=root|DBUser=zabbix|g' \
    -e 's|DBSocket=/tmp/mysql.sock|DBSocket=%{_localstatedir}/lib/mysql/mysql.sock|g' \
    > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/zabbix_server.conf
cat misc/conf/zabbix_proxy.conf | sed \
    -e 's|PidFile=.*|PidFile=%{_localstatedir}/run/zabbix/zabbix_proxy.pid|g' \
    -e 's|LogFile=.*|LogFile=%{_localstatedir}/log/zabbix/zabbix_proxy.log|g' \
    -e 's|#LogFileSize=.*|LogFileSize=0|g' \
    -e 's|AlertScriptsPath=/home/zabbix/bin/|AlertScriptsPath=%{_localstatedir}/lib/zabbix/|g' \
    -e 's|DBUser=root|DBUser=zabbix|g' \
    -e 's|DBSocket=/tmp/mysql.sock|DBSocket=%{_localstatedir}/lib/mysql/mysql.sock|g' \
    > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/zabbix_proxy.conf
install -m 0644 -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/%{name}.conf
# log rotation
cat %{SOURCE5} | sed -e 's|COMPONENT|server|g' > \
     $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zabbix-server
cat %{SOURCE5} | sed -e 's|COMPONENT|agentd|g' > \
     $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zabbix-agent
cat %{SOURCE5} | sed -e 's|COMPONENT|proxy|g' > \
     $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zabbix-proxy
# init scripts
install -m 0755 -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/init.d/zabbix-server
install -m 0755 -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/init.d/zabbix-agent
install -m 0755 -p %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/init.d/zabbix-proxy

# set up config dir

# install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_sbindir}/zabbix_server
install -m 0755 -p src/zabbix_server/zabbix_server_* $RPM_BUILD_ROOT%{_sbindir}/
rm $RPM_BUILD_ROOT%{_sbindir}/zabbix_proxy
install -m 0755 -p src/zabbix_proxy/zabbix_proxy_* $RPM_BUILD_ROOT%{_sbindir}/

# nuke static libs and empty oracle upgrade sql
rm -rf $RPM_BUILD_ROOT%{_libdir}/libzbx*.a
# nuke extraneous sql files
rm -rf $RPM_BUILD_ROOT%{_datadir}/%{name}/create

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# Add the "zabbix" user
/usr/sbin/useradd -c "Zabbix Monitoring System" \
        -s /sbin/nologin -r -d %{_localstatedir}/lib/%{name} zabbix 2> /dev/null || :

%post server
/sbin/chkconfig --add zabbix-server

%post agent
/sbin/chkconfig --add zabbix-agent

%post proxy
/sbin/chkconfig --add zabbix-proxy

%preun server
if [ "$1" = 0 ]
then
  /sbin/service zabbix-server stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del zabbix-server
fi

%preun agent
if [ "$1" = 0 ]
then
  /sbin/service zabbix-agent stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del zabbix-agent
fi

%preun proxy
if [ "$1" = 0 ]
then
  /sbin/service zabbix-proxy stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del zabbix-proxy
fi

%files
%defattr(-,root,root,-)
%dir %{_sysconfdir}/zabbix
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/log/zabbix
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/run/zabbix

%files server
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING FAQ NEWS README
%doc docs/*.pdf upgrades/dbpatches create/data create/schema
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_server.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-server
%{_sysconfdir}/init.d/zabbix-server

%files server-mysql
%doc AUTHORS ChangeLog COPYING FAQ NEWS README
%defattr(-,root,root,-)
%{_sbindir}/zabbix_server_mysql

%files server-pgsql
%doc AUTHORS ChangeLog COPYING FAQ NEWS README
%defattr(-,root,root,-)
%{_sbindir}/zabbix_server_pgsql

%files server-sqlite3
%doc AUTHORS ChangeLog COPYING FAQ NEWS README
%defattr(-,root,root,-)
%{_sbindir}/zabbix_server_sqlite3

%files agent
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING FAQ NEWS README
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_agent.conf
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_agentd.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-agent
%{_sysconfdir}/init.d/zabbix-agent
%{_sbindir}/zabbix_agent
%{_sbindir}/zabbix_agentd
%{_sbindir}/zabbix_sender
%{_sbindir}/zabbix_get

%files proxy
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING FAQ NEWS README
%config(noreplace) %{_sysconfdir}/zabbix/zabbix_proxy.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-proxy
%{_sysconfdir}/init.d/zabbix-proxy

%files proxy-mysql
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING FAQ NEWS README
%{_sbindir}/zabbix_proxy_mysql

%files proxy-pgsql
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING FAQ NEWS README
%{_sbindir}/zabbix_proxy_pgsql

%files proxy-sqlite3
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING FAQ NEWS README
%{_sbindir}/zabbix_proxy_sqlite3

%files web
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING FAQ NEWS README
%config(noreplace) %{_sysconfdir}/zabbix/zabbix.conf.php
%config(noreplace) %{_sysconfdir}/zabbix/db.inc.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/zabbix.conf
%{_datadir}/zabbix

%files web-mysql
%defattr(-,root,root,-)

%files web-pgsql
%defattr(-,root,root,-)

%files web-sqlite3
%defattr(-,root,root,-)

%changelog
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
