%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-SPARQLWrapper
Version:	1.8.2
Release:	1%{?dist}
Summary:	SPARQL Endpoint interface to Python

Group:		Development/Languages
License:	W3C License (W3C SOFTWARE NOTICE AND LICENSE)
URL:		https://pypi.org/project/sparqlwrapper/
Source0:	SPARQLWrapper-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
SPARQL Endpoint interface to Python

%prep
%setup -q -n SPARQLWrapper-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/SPARQLWrapper
%{pylibdir}/SPARQLWrapper-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.8.2
- first version for python36
