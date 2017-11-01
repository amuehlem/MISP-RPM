%define pythonver 3.4
%define pythondir /usr/lib/python%{pythonver}/site-packages

Name:		python34-rdflib
Version:	4.2.2
Release:	1%{?dist}
Summary:    rdflib for python

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.python.org/pypi/libtaxii
Source0:    rdflib-%{version}.tar.gz

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools
BuildRequires:  python34-pip, unzip
Requires:	python34, python34-pip

%description
Python rdflib

%prep
%setup -q -n rdflib-%{version}

%build
# intentianally left empty

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/csv2rdf
%{_bindir}/rdf2dot
%{_bindir}/rdfgraphisomorphism
%{_bindir}/rdfpipe
%{_bindir}/rdfs2dot
%{pythondir}/rdflib
%{pythondir}/rdflib-%{version}-py%{pythonver}.egg-info

%changelog
* Wed Oct 25 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 4.2.2
- first version
