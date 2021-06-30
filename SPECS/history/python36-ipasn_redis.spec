%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-ipasn_redis
Version:	2.0
Release:	1%{?dist}
Summary:	API to access an IP-ASN-history instance via Redis.

Group:		Development/Languages
License:	GPLv3
URL:		https://pypi.org/project/ipasn-redis/
Source0:	ipasn-redis-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
API to access an IP-ASN-history instance via Redis.

%prep
%setup -q -n ipasn-redis-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/ipasn*
%{pylibdir}/ipasn_redis
%{pylibdir}/ipasn_redis-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.0
- first version for python36
