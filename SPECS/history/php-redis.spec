%global php_inidir  %{_sysconfdir}/php.d
%global pecl_name   redis
%global pecl_xmldir /var/lib/pear/pkgxml
%global php_extdir %(php-config --extension-dir 2>/dev/null || echo "undefined")

Name:       php-redis
Version:    4.3.0
Release:    1%{?dist}
Summary:    PHP extension for interfacing redis

Group:      Development/Languages
License:    PHP
URL:        https://github.com/phpredis/phpredis/
Source0:    https://pecl.php.net/get/redis-%{version}.tgz

BuildRequires:  php, redis, autoconf
Requires:       php > 7.0 , redis

%description
PHP extension for interfacing redis

%prep
%setup -q -n redis-%{version}

# create the ini file
cat > %{pecl_name}.ini << EOF
extension=%{pecl_name}.so
EOF

%build
phpize
%configure \
    --enable-redis \
    --enable-redis-session \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%install
make install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}%{php_inidir}/%{pecl_name}.ini
install -D -m 644 ../package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%files
%{pecl_xmldir}/%{name}.xml
%{php_extdir}/%{pecl_name}.so
%config(noreplace) %{php_inidir}/%{pecl_name}.ini

%changelog
* Wed Jun 12 2019 Andreas Muehlemann  <andreas.muehlemann@switch.ch> - 4.3.0
- upgrade to php-redis 4.3.0

* Tue Aug 7 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 3.1.0
- testing with php 7.2

* Fri Dec 30 2016 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 3.1.0
- first version
