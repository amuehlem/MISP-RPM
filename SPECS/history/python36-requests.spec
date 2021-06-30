%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-requests
Version:	2.22.0
Release:	1%{?dist}
Summary:	requests

Group:		Development/Languages
License:	Apache Software License
URL:		https://pypi.org/project/requests/
Source0:	requests-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Python HTTP for Humans.

%prep
%setup -q -n requests-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/requests
%{pylibdir}/requests-%{version}-py%{pybasever}.egg-info

%changelog
* Fri Aug 23 2019 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.22.0
- update to version 2.22.0

* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.19.1
- first version for python36
