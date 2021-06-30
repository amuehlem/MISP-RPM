%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-click_plugins
Version:	1.0.3
Release:	1%{?dist}
Summary:	An extension module for click to enable registering CLI commands via setuptools entry-points.

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/click-plugins/
Source0:	click-plugins-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
An extension module for click to enable registering CLI commands via setuptools entry-points.

%prep
%setup -q -n click-plugins-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/click_plugins
%{pylibdir}/click_plugins-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0.3
- first version for python36
