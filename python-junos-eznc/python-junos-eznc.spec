# Created by pyp2rpm-3.3.2
%global pypi_name junos-eznc

Name:           python-%{pypi_name}
Version:        2.2.0
Release:        2%{?dist}
Summary:        Junos 'EZ' automation for non-programmers

License:        Apache 2.0
URL:            http://www.github.com/Juniper/py-junos-eznc
Source0:        https://files.pythonhosted.org/packages/source/j/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:	python-rpm-macros
BuildRequires:	python2-rpm-macros
BuildRequires:	python3-rpm-macros
BuildRequires:	python-srpm-macros
 
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
 
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%description


%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}
 
Requires:       python-jinja2 >= 2.7.1
Requires:       python-lxml >= 3.2.4
Requires:       python-ncclient >= 0.5.4
Requires:       python-netaddr
Requires:       python2-paramiko >= 1.15.2
Requires:       python2-pyserial
Requires:       python2-pyyaml >= 3.10
Requires:       python2-scp >= 0.7.0
Requires:       python2-six
%description -n python2-%{pypi_name}


%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}
 
Requires:       python%{python3_pkgversion}-jinja2 >= 2.7.1
Requires:       python%{python3_pkgversion}-lxml >= 3.2.4
Requires:       python%{python3_pkgversion}-ncclient >= 0.5.4
Requires:       python%{python3_pkgversion}-netaddr
Requires:       python%{python3_pkgversion}-paramiko >= 1.15.2
Requires:       python%{python3_pkgversion}-pyserial
Requires:       python%{python3_pkgversion}-PyYAML >= 3.10
Requires:       python%{python3_pkgversion}-scp >= 0.7.0
Requires:       python%{python3_pkgversion}-six
%description -n python%{python3_pkgversion}-%{pypi_name}



%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%py3_build

%install
# Must do the default python version install last because
# the scripts in /usr/bin are overwritten with every setup.py install.
%py2_install
%py3_install

%files -n python2-%{pypi_name}
%doc README.txt
%{python2_sitelib}/jnpr
%{python2_sitelib}/junos_eznc-%{version}-py?.?-*.pth
%{python2_sitelib}/junos_eznc-%{version}-py?.?.egg-info

%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README.txt
%{python3_sitelib}/jnpr
%{python3_sitelib}/junos_eznc-%{version}-py?.?-*.pth
%{python3_sitelib}/junos_eznc-%{version}-py?.?.egg-info

%changelog
* Fri Sep 28 2018 Michal Ingeli <mi@v3.sk> - 2.2.0-2
  Fixed BR.

* Thu Sep 27 2018 Michal Ingeli <mi@v3.sk> - 2.2.0-1
- Initial package.
