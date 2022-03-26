Name:		misp-mpc
Version:	1.2.1
Release: 	5%{?dist}
Summary:	C library for multiple precision complex arithmetic

License:	LGPLv3+ and GFDL
URL:		http://www.multiprecision.org/
Source0:	https://gcc.gnu.org/pub/gcc/infrastructure/mpc-1.2.1.tar.gz

BuildRequires:	misp-gmp-devel, misp-gmp, misp-gmp-libs
BuildRequires:	misp-mpfr-devel, misp-mpfr, misp-mpfr-libs

Requires(post): info
Requires(preun): info

%description
MPC is a C library for the arithmetic of complex numbers with
arbitrarily high precision and correct rounding of the result. It is
built upon and follows the same principles as Mpfr.

%package libs
Summary:        C library for multiple precision complex arithmetic
License:        LGPLv3+ and GFDL

%description libs
MPC is a C library for the arithmetic of complex numbers with
arbitrarily high precision and correct rounding of the result. It is
built upon and follows the same principles as Mpfr.

%package devel
Summary:	C library for multiple precision complex arithmetic
License:	LGPLv3+ and GFDL

%description devel
MPC is a C library for the arithmetic of complex numbers with
arbitrarily high precision and correct rounding of the result. It is
built upon and follows the same principles as Mpfr.

%prep
%setup -q -n mpc-%{version}

%build
./configure --prefix=/var/www/cgi-bin/misp-helpers --with-gmp=/var/www/cgi-bin/misp-helpers --with-mpfr=/var/www/cgi-bin/misp-helpers
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
echo "/var/www/cgi-bin/misp-helpers/lib" >> $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/%{name}.conf

rm -f $RPM_BUILD_ROOT/var/www/cgi-bin/misp-helpers/share/info/dir

%files
%doc
%license
/var/www/cgi-bin/misp-helpers
/etc/ld.so.conf.d/%{name}.conf

%files libs
/var/www/cgi-bin/misp-helpers/lib/*.so*

%files devel
/var/www/cgi-bin/misp-helpers/include/*.h
/var/www/cgi-bin/misp-helpers/lib/*.a
/var/www/cgi-bin/misp-helpers/lib/*.la

%post
/sbin/ldconfig
/sbin/install - info /var/www/cgi-bin/misp-helpers/share/info/%{name}. info /var/www/cgi-bin/misp-helpers/share/info/dir || :

%preun
if [$ 1 = 0 ]; then
/sbin/install - info --delete /var/www/cgi-bin/misp-helpers/share/info/%{name}. info /var/www/cgi-bin/misp-helpers/share/info/dir || :
fi

%changelog
* Thu Mar 24 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.2.1-4
- moving everything to /var/www/cgi-bin/misp-helpers

* Tue Jan 04 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.2.1
- first version
