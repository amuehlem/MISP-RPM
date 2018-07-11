%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-pyparsing
Version:	2.2.0
Release:	1%{?dist}
Summary:	Python parsing module

Group:		Development/Languages
License:	MIT License
URL:		https://pypi.org/project/pyparsing/
Source0:	pyparsing-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Python parsing module

%prep
%setup -q -n pyparsing-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/pyparsing.py
%{pylibdir}/pyparsing-%{version}-py%{pybasever}.egg-info
%exclude %{pylibdir}/__pycache__/pyparsing.cpython-*.pyc

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.2.0
- first version for python36
