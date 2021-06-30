%global _root_prefix    %{_prefix}
%global _root_bindir    %{_bindir}
%global mysql_config    %{_bindir}/mysql_config
%global mysql_sock %(mysql_config --socket 2>/dev/null || echo /var/lib/mysql/mysql.sock)

%global apiver		20190902
%global	zendver		20190902
%global	pdover		20170320
%global	fileinfover	1.0.5
%global oci8ver		2.2.0
%global zipver		1.13.0

%global with_onig	1
%global with_zts	1

%global with_dtrace	1
%global	with_libgd	1
%global with_libzip	1
%global	with_zip	0

%if "%{?dist}" == ".el7"
%global with_libpcre 	0
%global with_httpd2410	0
%global with_nginx	0
%else
%global with_libpcre 	1
%global with_httpd2410 	1
%global with_nginx	0
%endif

Name:		php
Version:	7.4.4
Release:	1%{?dist}
Summary:	PHP scripting language for creating dynamic web sites

Group:		Development/Languages
License:	PHP and Zend and BSD and MIT
URL:		http://www.php.net/
Source0:	https://secure.php.net/distributions/php-%{version}.tar.xz

Source1:    php.conf
Source2:    php.ini

BuildRequires:	gnupg2
BuildRequires:	bzip2-devel
BuildRequires:	pkgconfig(libcurl) > 7.15.5
BuildRequires:	httpd-devel >= 2.4.10-1
%if %{with_httpd2410}
BuildRequires:	httpd-filesystem
%endif
%if %{with_nginx}
BuildRequires:	nginx-filesystem
%endif
BuildRequires:	pam-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel
BuildRequires:	pkgconfig(oniguruma) >= 6.8
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig(sqlite3) >= 3.7.4
BuildRequires:	pkgconfig(zlib) >= 1.2.0.4
BuildRequires:	smtpdaemon
BuildRequires:	readline-devel
BuildRequires:	pkgconfig(libedit)
%if %{with_libpcre}
BuildRequires:	pkgconfig(libpcre2-8) >= 10.30
%else
Provides:	bundled(pcre2) = 10.32
%endif
BuildRequires:	bzip2
BuildRequires:	perl
BuildRequires:	perl-version
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gcc
BuildRequires:	gcc-c++
BuildRequires:	libtool
BuildRequires:	libtool-ltdl-devel
%if %{with_dtrace}
BuildRequires:	systemtap-sdt-devel
%endif
BuildRequires:	/bin/ps

Requires:	httpd
%if %{with_httpd2410}
Requires:	httpd-filesystem
%endif

%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts.

The php package contains the module (often referred to as mod_php)
which adds support for the PHP language to Apache HTTP Server.

%package mysql
Summary: A module for PHP applications that use MySQL databases
Group: Development/Languages
License: PHP

BuildRequires: mysql-devel > 4.1.0
Requires: mariadb, mariadb-server

Provides: php-mysqli = %{version}-%{release}
Provides: php-pdo_mysql
Provides: php-mysqlnd
Provides: php-mysql

%description mysql
The %{name}-mysql package contains a dynamic shared object that will add
MySQL database support to PHP. MySQL is an object-relational database
management system. PHP is an HTML-embeddable scripting language. If
you need MySQL support for PHP applications, you will need to install
this package and the %{name} package.

%package pgsql
Summary: A PostgreSQL database module for PHP
Group: Development/Languages
License: PHP

BuildRequires: postgresql-devel

Provides: php_database
Provides: php-pdo_pgsql

%description pgsql
The php-pgsql package add PostgreSQL database support to PHP.
PostgreSQL is an object-relational database management
system that supports almost all SQL constructs. PHP is an
HTML-embedded scripting language. If you need back-end support for
PostgreSQL, you should install this package in addition to the main
php package.

%package opcache
Summary: An opcode cache Zend extension
Group: Development/Languages
License: PHP

Provides: php-opcache = %{version}-%{release}

%description opcache
The %{name}-opcache package contains an opcode cache used for caching and
optimizing intermediate code.

%package gd
Summary: A module for PHP applications for using the gd graphics library
Group: Development/Languages
License: PHP and BSD

%if %{with_libgd}
BuildRequires: pkgconfig(gdlib) >= 2.1.1
%endif
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(libjpeg)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(xpm)
BuildRequires: pkgconfig(libwebp)

Requires: gd

Provides: bundled(gd) = 2.0.35

%description gd
The php-gd package contains a dynamic shared object that will add
support for using the gd graphics library to PHP.

%package curl
Summary: A module for PHP to use curl
Group: Development/Languages
License: PHP and BSD

Provides: php-curl = %{version}-%{release}

%description curl
The php-curl packages contains a dynamic shared object thtat will add curl
supprt to PHP.

%package intl
Summary: Internationalization extension for PHP applications
Group: Development/Languages
License: PHP

BuildRequires: libicu-devel >= 50

%description intl
The php-intl package contains a dynamic shared object that will add
support for using the ICU library to PHP.

%prep
%setup -q -n php-%{version}

%build
%configure \
    --with-libdir=%{_lib} \
    --with-config-file-path=%{_sysconfdir} \
    --with-config-file-scan-dir=%{_sysconfdir}/php.d \
    --disable-debug \
    --with-pic \
    --disable-rpath \
    --with-freetype-dir=%{_root_prefix} \
    --with-png-dir=%{_root_prefix} \
    --with-xpm-dir=%{_root_prefix} \
    --without-gdbm \
    --with-jpeg-dir=%{_root_prefix} \
    --with-openssl \
%if %{with_libpcre}
    --with-external-pcre\
%else
    --with-pcre-regex \
%endif
    --with-zlib \
    --with-layout=GNU \
    --with-kerberos \
    --with-libxml \
    --with-mhash \
    --disable-phpdbg \
    --libdir=%{_libdir}/php \
    --enable-pcntl \
    --without-readline \
    --with-libedit \
    --with-apxs2=%{_root_bindir}/apxs \
    --enable-pdo \
    --enable-mysqlnd=shared \
    --with-mysqli=shared,mysqlnd \
    --with-mysql-sock=%{mysql_sock} \
    --with-pdo-mysql=shared,mysqlnd \
    --without-pdo-sqlite \
    --with-pgsql=shared \
    --with-pdo-pgsql=shared \
    --enable-mbstring \
    --with-pear \
    --enable-intl=shared \
%if %{with_libgd}
      --with-external-gd \
%endif
%if "%{?dist}" != ".el7"
    --with-system-tzdata \
%endif
    --with-curl=shared

make %{?_smp_mflags}


%install
mkdir -p $RPM_BUILD_ROOT/var/lib/php/session
mkdir -p $RPM_BUILD_ROOT/var/lib/php/wsdlcache
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/php.d/
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.modules.d/php.conf
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/php.d/php.ini
install -D -m 644 /etc/httpd/conf/httpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/httpd.conf

# create mysqlnd.ini
cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/mysqlnd.ini << EOF
; enable mysqlnd extension module
extension=mysqlnd.so
EOF

# create pdo_mysql.ini
cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/pdo_mysql.ini << EOF
; enable mysqlnd extension module
extension=pdo_mysql.so
EOF

# create pgsql.ini
cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/pgsql.ini << EOF
; enable pgsql extension module
extension=pgsql.so
EOF

# create pgsql.ini
cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/pdo_pgsql.ini << EOF
; enable pgsql extension module
extension=pdo_pgsql.so
EOF

# create opcache.ini
cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/opcache.ini << EOF
; enable opcache extension module
zend_extension=opcache.so
EOF

# create gd.ini
cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/gd.ini << EOF
; enable gd module
extension=gd.so
EOF

# create intl.ini
cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/intl.ini << EOF
; enable intl module
extension=intl.so
EOF

# create curl.ini
cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/curl.ini << EOF
; enable curl module
extension=curl.so
EOF

make install INSTALL_ROOT=$RPM_BUILD_ROOT
# cleanup
rm $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/httpd.conf
rm $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/httpd.conf.bak

%files mysql
%config(noreplace) /etc/php.d/mysqlnd.ini
%config(noreplace) /etc/php.d/pdo_mysql.ini
/usr/lib64/php/%apiver-zts/mysqlnd.so
/usr/lib64/php/%apiver-zts/pdo_mysql.so

%files pgsql
%config(noreplace) /etc/php.d/pgsql.ini
%config(noreplace) /etc/php.d/pdo_pgsql.ini
/usr/lib64/php/%apiver-zts/pgsql.so
/usr/lib64/php/%apiver-zts/pdo_pgsql.so

%files opcache
%config(noreplace) /etc/php.d/opcache.ini
/usr/lib64/php/%apiver-zts/opcache.so

%files gd
%config(noreplace) /etc/php.d/gd.ini
/usr/lib64/php/%apiver-zts/gd.so

%files intl
%config(noreplace) /etc/php.d/intl.ini
/usr/lib64/php/%apiver-zts/intl.so

%files curl
%config(noreplace) /etc/php.d/curl.ini
/usr/lib64/php/%apiver-zts/curl.so

%files
%doc /usr/share/man/man1/*.gz
/usr/bin/*
/usr/include/php/*
/usr/lib64/*
/usr/share/pear/*
/usr/share/pear/.registry
%config(noreplace) /etc/pear.conf
%config(noreplace) /etc/httpd/conf.modules.d/php.conf
%config(noreplace) /etc/php.d/php.ini
%config(noreplace) /etc/php.d/mysqlnd.ini
%config(noreplace) /etc/php.d/pdo_mysql.ini
%config(noreplace) /etc/php.d/pgsql.ini
%config(noreplace) /etc/php.d/pdo_pgsql.ini
%config(noreplace) /etc/php.d/intl.ini
%attr(755,apache,apache) /var/lib/php
%exclude /.channels*
%exclude /.depdb*
%exclude /.filemap
%exclude /.lock
%exclude /usr/share/pear/.channels*
%exclude /usr/share/pear/.filemap
%exclude /usr/share/pear/.lock

%changelog
* Mon Mar 23 2020 Andreas Muehlemann <andreas.muehlemann@switch.ch - 7.4.4
- update to php 7.4.4

* Fri Feb 14 2020 Andreas Muehlemann <andreas.muehlemann@switch.ch - 7.2.27
- update to php 7.2.27

* Wed Nov 27 2019 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 7.2.25
- update to php 7.2.25
- added curl

* Wed Jun 5 2019 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 7.2.19
- updated to php 7.2.19
- added pgsql
- added intl

* Thu May 2 2019 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 7.2.18
- update to php 7.2.18

* Tue Aug 7 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 7.2.8
- update to php 7.2.8

* Thu Jan 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 7.0.27
- splitted mysql module into own package
- added opcache package
- update to php 7.0.27

* Wed Oct 18 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 7.0.22
- first version
