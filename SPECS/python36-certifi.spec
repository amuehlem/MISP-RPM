%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-certifi
Version:	2020.12.5
Release:	1%{?dist}
Summary:	Python package for providing Mozilla's CA Bundle.

Group:		Development/Languages
License:	Mozilla Public License 2.0
URL:		https://pypi.org/project/certifi/
Source0:	certifi-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Python package for providing Mozilla's CA Bundle.

%prep
%setup -q -n certifi-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/certifi
%{pylibdir}/certifi-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Mar 31 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2020.12.5
- update to version 2020.12.5

* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2018.4.16
- first version for python36
