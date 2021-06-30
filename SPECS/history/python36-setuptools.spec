%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-setuptools
Version:	57.0.0
Release:	1%{?dist}
Summary:	Python Setuptools

Group:		Development/Languages
License:	MIT
URL:		https://github.com/pypa/setuptools/
Source0:	fake-tgz.tgz

BuildArch:  	noarch
BuildRequires:	python36-devel, git
Requires:	python36

%description
Python setuptools

%prep
%setup -q -n fake-tgz


%build
# intentionally left blank

%install
python3 -m pip install --ignore-installed --root=$RPM_BUILD_ROOT setuptools

%files
%{pylibdir}/setuptools
%{pylibdir}/pkg_resources
%{pylibdir}/_distutils_hack
%{pylibdir}/distutils-precedence.pth
%{pylibdir}/setuptools-%{version}.dist-info

%changelog
* Fri May 28 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 57.0
- update to 57.0

* Wed Sep 16 2020 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 50.3.0
- update to 50.3.0

* Wed Sep 18 2019 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 41.2.0
- update to 41.2.0

* Thu May 17 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 36.6.0
- first version for python 3.6
