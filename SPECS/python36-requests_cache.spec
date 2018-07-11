%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-requests_cache
Version:	0.4.13
Release:	1%{?dist}
Summary:	Persistent cache for requests library

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/requests_cache/
Source0:	requests-cache-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Persistent cache for requests library

%prep
%setup -q -n requests-cache-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/requests_cache
%{pylibdir}/requests_cache-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.4.13
- first version for python36
