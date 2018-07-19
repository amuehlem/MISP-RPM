%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/lib64/python%{pybasever}/site-packages

Name:		python36-aiohttp
Version:	3.3.2
Release:	1%{?dist}
Summary:	Async http client/server framework (asyncio)

Group:		Development/Languages
License:	Apache Software License (Apache 2)
URL:		https://pypi.org/project/aiohttp/
Source0:	aiohttp-%{version}.tar.gz

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Async http client/server framework (asyncio)

%prep
%setup -q -n aiohttp-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/aiohttp
%{pylibdir}/aiohttp-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 18 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 3.3.2
- first version for python36
