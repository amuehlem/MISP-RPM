%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-pillow
Version:	5.2.0
Release:	1%{?dist}
Summary:	Python Imaging Library (Fork)

Group:		Development/Languages
License:	Other/Proprietary License (Standard PIL License)
URL:		https://pypi.org/project/pillow/
Source0:	Pillow-%{version}.tar.gz

BuildRequires:  python36, python36-devel, python36-setuptools	
BuildRequires:  zlib-devel, libjpeg-turbo-devel
Requires:	    python36, zlib, libjpeg-turbo

%description
Python Imaging Library (Fork)

%prep
%setup -q -n Pillow-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/PIL
%{pylibdir}/Pillow-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 5.2.0
- first version for python36
