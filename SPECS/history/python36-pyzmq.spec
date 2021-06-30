%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/lib64/python%{pybasever}/site-packages

Name:		python36-pyzmq
Version:	17.1.0
Release:	1%{?dist}
Summary:	Python bindings for 0MQ

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/pyzmq/
Source0:	pyzmq-%{version}.tar.gz

BuildRequires:  python36, python36-devel, python36-setuptools	
BuildRequires:  git
Requires:	    python36, python36-ordered_set, python36-lxml, python36-dateutils

%description
Python bindings for 0MQ

%prep
%setup -q -n pyzmq-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/zmq
%{pylibdir}/pyzmq-%{version}-py%{pybasever}.egg-info

%changelog
* Fri Aug 10 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 17.1.0
- first version for python36
