%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-click
Version:	6.7
Release:	1%{?dist}
Summary:	A simple wrapper around optparse for powerful command line utilities.

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/click/
Source0:	click-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
A simple wrapper around optparse for powerful command line utilities.

%prep
%setup -q -n click-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/click
%{pylibdir}/click-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 6.7
- first version for python36
