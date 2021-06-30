%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-urlarchiver
Version:	0.2
Release:	1%{?dist}
Summary:	url-archiver is a simple library to fetch and archive URL on the file-system.

Group:		Development/Languages
License:	AGPL
URL:		https://pypi.org/project/urlarchiver/
Source0:	urlarchiver-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
url-archiver is a simple library to fetch and archive URL on the file-system.

%prep
%setup -q -n urlarchiver-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/url_archiver
%{pylibdir}/urlarchiver-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.2
- first version for python36
