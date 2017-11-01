%define pythonver 3.4
%define pythondir /usr/lib/python%{pythonver}/site-packages

Name:		python34-requests
Version:	2.18.4
Release:	1%{?dist}
Summary:    requests for python

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.python.org/pypi/libtaxii
Source0:    requests-%{version}.tar.gz

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools
BuildRequires:  python34-pip, unzip, python34-urllib3 <= 1.21
Requires:	python34, python34-pip, python23-urllib3 <= 1.21

%description
Python requests

%prep
%setup -q -n requests-%{version}

%build
# intentianally left empty

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pythondir}/requests
%{pythondir}/requests-%{version}-py%{pythonver}.egg-info

%changelog
* Tue Oct 31 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.18.4
- first version
