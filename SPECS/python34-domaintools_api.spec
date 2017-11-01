%define pythonver 3.4
%define pythondir /usr/lib/python%{pythonver}/site-packages

Name:		python34-domaintools_api
Version:	0.2.0
Release:	1%{?dist}
Summary:    domaintools_api for python

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.python.org/pypi/libtaxii
Source0:    domaintools_api-%{version}.tar.gz

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools
BuildRequires:  python34-pip, unzip
Requires:	python34, python34-pip

%description
Python domaintools_api

%prep
%setup -q -n domaintools_api-%{version}

%build
# intentianally left empty

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/domaintools
%{pythondir}/domaintools
%{pythondir}/domaintools_api-%{version}-py%{pythonver}.egg-info

%changelog
* Tue Oct 31 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.2.0
- first version
