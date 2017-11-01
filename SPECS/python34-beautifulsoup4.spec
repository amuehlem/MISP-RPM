%define pythonver 3.4
%define pythondir /usr/lib/python%{pythonver}/site-packages

Name:		python34-beautifulsoup4
Version:	4.6.0
Release:	1%{?dist}
Summary:    beautifulsoup4 for python

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.python.org/pypi/libtaxii
Source0:    beautifulsoup4-%{version}.tar.gz

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools
BuildRequires:  python34-pip, unzip
Requires:	python34, python34-pip

%description
Python beautifulsoup4

%prep
%setup -q -n beautifulsoup4-%{version}

%build
# intentianally left empty

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pythondir}/bs4
%{pythondir}/beautifulsoup4-%{version}-py%{pythonver}.egg-info

%changelog
* Wed Oct 25 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 4.6.0
- first version
