%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/lib64/python%{pybasever}/site-packages

Name:		python36-pyyaml
Version:	3.13
Release:	1%{?dist}
Summary:	YAML parser and emitter for Python

Group:		Development/Languages
License:	MIT License
URL:		https://pypi.org/project/pyyaml/
Source0:	PyYAML-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Internationalized Domain Names in Applications (IDNA)

%prep
%setup -q -n PyYAML-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/yaml
%{pylibdir}/PyYAML-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 3.13
- first version for python36
