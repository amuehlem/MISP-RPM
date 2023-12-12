%define cmake cmake3 -DCMAKE_INSTALL_PREFIX:PATH=/usr

Name:		faup
Version:	1.6
Release:	2%{?dist}
Summary:    	Fast URL decoder library
License:    	Public

Group:		Development/Languages
URL:		https://github.com/stricaud/faup/

BuildRequires: cmake3, gtcaca-devel, git
Requires: gtcaca

%description
Fast URL decoder library https://github.com/stricaud/faup/

%package devel
Summary: Files needed to build faup

%description devel
This package contains the files needed for building faup extensions. 

%prep
%setup -q -T -c

%build
git clone https://github.com/stricaud/faup.git faup
cd faup
mkdir -p build
cd build
%cmake ..
make %{?_smp_mflags}

%install
cd faup/build/
%make_install

%files
/usr/bin/faup
%{_libdir}/pkgconfig/faup.pc
%{_libdir}/libfaupl.so
%{_libdir}/libfaupl.so.1
%dir /usr/share/faup
/usr/share/faup/README.txt
/usr/share/faup/modules_available/emulation_ie.lua
/usr/share/faup/modules_available/ipv4toint.lua
/usr/share/faup/modules_available/printcsv.lua
/usr/share/faup/modules_available/redis-url-threatintel.lua
/usr/share/faup/modules_available/uppercase.lua
/usr/share/faup/modules_available/writeall.lua
/usr/share/faup/modules_available/writeinput.lua
/usr/share/faup/mozilla.tlds
/usr/share/man/man1/faup.1.gz

%files devel
%dir /usr/include/faup
/usr/include/faup/*.h

%changelog
* Wed Nov 15 2023 Andreas Muehleamnn <andreas.muehlemann@switch.ch>
- removing cppcheck requirement

* Tue Jun 27 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch>
- simplified source and setup routine

* Wed Jun 30 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch>
- version 1.6
- clone from git

* Mon May 25 2020 Andreas Muehlemann <andreas.muehlemann@switch.ch>
- added cmake macro, changed source0 to not interfere with other master.tar.gz

* Sun May 24 2020 Todd E Johnson <todd@toddejohnson.net>
- first version
