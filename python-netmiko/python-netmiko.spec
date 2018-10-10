%bcond_without   python2
%bcond_without   python3

%global srcname netmiko
%global sum Multi-vendor library to simplify Paramiko SSH connections to network devices

Name:           python-%{srcname}
Version:        2.2.2
Release:        5%{?dist}
Summary:        %{sum}

License:        MIT and ASL 2.0
URL:            https://pypi.org/project/%{srcname}
Source0:        https://files.pythonhosted.org/packages/source/n/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:	python-rpm-macros
BuildRequires:	python2-rpm-macros
BuildRequires:	python3-rpm-macros
BuildRequires:	python-srpm-macros


%description
%{sum}

%if %{with python2}

%package -n python2-%{srcname}
Summary:        %{sum}
BuildRequires:  python2-devel
Requires:       python2-paramiko >= 2.0.0
Requires:       python2-scp >= 0.10.0
Requires:       PyYAML
Requires:       python2-pyserial
Requires:       python2-textfsm
# For import test, keep the same as requirements
BuildRequires:  python2-paramiko
BuildRequires:  python2-scp
BuildRequires:  PyYAML
BuildRequires:  python2-textfsm
BuildRequires:  python2-pyserial

%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
%{sum} - package for Python 2.

%endif  # with python2


%if %{with python3}

%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{sum}
BuildRequires:  python%{python3_pkgversion}-devel
Requires:       python%{python3_pkgversion}-paramiko >= 2.0.0
Requires:       python%{python3_pkgversion}-scp >= 0.10.0
Requires:       python%{python3_pkgversion}-PyYAML
Requires:       python%{python3_pkgversion}-pyserial
Requires:       python%{python3_pkgversion}-textfsm
# For import test, keep the same as requirements
BuildRequires:  python%{python3_pkgversion}-paramiko
BuildRequires:  python%{python3_pkgversion}-scp
BuildRequires:  python%{python3_pkgversion}-PyYAML
BuildRequires:  python%{python3_pkgversion}-pyserial
BuildRequires:  python%{python3_pkgversion}-textfsm

%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname}
%{sum} - package for Python 3.

%endif  # with python3

# FIXME: build the documentation, when upstream starts shipping its sources:
# https://github.com/ktbyers/netmiko/issues/507


%prep
%autosetup -n %{srcname}-%{version}

%build
%if %{with python2}
%py2_build
%endif  # with python2

%if %{with python3}
%py3_build
%endif  # with python3

%install
%if %{with python2}
%py2_install
%endif  # with python2

%if %{with python3}
%py3_install
%endif  # with python3

%check
# FIXME: run unit tests, when/if upstream creates them:
# https://github.com/ktbyers/netmiko/issues/509
%if %{with python2}
%{__python2} -c "from netmiko import ConnectHandler"
%endif  # with python2

%if %{with python3}
%{__python3} -c "from netmiko import ConnectHandler"
%endif  # with python3


%if %{with python2}

%files -n python2-%{srcname}
%license LICENSE
%doc README.md
%{python2_sitelib}/*

%endif  # with python2

%if %{with python3}

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/*

%endif  # with python3


%changelog
* Wed Sep 26 2018 Michal Ingeli <mi@v3.sk> - 2.2.2-4
- Fixed pyserial dependency

* Wed Sep 26 2018 Michal Ingeli <mi@v3.sk> - 2.2.2-3
- Fixed python3 EPEL build

* Mon Sep 10 2018 Dmitry Tantsur <divius.inside@gmail.com> - 2.2.2-2
- Disable Python 2 subpackage for Fedora (rhbz#1627402)

* Thu Jul 19 2018 Dmitry Tantsur <divius.inside@gmail.com> - 2.2.2-1
- Update to 2.2.2 (rhbz#1559654)

* Tue Jul 17 2018 Dmitry Tantsur <divius.inside@gmail.com> - 2.1.1-1
- Update to 2.1.1

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.1.0-2
- Rebuilt for Python 3.7

* Fri Mar 16 2018 Alan Pevec <alan.pevec@redhat.com> 2.1.0-1
- Update to 2.1.0 (rhbz#1532228)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 4 2018 Dmitry Tantsur <divius.inside@gmail.com> - 1.4.3-1
- Update to 1.4.3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Dmitry Tantsur <divius.inside@gmail.com> - 1.4.2-1
- Update to 1.4.2

* Mon Jul 24 2017 Dmitry Tantsur <divius.inside@gmail.com> - 1.4.1-1
- Initial packaging (#1465006)
