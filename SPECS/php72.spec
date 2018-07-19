%global _root_prefix    %{_prefix}
%global _root_bindir    %{_bindir}
%global mysql_config    %{_bindir}/mysql_config
%global mysql_sock %(mysql_config --socket 2>/dev/null || echo /var/lib/mysql/mysql.sock)

Name:		php72
Version:	7.2.7
Release:	1%{?dist}
Summary:	PHP scripting language for creating dynamic web sites

Group:		Development/Languages
License:	PHP and Zend and BSD
URL:		http://www.php.net/
Source0:	https://secure.php.net/distributions/php-%{version}.tar.xz

Source1:    php.conf
Source2:    php.ini

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

%package opcache
Summary: An opcode cache Zend extension
Group: Development/Languages
License: PHP

Provides: php-opcache = %{version}-%{release}

%description opcache
The %{name}-opcache package contains an opcode cache used for caching and
optimizing intermediate code.

%description
PHP is an HTML-embedded scripting language. PHP attempts to make it
easy for developers to write dynamically generated web pages. PHP also
offers built-in database integration for several commercial and
non-commercial database management systems, so writing a
database-enabled webpage with PHP is fairly simple. The most common
use of PHP coding is probably as a replacement for CGI scripts.

The %{name} package contains the module (often referred to as mod_php)
which adds support for the PHP language to Apache HTTP Server.

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
    --with-exec-dir=%{_bindir} \
    --with-freetype-dir=%{_root_prefix} \
    --with-png-dir=%{_root_prefix} \
    --with-xpm-dir=%{_root_prefix} \
    --enable-gt-native-ttf \
    --with-t1lib=%{_root_prefix} \
    --without-gdbm \
    --with-jpeg-dir=%{_root_prefix} \
    --with-openssl \
    --with-pcre-regex \
    --with-zlib \
    --with-layout=GNU \
    --with-kerberos \
    --with-libxml-dir=%{_root_prefix} \
    --with-system-tzdata \
    --with-mhash \
    --enable-force-cgi-redirect \
    --disable-phpdbg \
    --libdir=%{_libdir}/php \
    --enable-pcntl \
    --enable-fastcgi \
    --without-readline \
    --with-libedit \
    --with-apxs2=%{_root_bindir}/apxs \
    --enable-pdo \
    --enable-ldap \
    --enable-mysqlnd=shared \
    --with-mysqli=shared,mysqlnd \
    --with-mysql-sock=%{mysql_sock} \
    --with-pdo-mysql=shared,mysqlnd \
    --without-pdo-sqlite \
    --enable-mbstring

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

# create mysqli.ini
cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/mysqli.ini << EOF
; enable mysqli extension module
extension=mysqli.so
EOF

# create pdo_mysql.ini
cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/pdo_mysql.ini << EOF
; enable mysqlnd extension module
extension=pdo_mysql.so
EOF

# create opcache.ini
cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/opcache.ini << EOF
; enable opcache extension module
zend_extension=opcache.so
EOF

make install INSTALL_ROOT=$RPM_BUILD_ROOT
# cleanup
rm $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/httpd.conf
rm $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf/httpd.conf.bak

%files mysql
%config(noreplace) /etc/php.d/mysqlnd.ini
%config(noreplace) /etc/php.d/mysqli.ini
%config(noreplace) /etc/php.d/pdo_mysql.ini
/usr/lib64/php/20170718/mysqli.so
/usr/lib64/php/20170718/mysqlnd.so
/usr/lib64/php/20170718/pdo_mysql.so

%files opcache
%config(noreplace) /etc/php.d/opcache.ini
/usr/lib64/php/20170718/opcache.so

%files
%doc /usr/share/man/man1/*.gz
/usr/bin/*
/usr/include/php/*
/usr/lib64/*
%config(noreplace) /etc/httpd/conf.modules.d/php.conf
%config(noreplace) /etc/php.d/php.ini
%config(noreplace) /etc/php.d/mysqlnd.ini
%config(noreplace) /etc/php.d/mysqli.ini
%config(noreplace) /etc/php.d/pdo_mysql.ini
%attr(755,apache,apache) /var/lib/php
%exclude /.channels*
%exclude /.depdb*
%exclude /.filemap
%exclude /.lock
%exclude /usr/share/pear
%exclude /usr/bin/pear*
%exclude /usr/bin/pecl
%exclude /etc/pear.conf
%exclude /usr/share/pear/*

%changelog
* Thu Jan 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 7.0.27
- splitted mysql module into own package
- added opcache package
- update to php 7.0.27

* Wed Oct 18 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 7.0.22
- first version
