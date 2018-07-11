%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-pyaml
Version:	17.12.1
Release:	1%{?dist}
Summary:	PyYAML-based module to produce pretty and readable YAML-serialized data

Group:		Development/Languages
License:	WTFPL
URL:		https://pypi.org/project/pyaml/
Source0:	pyaml-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
PyYAML-based module to produce pretty and readable YAML-serialized data

%prep
%setup -q -n pyaml-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/pyaml
%{pylibdir}/pyaml-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 17.12.1
- first version for python36
