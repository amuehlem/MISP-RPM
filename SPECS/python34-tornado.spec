%define date %(date +"%Y%m%d")
%define pythonver 3.4
%define pythondir %{_libdir}/python%pythonver/site-packages

Name:		python34-tornado
Version:	4.5.2
Release:	1%{?dist}
Summary:	Python tornado

Group:		Development/Languages
License:	MIT
URL:		https://github.com/pypa/setuptools/
Source0:	tornado-%{version}.tar.gz

BuildRequires:	python34-devel
Requires:	python34

%description
Python tornado

%prep
%setup -q -n tornado-%{version}

%build
# intentianally left empty

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%pythondir/tornado-%{version}-py%pythonver.egg-info
%pythondir/tornado

%changelog
* Wed Oct 25 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 4.5.2
- first version
