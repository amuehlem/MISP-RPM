Name:		python34-pymisp
Version:	2.4.81
Release:	1%{?dist}
Summary:    Python interface to MISP

Group:		Development/Languages
License:	PyMISP-License
URL:		https://github.com/MISP/PyMISP
Source0:	fake-tgz.tgz

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools, git
BuildRequires:  python34-pip
Requires:	python34, python34-pip

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
* Mon Oct 17 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0
- first version
