%global __pear  /usr/bin/pear
%define pear_name Console_CommandLine

Name:        php-pear-Console_CommandLine    
Version:    1.2.2
Release:    1%{?dist}
Summary:    A full featured command line options and arguments parser

Group:        Development/Libraries
License:    LGPLv2+
URL:        http://pear.php.net/package/%{pear_name}
Source0:    http://download.pear.php.net/get/%{pear_name}-%{version}.tgz

BuildArch:  noarch
BuildRequires:    php > 7.0
BuildRequires:  php-pear
Requires:        php > 7.0
Requires:       php-pear
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:   php-pear(%{pear_name}) = %{version}

%description
Console_CommandLine is a full featured package for managing command-line 
options and arguments highly inspired from python optparse module, it allows 
the developer to easily build complex command line interfaces.

Main features:
* handles sub commands (ie. $ myscript.php -q subcommand -f file),
* can be completely built from an xml definition file,
* generate --help and --version options automatically,
* can be completely customized,
* builtin support for i18n,
* and much more...

%prep
%setup -q -c
cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml

%build
cd %{pear_name}-%{version}

%install
###%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT/opt/rh-php56/root %{name}.xml
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
%doc /usr/share/doc/pear/Console_CommandLine/*
/usr/share/tests/pear/Console_CommandLine/*
/usr/share/pear/Console/CommandLine/*
/usr/share/pear/Console/CommandLine.php
/usr/share/pear-data/Console_CommandLine/*
/var/lib/pear/.registry/console_commandline.reg
%exclude /var/lib/pear/.channels/*
%exclude /var/lib/pear/.channels/.alias/*
%exclude /var/lib/pear/.filemap
%exclude /var/lib/pear/.lock

%changelog
* Thu Dec 29 2016 Andreas Muehlemann <andreas.muehlemann@switch.ch>
- version 1.2.2

