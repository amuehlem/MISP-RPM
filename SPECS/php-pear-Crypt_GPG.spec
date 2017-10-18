%{!?__pear: %global __pear /usr/bin/pear}
%define pear_name Crypt_GPG

Name:	    php-pear-Crypt_GPG	
Version:	1.4.3
Release:	1%{?dist}
Summary:	PHP pear package for GNUPG

Group:		Development/Libraries
License:	LGPLv2+
URL:		http://pear.php.net/package/%{pear_name}
Source0:	http://download.pear.php.net/get/%{pear_name}-%{version}.tgz

BuildArch:  noarch
BuildRequires:  php > 7.0
BuildRequires:	php-pear
BuildRequires:  php-pear-Console_CommandLine
Requires:	    php-pear
Requires:       php > 7.0
Requires:       php-pear-Console_CommandLine
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:   php-pear(%{pear_name}) = %{version}

%description
This package provides an object oriented interface to GNU Privacy Guard (GnuPG). It requires the GnuPG executable to be on the system.
Though GnuPG can support symmetric-key cryptography, this package is intended only to facilitate public-key cryptography.
This package requires PHP version 5.4.8 or greater.

%prep
%setup -q -c
cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml

%build
cd %{pear_name}-%{version}

%install
#%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT/opt/rh-php56/root %{name}.xml
cp %{SOURCE0} .
%{__pear} install --packagingroot $RPM_BUILD_ROOT %{pear_name}-%{version}.tgz

%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml > /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{name} > /dev/null || :

%files
%defattr(-,root,root,-)
%doc /usr/share/doc/pear/Crypt_GPG/LICENSE
%doc /usr/share/doc/pear/Crypt_GPG/README.md
/usr/share/tests/pear/Crypt_GPG/*
/usr/share/pear/Crypt/GPG/*
/usr/share/pear/Crypt/GPG*php
/var/lib/pear/.registry/crypt_gpg.reg
/usr/bin/crypt-gpg-pinentry
/usr/share/pear-data/Crypt_GPG/data/pinentry-cli.xml
%exclude /var/lib/pear/.channels/*
%exclude /var/lib/pear/.channels/.alias/*
%exclude /var/lib/pear/.filemap
%exclude /var/lib/pear/.lock

%changelog
* Thu Dec 29 2016 Andreas Muehlemann <andreas.muehlemann@switch.ch>
- version 1.4.3
