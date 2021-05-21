%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages
%define __requires_exclude ^/opt/python/(.*)$

Name:		python36-pymisp
Version:	2.4.140
Release:	1%{?dist}
Summary:	Python interface to MISP

Group:		Development/Languages
License:	OSI Approved, BSD License
URL:		https://github.com/MISP/PyMISP
Source0:	fake-tgz.tgz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
BuildRequires:  git, ssdeep-devel
Requires:	python36, python36-six, python36-requests, python36-urllib3
Requires:       python36-python_dateutil, python36-jsonschema, python36-setuptools
Requires:       python36-chardet, python36-certifi, python36-idna

%description
Python interface to MISP

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
git clone https://github.com/MISP/PyMISP.git
cd PyMISP
git submodule update --init
python3 setup.py install --root=$RPM_BUILD_ROOT
pip3 install --root=$RPM_BUILD_ROOT -I .[fileobjects,neo,openioc,virustotal]

%files
%{pylibdir}/pymisp
%{pylibdir}/pymisp-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Mar 31 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.140
- update to 2.4.140

* Wed Jan 8 2020 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.119.1
- update to 2.4.119.1

* Thu May 2 2019 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.106
- update to 2.4.106

* Fri Jul 6 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.92
- first version for python36
