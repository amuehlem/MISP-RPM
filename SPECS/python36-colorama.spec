%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-colorama
Version:	0.3.9
Release:	1%{?dist}
Summary:	Cross-platform colored terminal text.

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/colorama/
Source0:	colorama-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Cross-platform colored terminal text.

%prep
%setup -q -n colorama-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/colorama
%{pylibdir}/colorama-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.3.9
- first version for python36
