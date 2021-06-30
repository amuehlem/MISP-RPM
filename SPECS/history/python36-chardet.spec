%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/lib/python%{pybasever}/site-packages

Name:		python36-chardet
Version:	3.0.4
Release:	1%{?dist}
Summary:	Universal encoding detector for Python 2 and 3

Group:		Development/Languages
License:	LGPL
URL:		https://pypi.org/project/chardet/
Source0:	chardet-%{version}.tar.gz

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Universal encoding detector for Python 2 and 3

%prep
%setup -q -n chardet-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/chardet
%{pylibdir}/chardet-%{version}-py%{pybasever}.egg-info
%exclude %{_bindir}/chardetect

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 3.0.4
- first version for python36
