Name:	php70
Version:	7.0.14	
Release:	1%{?dist}
Summary:	php

Group:		Development/Languages
License:	PHP and Zend and BSD
URL:		http://www.php.net/
Source0:	https://secure.php.net/distributions/php-%{version}%{?rcver}.tar.xz

BuildRequires:	bzip2-devel, curl-devel >= 7.9, gmp-devel, httpd-devel >= 2.0.46-1, pam-devel, libstdc++-devel, openssl-devel, zlib-devel, pcre-devel >= 6.6, smtpdaemon, libedit-devel, bzip2, perl, libtool >= 1.4.3, gcc-c++, libtool-ltdl-devel
BuildRequires: MariaDB-devel >= 10.1
BuildRequires: MariaDB-client >= 10.1

%description
bla

%prep
%setup -q -n php-%{version}


%build
touch configure.in
./buildconf --force
%configure \
  --prefix=/usr \
  --mandir=/usr/share/man \ 
  --infodir=/usr/share/info \
  --disable-silent-rules \
  --libdir=/usr/lib/x86_64-linux-gnu \
  --libexecdir=/usr/lib/x86_64-linux-gnu \
  --disable-maintainer-mode \
  --disable-dependency-tracking \
  --enable-cli \
  --disable-cgi \
  --disable-phpdbg \
  --with-config-file-path=/etc/php/7.0/cli \
  --with-config-file-scan-dir=/etc/php/7.0/cli/conf.d \
  --build=x86_64-linux-gnu \
  --host=x86_64-linux-gnu \
  --config-cache \
  --cache-file=/build/php7.0-x25jsn/php7.0-7.0.13/config.cache \
  --libdir=${prefix}/lib/php \
  --libexecdir=${prefix}/lib/php \
  --datadir=${prefix}/share/php/7.0 \
  --program-suffix=7.0 \
  --sysconfdir=/etc \
  --localstatedir=/var \
  --mandir=/usr/share/man \
  --disable-all \
  --disable-debug \
  --disable-rpath \
  --disable-static \
  --with-pic \
  --with-layout=GNU \
  --without-pear \
  --enable-filter \
  --with-openssl=yes \
  --with-pcre-regex=/usr \
  --enable-hash \
  --with-mhash=/usr \
  --enable-libxml \
  --enable-session \
  --with-system-tzdata \
  --with-zlib=/usr \
  --with-zlib-dir=/usr \
  --enable-dtrace \
  --enable-pcntl \
  --with-libedit=shared,/usr\
  --with-mysqlnd=shared,/usr/bin/mysql_config \
  --enable-mysqlnd-threading \
  --with-mysqli=shared,/usr/bin/mysql_config

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}


%files
%doc



%changelog

