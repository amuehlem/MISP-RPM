%define pythonver 3.4
%define pythondir /usr/lib/python%{pythonver}/site-packages

Name:		python34-ez_setup
Version:	0.9
Release:	1%{?dist}
Summary:    ez_setup for python

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.python.org/pypi/libtaxii
Source0:    ez_setup-%{version}.tar.gz

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools
BuildRequires:  python34-pip, unzip
Requires:	python34, python34-pip

%description
Python ez_setup

%prep
%setup -q -n ez_setup-%{version}

%build
# intentianally left empty

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pythondir}/ez_setup.py
%{pythondir}/distribute_setup.py
%{pythondir}/ez_setup-%{version}-py%{pythonver}.egg-info
%{pythondir}/__pycache__/*.pyc

%changelog
* Tue Oct 31 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.9
- first version
