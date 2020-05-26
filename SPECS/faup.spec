%define cmake cmake3 -DCMAKE_INSTALL_PREFIX:PATH=/usr

Name:		faup
Version:	1.5+git685acb0
Release:	1%{?dist}
Summary:    	Fast URL decoder library
License:    	Public

Group:		Development/Languages
URL:		https://github.com/stricaud/faup/
Source0:	faup-master.tar.gz

BuildRequires: cmake3, cppcheck, gtcaca-devel
Requires: gtcaca

%description
Fast URL decoder library https:////github.com/stricaud/faup/

%package devel
Summary: Files needed to build faup

%description devel
This package contains the files needed for building faup extensions. 

%prep
%setup -q -n %{name}-master

%build
mkdir -p build
cd build
%cmake ..
make %{?_smp_mflags}

%install
cd build/
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
/usr/include/faup/compat.h
/usr/include/faup/datadir.h
/usr/include/faup/decode.h
/usr/include/faup/errors.h
/usr/include/faup/faup.h
/usr/include/faup/features.h
/usr/include/faup/handler.h
/usr/include/faup/options.h
/usr/include/faup/output.h
/usr/include/faup/parson.h
/usr/include/faup/portable.h
/usr/include/faup/return-codes.h
/usr/include/faup/scheme-codes.h
/usr/include/faup/snapshot-file.h
/usr/include/faup/snapshot.h
/usr/include/faup/tld-tree.h
/usr/include/faup/tld.h
/usr/include/faup/urllengths.h
/usr/include/faup/utils.h
/usr/include/faup/version.h
/usr/include/faup/webserver.h

%changelog
* Mon May 25 2020 Andreas Muehlemann <andreas.muehlemann@switch.ch>
- added cmake macro, changed source0 to not interfere with other master.tar.gz

* Sun May 24 2020 Todd E Johnson <todd@toddejohnson.net>
- first version
