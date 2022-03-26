%undefine _missing_build_ids_terminate_build

Name:		misp-gcc
Version:	9.4.0
Release: 	8%{?dist}
Summary:	Various compilers (C, C++, Objective-C, Java, ...)

License:	GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
URL:		http://gcc.gnu.org
Source0:	https://gcc.gnu.org/pub/gcc/releases/gcc-9.4.0/gcc-9.4.0.tar.gz

BuildRequires:	misp-gmp-devel, misp-gmp-libs misp-gmp, misp-isl-devel, misp-isl, misp-isl-libs
BuildRequires:	misp-mpfr-devel, misp-mpfr, misp-mpfr-libs, misp-mpc-devel, misp-mpc, misp-mpc-libs
BuildRequires:	glibc-devel(x86-32)

Requires:	misp-gmp-libs, misp-isl-libs, misp-mpfr-libs, misp-mpc-libs

Requires(post): info
Requires(preun): info

%description
The gcc package contains the GNU Compiler Collection
You'll need this package in order to compile C code.

%package libs
Summary:	Various compilers (C, C++, Objective-C, Java, ...)
License:	GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
Requires:	pkgconfig, misp-gcc-libs, misp-mpfr-libs, misp-mpc-libs
Requires:	misp-gmp-libs, misp-isl-libs

%description libs
The gcc package contains the GNU Compiler Collection
You'll need this package in order to compile C code.

%prep
%setup -q -n gcc-%{version}


%build
./configure \
  -enable-checking=release \
  -enable-languages=c,c++,fortran \
  -enable-multilib \
  --prefix=/var/www/cgi-bin/misp-helpers \
  --with-gmp=/var/www/cgi-bin/misp-helpers \
  --with-mpfr=/var/www/cgi-bin/misp-helpers \
  --with-isl=/var/www/cgi-bin/misp-helpers \
  --with-mpc=/var/www/cgi-bin/misp-helpers

make %{?_smp_mflags}

%install
%make_install

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
echo "/var/www/cgi-bin/misp-helpers/lib" >> $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/%{name}.conf
echo "/var/www/cgi-bin/misp-helpers/lib64" >> $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/%{name}.conf

rm -f $RPM_BUILD_ROOT/var/www/cgi-bin/misp-helpers/share/info/dir

%files
%doc
%license
/var/www/cgi-bin/misp-helpers
/etc/ld.so.conf.d/%{name}.conf

%files libs
/var/www/cgi-bin/misp-helpers/lib/*.so*
/var/www/cgi-bin/misp-helpers/lib64/*.so*

%post
/sbin/ldconfig
/sbin/install - info /var/www/cgi-bin/misp-helpers/share/info/%{name}. info /var/www/cgi-bin/misp-helpers/share/info/dir || :

%preun
if [$ 1 = 0 ]; then
/sbin/install - info --delete /var/www/cgi-bin/misp-helpers/share/info/%{name}. info /var/www/cgi-bin/misp-helpers/share/info/dir || :
fi

%changelog
* Thu Mar 24 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 9.4.0-4
- moving everything to /var/www/cgi-bin/misp-helpers and splitting libs

* Wed Jan 05 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 9.4.0
- first version
