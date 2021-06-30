%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-orderedmultidict
Version:	1.0
Release:	1%{?dist}
Summary:	Ordered Multivalue Dictionary - omdict.

Group:		Development/Languages
License:	Freely Distributable (Unlicense)
URL:		https://pypi.org/project/orderedmultidict/
Source0:	orderedmultidict-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Ordered Multivalue Dictionary - omdict.

%prep
%setup -q -n orderedmultidict-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/orderedmultidict
%{pylibdir}/orderedmultidict-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0
- first version for python36
