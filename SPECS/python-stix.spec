Name:		python-stix
Version:	1.1.1.4
Release:	1%{?dist}
Summary:	Python extension for interfacing stix

Group:		Development/Languages
License:	PHP
URL:		https://github.com/STIXProject/
Source0:	fake-tgz.tgz

BuildArch:  noarch
BuildRequires:	python-devel, python-setuptools, git
Requires:	python

%description
Python extension for stix

%prep
%setup -q -n fake-tgz

%build
# intentianally left empty

%install
git clone https://github.com/STIXProject/python-stix.git
cd python-stix
git checkout v1.1.1.4
python setup.py install --root=$RPM_BUILD_ROOT

%files
/usr/lib/python2.7/site-packages/stix
/usr/lib/python2.7/site-packages/stix-%{version}-py2.7.egg-info

%changelog
* Mon Jan 02 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.1.0.12
- first version
