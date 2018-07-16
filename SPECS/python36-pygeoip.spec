%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-pygeoip
Version:	0.3.2
Release:	1%{?dist}
Summary:	Pure Python GeoIP API

Group:		Development/Languages
License:	LGPLv3+
URL:		https://pypi.org/project/pygeoip/
Source0:	pygeoip-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Pure Python GeoIP API

%prep
%setup -q -n pygeoip-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/pygeoip
%{pylibdir}/pygeoip-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.3.2
- first version for python36
