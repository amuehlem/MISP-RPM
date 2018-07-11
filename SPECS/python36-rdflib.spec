%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/lib/python%{pybasever}/site-packages

Name:		python36-rdflib
Version:	4.2.2
Release:	1%{?dist}
Summary:	RDFLib is a Python library for working with RDF, a simple yet powerful language for representing information.

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/rdflib/
Source0:	rdflib-%{version}.tar.gz

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
RDFLib is a Python library for working with RDF, a simple yet powerful language for representing information.

%prep
%setup -q -n rdflib-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/csv2rdf
%{_bindir}/rdf2dot
%{_bindir}/rdfgraphisomorphism
%{_bindir}/rdfpipe
%{_bindir}/rdfs2dot
%{pylibdir}/rdflib
%{pylibdir}/rdflib-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 4.2.2
- first version for python36
