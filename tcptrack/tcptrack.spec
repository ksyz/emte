Name:           tcptrack
Version:        1.4.2
Release:        10%{?dist}
Summary:        Displays information about tcp connections on a network interface

Group:          Applications/System
License:        LGPLv2+
URL:            http://www.rhythm.cx/~steve/devel/tcptrack/
Source0:        http://www.rhythm.cx/~steve/devel/%{name}/release/%{version}/source/%{name}-%{version}.tar.gz
#Increase text ui select timeout to 10000 usec, upstream agrees
Patch0:         tcptrack-1.4.0-timeout.patch
#Kick out -Werror from AM_CXXFLAGS
Patch1:         tcptrack-1.4.2-no-werror.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  ncurses-devel
BuildRequires:  libpcap-devel

%description
tcptrack is a sniffer which displays information about TCP connections
it sees on a network interface. It passively watches for connections on 
the network interface, keeps track of their state and displays a list of
connections in a manner similar to the unix 'top' command. It displays 
source and destination addresses and ports, connection state, idle time, 
and bandwidth usage

%prep
%setup -q
%patch0 -p1 -b .timeout
%patch1 -p1

%build
%configure
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%{_bindir}/tcptrack
%{_mandir}/man1/tcptrack.1.gz


%changelog
* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.4.2-9
- Rebuilt for GCC 5 C++11 ABI change

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.4.2-7
- Remove -Werror from AM_CXXFLAGS in src/Makefile.* (FTBFS RHBZ#1107444).

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Patrick Uiterwijk <puiterwijk@gmail.com> - 1.4.2-3
- Rebuild for package maintainership change

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 09 2011 Jitesh Shah <jitesh.1337@gmail.com> - 1.4.2-1
- New release 1.4.2
- Heap overflow fix and misc fixes (No official changelog on the website)

* Thu Jul 14 2011 Jitesh Shah <jitesh.1337@gmail.com> - 1.4.0-3
- Fixed a build fault

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Orion Poplawski <orion@cora.nwra.com> - 1.4.0-1
- Update to 1.4.0
- Add patch to increase text ui select timeout to reduce cpu usage

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 27 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.3.0-1
- Update to 1.3.0
- Added tcptrack-1.3.0-util.patch patch 

* Mon Jan 28 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.2.0-5
- Modified lincese to LGPLv2+

* Mon Jan 28 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.2.0-4
- Removed minimal version from BuildRequires

* Tue Jan 22 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.2.0-3
- Removed "Requires: libpcap >= 0.9.7"

* Tue Jan 22 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.2.0-2
- Fixed mixed-use-of-spaces-and-tabs (spaces: line 1, tab: line 13)
- Fixed strange-permission tcptrack-1.2.0.tar.gz 0770
- Fixed strange-permission tcptrack.spec 0770
- Fixed Source0 using %%{name} and %%{version} 

* Mon Jan 21 2008 Kairo Araujo <kairoaraujo@gmail.com> - 1.2.0-1
- Initial RPM release
