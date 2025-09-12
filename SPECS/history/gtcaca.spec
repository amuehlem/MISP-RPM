%define cmake cmake3 -DCMAKE_INSTALL_PREFIX:PATH=/usr

Name:		gtcaca
Version:	0+gitb05ed3c
Release:	3%{?dist}
Summary:    	some widgets for libcaca
License:    	Public

Group:		Development/Languages
URL:		https://github.com/stricaud/gtcaca/

BuildRequires: cmake3, libcaca-devel, git
Requires: libcaca

%description
some widgets for libcaca https://github.com/stricaud/gtcaca/

%package devel
Summary: Files needed to build gtcaca

%description devel
This package contains the files needed for building gtcaca extensions. 

%prep
%setup -q -T -c

%build
git clone https://github.com/stricaud/gtcaca.git gtcaca
cd gtcaca
mkdir build
cd build
%cmake ..
make %{?_smp_mflags}

%install
cd gtcaca/build/
%make_install

%files
%{_libdir}/libgtcaca.so
%{_libdir}/libgtcaca.so.1

%files devel
%{_libdir}/pkgconfig/gtcaca.pc
%dir /usr/include/gtcaca/
/usr/include/gtcaca/application.h
/usr/include/gtcaca/button.h
/usr/include/gtcaca/iniparse.h
/usr/include/gtcaca/label.h
/usr/include/gtcaca/log.h
/usr/include/gtcaca/main.h
/usr/include/gtcaca/textlist.h
/usr/include/gtcaca/theme.h
/usr/include/gtcaca/utarray.h
/usr/include/gtcaca/utlist.h
/usr/include/gtcaca/widget.h
/usr/include/gtcaca/window.h

%changelog
* Wed Nov 15 2023 Andreas Muehleamnn <andreas.muehlemann@switch.ch>
- removing cppcheck requirement

* Tue Jun 27 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch>
- simplified source and setup routine

* Mon May 25 2020 Andreas Muehlemann <andreas.muehlemann@switch.ch>
- added cmake macro, changed source0 to not interfere with other master.tar.gz files

* Sun May 24 2020 Todd E Johnson <todd@toddejohnson.net>
- first version
