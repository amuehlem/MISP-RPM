%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-attrs
Version:	18.1.0
Release:	1%{?dist}
Summary:	Classes Without Boilerplate

Group:		Development/Languages
License:	MIT License
URL:		https://pypi.org/project/attrs/
Source0:	attrs-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Classes Without Boilerplate

%prep
%setup -q -n attrs-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/attr
%{pylibdir}/attrs-%{version}-py%{pybasever}.egg-info

%changelog
* Thu Jul 19 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.7
- first version for python36
