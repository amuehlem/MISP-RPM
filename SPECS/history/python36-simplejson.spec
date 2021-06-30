%define pymajorver 3
%define pybasever 3.6
%define pylibdir %{_libdir}/python%{pybasever}/site-packages

Name:		python36-simplejson
Version:	3.16.0
Release:	1%{?dist}
Summary:	Simple, fast, complete JSON encoder and decoder

Group:		Development/Languages
License:	Academic Free License, MIT License
URL:		https://pypi.org/project/simplejson/
Source0:	simplejson-%{version}.tar.gz

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
simplejson is a simple, fast, complete, correct and extensible JSON <http://json.org> encoder and decoder for Python 2.5+ and Python 3.3+. It is pure Python code with no dependencies, but includes an optional C extension for a serious speed boost.

%prep
%setup -q -n simplejson-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/simplejson
%{pylibdir}/simplejson-%{version}-py%{pybasever}.egg-info

%changelog
* Tue Mar 5 2019 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 3.16.0
- first version for python36
