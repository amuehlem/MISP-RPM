%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-six
Version:	1.15.0
Release:	1%{?dist}
Summary:	Python 2 and 3 compatibility utilities

Group:		Development/Languages
License:	MIT License
URL:		https://pypi.org/project/six/
Source0:	six-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Python 2 and 3 compatibility utilities

%prep
%setup -q -n six-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/six.py
%{pylibdir}/six-%{version}-py%{pybasever}.egg-info
%{pylibdir}/__pycache__/*.pyc

%changelog
* Wed Sep 16 2020 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.15.0
- update to 1.15.0

* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.11.0
- first version for python36
