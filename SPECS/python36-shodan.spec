%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-shodan
Version:	1.8.1
Release:	1%{?dist}
Summary:	Python library and command-line utility for Shodan (https://developer.shodan.io)

Group:		Development/Languages
License:	MIT License
URL:		https://pypi.org/project/shodan/
Source0:	shodan-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Python library and command-line utility for Shodan (https://developer.shodan.io)

%prep
%setup -q -n shodan-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/shodan
%{pylibdir}/shodan
%{pylibdir}/shodan-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.8.1
- first version for python36
