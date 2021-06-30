%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-httplib2
Version:	0.11.3
Release:	1%{?dist}
Summary:	A comprehensive HTTP client library.

Group:		Development/Languages
License:    MIT License
URL:		https://pypi.org/project/httplib2/
Source0:	httplib2-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
A comprehensive HTTP client library.

%prep
%setup -q -n httplib2-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/httplib2
%{pylibdir}/httplib2-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 18 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.11.3
- first version for python36
