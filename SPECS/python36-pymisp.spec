%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-pymisp
Version:	2.4.93
Release:	4%{?dist}
Summary:	Python interface to MISP

Group:		Development/Languages
License:	OSI Approved, BSD License
URL:		https://github.com/MISP/PyMISP
Source0:	fake-tgz.tgz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
BuildRequires:  git
Requires:	    python36, python36-six, python36-requests, python36-urllib3
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

%files
%{pylibdir}/pymisp
%{pylibdir}/pymisp-%{version}-py%{pybasever}.egg-info

%changelog
* Fri Jul 6 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.92
- first version for python36
