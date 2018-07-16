%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-pypdns
Version:	1.3
Release:	1%{?dist}
Summary:	Python API for PDNS.

Group:		Development/Languages
License:	GPLv3
URL:		https://pypi.org/project/pypdns/
Source0:	pypdns-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Python API for PDNS.

%prep
%setup -q -n pypdns-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/pypdns
%{pylibdir}/pypdns-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.3
- first version for python36
