Name:           perl-Async-Interrupt
Version:        1.24
Release:        2%{?dist}
Summary:        Allow C/XS libraries to interrupt perl asynchronously
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Async-Interrupt/
Source0:        http://www.cpan.org/authors/id/M/ML/MLEHMANN/Async-Interrupt-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  perl(Canary::Stability)
BuildRequires:  perl(common::sense)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.52
BuildRequires:  gcc
BuildRequires:  perl-devel
BuildRequires:  perl-generators
Requires:       perl(Canary::Stability)
Requires:       perl(common::sense)
Requires:       perl(ExtUtils::MakeMaker) >= 6.52
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
This module implements a single feature only of interest to advanced perl
modules, namely asynchronous interruptions (think "UNIX signals", which are
very similar).

%prep
%setup -q -n Async-Interrupt-%{version}

%build
PERL_CANARY_STABILITY_NOPROMPT=1 %{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc Changes COPYING META.json README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Async*
%{_mandir}/man3/*

%changelog
* Wed Sep 19 2018 Michal Ingeli <mi@v3.sk> 1.24-2
- Added perl-generators BR

* Wed Sep 19 2018 Michal Ingeli <mi@v3.sk> 1.24-1
- Specfile autogenerated by cpanspec 1.78.
