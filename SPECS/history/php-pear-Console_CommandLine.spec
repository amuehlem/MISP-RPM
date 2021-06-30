%global __pear  /usr/bin/pear
%define pear_name Console_CommandLine

Name:       php-pear-Console_CommandLine    
Version:    1.2.2
Release:    4%{?dist}
Summary:    A full featured command line options and arguments parser

Group:        Development/Libraries
License:    LGPLv2+
URL:        http://pear.php.net/package/%{pear_name}
Source0:    http://download.pear.php.net/get/%{pear_name}-%{version}.tgz

BuildArch:          noarch
BuildRequires:      php > 7.0
Requires:           php > 7.0
Provides:           php-pear(%{pear_name}) = %{version}

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
cp %{SOURCE0} .
%{__pear} -d php_dir=/tmp install --packagingroot $RPM_BUILD_ROOT %{pear_name}-%{version}.tgz
cp -r $RPM_BUILD_ROOT/tmp/Console $RPM_BUILD_ROOT/usr/share/pear
cp -r $RPM_BUILD_ROOT/tmp/.registry $RPM_BUILD_ROOT/usr/share/pear

%files
%defattr(-,root,root,-)
%doc /usr/share/pear/doc/Console_CommandLine
/usr/share/pear/Console/CommandLine/*
/usr/share/pear/Console/CommandLine.php
/usr/share/pear/data
/usr/share/pear/test
/usr/share/pear/.registry/console_commandline.reg
%exclude /tmp

%changelog
* Wed Aug 8 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.2.2
- update to php 7.2

* Thu Dec 29 2016 Andreas Muehlemann <andreas.muehlemann@switch.ch>
- version 1.2.2

