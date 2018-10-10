%global srcname ncclient

Name:           python-ncclient
Version:        0.6.3
Release:        3%{?dist}
Summary:        Python library for NETCONF clients

License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://github.com/leopoul/%{srcname}/archive/v%{version}.tar.gz#/%{srcname}-%{version}.tar.gz
Patch0:			version-req.patch

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-lxml
BuildRequires:  python2-nose
BuildRequires:  python2-paramiko
BuildRequires:  python2-setuptools
BuildRequires:  python2-selectors2
BuildRequires:  python2-mock
# docs
BuildRequires:  python2-sphinx

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-nose
BuildRequires:  python%{python3_pkgversion}-paramiko
BuildRequires:  python%{python3_pkgversion}-selectors2
BuildRequires:  python%{python3_pkgversion}-mock


%global _description\
This project is a Python library that facilitates client-side scripting and\
application development around the NETCONF protocol.\

%description %_description

%package -n python2-ncclient
Summary: %summary
Requires:       libxml2-python
Requires:       libxslt-python
Requires:       python2-selectors2
Requires:       python2-six
Requires:       python-lxml
Requires:       python2-paramiko
%{?python_provide:%python_provide python2-ncclient}

%description -n python2-ncclient %_description

%package -n     python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
 
# Requires:       python%{python3_pkgversion}-lxml >= 3.3.0
Requires:       python%{python3_pkgversion}-lxml
Requires:       python%{python3_pkgversion}-paramiko >= 1.15.0
Requires:       python%{python3_pkgversion}-selectors2 >= 2.0.1
Requires:       python%{python3_pkgversion}-setuptools > 0.6
Requires:       python%{python3_pkgversion}-six

%description -n python%{python3_pkgversion}-%{srcname} %_description

%package -n python-%{srcname}-doc
Summary:        ncclient documentation
%description -n python-%{srcname}-doc
Documentation for ncclient


%prep
%setup -q -n %{srcname}-%{version}
%patch0 -p1 -b .version-req
# Remove bundled egg-info
rm -rf %{srcname}.egg-info


%build
# %{__python2} setup.py build
# make -C docs html
# rm -f docs/build/html/.buildinfo

%py2_build
%py3_build
# generate html docs 
PYTHONPATH=${PWD} sphinx-build docs/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}



%check
nosetests
make -C docs doctest


%install
# %{__python2} setup.py install --skip-build --root $RPM_BUILD_ROOT

%py2_install
%py3_install

 
%files -n python2-%{srcname}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}-%{version}-py?.?.egg-info


%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-%{version}-py?.?.egg-info

%files -n python-%{srcname}-doc
%doc html
%license LICENSE


%changelog
* Mon Oct  1 2018 Michal Ingeli <mi@v3.sk> - 0.6.3-3
- Added requirements.txt patch

* Fri Sep 28 2018 Michal Ingeli <mi@v3.sk> - 0.6.3-2
- Fixed BR.

* Fri Sep 28 2018 Michal Ingeli <mi@v3.sk> - 0.6.3-1
- Version bump

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.4.7-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.4.7-5
- Python 2 binary package renamed to python2-ncclient
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Mar 08 2016 Ihar Hrachyshka <ihrachys@redhat.com> 0.4.7-1.el7
- Update to 0.4.7

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Dec  5 2014 Ihar Hrachyshka <ihrachys@redhat.com> - 0.4.2-2
- Added missing python-setuptools as a build dependency.
- Include documentation and examples.
- Run unit tests on build.
- Rebuild egg file.
- Added python2 macros needed for el6.
- Made python macros more specific (python -> python2).
- Made %{python2_sitelib} file inclusion wildcard a bit more strict.

* Thu Dec  4 2014 Ihar Hrachyshka <ihrachys@redhat.com> - 0.4.2-1
- Updated to upstream 0.4.2 version

* Thu Aug  7 2014 Ihar Hrachyshka <ihrachys@redhat.com> - 0.4.1-1
- Initial package for Fedora
