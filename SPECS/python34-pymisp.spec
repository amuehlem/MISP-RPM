Name:		python34-pymisp
Version:	2.4.82
Release:	2%{?dist}
Summary:    Python interface to MISP

Group:		Development/Languages
License:	PyMISP-License
URL:		https://github.com/MISP/PyMISP
Source0:	fake-tgz.tgz

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools, git
BuildRequires:  python34-pip
Requires:	python34, python34-pip, python34-requests

%description
Python interface to MISP

%prep
%setup -q -n fake-tgz

%build
# intentianally left empty

%install
git clone https://github.com/CIRCL/PyMISP.git
cd PyMISP
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
/usr/lib/python3.4/site-packages/pymisp-%{version}-py3.4.egg-info
/usr/lib/python3.4/site-packages/pymisp

%changelog
* Fri Jan 12 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.82
- update to version 2.4.82

* Tue Oct 17 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.81
- first version
