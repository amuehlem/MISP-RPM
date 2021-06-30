%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/lib64/python%{pybasever}/site-packages

Name:		python36-ujson
Version:	1.35
Release:	1%{?dist}
Summary:	Ultra fast JSON encoder and decoder for python

Group:		Development/Languages
License:	Apache Software License
URL:		https://pypi.org/project/ujson/
Source0:    ujson-%{version}.tar.gz

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Ultra fast JSON encoder and decoder for Python

%prep
%setup -q -n ujson-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/ujson.cpython-36m-x86_64-linux-gnu.so
%{pylibdir}/ujson-%{version}-py%{pybasever}.egg-info

%changelog
* Thu Jan 3 2019 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.35
- first version for python36
