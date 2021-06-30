%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-stix
Version:	1.2.0.9
Release:	0%{?dist}
Summary:	An API for parsing and generating STIX content.

Group:		Development/Languages
License:	BSD License
URL:		https://github.com/STIXProject/
Source0:	fake-tgz.tgz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
BuildRequires:  git
Requires:	    python36, python36-ordered_set, python36-lxml, python36-dateutils

%description
An API for parsing and generating STIX content.

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
git clone https://github.com/STIXProject/python-stix.git
cd python-stix
git checkout v%{version}
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/stix
%{pylibdir}/stix-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Mar 31 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.2.0.9
- update to 1.2.0.9

* Fri Jul 6 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.2.0.6
- first version for python36
