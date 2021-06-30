%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-isodate
Version:	0.6.0
Release:	1%{?dist}
Summary:	An ISO 8601 date/time/duration parser and formatter

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/isodate/
Source0:	isodate-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
An ISO 8601 date/time/duration parser and formatter

%prep
%setup -q -n isodate-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/isodate
%{pylibdir}/isodate-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.6.0
- first version for python36
