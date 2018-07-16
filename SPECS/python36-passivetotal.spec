%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-passivetotal
Version:	1.0.30
Release:	1%{?dist}
Summary:	Client for the PassiveTotal REST API

Group:		Development/Languages
License:	GPLv2
URL:		https://pypi.org/project/passivetotal/
Source0:	passivetotal-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Client for the PassiveTotal REST API

%prep
%setup -q -n passivetotal-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/pt*
%{pylibdir}/passivetotal
%{pylibdir}/passivetotal-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0.30
- first version for python36
