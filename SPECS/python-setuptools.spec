%define date %(date +"%Y%m%d")
%define pythonver 2.7
%define pythondir %{_libdir}/python%pythonver/site-packages

Name:		python-setuptools
Version:	36.6.0
Release:	1%{?dist}
Summary:	Python setuptools

Group:		Development/Languages
License:	MIT
URL:		https://github.com/pypa/setuptools/
Source0:	setuptools-%{version}.zip

BuildArch:  noarch
BuildRequires:	python-devel
Requires:	python

%description
Python setuptools

%prep
%setup -q -n setuptools-master

%build
# intentianally left empty

%install
python bootstrap.py
python setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/easy_install
%{_bindir}/easy_install-%pythonver
%pythondir/easy_install.py*
%pythondir/pkg_resources/*
%pythondir/setuptools-%{version}.post%{date}-py%pythonver.egg-info
%pythondir/setuptools

%changelog
* Mon Oct 17 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 36.6.0
- first version
