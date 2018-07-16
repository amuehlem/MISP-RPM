%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-maec
Version:	4.1.0.13
Release:	3%{?dist}
Summary:	An API for parsing and creating MAEC content.

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/maec/
Source0:	maec-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
An API for parsing and creating MAEC content.

%prep
%setup -q -n maec-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/maec
%{pylibdir}/maec-%{version}-py%{pybasever}.egg-info

%changelog
* Thu Jul 12 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 4.1.0.13
- first version for python36
