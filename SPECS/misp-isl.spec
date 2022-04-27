Name:		misp-isl
Version:	0.24
Release: 	7%{?dist}
Summary:	ISL Library

License:	MIT
URL:		https://gcc.gnu.org/install/prerequisites.html	
Source0:	https://gcc.gnu.org/pub/gcc/infrastructure/isl-0.24.tar.bz2

BuildRequires:	misp-gmp-devel, misp-gmp-libs, misp-gmp
Requires:	pkgconfig
Requires(post): info
Requires(preun): info

%description
isl is a thread-safe C library for manipulating sets and relations
of integer points bounded by affine constraints.  The descriptions of
the sets and relations may involve both parameters and existentially
quantified variables.  All computations are performed in exact integer
arithmetic using GMP.

isl is released under the MIT license, but depends on the LGPL GMP
library.

%package libs
Summary:        ISL Library
License:        MIT
Requires:       pkgconfig

%description libs
isl is a thread-safe C library for manipulating sets and relations
of integer points bounded by affine constraints.  The descriptions of
the sets and relations may involve both parameters and existentially
quantified variables.  All computations are performed in exact integer
arithmetic using GMP.

isl is released under the MIT license, but depends on the LGPL GMP
library.

%package devel
Summary:	ISL Library
License:	MIT
Requires:	pkgconfig

%description devel
isl is a thread-safe C library for manipulating sets and relations
of integer points bounded by affine constraints.  The descriptions of
the sets and relations may involve both parameters and existentially
quantified variables.  All computations are performed in exact integer
arithmetic using GMP.

isl is released under the MIT license, but depends on the LGPL GMP
library.

%prep
%setup -q -n isl-%{version}


%build
./configure --prefix=/var/www/cgi-bin/misp-helpers --with-gmp-prefix=/var/www/cgi-bin/misp-helpers
make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT/var/www/cgi-bin/misp-helpers/share/gdb/auto-load/usr/lib64
mv $RPM_BUILD_ROOT/var/www/cgi-bin/misp-helpers/lib/*-gdb.py* $RPM_BUILD_ROOT/var/www/cgi-bin/misp-helpers/share/gdb/auto-load/usr/lib64

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
/var/www/cgi-bin/misp-helpers/include/isl/*.h
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
* Wed Apr 27 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.24-7
- moving *gdb.py files out of the way

* Thu Mar 24 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.24-2
- moving everything to /var/www/cgi-bin/misp-helpers

* Tue Jan 04 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.24
- first version
