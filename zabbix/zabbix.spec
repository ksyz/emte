Name:           zabbix
Version:        1.1.4
Release:        5%{?dist}
Summary:        Open-source monitoring solution for your IT infrastructure

Group:          Applications/Internet
License:        GPL
URL:            http://www.zabbix.com/
Source0:        http://dl.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Source1:        zabbix-web.conf
Source2:        zabbix-server.init
Source3:        zabbix-agent.init
Source4:        zabbix-logrotate.in
Patch0:         zabbix-1.1.4-snmp-poll-overflow.patch
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define database mysql
%define zdb mysql
%define with_postgresql %{?_with_postgresql: 1} %{?!_with_postgresql: 0}

# Zabbix can only be built with mysql -or- postgresql
# support. We build with mysql by default, but you can
# pass --with postgresql to build with postgresql instead.
%if %{with_postgresql}
%define database postgresql
%define zdb pgsql
%endif

BuildRequires:  %{database}-devel, net-snmp-devel
BuildRequires:  openldap-devel, gnutls-devel
Requires:       logrotate, fping, net-snmp-libs
Requires(pre):      /usr/sbin/useradd
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/chkconfig
Requires(preun):    /sbin/service

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


%package agent
Summary:        Zabbix Agent
Group:          Applications/Internet
Requires:       logrotate
Requires(pre):      /usr/sbin/useradd
Requires(post):     /sbin/chkconfig
Requires(preun):    /sbin/chkconfig
Requires(preun):    /sbin/service

%description agent
The zabbix client agent, to be installed on monitored systems.

%package web
Summary:        Zabbix Web Frontend
Group:          Applications/Internet
Requires:       php-%{zdb}, php-gd, php

%description web
The php frontend to display the zabbix web interface.

%prep
%setup -q
%patch0 -p1 -b .overflow

# fix up some lib64 issues
%{__perl} -pi.orig -e 's|_LIBDIR=/usr/lib|_LIBDIR=%{_libdir}|g' \
    configure

# fix up pt_br
%{__chmod} a-x frontends/php/include/locales/pt_br.inc.php
%{__sed} -i 's/\r//' frontends/php/include/locales/pt_br.inc.php

%build
%configure \
    --enable-server \
    --enable-agent \
    --with-%{zdb} \
    --with-net-snmp \
    --with-ldap \
    --disable-static

# --disable-static is partially broken atm,
# -static still gets into CFLAGS, so fix up in make
# (and even then, .a files still show their face...)
make %{?_smp_mflags} CFLAGS="$RPM_OPT_FLAGS"

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
# php frontend
cp -a frontends/php $RPM_BUILD_ROOT%{_datadir}/%{name}
mv $RPM_BUILD_ROOT%{_datadir}/%{name}/include/db.inc.php \
    $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/
ln -s ../../../..%{_sysconfdir}/%{name}/db.inc.php \
    $RPM_BUILD_ROOT%{_datadir}/%{name}/include/db.inc.php
# kill off .htaccess files, options set in SOURCE1
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/include/.htaccess
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/include/classes/.htaccess
# drop config files in place
install -m 0644 misc/conf/zabbix_agent.conf $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
cat misc/conf/zabbix_agentd.conf | sed \
    -e 's|PidFile=.*|PidFile=%{_localstatedir}/run/zabbix/zabbix_agentd.pid|g' \
    -e 's|LogFile=.*|LogFile=%{_localstatedir}/log/zabbix/zabbix_agentd.log|g' \
    > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/zabbix_agentd.conf
cat misc/conf/zabbix_server.conf | sed \
    -e 's|PidFile=.*|PidFile=%{_localstatedir}/run/zabbix/zabbix.pid|g' \
    -e 's|LogFile=.*|LogFile=%{_localstatedir}/log/zabbix/zabbix_server.log|g' \
    -e 's|AlertScriptsPath=/home/zabbix/bin/|AlertScriptsPath=%{_localstatedir}/lib/zabbix/|g' \
    -e 's|DBUser=root|DBUser=zabbix|g' \
    -e 's|DBSocket=/tmp/mysql.sock|DBSocket=%{_localstatedir}/lib/%{zdb}/%{zdb}.sock|g' \
    > $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/zabbix_server.conf
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/%{name}.conf
# log rotation
cat %{SOURCE4} | sed -e 's|COMPONENT|server|g' > \
     $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zabbix
cat %{SOURCE4} | sed -e 's|COMPONENT|agentd|g' > \
     $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/zabbix-agent
# init scripts
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/init.d/zabbix
install -m 0755 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/init.d/zabbix-agent

make DESTDIR=$RPM_BUILD_ROOT install
rm -rf $RPM_BUILD_ROOT%{_libdir}/libzbx*.a

%clean
rm -rf $RPM_BUILD_ROOT

%pre
# Add the "zabbix" user
/usr/sbin/useradd -c "Zabbix Monitoring System" \
        -s /sbin/nologin -r -d %{_localstatedir}/lib/%{name} zabbix 2> /dev/null || :

%pre agent
# Add the "zabbix" user
/usr/sbin/useradd -c "Zabbix Monitoring System" \
        -s /sbin/nologin -r -d %{_localstatedir}/lib/%{name} zabbix 2> /dev/null || :

%post
/sbin/chkconfig --add zabbix

%post agent
/sbin/chkconfig --add zabbix-agent

%preun
if [ "$1" = 0 ]
then
  /sbin/service zabbix stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del zabbix
fi

%preun agent
if [ "$1" = 0 ]
then
  /sbin/service zabbix-agent stop >/dev/null 2>&1 || :
  /sbin/chkconfig --del zabbix-agent
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING FAQ NEWS README
%doc create/data create/%{database}
%dir %{_sysconfdir}/%{name}
%{_bindir}/zabbix_server
%{_sysconfdir}/init.d/zabbix
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix
%config(noreplace) %{_sysconfdir}/%{name}/zabbix_server.conf
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/log/%{name}
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/run/%{name}

%files agent
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING FAQ NEWS README
%dir %{_sysconfdir}/%{name}
%{_bindir}/zabbix_agent
%{_bindir}/zabbix_agentd
%{_bindir}/zabbix_sender
%{_bindir}/zabbix_get
%{_sysconfdir}/init.d/zabbix-agent
%config(noreplace) %{_sysconfdir}/logrotate.d/zabbix-agent
%config(noreplace) %{_sysconfdir}/%{name}/zabbix_agent.conf
%config(noreplace) %{_sysconfdir}/%{name}/zabbix_agentd.conf
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/log/%{name}
%attr(0755,zabbix,zabbix) %dir %{_localstatedir}/run/%{name}

%files web
%defattr(-,root,root,-)
%doc README
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/db.inc.php
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_datadir}/%{name}

%changelog
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
