%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages
%define __requires_exclude ^/opt/python/(.*)$

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global _python_bytecompile_extra 0
%define _binaries_in_noarch_packages_terminate_build 0
# disable mangling of shebangs #!
%define __brp_mangle_shebangs /usr/bin/true

Name:		python36-pymisp
Version:	2.4.143
Release:	1%{?dist}
Summary:	Python interface to MISP

Group:		Development/Languages
License:	OSI Approved, BSD License
URL:		https://github.com/MISP/PyMISP
Source0:	fake-tgz.tgz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
BuildRequires:  git, ssdeep-devel
Requires:	python36, python36-six, python36-requests, python36-urllib3
Requires:       python36-python_dateutil, python36-jsonschema, python36-setuptools
Requires:       python36-chardet, python36-certifi, python36-idna

%description
Python interface to MISP

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
python3 -m venv --copies $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip3 install -U pip setuptools
git clone https://github.com/MISP/PyMISP.git
cd PyMISP
git submodule update --init
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/python3 setup.py install
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip3 install -I .[fileobjects,neo,openioc,virustotal]

# remove __pycache__ directory
rm -rf $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/__pycache__

# rewrite PATH in virtualenv
sed -e "s/\/builddir\/build\/BUILDROOT\/%{name}-%{version}-%{release}.%{_arch}//g" -i $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/*

# cleanup
rm -rf .git .github .gitchangelog.rc .gitignore .gitmodules .travis.yml
find . -name \.git | xargs -i rm -rf {}

%files
%defattr(-,apache,apache,-)
/var/www/cgi-bin/misp-virtualenv
%exclude /usr/lib/debug/

%changelog
* Fri May 28 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.143
- update to 2.4.143

* Wed Mar 31 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.140
- update to 2.4.140

* Wed Jan 8 2020 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.119.1
- update to 2.4.119.1

* Thu May 2 2019 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.106
- update to 2.4.106

* Fri Jul 6 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.92
- first version for python36
