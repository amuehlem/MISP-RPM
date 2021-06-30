%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/lib64/python%{pybasever}/site-packages

Name:		python36-yarl
Version:	1.2.6
Release:	1%{?dist}
Summary:	Yet another URL library

Group:		Development/Languages
License:	Apache Software License (Apache 2)
URL:		https://pypi.org/project/yarl/
Source0:	yarl-%{version}.tar.gz

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Yet another URL library

%prep
%setup -q -n yarl-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/yarl
%{pylibdir}/yarl-%{version}-py%{pybasever}.egg-info

%changelog
* Thu Jul 19 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.2.6
- first version for python36
