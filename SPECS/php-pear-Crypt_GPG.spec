%{!?__pear: %global __pear /usr/bin/pear}
%define pear_name Crypt_GPG

Name:       php-pear-Crypt_GPG    
Version:    1.6.4
Release:    1%{?dist}
Summary:    PHP pear package for GNUPG

Group:        Development/Libraries
License:    LGPLv2+
URL:        http://pear.php.net/package/%{pear_name}
Source0:    http://download.pear.php.net/get/%{pear_name}-%{version}.tgz

BuildArch:      noarch
BuildRequires:  php > 7.0
BuildRequires:  php-pear-Console_CommandLine
Requires:       php > 7.0
Requires:       php-pear-Console_CommandLine
Provides:       php-pear(%{pear_name}) = %{version}

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
%{__pear} -d php_dir=/tmp install --nodeps --packagingroot $RPM_BUILD_ROOT %{pear_name}-%{version}.tgz
cp -r $RPM_BUILD_ROOT/tmp/Crypt $RPM_BUILD_ROOT/usr/share/pear
cp -r $RPM_BUILD_ROOT/tmp/.registry $RPM_BUILD_ROOT/usr/share/pear

%files
%defattr(-,root,root,-)
%doc /usr/share/pear/doc/Crypt_GPG
/usr/share/pear/Crypt/GPG/*
/usr/share/pear/Crypt/GPG*php
/usr/bin/crypt-gpg-pinentry
/usr/share/pear/data/Crypt_GPG
/usr/share/pear/test/Crypt_GPG
/usr/share/pear/.registry/crypt_gpg.reg
%exclude /usr/share/pear/.channels
%exclude /usr/share/pear/.depdb
%exclude /usr/share/pear/.depdblock
%exclude /usr/share/pear/.filemap
%exclude /usr/share/pear/.lock
%exclude /tmp

%changelog
* Wed Aug 8 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.4.3
- update to php 7.2

* Thu Dec 29 2016 Andreas Muehlemann <andreas.muehlemann@switch.ch>
- version 1.4.3

