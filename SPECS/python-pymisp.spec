Name:		python-pymisp
Version:	2.4.81
Release:	1%{?dist}
Summary:    Python interface to MISP

Group:		Development/Languages
License:	PyMISP-License
URL:		https://github.com/MISP/PyMISP
Source0:	fake-tgz.tgz

BuildArch:  noarch
BuildRequires:	python-devel, python-setuptools, git
BuildRequires:  python-pip
Requires:	python, python-pip

%description
Python interface to MISP

%prep
%setup -q -n fake-tgz

%build
# intentianally left empty

%install
git clone https://github.com/CIRCL/PyMISP.git
cd PyMISP
python setup.py install --root=$RPM_BUILD_ROOT

%files
/usr/lib/python2.7/site-packages/pymisp-%{version}-py2.7.egg-info
/usr/lib/python2.7/site-packages/pymisp

%changelog
* Mon Oct 17 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0
- first version
