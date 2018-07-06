%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-mixbox
Version:	1.0.3
Release:	1%{?dist}
Summary:	Utility library for cybox, maec, and stix packages

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/libtaxii/
Source0:	fake-tgz.tgz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
BuildRequires:  git
Requires:	    python36

%description
A library of common code leveraged by python-cybox, python-maec, and python-stix.

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
git clone https://github.com/CybOXProject/mixbox.git
cd mixbox
git checkout v%{version}
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/mixbox
%{pylibdir}/mixbox-%{version}-py%{pybasever}.egg-info

%changelog
* Fri Jul 6 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 10.0.1
- first version for python36
