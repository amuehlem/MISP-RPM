%define pythonver 3.4
%define pythondir /usr/lib/python%{pythonver}/site-packages

Name:		python34-isodate
Version:	0.6.0
Release:	1%{?dist}
Summary:    isodate for python

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.python.org/pypi/libtaxii
Source0:    isodate-%{version}.tar.gz

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools
BuildRequires:  python34-pip, unzip
Requires:	python34, python34-pip

%description
Python isodate

%prep
%setup -q -n isodate-%{version}

%build
# intentianally left empty

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pythondir}/isodate
%{pythondir}/isodate-%{version}-py%{pythonver}.egg-info

%changelog
* Wed Oct 25 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.6.0
- first version
