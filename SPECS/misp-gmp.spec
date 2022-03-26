Name:		misp-gmp
Version:	6.2.1
Release: 	7%{?dist}
Summary:	A GNU arbitrary precision library

License:	LGPLv3+ or GPLv2+
URL:		http://gmplib.org/
Source0:	https://gcc.gnu.org/pub/gcc/infrastructure/gmp-6.2.1.tar.bz2

BuildRequires:	m4
Requires:	pkgconfig
Requires(post): info
Requires(preun): info

%description
The gmp package contains GNU MP, a library for arbitrary precision
arithmetic, signed integers operations, rational numbers and floating
point numbers. GNU MP is designed for speed, for both small and very
large operands. GNU MP is fast because it uses fullwords as the basic
arithmetic type, it uses fast algorithms, it carefully optimizes
assembly code for many CPUs' most common inner loops, and it generally
emphasizes speed over simplicity/elegance in its operations.

Install the gmp package if you need a fast arbitrary precision
library.

%package libs
Summary:	Libraries for the GNU MP arbitrary precision library
License:        LGPLv3+ or GPLv2+
Requires:       pkgconfig

%description libs
The gmp package contains GNU MP, a library for arbitrary precision
arithmetic, signed integers operations, rational numbers and floating
point numbers. GNU MP is designed for speed, for both small and very
large operands. GNU MP is fast because it uses fullwords as the basic
arithmetic type, it uses fast algorithms, it carefully optimizes
assembly code for many CPUs' most common inner loops, and it generally
emphasizes speed over simplicity/elegance in its operations.

Install the gmp package if you need a fast arbitrary precision
library.

%package devel
Summary:	Development tools for the GNU MP arbitrary precision library
License:	LGPLv3+ or GPLv2+
Requires: 	pkgconfig

%description devel
The gmp package contains GNU MP, a library for arbitrary precision
arithmetic, signed integers operations, rational numbers and floating
point numbers. GNU MP is designed for speed, for both small and very
large operands. GNU MP is fast because it uses fullwords as the basic
arithmetic type, it uses fast algorithms, it carefully optimizes
assembly code for many CPUs' most common inner loops, and it generally
emphasizes speed over simplicity/elegance in its operations.

Install the gmp package if you need a fast arbitrary precision
library.

%prep
%setup -q -n gmp-%{version}

%build
./configure --prefix=/var/www/cgi-bin/misp-helpers
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
/var/www/cgi-bin/misp-helpers/lib/pkgconfig/*.pc

%post
/sbin/ldconfig
/sbin/install - info /var/www/cgi-bin/misp-helpers/share/info/%{name}. info /var/www/cgi-bin/misp-helpers/share/info/dir || :

%preun
if [$ 1 = 0 ]; then
/sbin/install - info --delete /var/www/cgi-bin/misp-helpers/share/info/%{name}. info /var/www/cgi-bin/misp-helpers/share/info/dir || :
fi

%changelog
* Thu Mar 24 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 6.2.1-3
- moving all to /var/www/cgi-bin/misp-helpers

* Tue Jan 04 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 6.2.1
- first version
