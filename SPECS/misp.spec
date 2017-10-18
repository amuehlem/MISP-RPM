Name:	    misp
Version:	2.4.81
Release:	1%{?dist}
Summary:	MISP - malware information sharing platform

Group:		Internet Applications
License:	GPLv3
URL:		http://www.misp-project.org/
Source0:	fake-tgz.tgz
Source1:    misp.conf

BuildArch:      noarch
BuildRequires:  git, python-devel, python-pip, libxslt-devel, zlib-devel
BuildRequires:  php > 7.0
BuildRequires:  python-lxml, python-dateutil, python-six, curl
BuildRequires:  python-setuptools, wget
BuildRequires:  php-pear-Crypt_GPG
Requires:	    mariadb, mariadb-server, httpd, redis, libxslt, zlib
Requires:       php > 7.0
Requires:       python-lxml, python-dateutil, python-six
Requires:	    python-cybox, python-stix, php-redis
Requires:       php-pear-Crypt_GPG
Requires:       python-magic, python-pydeep, python-pymisp, python34-pymisp
Requires:       python-lief, python-mixbox

%description
MISP - malware information sharing platform & threat sharing

%prep
%setup -q -n fake-tgz

%build

%install
mkdir -p $RPM_BUILD_ROOT/var/www
git clone https://github.com/MISP/MISP.git $RPM_BUILD_ROOT/var/www/MISP
cd $RPM_BUILD_ROOT/var/www/MISP
git checkout tags/v%{version}
git config core.filemode false
git submodule init
git submodule update
wget https://getcomposer.org/download/1.2.1/composer.phar -O composer.phar
cd $RPM_BUILD_ROOT/var/www/MISP/app
php composer.phar require kamisama/cake-resque:4.1.2
php composer.phar config vendor-dir Vendor
php composer.phar install
mkdir -p $RPM_BUILD_ROOT/var/www/MISP/app/Plugin/CakeResque/Config
cp -fa $RPM_BUILD_ROOT/var/www/MISP/INSTALL/setup/config.php $RPM_BUILD_ROOT/var/www/MISP/app/Plugin/CakeResque/Config/config.php
mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/conf.d/

%files
%defattr(-,root,root,-)
#%config(noreplace) /etc/httpd/conf.d/misp.conf
%defattr(-,apache,apache,-)
/var/www/MISP
%config(noreplace) /var/www/MISP/app/Plugin/CakeResque/Config/config.php
%config(noreplace) /etc/httpd/conf.d/misp.conf
%post
setsebool -P httpd_can_network_connect 1
setsebool -P httpd_unified 1
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp'
restorecon -v '/var/www/MISP/app/tmp'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/'
restorecon -v '/var/www/MISP/app/tmp/'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/logs/'
restorecon -v '/var/www/MISP/app/tmp/logs/'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/cache'
restorecon -v '/var/www/MISP/app/tmp/cache'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/cache/'
restorecon -v '/var/www/MISP/app/tmp/cache/'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/cache/feeds'
restorecon -v '/var/www/MISP/app/tmp/cache/feeds'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/cache/models'
restorecon -v '/var/www/MISP/app/tmp/cache/models'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/cache/persistent'
restorecon -v '/var/www/MISP/app/tmp/cache/persistent'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/cache/views'
restorecon -v '/var/www/MISP/app/tmp/cache/views'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/Config/config.php'
restorecon -v '/var/www/MISP/app/Config/config.php'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/Lib/cakephp/lib/Cake/Config/config.php'
restorecon -v '/var/www/MISP/app/Lib/cakephp/lib/Cake/Config/config.php'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/Plugin/CakeResque/Config/config.default.php'
restorecon -v '/var/www/MISP/app/Plugin/CakeResque/Config/config.php'

%changelog
* Wed Oct 17 2917 Andreas Muehlemann <andreas.muelemann@switch.ch>
- fixes and optimizations after install tests

* Thu Dec 29 2016 Andreas Muehlemann <andreas.muehlemann@switch.ch>
- adapted to use the php-pear RPMs

* Wed Nov 09 2016 Andreas Muehlemann <andreas.muehlemann@switch.ch>
- first version for centos
