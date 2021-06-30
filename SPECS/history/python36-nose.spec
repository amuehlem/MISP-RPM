%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/lib/python%{pybasever}/site-packages

Name:		python36-nose
Version:	1.3.7
Release:	1%{?dist}
Summary:	nose extends unittest to make testing easier

Group:		Development/Languages
License:	LGPL
URL:		https://pypi.org/project/nose/
Source0:	nose-%{version}.tar.gz

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
nose extends unittest to make testing easier

%prep
%setup -q -n nose-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/nosetests
%{_bindir}/nosetests-%{pybasever}
/usr/man/man1/nosetests.1.gz
%{pylibdir}/nose
%{pylibdir}/nose-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.3.7
- first version for python36
