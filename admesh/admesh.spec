%global curdatetime %(date +%%Y%%m%%d%%H%%M%%S)
%global commit0  64e86ea3107c757090f2a7045a1a6a1982a4ba08
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           admesh
Version:        0.99.0
Release:        1.%{shortcommit0}%{?dist}
Summary:        Diagnose and/or repair problems with STereo Lithography files
License:        GPLv2+
Group:          Applications/Engineering
URL:            https://github.com/admesh/%{name}/
# Source0:        http://github.com/admesh/admesh/releases/download/v%{version}/admesh-%{version}.tar.gz
Source0:		https://github.com/admesh/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{version}.git_%{shortcommit0}.tar.gz
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

BuildRequires:	autoconf, automake, libtool

%description
ADMesh is a program for diagnosing and/or repairing commonly encountered
problems with STL (STereo Lithography) data files. It can remove degenerate
and unconnected facets, connect nearby facets, fill holes by adding facets,
and repair facet normals. Simple transformations such as scaling,
translation and rotation are also supported. ADMesh can read both
ASCII and binary format STL files, while the output can be in
AutoCAD DXF, Geomview OFF, STL, or VRML format.

%package devel
Summary:        Development files for the %{name} library
Group:          Development/Libraries
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
ADMesh is a program for diagnosing and/or repairing commonly encountered
problems with STL (STereo Lithography) data files.

This package contains the development files needed for building new
applications that utilize the %{name} library.

%package libs
Summary:        Runtime library for the %{name} application
Group:          Development/Libraries

%description libs
This package contains the %{name} runtime library.

%prep
%setup -qn %{name}-%{commit0}

%build
./autogen.sh
%configure
# Pass the -v option to libtool so we can better see what's going on
make %{?_smp_mflags} CFLAGS="%{optflags}" LIBTOOLFLAGS="-v"

%install
%{make_install}
# Remove the documentation installed by "make install" (rpm will handle that)
rm -rf %{buildroot}%{_defaultdocdir}/%{name}
# Remove the libtool archive installed by "make install"
rm -f %{buildroot}%{_libdir}/lib%{name}.la

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%doc ChangeLog ChangeLog.old COPYING README.md AUTHORS
%doc %{name}-doc.txt block.stl
%{_bindir}/%{name}
%{_mandir}/man1/*

%files devel
%{_includedir}/*
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/*

%files libs
%doc COPYING AUTHORS
%{_libdir}/lib%{name}.so.*

%changelog
* Mon Oct 22 2018 Michal Ingeli <mi@v3.sk> - 0.99.0-1
- Upstream master release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.98.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 18 2017 Miro Hrončok <mhroncok@redhat.com> - 0.98.3-1
- Updated to 0.98.3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.98.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.98.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.98.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.98.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 22 2015 Miro Hrončok <mhroncok@redhat.com> - 0.98.2-1
- Updated to 0.98.2

* Tue Sep 23 2014 Miro Hrončok <mhroncok@redhat.com> - 0.98.1-1
- Updated to 0.98.1

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.98.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 29 2014 Miro Hrončok <mhroncok@redhat.com> - 0.98.0-1
- Update to 0.98.0

* Sun Jun 29 2014 Miro Hrončok <mhroncok@redhat.com> - 0.97.5-1
- Update to 0.97.5

* Sun Jun 29 2014 Miro Hrončok <mhroncok@redhat.com> - 0.97.4-1
- Update to 0.97.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.97.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Oct 23 2013 John C. Peterson <jcp[at]eskimo.com> - 0.97.2-1
- Fixed the post and postun scriptlets (needed only for the libs subpackage)
- Fixed the requires for the devel package (namely the libs subpackage)
- Added the license file to the docs of the libs package
- Fixed the inconsistent use of spaces vs. tabs

* Tue Oct 22 2013 John C. Peterson <jcp[at]eskimo.com> - 0.97.2-1
- Added a README.Fedora file. It references the Masters Thesis associated with
  the source code (because it can't be packaged due to an ambiguous copyright)
- Moved the versioned runtime libraries to a libs subpackage
- Modified the install section to use the make_install macro
- Some minor additions to the package descriptions
- Removed some extraneous info from the changelog

* Mon Oct 21 2013 John C. Peterson <jcp[at]eskimo.com> - 0.97.2-1
- Switched over to a fork of admesh that is being actively maintained.

* Sun Sep 15 2013 John C. Peterson <jcp[at]eskimo.com> - 0.97.2-1
- Initial spec file (for code from http://www.varlog.com/admesh-htm).

