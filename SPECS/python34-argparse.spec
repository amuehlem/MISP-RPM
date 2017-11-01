%define pythonver 3.4
%define pythondir /usr/lib/python%{pythonver}/site-packages

Name:		python34-argparse
Version:	1.4.0
Release:	1%{?dist}
Summary:    argparse for python

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.python.org/pypi/libtaxii
Source0:    argparse-%{version}.tar.gz

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools
BuildRequires:  python34-pip, unzip
Requires:	python34, python34-pip

%description
Python argparse

%prep
%setup -q -n argparse-%{version}

%build
# intentianally left empty

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pythondir}/argparse.py
%{pythondir}/argparse-%{version}-py%{pythonver}.egg-info
%exclude %{pythondir}/__pycache__/argparse.cpython-*.pyc

%changelog
* Wed Oct 25 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.4.0
- first version
