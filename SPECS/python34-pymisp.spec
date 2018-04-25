Name:		python34-pymisp
Version:	2.4.90
Release:	1%{?dist}
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
git clone https://github.com/MISP/PyMISP.git
cd PyMISP
git submodule update --init
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
/usr/lib/python3.4/site-packages/pymisp-%{version}-py3.4.egg-info
/usr/lib/python3.4/site-packages/pymisp

%changelog
* Wed Apr 25 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.90
- update to version 2.4.90

* Fri Mar 20 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.82-2
- update to version 2.4.89-2

* Fri Jan 12 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.82
- update to version 2.4.82

* Tue Oct 17 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.81
- first version
