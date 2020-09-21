#%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
#%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-strip[[:space:]].*$!!g')
#%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/bin[^[:space:]]*/strip[[:space:]].*$!!g')
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%global _python_bytecompile_extra 0
%global _build_id_links none

# prevent empty debug file error
%global debug_package %{nil}

%define pymajorver 3
%define pybasever 3.6
%define venvbasedir /opt/misp-modules-venv

%global __requires_exclude_from ^%{venvbasedir}/lib/python%{pybasever}/site-packages/cv2/\.libs/.*\\.so*$
%global __requires_exclude ^lib.*\-[0-9a-f]{8}.so.*$

Name:		misp-modules
Version:	1.0
Release:	1%{?dist}
Summary:	MISP modules for expansion services, import and export

Group:		Development/Languages
License:	GPLv3
URL:		https://github.com/MISP/misp-modules
Source0:	fake-tgz.tgz
Source1:    	misp8-modules.service

BuildRequires:  git, python3-devel, python3-pip
BuildRequires:	ssdeep-devel, poppler-cpp-devel
BuildRequires:  /usr/bin/pathfix.py
Requires:       %{venvbasedir}/bin/python3, libSM
Requires:	zbar

%description
MISP modules for expansion services, import and export

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
python3 -m venv --copies $RPM_BUILD_ROOT%{venvbasedir}
$RPM_BUILD_ROOT%{venvbasedir}/bin/pip install -U pip setuptools

git clone https://github.com/MISP/misp-modules.git
cd misp-modules

# install requirements
LANG="en_US.UTF-8"
###LC_CTYPE="en_US.UTF-8"
$RPM_BUILD_ROOT%{venvbasedir}/bin/pip3 install -r REQUIREMENTS
$RPM_BUILD_ROOT%{venvbasedir}/bin/pip3 install git+https://github.com/abenassi/Google-Search-API

# install misp-modules
$RPM_BUILD_ROOT%{venvbasedir}/bin/python3 setup.py install

# path fix for python3
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" . $RPM_BUILD_ROOT%{venvbasedir}

# remove __pycache__ directory and files
rm -rf $RPM_BUILD_ROOT%{venvbasedir}/bin/__pycache__

# rewrite PATH in virtualenv
sed -e "s/\/builddir\/build\/BUILDROOT\/%{name}-%{version}-%{release}.%{_arch}//g" -i $RPM_BUILD_ROOT%{venvbasedir}/bin/*	
sed -e "s/\/builddir\/build\/BUILDROOT\/%{name}-%{version}-%{release}.%{_arch}//g" -i $RPM_BUILD_ROOT%{venvbasedir}/lib/python%{pybasever}/site-packages/*.egg-link
sed -e "s/\/builddir\/build\/BUILDROOT\/%{name}-%{version}-%{release}.%{_arch}//g" -i $RPM_BUILD_ROOT%{venvbasedir}/lib/python%{pybasever}/site-packages/*.pth

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/misp-modules.service

%files
%defattr(-,apache,apache,-)
%{venvbasedir}
%{_sysconfdir}/systemd/system/misp-modules.service

%changelog
* Tue Sep 08 2020 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0-1
- first version for RHEL8/CentOS8
