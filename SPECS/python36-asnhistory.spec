%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-asnhistory
Version:	2.0.4
Release:	1%{?dist}
Summary:	Query a redis database to access to the ASNs descriptions.

Group:		Development/Languages
License:	GPLv3
URL:		https://pypi.org/project/asnhistory/
Source0:	asnhistory-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Query a redis database to access to the ASNs descriptions.

%prep
%setup -q -n asnhistory-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/asnhistory
%{pylibdir}/asnhistory-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.0.4
- first version for python36
