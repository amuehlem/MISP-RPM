%define pybasever 3.6
%define pythondir %{_libdir}/python%pybasever/site-packages

Name:		python36-setuptools
Version:	41.2.0
Release:	3%{?dist}
Summary:	Python Setuptools

Group:		Development/Languages
License:	MIT
URL:		https://github.com/pypa/setuptools/
Source0:	setuptools-%{version}.zip

BuildArch:  noarch
BuildRequires:	python36-devel
Requires:	python36

%description
Python setuptools

%prep
%setup -q -n setuptools-master


%build
# intentionally left blank

%install
python3 bootstrap.py
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%exclude %{_bindir}/easy_install
%{_bindir}/easy_install-%{pybasever}
%pythondir/easy_install.py*
%pythondir/pkg_resources/*
%pythondir/setuptools-%{version}.post%(date +%%Y%%m%%d)-py%{pybasever}.egg-info
%pythondir/setuptools
%exclude %pythondir/__pycache__

%changelog
* Wed Sep 18 2019 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 41.2.0
- update to 41.2.0

* Thu May 17 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 36.6.0
- first version for python 3.6
