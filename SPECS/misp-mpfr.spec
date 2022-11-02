Name:		misp-mpfr
Version:	4.1.0
Release: 	8%{?dist}
Summary:	A C library for multiple-precision floating-point computations

License:	LGPLv3+ and GPLv3+ and GFDL
URL:		http://www.mpfr.org/
Source0:	https://gcc.gnu.org/pub/gcc/infrastructure/mpfr-4.1.0.tar.bz2

BuildRequires:	misp-gmp-devel, misp-gmp-libs
Requires:	pkgconfig
Requires(post): info
Requires(preun): info

%description
The MPFR library is a C library for multiple-precision floating-point
computations with "correct rounding". The MPFR is efficient and
also has a well-defined semantics. It copies the good ideas from the
ANSI/IEEE-754 standard for double-precision floating-point arithmetic
(53-bit mantissa). MPFR is based on the GMP multiple-precision library.

%package libs
Summary:	A C library for multiple-precision floating-point computations
License:        LGPLv3+ and GPLv3+ and GFDL
Requires:       pkgconfig

%description libs
The MPFR library is a C library for multiple-precision floating-point
computations with "correct rounding". The MPFR is efficient and
also has a well-defined semantics. It copies the good ideas from the
ANSI/IEEE-754 standard for double-precision floating-point arithmetic
(53-bit mantissa). MPFR is based on the GMP multiple-precision library.

%package devel
Summary:	A C library for multiple-precision floating-point computations
License:	LGPLv3+ and GPLv3+ and GFDL
Requires:	pkgconfig

%description devel
The MPFR library is a C library for multiple-precision floating-point
computations with "correct rounding". The MPFR is efficient and
also has a well-defined semantics. It copies the good ideas from the
ANSI/IEEE-754 standard for double-precision floating-point arithmetic
(53-bit mantissa). MPFR is based on the GMP multiple-precision library.

%prep
%setup -q -n mpfr-%{version}

%build
./configure --prefix=/var/www/cgi-bin/misp-helpers --with-gmp=/var/www/cgi-bin/misp-helpers
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
echo "/var/www/cgi-bin/misp-helpers/lib" >> $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/%{name}.conf

rm -f $RPM_BUILD_ROOT/var/www/cgi-bin/misp-helpers/share/info/dir

%files
%doc
%license
/var/www/cgi-bin/misp-helpers/share/

%files libs
/var/www/cgi-bin/misp-helpers/lib/*.so*
/etc/ld.so.conf.d/%{name}.conf

%files devel
/var/www/cgi-bin/misp-helpers/include/*.h
/var/www/cgi-bin/misp-helpers/lib/*.a
/var/www/cgi-bin/misp-helpers/lib/*.la
/var/www/cgi-bin/misp-helpers/lib/pkgconfig/*.pc

%post
/sbin/ldconfig
/sbin/install - info /var/www/cgi-bin/misp-helpers/share/info/%{name}. info /var/www/cgi-bin/misp-helpers/share/info/dir || :

%post libs
/sbin/ldconfig

%preun
if [$ 1 = 0 ]; then 
/sbin/install - info --delete /var/www/cgi-bin/misp-helpers/share/info/%{name}. info /var/www/cgi-bin/misp-helpers/share/info/dir || :
fi

%changelog
* Wed Oct 19 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 4.1.0-6
- moving the ld.so.conf.d file into the libs package

* Thu Mar 24 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 4.1.0-2
- moving all to /var/www/cgi-bin/misp-helper

* Tue Jan 04 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 4.1.0
- first version
