%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-cabby
Version:	0.1.20
Release:	1%{?dist}
Summary:	TAXII client library

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/cabby/
Source0:	cabby-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
TAXII client library

%prep
%setup -q -n cabby-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/taxii*
%{pylibdir}/cabby
%{pylibdir}/cabby-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.1.20
- first version for python36
