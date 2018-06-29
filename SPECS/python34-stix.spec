Name:		python34-stix
Version:	1.2.0.6
Release:	1%{?dist}
Summary:	Python extension for interfacing stix

Group:		Development/Languages
License:	PHP
URL:		https://github.com/STIXProject/
Source0:	fake-tgz.tgz

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools, git
Requires:	python34

%description
Python extension for stix

%prep
%setup -q -n fake-tgz

%build
# intentianally left empty

%install
git clone https://github.com/STIXProject/python-stix.git
cd python-stix
git checkout v%{version}
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
/usr/lib/python3.4/site-packages/stix
/usr/lib/python3.4/site-packages/stix-%{version}-py3.4.egg-info

%changelog
* Fri Jun 29 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.2.0.6
- update to version 1.2.0.6

* Wed Oct 25 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.1.1.4
- first version
