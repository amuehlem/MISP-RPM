%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-plyara
Version:	2.0.2
Release:	2%{?dist}
Summary:	Parse YARA rules into a dictionary representation

Group:		Development/Languages
License:	Apache License 2.0
URL:		https://github.com/plyara/plyara
Source0:	fake-tgz.tgz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
BuildRequires:  git
Requires:	    python36, python36-ordered_set, python36-lxml, python36-dateutils
Requires:       python36-ply

%description
Arse YARA rules into a dictionary representation.

Plyara is a script and library that lexes and parses a file consisting of one more YARA rules into a python dictionary representation. The goal of this tool is to make it easier to perform bulk operations or transformations of large sets of YARA rules, such as extracting indicators, updating attributes, and analyzing a corpus. Other applications include linters and dependency checkers.

Plyara leverages the Python module PLY for lexing YARA rules.n API for parsing and generating STIX content.

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
git clone https://github.com/plyara/plyara
cd plyara
git checkout v%{version}
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/plyara
%{pylibdir}/plyara-%{version}-py%{pybasever}.egg-info
%{_bindir}/plyara

%changelog
* Thu May 8 2019 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.0.2
- first version for python36
