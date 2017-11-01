%define pythonver 3.4
%define pythondir /usr/lib/python%{pythonver}/site-packages

Name:		python34-pyparsing
Version:	2.2.0
Release:	1%{?dist}
Summary:    pyparsing for python

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.python.org/pypi/libtaxii
Source0:    pyparsing-%{version}.tar.gz

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools
BuildRequires:  python34-pip, unzip
Requires:	python34, python34-pip

%description
Python pyparsing

%prep
%setup -q -n pyparsing-%{version}

%build
# intentianally left empty

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pythondir}/pyparsing.py
%{pythondir}/pyparsing-%{version}-py%{pythonver}.egg-info
%exclude %{pythondir}/__pycache__/pyparsing.cpython-*.pyc

%changelog
* Wed Oct 25 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.2.0
- first version
