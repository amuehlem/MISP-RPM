%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-argparse
Version:	1.4.0
Release:	1%{?dist}
Summary:	Python command-line parsing library

Group:		Development/Languages
License:	Python Software Foundation License
URL:		https://pypi.org/project/argparse/
Source0:	argparse-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Python command-line parsing library

%prep
%setup -q -n argparse-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/argparse.py
%{pylibdir}/argparse-%{version}-py%{pybasever}.egg-info
%exclude %{pylibdir}/__pycache__/argparse.cpython-*.pyc

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.4.0
- first version for python36
