Name:		misp-pcre
Version:	8.42
Release:	1%{?dist}
Summary:	PCRE - Perl Compatible Regular Expressions

Group:		System Environment/Libraries
License:	BSD Licence
URL:		https://www.pcre.org/
Source0:	pcre-%{version}.tar.gz
Patch:      pcre-%{version}.patch

BuildRequires:  devtoolset-7, cmake3, git, cppcheck
BuildRequires:  autoconf, automake, readline-devel
BuildRequires:  libtool-ltdl-devel, libtool
Requires:       readline

%define libname libpcre3

%description
PCRE - Perl Compatible Regular Expressions
special package for MISP installations, provides /usr/local/lib/libpcre.so.3
which is needed for python36-yara

%package devel
Summary:    PCRE - Perl Compatible Regular Expressions devel files
Group:      System Environment/Libraries
License:    BSD Licence

Requires:   pkgconfig

%description devel
PCRE - Perl Compatible Regular Expressions devel files

%prep
%setup -q -n pcre-%{version}
%patch -p1

%build
autoreconf -f -i
scl enable devtoolset-7 './configure --prefix=/usr/local'
scl enable devtoolset-7 'cmake3'

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d
echo "/usr/local/lib/" >> $RPM_BUILD_ROOT%{_sysconfdir}/ld.so.conf.d/misp-pcre.conf

%files
/usr/local/bin/pcre*
/usr/local/lib/libpcre*
%doc /usr/local/share/doc/pcre
%doc /usr/local/share/man/man*
%config %{_sysconfdir}/ld.so.conf.d/misp-pcre.conf

%files devel
/usr/local/include/pcre*.h
/usr/local/lib/libpcre*.a
/usr/local/lib/libpcre*.la
/usr/local/lib/pkgconfig/libpcre*.pc

%post -p /sbin/ldconfig

%changelog
* Wed Jul 19 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 8.43
- first version
