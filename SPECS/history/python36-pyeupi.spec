%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-pyeupi
Version:	1.0
Release:	1%{?dist}
Summary:	Python API for the European Union anti-phishing initiative.

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/pyeupi/
Source0:	pyeupi-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Python API for the European Union anti-phishing initiative.

%prep
%setup -q -n pyeupi-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/pyeupi
%{pylibdir}/pyeupi
%{pylibdir}/pyeupi-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0
- first version for python36
