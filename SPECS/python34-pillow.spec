%define pythonver 3.4
%define pythondir /usr/lib64/python%{pythonver}/site-packages

Name:		python34-pillow
Version:	4.3.0
Release:	1%{?dist}
Summary:    pillow for python

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.python.org/pypi/libtaxii
Source0:    Pillow-%{version}.tar.gz

BuildRequires:	python34-devel, python34-setuptools
BuildRequires:  python34-pip, unzip, zlib-devel, libjpeg-turbo-devel
Requires:	python34, python34-pip, zlib, libjpeg-turbo

%description
Python pillow

%prep
%setup -q -n Pillow-%{version}

%build
# intentianally left empty

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/*.py
%{pythondir}/PIL
%{pythondir}/Pillow-%{version}-py%{pythonver}.egg-info

%changelog
* Tue Oct 31 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 4.3.0
- first version
