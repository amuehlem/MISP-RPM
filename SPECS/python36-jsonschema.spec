%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/lib/python%{pybasever}/site-packages

Name:		python36-jsonschema
Version:	2.6.0
Release:	1%{?dist}
Summary:	An implementation of JSON Schema validation for Python

Group:		Development/Languages
License:	MIT License
URL:		https://pypi.org/project/jsonschema/
Source0:	jsonschema-%{version}.tar.gz

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
An implementation of JSON Schema validation for Python

%prep
%setup -q -n jsonschema-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/jsonschema
%{pylibdir}/jsonschema
%{pylibdir}/jsonschema-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.6.0
- first version for python36
