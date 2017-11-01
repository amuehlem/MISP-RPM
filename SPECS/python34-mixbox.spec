Name:		python34-mixbox
Version:	1.0.2
Release:	1%{?dist}
Summary:	Python extension for mixbox

Group:		Development/Languages
License:	PHP
URL:		https://github.com/CybOXProject/
Source0:	fake-tgz.tgz

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools, git
Requires:	python34

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
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
/usr/lib/python3.4/site-packages/mixbox
/usr/lib/python3.4/site-packages/mixbox-%{version}-py3.4.egg-info

%changelog
* Mon Oct 17 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0.2
- first version
