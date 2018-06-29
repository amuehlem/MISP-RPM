Name:		python-mixbox
Version:	1.0.3
Release:	1%{?dist}
Summary:	Python extension for mixbox

Group:		Development/Languages
License:	PHP
URL:		https://github.com/CybOXProject/
Source0:	fake-tgz.tgz

BuildArch:  noarch
BuildRequires:	python-devel, python-setuptools, git
Requires:	python

%description
Python extension for mixbox

%prep
%setup -q -n fake-tgz

%build
# intentianally left empty

%install
git clone https://github.com/CybOXProject/mixbox.git
cd mixbox
git checkout v%{version}
python setup.py install --root=$RPM_BUILD_ROOT

%files
/usr/lib/python2.7/site-packages/mixbox
/usr/lib/python2.7/site-packages/mixbox-%{version}-py2.7.egg-info

%changelog
* Mon Oct 17 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0.2
- first version
