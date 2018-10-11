%global commit0 a22cfaf3bb93bd83e6b72f3f9614ddcec94220bc
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global package_name chbs

Name:           perl-Acme-CHBS
Version:        6
Release:        1.%{shortcommit0}%{?dist}
Summary:        Correct horse battery staple
License:        WTFPL
Group:          Development/Libraries
URL:            https://github.com/ksyz/chbs
Source0:        https://github.com/ksyz/%{package_name}/archive/%{commit0}.tar.gz#/%{package_name}-%{shortcommit0}.tar.gz
Source1:        https://world.std.com/~reinhold/diceware8k.txt

# https://github.com/bitcoin/bips/blob/master/bip-0039/bip-0039-wordlists.md
Source10:		https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt
Source11:		https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/french.txt
Source12:		https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/italian.txt
Source13:		https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/spanish.txt
Source14:		https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/korean.txt
Source15:		https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/japanese.txt
Source16:		https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/chinese_simplified.txt
Source17:		https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/chinese_traditional.txt

BuildArch:      noarch
BuildRequires:  perl >= 0:5.010001
Requires:       perl(Crypt::Random::TESHA2)
Requires:       perl(File::Slurp)
Requires:       words
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
Another xkcd-936 inspired, correct horse battery staple password 
generator.

%prep
%setup -q -n chbs-%{commit0}
echo %{SOURCE1}

%build

%install
install -d -m755 %{buildroot}%{perl_vendorlib}/Acme
install -m644 lib/Acme/CHBS.pm %{buildroot}%{perl_vendorlib}/Acme

install -d -m755 %{buildroot}%{_bindir}
install -m755 chbs %{buildroot}%{_bindir}/chbs
install -m755 dwgen %{buildroot}%{_bindir}/dwgen

install -d -m755 %{buildroot}%{_datadir}/dict/
install -d -m755 %{buildroot}%{_datadir}/dict/bip0039
install -m644 %{SOURCE1} %{buildroot}%{_datadir}/dict/
install -m644 dict/dw-sk-8k.txt %{buildroot}%{_datadir}/dict/
install -m644 dict/dw-cs-8k.txt %{buildroot}%{_datadir}/dict/

for i in %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE15} %{SOURCE16} %{SOURCE17}
do
	install -m644 "$i" %{buildroot}%{_datadir}/dict/bip0039/
done

%{_fixperms} %{buildroot}

%files
%{perl_vendorlib}/*
%{_bindir}/*
%{_datadir}/dict/*
%doc README.md

%changelog
* Wed Jan  3 2018 Michal Ingeli <mi@v3.sk> 6-1
- Version upgrade

* Wed Jan  3 2018 Michal Ingeli <mi@v3.sk> 5-2
- Added perl into BR, to expand perl(:MODULE_COMPAT_) macro.

* Mon Sep 11 2017 Michal Ingeli <mi@v3.sk> 5-1
- Version upgrade
- Added BIP-0039 word lists

* Mon Sep 11 2017 Michal Ingeli <mi@v3.sk> 4-1
- Version upgrade

* Tue Jul 26 2016 Michal Ingeli <mi@v3.sk> 3-2
- Added sk, cs wordlists

* Tue Nov  3 2015 Michal Ingeli <mi@v3.sk> 3-1
- New release
- provided/random word-glueing character (-s/-R)

* Tue Nov  3 2015 Michal Ingeli <mi@v3.sk> 2-1
- New release
- Release numbering with one integer increments, from now on.

* Mon Nov  2 2015 Michal Ingeli <mi@v3.sk> 1.1-1
- New release

* Mon Nov  2 2015 Michal Ingeli <mi@v3.sk> 1.0-1
- Initial package.
