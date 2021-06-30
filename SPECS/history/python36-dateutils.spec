%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-dateutils
Version:	0.6.6
Release:	1%{?dist}
Summary:	Various utilities for working with date and datetime objects

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/dateutils/
Source0:	dateutils-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Various utilities for working with date and datetime objects

%prep
%setup -q -n dateutils-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/dateadd
%{_bindir}/datediff
%{pylibdir}/dateutils
%{pylibdir}/dateutils-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.6.6
- first version for python36
