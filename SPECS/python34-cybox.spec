%define pythondir /usr/lib/python3.4/site-packages

Name:		python34-cybox
Version:	2.1.0.17
Release:	1%{?dist}
Summary:	Python extension for interfacing cybox

Group:		Development/Languages
License:	BSD
URL:		https://github.com/CybOXProject/
Source0:	fake-tgz.tgz

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools, git
BuildRequires:  unzip
Requires:	python34

%description
Python extension for cybox

%prep
%setup -q -n fake-tgz

%build
# intentianally left empty

%install
git clone https://github.com/CybOXProject/python-cybox.git
cd python-cybox
git checkout v%{version}
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
/usr/lib/python3.4/site-packages/cybox
/usr/lib/python3.4/site-packages/cybox-%{version}-py3.4.egg-info

%changelog
* Fri Jun 29 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.1.0.17
- updated to version 2.1.0.17

* Mon Jan 02 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.1.0.12
- first version
