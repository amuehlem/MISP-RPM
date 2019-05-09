%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/lib/python%{pybasever}/site-packages

Name:		python36-ply
Version:	3.11
Release:	1%{?dist}
Summary:	Python Lex & Yacc

Group:		Development/Languages
License:	Apache Software License (Apache 2)
URL:		https://pypi.org/project/ply/
Source0:	ply-%{version}.tar.gz

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Yet another URL library

%prep
%setup -q -n ply-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/ply
%{pylibdir}/ply-%{version}-py%{pybasever}.egg-info

%changelog
* Thu May 9 2019 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 3.11
- first version for python36
