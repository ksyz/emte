# Created by pyp2rpm-3.3.2
%global pypi_name pyIOSXR

Name:           python-%{pypi_name}
Version:        0.53
Release:        2%{?dist}
Summary:        Python API to interact with network devices running IOS-XR

License:        None
URL:            https://github.com/fooelisa/pyiosxr/
Source0:        https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
 
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%description


%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}
 
Requires:       python-lxml >= 3.2.4
Requires:       python2-netmiko >= 1.4.3
%description -n python2-%{pypi_name}


%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}
 
Requires:       python%{python3_pkgversion}-lxml >= 3.2.4
Requires:       python%{python3_pkgversion}-netmiko >= 1.4.3
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
%doc README.md
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README.md
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Mon Oct  1 2018 Michal Ingeli <mi@v3.sk> - 0.53-2
- Fixed BR

* Thu Sep 27 2018 Michal Ingeli <mi@v3.sk> - 0.53-1
- Initial package.
