Name:	    	lief
Version:	0.8.3
Release:	1%{?dist}
Summary:	Python extension for lief

Group:		Development/Languages
License:	Apache
URL:		https://github.com/lief-project/
Source0:	fake-tgz.tgz

BuildRequires: devtoolset-7, cmake3, git, cppcheck
Requires:	python

%package python
Summary:    Python extension for lief
Group:      Development/Languages
License:    Apache

BuildRequires:  python-devel, python-setuptools > 36
Requires:       python

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
scl enable devtoolset-7 '/bin/bash -c "cmake3 -DLIEF_PYTHON_API=on -DLIEF_DOC=off -DCMAKE_INSTALL_PREFIX=$RPM_BUILD_ROOT -DCMAKE_BUILD_TYPE=Release -DPYTHON_VERSION=2.7 .."'
make %{?_smp_mflags}

%install
cd LIEF/build/api/python
python setup.py install --root=$RPM_BUILD_ROOT ||:
cd ../..
make install INSTALL_ROOT=$RPM_BUILD_ROOT

%files python
%{_libdir}/python2.7/site-packages/_pylief.so
%{_libdir}/python2.7/site-packages/lief-%{version}-py2.7.egg-info
%{_libdir}/python2.7/site-packages/lief

%files devel
/include/json.hpp
/include//LIEF
/lib/libLIEF.a

%files
/lib/libLIEF.so
/share/LIEF

%changelog
* Tue Jan 16 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.8.3
- renamed package to lief, added subpackages python and devel

* Fri Jan 12 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.8.3
- new version based on https://github.com/MISP/MISP/issues/2743

* Tue Oct 17 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch>
- first version
