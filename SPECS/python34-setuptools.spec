%define date %(date +"%Y%m%d")
%define pythonver 3.4
%define pythondir %{_libdir}/python%pythonver/site-packages

Name:		python34-setuptools
Version:	36.6.0
Release:	2%{?dist}
Summary:	Python setuptools

Group:		Development/Languages
License:	MIT
URL:		https://github.com/pypa/setuptools/
Source0:	setuptools-%{version}.zip

BuildArch:  noarch
BuildRequires:	python34-devel
Requires:	python34

%description
Python setuptools

%prep
%setup -q -n setuptools-master

%build
# intentianally left empty

%install
python3 bootstrap.py
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%exclude %{_bindir}/easy_install
%{_bindir}/easy_install-%pythonver
%pythondir/easy_install.py*
%pythondir/pkg_resources/*
%pythondir/setuptools-%{version}.post%{date}-py%pythonver.egg-info
%pythondir/setuptools
%exclude %pythondir/__pycache__

%changelog
* Fri Oct 20 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 36.6.0
- first version
