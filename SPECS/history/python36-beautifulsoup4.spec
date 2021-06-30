%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-beautifulsoup4
Version:	4.6.0
Release:	1%{?dist}
Summary:	Screen-scraping library

Group:		Development/Languages
License:	Python Software Foundation License (BSD)
URL:		https://pypi.org/project/beautifulsoup4/
Source0:	beautifulsoup4-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Screen-scraping library

%prep
%setup -q -n beautifulsoup4-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/bs4
%{pylibdir}/beautifulsoup4-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 4.6.0
- first version for python36
