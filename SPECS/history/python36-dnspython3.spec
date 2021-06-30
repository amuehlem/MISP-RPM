%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-dnspython3
Version:    1.15.0
Release:	1%{?dist}
Summary:	A DNS toolkit for Python 3.x

Group:		Development/Languages
License:	Freeware (http://www.dnspython.org/LICENSE)
URL:		https://pypi.org/project/dnspython3/
Source0:	dnspython3-%{version}.zip
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
A DNS toolkit for Python 3.x

%prep
%setup -q -n dnspython3-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/dnspython3-%{version}-py%{pybasever}.egg-info

%changelog
* Fri Jul 13 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.15.0
- first version for python36
