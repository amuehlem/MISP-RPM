%global _root_prefix    %{_prefix}
%global _root_bindir    %{_bindir}
%global mysql_config    %{_bindir}/mysql_config
%global mysql_sock %(mysql_config --socket 2>/dev/null || echo /var/lib/mysql/mysql.sock)

%global getoptver 1.4.1
%global arctarver 1.4.2
%global structver 1.1.1
%global xmlutil   1.3.0
%global manpages  1.10.0
%global phpapiver 20170718

Name:		php
Version:	7.2.27
Release:	2%{?dist}
Summary:	PHP scripting language for creating dynamic web sites

Group:		Development/Languages
License:	PHP and Zend and BSD
URL:		http://www.php.net/
Source0:	https://secure.php.net/distributions/php-%{version}.tar.xz

Source1:    php.conf
Source2:    php.ini

Obsoletes:  php-pear

BuildRequires:	bzip2-devel, curl-devel >= 7.9, gmp-devel
BuildRequires:	httpd-devel >= 2.0.46-1, pam-devel
BuildRequires:	libstdc++-devel, openssl-devel
BuildRequires:	readline-devel
BuildRequires: 	krb5-devel, openssl-devel, libc-client-devel
BuildRequires: 	cyrus-sasl-devel, openldap-devel, openssl-devel
BuildRequires:	libxslt-devel >= 1.0.18-1, libxml2-devel >= 2.4.14-1
BuildRequires:	libjpeg-devel, libpng-devel, freetype-devel
BuildRequires:	libXpm-devel, t1lib-devel
BuildRequires:	sqlite-devel >= 3.6.0
BuildRequires:	zlib-devel, pcre-devel >= 6.6, smtpdaemon, libedit-devel
BuildRequires:	bzip2, perl, libtool >= 1.4.3, gcc-c++
BuildRequires:	libtool-ltdl-devel
BuildRequires:	tokyocabinet-devel
BuildRequires:	libmcrypt-devel, libtidy-devel
BuildRequires:	aspell-devel >= 0.50.0, recode-devel, libicu-devel >= 4.0
BuildRequires: 	enchant-devel >= 1.2.4
Requires:	httpd

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

BuildRequires: gd-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: freetype-devel
BuildRequires: libXpm-devel
BuildRequires: libwebp-devel

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

%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts.

The %{name} package contains the module (often referred to as mod_php)
which adds support for the PHP language to Apache HTTP Server.

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
    --with-pcre-regex \
    --with-zlib \
    --with-layout=GNU \
    --with-kerberos \
    --with-libxml-dir=%{_root_prefix} \
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
    --with-gd=shared \
    --enable-intl=shared \
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
/usr/lib64/php/%phpapiver/mysqlnd.so
/usr/lib64/php/%phpapiver/pdo_mysql.so

%files pgsql
%config(noreplace) /etc/php.d/pgsql.ini
%config(noreplace) /etc/php.d/pdo_pgsql.ini
/usr/lib64/php/%phpapiver/pgsql.so
/usr/lib64/php/%phpapiver/pdo_pgsql.so

%files opcache
%config(noreplace) /etc/php.d/opcache.ini
/usr/lib64/php/%phpapiver/opcache.so

%files gd
%config(noreplace) /etc/php.d/gd.ini
/usr/lib64/php/%phpapiver/gd.so

%files intl
%config(noreplace) /etc/php.d/intl.ini
/usr/lib64/php/%phpapiver/intl.so

%files curl
%config(noreplace) /etc/php.d/curl.ini
/usr/lib64/php/%phpapiver/curl.so

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
