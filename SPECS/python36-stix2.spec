%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-stix2
Version:	1.1.1
Release:	2%{?dist}
Summary:	An API for parsing and generating STIX2 content.

Group:		Development/Languages
License:	BSD License
URL:		https://github.com/oasis-open/cti-python-stix2
Source0:	fake-tgz.tgz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
BuildRequires:  git
Requires:	    python36, python36-ordered_set, python36-lxml, python36-dateutils
Requires:       python36-simplejson, python36-antlr4

%description
This repository provides Python APIs for serializing and de-serializing STIX2 JSON content, along with higher-level APIs for common tasks, including data markings, versioning, and for resolving STIX IDs across multiple data sources.

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
git clone https://github.com/oasis-open/cti-python-stix2.git
cd cti-python-stix2
git checkout v%{version}
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/stix2
%{pylibdir}/stix2-%{version}-py%{pybasever}.egg-info

%changelog
* Tue Mar 5 2019 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.1.1
- first version for python36
