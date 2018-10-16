%global commit0 b4a22e3343586fd2ec42f23a589e90601fa51268
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global package_name FreeSSM

%global debug_package %{nil}

Name:		FreeSSM
Version:	1.25
Release:	2.%{shortcommit0}%{?dist}
Summary:	Diagnostic and adjustment tool for Subaru vehicles

Group:		Applications/Engineering
License:	GPLv3+

URL:		https://github.com/Comer352L/FreeSSM
Source0:	https://github.com/Comer352L/%{package_name}/archive/%{commit0}.tar.gz#/%{package_name}-%{shortcommit0}.tar.gz
Source1:	%{name}.desktop
Source2:	%{name}.png

BuildRequires:	qt5-qtbase-devel
BuildRequires:	desktop-file-utils
# Requires:	

%description
FreeSSM is a free and easy to use diagnostic and adjustment tool for SUBARU®
vehicles. It currently supports the models LEGACY®, LIBERTY®, OUTBACK®, BAJA®,
IMPREZA®, FORESTER® and TRIBECA® starting with model year 1999 and provides
access to the engine and transmission control units.

PLEASE NOTE:
This program is NOT A PRODUCT OF FUJI HEAVY INDUSTRIES LTD. OR ANY SUBARU®-
ASSOCIATED COMPANY. It is a free re-engineering project which is not
contributed, provided or supported by any company in any way.

All trademarks are property of Fuji Heavy Industries Ltd. or their respective
owners.

%prep
%setup -q -n %{package_name}-%{commit0}

sed \
	-e 's|\(target.path\).*|\1 = %{buildroot}%{_bindir}|g' \
	-e 's|\(doctarget.path\).*|\1 = %{buildroot}%{_docdir}/%{package_name}|g' \
	-e 's|\(filestarget.path\).*|\1 = %{buildroot}%{_datadir}/%{package_name}|g' \
	-e 's|\(defstarget.path\).*|\1 = %{buildroot}%{_datadir}/%{package_name}/definitions|g' \
	-i FreeSSM.pro

%build
# % configure
qmake-qt5
make %{?_smp_mflags}

%install
%make_install
install -d 755 %{buildroot}%{_datadir}/pixmaps/
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/pixmaps/
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE1}

%files
%doc README.txt LICENSE.txt
%{_bindir}/FreeSSM
%{_datadir}/%{package_name}
%{_docdir}/%{package_name}/bg.jpg
%{_docdir}/%{package_name}/help_*.html
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop


%changelog
* Tue Oct 16 2018 Michal Ingeli <mi@v3.sk> 1.25-1
- New HEAD commit

* Wed Mar 22 2017 Michal Ingeli <mi@v3.sk> 1.25-1
- Initial package.
