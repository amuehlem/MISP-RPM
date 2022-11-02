%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%global _python_bytecompile_extra 0
%global _build_id_links none

# prevent empty debug file error
%global debug_package %{nil}

%define pymajorver 3
%define pybasever 3.8
%define venvbasedir /var/www/cgi-bin/misp-modules-venv

%global __requires_exclude_from ^%{venvbasedir}/lib/python%{pybasever}/site-packages/cv2/\.libs/.*\\.so*$
%global __requires_exclude ^lib.*\-[0-9a-f]{8}.so.*$

Name:		misp-modules
Version:	2.4.163
Release:	1%{?dist}
Summary:	MISP modules for expansion services, import and export

Group:		Development/Languages
License:	GPLv3
URL:		https://github.com/MISP/misp-modules
Source0:	fake-tgz.tgz
Source1:    	misp-modules.service
Source2:	misp-modules8.pp

BuildRequires:  git, python38-devel, python38-pip
BuildRequires:	ssdeep-devel, poppler-cpp-devel
BuildRequires:	openjpeg2-devel
BuildRequires:  /usr/bin/pathfix.py
Requires:       %{venvbasedir}/bin/python3, libSM
Requires:	poppler-cpp, zbar, glibc(x86-32)

%description
MISP modules for expansion services, import and export

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
python3.8 -m venv --copies $RPM_BUILD_ROOT%{venvbasedir}
$RPM_BUILD_ROOT%{venvbasedir}/bin/pip3 install -U pip setuptools

git clone https://github.com/MISP/misp-modules.git
cd misp-modules

# install requirements
LANG="en_US.UTF-8"
$RPM_BUILD_ROOT%{venvbasedir}/bin/pip3 install importlib2
# remove specific pymisp commit id
###sed -i '/-e git+https:\/\/github.com\/MISP\/PyMISP.git/d' REQUIREMENTS
$RPM_BUILD_ROOT%{venvbasedir}/bin/pip3 install -r REQUIREMENTS
###$RPM_BUILD_ROOT%{venvbasedir}/bin/pip3 install git+https://github.com/misp/PyMISP
$RPM_BUILD_ROOT%{venvbasedir}/bin/pip3 install git+https://github.com/abenassi/Google-Search-API

# install misp-modules
$RPM_BUILD_ROOT%{venvbasedir}/bin/python3 setup.py install

# path fix for python3
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" . $RPM_BUILD_ROOT%{venvbasedir}

# remove __pycache__ directory and files
rm -rf $RPM_BUILD_ROOT%{venvbasedir}/bin/__pycache__

# rewrite PATH in virtualenv
sed -e "s/\/builddir\/build\/BUILDROOT\/%{name}-%{version}-%{release}.%{_arch}//g" -i $RPM_BUILD_ROOT%{venvbasedir}/bin/*	
sed -e "s/\/builddir\/build\/BUILDROOT\/%{name}-%{version}-%{release}.%{_arch}//g" -i $RPM_BUILD_ROOT%{venvbasedir}/lib/python%{pybasever}/site-packages/*.pth

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/misp-modules.service
mkdir -p $RPM_BUILD_ROOT/usr/share/MISP-modules/policy/selinux
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/MISP-modules/policy/selinux

# cleanup remove .pyc and .git files
find $RPM_BUILD_ROOT%{venvbasedir} -name ".pyc" -delete
find $RPM_BUILD_ROOT%{venvbasedir} -name ".git" -exec rm -rf "{}" \;

%files
%defattr(-,apache,apache,-)
%{venvbasedir}
%exclude %{venvbasedir}/*.pyc
%{_sysconfdir}/systemd/system/misp-modules.service
/usr/share/MISP-modules/policy/selinux/misp-*.pp

%post
semodule -i /usr/share/MISP-modules/policy/selinux/misp-modules8.pp

%changelog
* Wed Oct 19 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.163
- update to 2.4.163

* Mon Aug 08 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.160
- update to 2.4.160

* Tue May 31 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.159
- update to 2.4.159

* Thu Mar 10 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.154
- update to 2.4.154
- first version for RHEL8/CentOS8
