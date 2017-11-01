%define pythonver 3.4
%define pythondir /usr/lib64/python%{pythonver}/site-packages

Name:		python34-PyYAML
Version:	3.12
Release:	1%{?dist}
Summary:    PyYAML for python

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.python.org/pypi/libtaxii
Source0:    PyYAML-%{version}.tar.gz

BuildRequires:	python34-devel, python34-setuptools
BuildRequires:  python34-pip, unzip
Requires:	python34, python34-pip

%description
Python PyYAML

%prep
%setup -q -n PyYAML-%{version}

%build
# intentianally left empty

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pythondir}/yaml
%{pythondir}/PyYAML-%{version}-py%{pythonver}.egg-info

%changelog
* Tue Oct 31 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 3.12
- first version
