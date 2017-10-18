Name:		python-cybox
Version:	2.1.0.12
Release:	1%{?dist}
Summary:	Python extension for interfacing cybox

Group:		Development/Languages
License:	PHP
URL:		https://github.com/CybOXProject/
Source0:	fake-tgz.tgz

BuildArch:  noarch
BuildRequires:	python-devel, python-setuptools, git
Requires:	python

%description
Python extension for cybox

%prep
%setup -q -n fake-tgz

%build
# intentianally left empty

%install
git clone https://github.com/CybOXProject/python-cybox.git
cd python-cybox
git checkout v2.1.0.12
python setup.py install --root=$RPM_BUILD_ROOT

%files
/usr/lib/python2.7/site-packages/cybox
/usr/lib/python2.7/site-packages/cybox-%{version}-py2.7.egg-info

%changelog
* Mon Jan 02 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.1.0.12
- first version
