%global commit0 31dbfef4f228699115a74524c5021b81d86d39c2
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%global srcname napalm
%global sum Network Automation and Programmability Abstraction Layer with Multivendor support
%global	desc NAPALM (Network Automation and Programmability Abstraction Layer with \
Multivendor support) is a Python library that implements a set of \
functions to interact with different router vendor devices using \
a unified API.

%global pypi_name napalm

Name:           python-%{pypi_name}
Version:        2.3.2
Release:        3%{?dist}
Summary:        %{sum}

License:        ASL 2.0
URL:            https://github.com/napalm-automation/napalm
Source0:        https://github.com/napalm-automation/%{srcname}/archive/%{commit0}.tar.gz#/%{srcname}-%{shortcommit0}.tar.gz
# Source0:        https://files.pythonhosted.org/packages/source/n/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

Patch1:			remove-arista-eos.patch
Patch2:			version-req.patch

BuildArch:      noarch

BuildRequires:	python-rpm-macros
BuildRequires:	python2-rpm-macros
BuildRequires:	python3-rpm-macros
BuildRequires:	python-srpm-macros



BuildRequires:  python2-devel
# BuildRequires:  python2-cffi >= 1.11.3
BuildRequires:  python-cffi
BuildRequires:  python2-future
BuildRequires:  python-jinja2
BuildRequires:  python2-junos-eznc >= 2.1.5
BuildRequires:  python-netaddr
BuildRequires:  python2-netmiko >= 2.1.1
BuildRequires:  python2-pyIOSXR >= 0.53
BuildRequires:  python2-pynxos >= 0.0.3
BuildRequires:  PyYAML
BuildRequires:  python2-scp
BuildRequires:  python2-setuptools
BuildRequires:  python2-textfsm
BuildRequires:  python2-paramiko
BuildRequires:  python2-pyserial
 
BuildRequires:  python%{python3_pkgversion}-devel
# BuildRequires:  python%{python3_pkgversion}-cffi >= 1.11.3
BuildRequires:  python%{python3_pkgversion}-cffi
BuildRequires:  python%{python3_pkgversion}-future
BuildRequires:  python%{python3_pkgversion}-jinja2
BuildRequires:  python%{python3_pkgversion}-junos-eznc >= 2.1.5
BuildRequires:  python%{python3_pkgversion}-netaddr
BuildRequires:  python%{python3_pkgversion}-netmiko >= 2.1.1
BuildRequires:  python%{python3_pkgversion}-pyIOSXR >= 0.53
BuildRequires:  python%{python3_pkgversion}-pynxos >= 0.0.3
BuildRequires:  python%{python3_pkgversion}-PyYAML
BuildRequires:  python%{python3_pkgversion}-scp
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-textfsm
BuildRequires:  python%{python3_pkgversion}-paramiko
BuildRequires:  python%{python3_pkgversion}-pyserial

%description


%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}
 
Requires:       python-cffi
Requires:       python2-future
Requires:       python-jinja2
Requires:       python2-junos-eznc >= 2.1.5
Requires:       python-netaddr
Requires:       python2-netmiko >= 2.1.1
Requires:       python2-pyIOSXR >= 0.53
Requires:       python2-pynxos >= 0.0.3
Requires:       PyYAML
Requires:       python2-scp
Requires:       python2-setuptools
Requires:       python2-textfsm
Requires:       python2-paramiko
Requires:       python2-pyserial
%description -n python2-%{pypi_name}


%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}
 
Requires:       python%{python3_pkgversion}-cffi
Requires:       python%{python3_pkgversion}-future
Requires:       python%{python3_pkgversion}-jinja2
Requires:       python%{python3_pkgversion}-junos-eznc >= 2.1.5
Requires:       python%{python3_pkgversion}-netaddr
Requires:       python%{python3_pkgversion}-netmiko >= 2.1.1
Requires:       python%{python3_pkgversion}-pyIOSXR >= 0.53
Requires:       python%{python3_pkgversion}-pynxos >= 0.0.3
Requires:       python%{python3_pkgversion}-PyYAML
Requires:       python%{python3_pkgversion}-scp
Requires:       python%{python3_pkgversion}-setuptools
Requires:       python%{python3_pkgversion}-textfsm
Requires:       python%{python3_pkgversion}-paramiko
Requires:       python%{python3_pkgversion}-pyserial
%description -n python%{python3_pkgversion}-%{pypi_name}



%prep
# % autosetup -n %{pypi_name}-%{version}
%setup -qn %{pypi_name}-%{commit0}
%patch1  -p1 -b .remove-eos
%patch2  -p1 -b .version-req
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%py3_build

%install
# Must do the default python version install last because
# the scripts in /usr/bin are overwritten with every setup.py install.
%py2_install
rm -rf %{buildroot}%{_bindir}/*
%py3_install

%check
# ImportError: No module named 'test_base'
# % {__python2} setup.py test
# % {__python3} setup.py test

%files -n python2-%{pypi_name}
%doc README.md
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%files -n python%{python3_pkgversion}-%{pypi_name}
%doc README.md
%{_bindir}/cl_napalm_configure
%{_bindir}/cl_napalm_test
%{_bindir}/cl_napalm_validate
%{_bindir}/napalm
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%changelog
* Mon Oct  1 2018 Michal Ingeli <mi@v3.sk> - 2.3.2-3
- Fixed pynxos version requirements.txt
- Disabled checks, due to test suite errors

* Fri Sep 28 2018 Michal Ingeli <mi@v3.sk> - 2.3.2-2
- Removed EOS support.
- Fixed BR.

* Thu Sep 27 2018 Michal Ingeli <mi@v3.sk> - 2.3.2-1
- Initial package.
