# Created by pyp2rpm-3.3.2
%global pypi_name pyeapi

Name:           python-%{pypi_name}
Version:        0.8.2
Release:        1%{?dist}
Summary:        Python Client for eAPI

License:        BSD-3
URL:            https://github.com/arista-eosplus/pyeapi
Source0:        https://files.pythonhosted.org/packages/source/p/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
BuildRequires:	python-rpm-macros
BuildRequires:	python2-rpm-macros
BuildRequires:	python3-rpm-macros
BuildRequires:	python-srpm-macros
 
BuildRequires:  python2-devel
BuildRequires:  python2-check-manifest
BuildRequires:  python2-coverage
BuildRequires:  python2-mock
BuildRequires:  python2-netaddr
BuildRequires:  python2-pep8
BuildRequires:  python2-pyflakes
BuildRequires:  python2-setuptools
BuildRequires:  python2-twine
 
BuildRequires:  python3-devel
BuildRequires:  python%{python3_pkgversion}-check-manifest
BuildRequires:  python%{python3_pkgversion}-coverage
BuildRequires:  python%{python3_pkgversion}-mock
BuildRequires:  python%{python3_pkgversion}-netaddr
BuildRequires:  python%{python3_pkgversion}-pep8
BuildRequires:  python%{python3_pkgversion}-pyflakes
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-twine
BuildRequires:  python%{python3_pkgversion}-sphinx

%description
The Python Client for eAPI The Python Client for eAPI (pyeapi) is a native
Python library wrapper around Arista EOS eAPI. It provides a set of Python
language bindings for configuring Arista EOS nodes.The Python library can be
used to communicate with EOS either locally (on-box) or remotely (off-box). It
uses a standard INI-style configuration file to specify one or more nodes and
connection...

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}
 
Requires:       python2-coverage
Requires:       python2-mock
Requires:       python2-netaddr
%description -n python2-%{pypi_name}
The Python Client for eAPI The Python Client for eAPI (pyeapi) is a native
Python library wrapper around Arista EOS eAPI. It provides a set of Python
language bindings for configuring Arista EOS nodes.The Python library can be
used to communicate with EOS either locally (on-box) or remotely (off-box). It
uses a standard INI-style configuration file to specify one or more nodes and
connection...

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}
 
Requires:       python%{python3_pkgversion}-coverage
Requires:       python%{python3_pkgversion}-mock
Requires:       python%{python3_pkgversion}-netaddr
%description -n python%{python3_pkgversion}-%{pypi_name}
The Python Client for eAPI The Python Client for eAPI (pyeapi) is a native
Python library wrapper around Arista EOS eAPI. It provides a set of Python
language bindings for configuring Arista EOS nodes.The Python library can be
used to communicate with EOS either locally (on-box) or remotely (off-box). It
uses a standard INI-style configuration file to specify one or more nodes and
connection...

%package -n python-%{pypi_name}-doc
Summary:        pyeapi documentation
%description -n python-%{pypi_name}-doc
Documentation for pyeapi

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%py3_build
# generate html docs 
PYTHONPATH=${PWD} sphinx-build-3 docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
# Must do the default python version install last because
# the scripts in /usr/bin are overwritten with every setup.py install.
%py2_install
%py3_install

%check
%{__python2} setup.py test
%{__python3} setup.py test

%files -n python2-%{pypi_name}
%license docs/license.rst LICENSE
%doc README.md
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%files -n python%{python3_pkgversion}-%{pypi_name}
%license docs/license.rst LICENSE
%doc README.md
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%files -n python-%{pypi_name}-doc
%doc html
%license docs/license.rst LICENSE

%changelog
* Thu Sep 27 2018 Michal Ingeli <mi@v3.sk> - 0.8.2-1
- Initial package.
