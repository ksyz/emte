%global curdatetime %(date +%%Y%%m%%d%%H%%M%%S)

%global commit0  61a7d17b85e9b4b040fdaf84e02599d186f8b585
# % global gittag0 GIT-TAG
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           lm4tools
Version:        0.1.3
Release:        1.%{curdatetime}.%{shortcommit0}%{?dist}

Summary:		Development tools for TI Stellaris Launchpad boards

License:		GPLv2+ 
#BSD
URL:			https://github.com/utzig/lm4tools
Source0:		https://github.com/utzig/lm4tools/archive/%{commit0}.tar.gz#/%{name}-%{version}.git_%{shortcommit0}.tar.gz

BuildRequires:	libusbx-devel

%description
* lm4flash Command-line firmware flashing tool using libusb-1.0 to communicate 
with the Stellaris Launchpad ICDI. Works on all Linux, Mac OS X, Windows, and 
BSD systems. GPLv2+ license. See lm4flash/COPYING for details.

* lmicdiusb TCP/USB bridge created by TI, letting GDB communicate with the 
Stellaris Launchpad ICDI. Works on all Linux, Mac OS X, and BSD systems. 
Currently not on Windows, due to the use of poll() which does not work for USB 
on Windows. BSD-style license. See lmicdiusb/license.txt for details.

%prep
%setup -qn %{name}-%{commit0}
sed -e 's/@${MAKE} -C lm4flash all/@${MAKE} -C lm4flash debug/g' -i Makefile

%build
make %{?_smp_mflags}
mv ./lmicdiusb/README ./lmicdiusb/README.lmicdi

%install

install -dm755 %{buildroot}%{_bindir}
install -m755 lmicdiusb/lmicdi lm4flash/lm4flash %{buildroot}%{_bindir}/

%files
%doc README.md lmicdiusb/commands.txt lmicdiusb/README.lmicdi lm4flash/COPYING

%{_bindir}/*

%changelog
* Thu Oct 11 2018 Michal Ingeli <mi@v3.sk> - 0.1.3-1
- Initial release
