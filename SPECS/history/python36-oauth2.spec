%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-oauth2
Version:    1.9.0.post1
Release:	1%{?dist}
Summary:	library for OAuth version 1.9

Group:		Development/Languages
License:	MIT License
URL:		https://pypi.org/project/oauth2/
Source0:	oauth2-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
library for OAuth version 1.9

%prep
%setup -q -n oauth2-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/oauth2
%{pylibdir}/oauth2-%{version}-py%{pybasever}.egg-info
%{pylibdir}/tests

%changelog
* Wed Jul 18 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.9.0.post1
- first version for python36
