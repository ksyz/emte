%global git_commit 2492c20822ca6a49dce97967caf394b1d4b2c43e
%global git_short_commit %(c=%{git_commit}; echo ${c:0:7})

Name:             kalibrate-hackrf
URL:              https://github.com/scateu/kalibrate-hackrf
Version:          0.4.1
Release:          7.%{git_short_commit}%{?dist}
License:          BSD
BuildRequires:    autoconf, automake, rtl-sdr-devel, fftw-devel
BuildRequires:    libusbx-devel
BuildRequires:    hackrf-devel
Group:            Applications/Communications
Summary:          GSM based frequency calibration for HackRF
Source0:          https://github.com/scateu/%{name}/archive/%{git_commit}/%{name}-%{git_commit}.tar.gz


%description
Kalibrate, or kal, can scan for GSM base stations in a given frequency band and
can use those GSM base stations to calculate the local oscillator frequency
offset.
Kalibrate-hackrf is a fork of Joshua Lackey's kalibrate originally for USRP, 
ported to support the HackRF. 

%prep
%setup -qn %{name}-%{git_commit}
echo "AUTOMAKE_OPTIONS = foreign" >> Makefile.am
autoreconf -fi

%build
%configure
make CFLAGS="%{optflags}" LDFLAGS="%{?__global_ldflags}" %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# Rename kal to kal-rtl to avoid possible conflicts
mv %{buildroot}%{_bindir}/kal %{buildroot}%{_bindir}/kal-hackrf

%files
%doc COPYING README.md AUTHORS
%{_bindir}/*

%changelog
* Wed Oct 17 2018 Michal Ingeli <mi@v3.sk> - 0.4.1-7
- Latest git commit

* Wed Jun 15 2016 Michal Ingeli <mi@v3.sk> - 0.4.1-6.20160608git2115961e
- Re-fit for kalibrate-hackrf purpose
- Added foreign to Makefile.AM to skip README checking
- Added libhackrf BR

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-5.20141008gitaae11c8a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.4.1-4.20141008gitaae11c8a
- Rebuilt for GCC 5 C++11 ABI change

* Tue Oct 14 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 0.4.1-3.20141008gitaae11c8a
- required libusbx-devel instead of libusb-devel

* Fri Oct 10 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 0.4.1-2.20141008gitaae11c8a
- Fixed source URL according to fedora review

* Wed Oct  8 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 0.4.1-1.20141008gitaae11c8a
- Initial release
