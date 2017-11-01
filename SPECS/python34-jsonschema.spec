%define pythonver 3.4
%define pythondir /usr/lib/python%{pythonver}/site-packages

Name:		python34-jsonschema
Version:	2.6.0
Release:	1%{?dist}
Summary:    jsonschema for python

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.python.org/pypi/libtaxii
Source0:    jsonschema-%{version}.tar.gz

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools
BuildRequires:  python34-pip, unzip
Requires:	python34, python34-pip

%description
Python jsonschema

%prep
%setup -q -n jsonschema-%{version}

%build
# intentianally left empty

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/jsonschema
%{pythondir}/jsonschema
%{pythondir}/jsonschema-%{version}-py%{pythonver}.egg-info

%changelog
* Wed Oct 25 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.3.7
- first version
