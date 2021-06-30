%global __python %{__python3}
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global _python_bytecompile_extra 0
%define _binaries_in_noarch_packages_terminate_build 0
# disable mangling of shebangs #!
%define __brp_mangle_shebangs /usr/bin/true
# prevent empty debug file error
%global debug_package %{nil}
# accept unpackaged files
%define _unpackaged_files_terminate_build 0

Name:	    	misp-python-virtualenv-lief
Version:	0.10.1
release:	1%{?dist}
Summary:	the lief module for the MISP python virtual environment

Group:		Internet Applications
License:	GPLv3
URL:		https://github.com/lief-project/
Source0:	fake-tgz.tgz

BuildRequires:  git, python3-devel, python3-pip
BuildRequires:  libxslt-devel, zlib-devel
BuildRequires:	cmake3
BuildRequires: 	misp-python-virtualenv
Requires:	misp-python-virtualenv

%description
the lief module for the MISP python virtual environment

%prep
%setup -q -n fake-tgz

%build
# intentionally left blank

%install

git clone --branch master --single-branch https://github.com/lief-project/LIEF.git lief

mkdir lief/build
cd lief/build

cmake3 -DLIEF_PYTHON_API=on -DPYTHON_VERSION=3.6 -DPYTHON_EXECUTABLE=/var/www/cgi-bin/misp-virtualenv/bin/python3 -DLIEF_DOC=off -DCMAKE_BUILD_TYPE=Release ..
make -j3 pyLIEF
mkdir -p $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/lib/python3.6/site-packages/
mkdir -p $RPM_BUILD_ROOT/var/www/MISP/app/files/scripts/lief/build
cp -r api $RPM_BUILD_ROOT/var/www/MISP/app/files/scripts/lief/build
echo /var/www/MISP/app/files/scripts/lief/build/api/python | tee $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/lib/python3.6/site-packages/lief.pth

# path fix for python3
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" . $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/*

# cleanup

%files
%defattr(-,apache,apache,-)
/var/www/cgi-bin/misp-virtualenv/lib/python3.6/site-packages/lief.pth
/var/www/MISP/app/files/scripts/lief/build/api/python/lief
/var/www/MISP/app/files/scripts/lief/build/api/python/lief.so

%post

%changelog
* Thu Sep 03 2020 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.130
- first version for RHEL8 / Centos8
