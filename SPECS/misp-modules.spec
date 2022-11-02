%global __os_install_post /usr/lib/rpm/brp-compress %{nil}
%global _python_bytecompile_extra 0
%global _build_id_links none

# prevent empty debug file error
%global debug_package %{nil}

%define pymajorver 3
%define pybasever 3.9
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

BuildRequires:  git, misp-python
BuildRequires:	ssdeep-devel, poppler-cpp-devel
BuildRequires:  /usr/bin/pathfix.py
Requires:       %{venvbasedir}/bin/python3, libSM
Requires:	poppler-cpp, zbar, glibc(x86-32)
Requires:	misp-gcc-libs, misp-python

%description
MISP modules for expansion services, import and export

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
/var/www/cgi-bin/misp-python/bin/python3 -m venv --copies $RPM_BUILD_ROOT%{venvbasedir}
$RPM_BUILD_ROOT%{venvbasedir}/bin/pip3 install -U pip setuptools

git clone https://github.com/MISP/misp-modules.git
cd misp-modules

# install requirements
LANG="en_US.UTF-8"
$RPM_BUILD_ROOT%{venvbasedir}/bin/pip3 install importlib2
# remove specific pymisp commit id
sed -i '/-e git+https:\/\/github.com\/MISP\/PyMISP.git/d' REQUIREMENTS
$RPM_BUILD_ROOT%{venvbasedir}/bin/pip3 install -r REQUIREMENTS
$RPM_BUILD_ROOT%{venvbasedir}/bin/pip3 install git+https://github.com/misp/PyMISP
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

# cleanup remove .pyc and .git files
find $RPM_BUILD_ROOT%{venvbasedir} -name ".pyc" -delete
find $RPM_BUILD_ROOT%{venvbasedir} -name ".git" -exec rm -rf "{}" \;

%files
%defattr(-,apache,apache,-)
%{venvbasedir}
%{_sysconfdir}/systemd/system/misp-modules.service

%changelog
* Wed Oct 19 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.163
- update to 2.4.163

* Mon Aug 08 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.160
- update to 2.4.160

* Tue May 31 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.159
- update to 2.4.159

* Sat Mar 26 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.156
- update to 2.4.156
- using misp-python (version 3.9)

* Wed Aug 11 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.148
- update to 2.4.148

* Tue Jul 27 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.147
- update to 2.4.147

* Wed Jun 30 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.145-1
- new version following misp-2.4.145

* Wed Jun 23 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.121-5
- fixed typos in dependencies

* Wed Oct 07 2020 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.121-3
- added glibc.i686 as depedency

* Thu Oct 01 2020 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.121-2
- added missing poppler-cpp, new version number from git-tags

* Tue Sep 08 2020 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0-1
- first version for RHEL8/CentOS8
