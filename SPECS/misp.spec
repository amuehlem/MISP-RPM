%global __python %{__python3}

Name:	    misp
Version:	2.4.108
release:	1%{?dist}
Summary:	MISP - malware information sharing platform

Group:		Internet Applications
License:	GPLv3
URL:		http://www.misp-project.org/
Source0:	fake-tgz.tgz
Source1:    misp.conf
Source2:    misp-httpd.pp
Source3:    misp-bash.pp
Source4:    misp-ps.pp
Source5:    misp-workers.service
Source6:    start-misp-workers.sh
Patch0:     MISP-Server.php.patch

BuildArch:      noarch
BuildRequires:  git, python36-devel, python36-pip, libxslt-devel, zlib-devel
BuildRequires:  php > 7.0
BuildRequires:  python36-lxml, python36-python_dateutil, python36-six, curl
BuildRequires:  python36-setuptools, wget
BuildRequires:  php-pear-Crypt_GPG
Requires:	    httpd, redis, libxslt, zlib
Requires:       php > 7.0, php-gd > 7.0
Requires:       python36-lxml, python36-python_dateutil, python36-six
Requires:	    python36-cybox, python36-stix, php-redis
Requires:       php-pear-Crypt_GPG, php-zmq, python36-pyzmq
Requires:       python36-python_magic, python36-pydeep, python36-pymisp
Requires:       python36-cybox, python36-stix, python36-mixbox, python36-maec
Requires:       lief-python, python36-mixbox, policycoreutils-python
Requires:       python36-stix2, python36-plyara

%description
MISP - malware information sharing platform & threat sharing

%prep
%setup -q -n fake-tgz

%build
# intentionally left blank

%install

mkdir -p $RPM_BUILD_ROOT/var/www
git clone https://github.com/MISP/MISP.git $RPM_BUILD_ROOT/var/www/MISP
cd $RPM_BUILD_ROOT/var/www/MISP
#git checkout tags/v%{version}

git submodule update --init --recursive
git submodule foreach --recursive git config core.filemode false
git config core.filemode false

# patch app/Model/Server.php to show commit ID
patch --ignore-whitespace -p0 < %{PATCH0}

# copy pear data to accessible directory for build process
mkdir -p $RPM_BUILD_ROOT/usr/share/pear
cp -r /usr/share/pear/* $RPM_BUILD_ROOT/usr/share/pear/

#pear -D php_dir= $RPM_BUILD_ROOT/usr/share/pear channel-update pear.php.net
#pear -D php_dir= $RPM_BUILD_ROOT/usr/share/pear install INSTALL/dependencies/Console_CommandLine/package.xml
#pear -D php_dir= $RPM_BUILD_ROOT/usr/share/pear install INSTALL/dependencies/Crypt_GPG/package.xml

cd $RPM_BUILD_ROOT/var/www/MISP/app
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php -r "if (hash_file('SHA384', 'composer-setup.php') === '48e3236262b34d30969dca3c37281b3b4bbe3221bda826ac6a9a62d6444cdb0dcd0615698a5cbe587c3f0fe57a54d8f5') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"
php composer-setup.php
php -r "unlink('composer-setup.php');"
php composer.phar require kamisama/cake-resque:4.1.2
php composer.phar config vendor-dir Vendor
php composer.phar install

mkdir -p $RPM_BUILD_ROOT/var/www/MISP/app/Plugin/CakeResque/Config
cp -fa $RPM_BUILD_ROOT/var/www/MISP/INSTALL/setup/config.php $RPM_BUILD_ROOT/var/www/MISP/app/Plugin/CakeResque/Config/config.php
cd $RPM_BUILD_ROOT/var/www/MISP

# save commit ID of this installation
git rev-parse HEAD > .git_commit_version
# cleanup
rm -rf .git .github .gitchangelog.rc .gitignore .gitmodules .travis.yml
find . -name \.git | xargs -i rm -rf {}

mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/conf.d/
mkdir -p $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system
mkdir -p $RPM_BUILD_ROOT/usr/local/sbin
install -m 755 %{SOURCE6} $RPM_BUILD_ROOT/usr/local/sbin
chmod g+w $RPM_BUILD_ROOT/var/www/MISP/app/Config

%files
%defattr(-,apache,apache,-)
%config(noreplace) /var/www/MISP/app/Plugin/CakeResque/Config/config.php
/var/www/MISP
%config(noreplace) /etc/httpd/conf.d/misp.conf
/usr/share/MISP/policy/selinux/misp-*.pp
%{_sysconfdir}/systemd/system/misp-workers.service
%defattr(-,root,root,-)
/usr/local/sbin/start-misp-workers.sh
%exclude /usr/share/pear

%post
chcon -t httpd_sys_rw_content_t /var/www/MISP/app/files
chcon -t httpd_sys_rw_content_t /var/www/MISP/app/files/terms
chcon -t httpd_sys_rw_content_t /var/www/MISP/app/files/scripts/tmp
chcon -t httpd_sys_rw_content_t /var/www/MISP/app/Plugin/CakeResque/tmp
chcon -R -t httpd_sys_rw_content_t /var/www/MISP/app/tmp
chcon -R -t httpd_sys_rw_content_t /var/www/MISP/app/webroot/img/orgs
chcon -R -t httpd_sys_rw_content_t /var/www/MISP/app/webroot/img/custom
setsebool -P httpd_can_network_connect 1
setsebool -P httpd_unified 1
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/'
restorecon -v '/var/www/MISP/app/tmp/'
semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/logs/'
restorecon -v '/var/www/MISP/app/tmp/logs/'
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
semodule -i /usr/share/MISP/policy/selinux/misp-httpd.pp
semodule -i /usr/share/MISP/policy/selinux/misp-bash.pp
semodule -i /usr/share/MISP/policy/selinux/misp-ps.pp

%changelog
* Wed Jun 12 2019 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.108
- update to 2.4.108

* Mon May 13 2019 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.107
- update to 2.4.107

* Tue May 7 2019 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.106-2
- updated install routines

* Thu May 2 2019 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.106
- update to 2.4.106

* Wed Jun 27 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.93
- update to 2.4.93

* Mon May 7 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.90
- added policycoreutils-python as requirement

* Sat Mar 3 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.88-4
- updated to MISP version 2.4.88
- added systemctl unit for misp-workers

* Tue Jan 16 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.8.86
- updated to MISP version 2.4.86

* Thu Jan 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.85
- updated to MISP version 2.4.85
- added misp-*.pp selinux policies

* Tue Oct 17 2017 Andreas Muehlemann <andreas.muelemann@switch.ch>
- fixes and optimizations after install tests

* Thu Dec 29 2016 Andreas Muehlemann <andreas.muehlemann@switch.ch>
- adapted to use the php-pear RPMs

* Wed Nov 09 2016 Andreas Muehlemann <andreas.muehlemann@switch.ch>
- first version for centos
