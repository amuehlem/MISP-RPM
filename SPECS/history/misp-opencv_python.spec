%undefine _missing_build_ids_terminate_build
%define venvbasedir /var/www/cgi-bin/misp-modules-venv
%define __arch_install_post ${nil}

Name:		misp-opencv_python
Version:	4.5.3.56
Release: 	0%{?dist}
Summary:	opencv_python python package

License:	MIT, Apache License	
URL:		https://github.com/opencv/opencv-python
Source0:	opencv-python-4.5.3.56.tar.gz

BuildRequires:	misp-gcc, misp-cmake, misp-python
BuildRequires:	openssl-devel
BuildRequires:  /usr/bin/pathfix.py

%description
Pre-built CPU-only OpenCV packages for Python.

%prep
%setup -q -n opencv-python-%{version}

%build

%install
export PATH=/usr/local/misp-gcc-9.4.0/bin:/usr/local/misp-cmake-3.22.1/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/misp-gcc-9.4.0/lib64:$LD_LIBRARY_PATH
export CMAKE_MAKE_PROGRAM=/usr/local/misp-cmake-3.22.1/bin/cmake
export CC=/usr/local/misp-gcc-9.4.0/bin/gcc
/var/www/cgi-bin/misp-python/bin/python3 -m venv --copies $RPM_BUILD_ROOT/%{venvbasedir}
$RPM_BUILD_ROOT%{venvbasedir}/bin/pip3 install --upgrade pip setuptools wheel
$RPM_BUILD_ROOT%{venvbasedir}/bin/pip3 wheel . --no-binary :all:
$RPM_BUILD_ROOT%{venvbasedir}/bin/pip3 install numpy-1.22.0-cp39-cp39-linux_x86_64.whl
$RPM_BUILD_ROOT%{venvbasedir}/bin/pip3 install opencv_python-%{version}-cp39-cp39-linux_x86_64.whl

# path fix for python3
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" . $RPM_BUILD_ROOT%{venvbasedir}

# remove __pycache__ directory and files
rm -rf $RPM_BUILD_ROOT%{venvbasedir}/bin/__pycache__

# rewrite PATH in virtualenv
sed -e "s/\/builddir\/build\/BUILDROOT\/%{name}-%{version}-%{release}.%{_arch}//g" -i $RPM_BUILD_ROOT%{venvbasedir}/bin/*

%files
%{venvbasedir}

%changelog
* Fri Jan 07 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 4.5.5.62
- first version
