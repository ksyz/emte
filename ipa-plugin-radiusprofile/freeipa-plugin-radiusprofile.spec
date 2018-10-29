%if 0%{?fedora}
%define _in_dist_name	freeipa
%else
%define _in_dist_name	ipa
%endif

Name:		%{_in_dist_name}-plugin-radiusprofile
Version:	1
Release:	2%{?dist}
Summary:	Radius profile CLI and UI plugin

License:	WTFPL
URL:		https://v3.sk/~xyzz
Source0:	user-radiusprofile.py
Source1:	radiusprofile.js
Source2:	Attributes.ldif
Source3:	Classes.ldif
Source4:	README.md

%if 0%{?fedora}
Requires:	freeipa-server >= 3.3
Requires:	freeipa-python >= 3.3
%else
Requires:	ipa-server >= 3.3
Requires:	ipa-python >= 3.3
%endif

Requires:	python(abi) = 2.7
BuildRequires: python(abi) = 2.7

BuildArch:	noarch

%description
Plugin provides access to selected radius profile fields. Default IPA 
389DS schema have to be extended. Read the docs.


%prep
true


%build
true


%install
install -d -m 0755 %{buildroot}%{_docdir}/%{name}
install -d -m 0755 %{buildroot}%{_libdir}/python2.7/site-packages/ipalib/plugins
install -d -m 0755 %{buildroot}%{_datadir}/ipa/ui/js/plugins/radiusprofile
install -m 0644 %{SOURCE0} %{buildroot}%{_libdir}/python2.7/site-packages/ipalib/plugins
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/ipa/ui/js/plugins/radiusprofile
install -m 0644 %{SOURCE2} %{SOURCE3} %{SOURCE4} %{buildroot}%{_docdir}/%{name}


%files
%doc %{_docdir}/%{name}/Attributes.ldif 
%doc %{_docdir}/%{name}/Classes.ldif 
%doc %{_docdir}/%{name}/README.md
%{_libdir}/python2.7/site-packages/ipalib/plugins
%{_datadir}/ipa/ui/js/plugins/radiusprofile


%changelog
* Tue Apr 5 2016 Michal Ingeli <mi@v3.sk> 1-2
- Fedora/EL compat

* Tue Apr 5 2016 Michal Ingeli <mi@v3.sk> 1-1
- Initial release

