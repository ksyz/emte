# Created by pyp2rpm-3.3.2
%global pypi_name pynxos

Name:           python-%{pypi_name}
Version:        0.0.4
Release:        1%{?dist}
Summary:        A library for managing Cisco NX-OS devices through NX-API

License:        None
URL:            https://github.com/networktocode/pynxos/
Source0:        https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
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
...

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}
 
Requires:       python2-future
Requires:       python2-requests >= 2.7.0
Requires:       python2-scp
%description -n python2-%{pypi_name}


%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}
 
Requires:       python%{python3_pkgversion}-future
Requires:       python%{python3_pkgversion}-requests >= 2.7.0
Requires:       python%{python3_pkgversion}-scp
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
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%files -n python%{python3_pkgversion}-%{pypi_name}
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Thu Sep 27 2018 Michal Ingeli <mi@v3.sk> - 0.0.4-1
- Initial package.
