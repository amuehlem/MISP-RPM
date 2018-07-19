%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-async_timeout
Version:	3.0.0
Release:	1%{?dist}
Summary:	Timeout context manager for asyncio programs

Group:		Development/Languages
License:	Apache Software License (Apache 2)
URL:		https://pypi.org/project/async_timeout/
Source0:	async-timeout-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Timeout context manager for asyncio programs

%prep
%setup -q -n async-timeout-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/async_timeout
%{pylibdir}/async_timeout-%{version}-py%{pybasever}.egg-info

%changelog
* Thu Jul 19 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 3.0.0
- first version for python36
