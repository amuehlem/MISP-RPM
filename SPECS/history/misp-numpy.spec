%undefine _missing_build_ids_terminate_build
%define venvbasedir /var/www/cgi-bin/misp-modules-venv
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global _python_bytecompile_extra 0

Name:		misp-numpy
Version:	1.22.0
Release: 	0%{?dist}
Summary:	A fast multidimensional array facility for Python

License:	BSD
URL:		http://www.numpy.org/
Source0:	numpy-1.22.0.zip

BuildRequires:	misp-gcc, misp-cmake, misp-python
BuildRequires:	/usr/bin/pathfix.py

%description
NumPy is a general-purpose array-processing package designed to
efficiently manipulate large multi-dimensional arrays of arbitrary
records without sacrificing too much speed for small multi-dimensional
arrays.  NumPy is built on the Numeric code base and adds features
introduced by numarray as well as an extended C-API and the ability to
create arrays of arbitrary type.

There are also basic facilities for discrete fourier transform,
basic linear algebra and random number generation. Also included in
this package is a version of f2py that works properly with NumPy.

%prep
%setup -q -n numpy-%{version}


%build

%install
export PATH=/usr/local/misp-gcc-9.4.0/bin:/usr/local/misp-cmake-3.22.1/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/misp-gcc-9.4.0/lib64:$LD_LIBRARY_PATH
export CMAKE_MAKE_PROGRAM=/usr/local/misp-cmake-3.22.1/bin/cmake
export CC=/usr/local/misp-gcc-9.4.0/bin/gcc
/var/www/cgi-bin/misp-python/bin/python3 -m venv --copies $RPM_BUILD_ROOT/%{venvbasedir}
$RPM_BUILD_ROOT%{venvbasedir}/bin/pip3 install --upgrade pip setuptools wheel
$RPM_BUILD_ROOT%{venvbasedir}/bin/pip3 install Cython
$RPM_BUILD_ROOT%{venvbasedir}/bin/pip3 wheel .
$RPM_BUILD_ROOT%{venvbasedir}/bin/pip3 install numpy-%{version}-cp39-cp39-linux_x86_64.whl

# path fix for python3
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" . $RPM_BUILD_ROOT%{venvbasedir}

# remove __pycache__ directory and files
rm -rf $RPM_BUILD_ROOT%{venvbasedir}/bin/__pycache__

# rewrite PATH in virtualenv
sed -e "s/\/builddir\/build\/BUILDROOT\/%{name}-%{version}-%{release}.%{_arch}//g" -i $RPM_BUILD_ROOT%{venvbasedir}/bin/*

%files
%defattr(-,apache,apache,-)
%exclude %{venvbasedir}/*.pyc
%{venvbasedir}


%changelog
* Tue Jan 11 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.22.0
- first version
