%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global _python_bytecompile_extra 0

Name:	    lief
Version:	0.11.4
Release:	1%{?dist}
Summary:	Python extension for lief

Group:		Development/Languages
License:	Apache
URL:		https://github.com/lief-project/
Source0:	fake-tgz.tgz

BuildRequires: devtoolset-7, cmake3, git, cppcheck
Requires:	python36

%package python
Summary:    Python extension for lief
Group:      Development/Languages
License:    Apache

BuildRequires:  python36-devel, python36-setuptools, cmake3
Requires:       python36

%description python
Python extension for LIEF

%package devel
Summary:    Files needed to build LIEF extensions
Group:      Development/Libraries

%description devel
This package contains the files needed for building LIEF extensions.

%description
LIEF - Library to Instrument Executable Formats https://lief.quarkslab.com

%prep
%setup -q -n fake-tgz

%build
git clone --branch master --single-branch https://github.com/lief-project/LIEF.git LIEF
cd LIEF
mkdir build
cd build
scl enable devtoolset-7 '/bin/bash -c "cmake3 -DLIEF_PYTHON_API=on -DLIEF_DOC=off -DCMAKE_INSTALL_PREFIX=$RPM_BUILD_ROOT -DCMAKE_BUILD_TYPE=Release -DPYTHON_VERSION=3.6 .."'
make %{?_smp_mflags}

%install
cd LIEF
python3 setup.py install --root=$RPM_BUILD_ROOT ||:
scl enable devtoolset-7 '/bin/bash -c "make install INSTALL_ROOT=$RPM_BUILD_ROOT"'

# clean up paths
sed -e "s/\/builddir\/build\/BUILDROOT\/%{name}-%{version}-%{release}.%{_arch}//g" -i $RPM_BUILD_ROOT/lib/pkgconfig/LIEF.pc

%files python
%{pylibdir}/lief-%{version}-py3.6.egg-info
%{pylibdir}/lief
%{pylibdir}/_pylief.cpython*.so

%files devel
/include/json.hpp
/include//LIEF
/lib/libLIEF.a

%files
#/lib/libLIEF.so
/share/LIEF

%changelog
* Thu Mar 25 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.11.4
- updated version

* Thu Jul 12 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.8.3
- first version for python 3.6

* Tue Jan 16 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.8.3
- renamed package to lief, added subpackages python and devel

* Fri Jan 12 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.8.3
- new version based on https://github.com/MISP/MISP/issues/2743

* Tue Oct 17 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch>
- first version
