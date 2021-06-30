%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-future
Version:	0.16.0
Release:	1%{?dist}
Summary:	Clean single-source support for Python 3 and 2

Group:		Development/Languages
License:	OSI Approved, MIT License
URL:		https://pypi.org/project/future/
Source0:	future-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Internationalized Domain Names in Applications (IDNA)

%prep
%setup -q -n future-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/futurize
%{_bindir}/pasteurize
%{pylibdir}/future
%{pylibdir}/libfuturize
%{pylibdir}/libpasteurize
%{pylibdir}/past
%{pylibdir}/future-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.16.0
- first version for python36
