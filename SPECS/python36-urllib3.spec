%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-urllib3
Version:	1.25.3
Release:	1%{?dist}
Summary:	HTTP library with thread-safe connection pooling, file post, and more.

Group:		Development/Languages
License:	MIT License
URL:		https://pypi.org/project/urllib3/
Source0:	urllib3-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
HTTP library with thread-safe connection pooling, file post, and more.

%prep
%setup -q -n urllib3-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/urllib3
%{pylibdir}/urllib3-%{version}-py%{pybasever}.egg-info

%changelog
* Fri Aug 23 2019 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.25.3
- update to 1.25.3

* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.23
- first version for python36
