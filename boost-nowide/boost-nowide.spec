%global gh_commit ec9672b6cd883193be8451ee4cedab593420ae19
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner  artyom-beilis
%global gh_project nowide

Name:       boost-nowide
Version:    0
Release:    20181022.2.git%{gh_short}%{?dist}
Summary:    Boost.Nowide makes cross platform Unicode aware programming easier.

License:    Boost
URL:        https://github.com/%{gh_owner}/%{gh_project}

# This is a header only library
BuildArch:  noarch

Source0:    https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}.tar.gz#/%{name}-%{gh_short}.tar.gz

# Use upstream pull request to have proper cmake files for shared library building
Patch0: https://patch-diff.githubusercontent.com/raw/%{gh_owner}/%{gh_project}/pull/27.patch#/%{name}-PR-27.patch
Patch1: https://patch-diff.githubusercontent.com/raw/%{gh_owner}/%{gh_project}/pull/38.patch#/%{name}-PR-38.patch
Patch2: https://patch-diff.githubusercontent.com/raw/%{gh_owner}/%{gh_project}/pull/39.patch#/%{name}-PR-39.patch
Patch3: https://patch-diff.githubusercontent.com/raw/%{gh_owner}/%{gh_project}/pull/40.patch#/%{name}-PR-40.patch
Patch4: boost-nowide-Slic3r.patch

%if 0%{?fedora}
BuildRequires: cmake
BuildRequires: boost-devel
%else
# this isn't in EPEL yet ... but it will be soon
BuildRequires:  boost157-devel
BuildRequires:  cmake3
%endif

# To create the docs
BuildRequires: doxygen

%package devel
Requires: %{name} == %{version}-%{release}
# nowide is a header only library on linux
Provides: boost-nowide-static = %{version}-%{release}
%if 0%{?fedora}
Requires: boost-devel
%else
# this isn't in EPEL yet ... but it will be soon
Requires:  boost157-devel
%endif

Summary: The header files to compile against boost.nowide

%package docs
Requires: %{name} == %{version}-%{release}
Summary: Documentation for using the nowide boost module

%description
Boost.Nowide is a library implemented by Artyom Beilis
that makes cross platform Unicode aware programming
easier.

The library provides an implementation of standard C and C++ library
functions, such that their inputs are UTF-8 aware on Windows without
requiring to use Wide API.

%description devel
Development files for building against boost-nowide

%description docs
This provides the documentation for boost.nowide in html format.

%prep
%autosetup -p1 -n %{gh_project}-%{gh_commit}


%build
# Need to build the static for install and tests to pass
%if 0%{?fedora}
%cmake -DNOWIDE_BUILD_STATIC=ON -DNOWIDE_SYSTEM_INCLUDE=ON
%else
%cmake3 -DNOWIDE_BUILD_STATIC=ON -DNOWIDE_SYSTEM_INCLUDE=ON \
        -DBOOST_INCLUDEDIR=/usr/include/boost157 \
        -DBOOST_LIBRARYDIR=%{_libdir}/boost157
%endif
%__make %{gh_project}

# Build the docs
cd doc
doxygen

%install
%make_install
# It's header only on linux so remove the libraries generated
rm -f %{buildroot}/usr/lib*/libnowide*

# move to boost157 directory in epel
%if 0%{?rhel}
mkdir -p %{buildroot}%{_includedir}/boost157/boost
mv %{buildroot}%{_includedir}/boost/nowide %{buildroot}%{_includedir}/boost157/boost/
rmdir %{buildroot}%{_includedir}/boost
%endif

%check
%__make test

%files
%license doc/LICENSE_1_0.txt

%files docs
%doc doc/html


%files devel
%if 0%{?fedora}
%{_includedir}/boost/nowide
%else
%{_includedir}/boost157/boost/nowide
%endif

%changelog
* Mon Oct 22 2018 Michal Ingeli <mi@v3.sk> - 0-20181022.2
- Slic3r patch

* Fri Oct 19 2018 Michal Ingeli <mi@v3.sk> - 0-20181019.1
- Apply PR #38 #39 #40

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0-20171027.gitec9672b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Oct 19 2017 James Hogarth <james.hogarth@gmail.com> - 0-20171026.gitec9672b
- Fix the directory location on EPEL to align with the boost157 package correctly
- Move the docs to a dedicated subpackage

* Thu Oct 19 2017 James Hogarth <james.hogarth@gmail.com> - 0-20171019.gitec9672b
- Include documentation files
- Adjust to bring in line with guidelines for a header only package
- Place headers in correct place for epel

* Wed Oct 04 2017 James Hogarth <james.hogarth@gmail.com> - 0-20171003.gitec9672b
- Initial packaging
