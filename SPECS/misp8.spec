%global __python %{__python3}
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global _python_bytecompile_extra 0
%global debug_package %{nil}
%define _build_id_links none
%define _binaries_in_noarch_packages_terminate_build 0
# disable mangling of shebangs #!
%define __brp_mangle_shebangs /usr/bin/true
# exclude for requirements
%global __requires_exclude ^/opt/python/cp3.*

%define pymispver 2.4.170
%define mispstixver 2.4.169

Name:	    	misp
Version:	2.4.170
release:	1%{?dist}
Summary:	MISP - malware information sharing platform

Group:		Internet Applications
License:	GPLv3
URL:		http://www.misp-project.org/
Source0:	fake-tgz.tgz
Source1:    	misp.conf
Source2:    	misp-httpd.pp
Source3:    	misp-bash.pp
Source4:    	misp-ps.pp
Source5:    	misp-workers.service
Source6:    	start-misp-workers.sh
Source7:	misp-workers.ini
Source8:	misp-workers8.pp
Patch0:     	MISP-AppModel.php.patch

BuildRequires:	/usr/bin/pathfix.py
BuildRequires:  git, python38-devel, python38-pip
BuildRequires:  libxslt-devel, zlib-devel
BuildRequires:  php74-php, php74-php-cli, php74-php-xml
BuildRequires:	php74-php-mbstring
BuildRequires:	ssdeep-devel
BuildRequires:	cmake3, bash-completion
Requires:	httpd, mod_ssl, redis, libxslt, zlib
Requires:	mariadb, mariadb-server
Requires:       php74-php, php74-php-cli, php74-php-gd, php74-php-pdo
Requires:	php74-php-mysqlnd, php74-php-mbstring, php74-php-xml
Requires:	php74-php-bcmath, php74-php-opcache, php74-php-json
Requires:	php74-php-pecl-zip, php74-php-pecl-redis5, php74-php-intl
Requires:	php74-php-pecl-gnupg, php74-php-pecl-ssdeep, php74-php-process
Requires:	php74-php-pecl-apcu, php74-php-brotli, php74-php-pecl-rdkafka
Requires:	php74-php-pecl-simdjson
Requires:	supervisor, faup, gtcaca

%package python-virtualenv
Summary: 	the python virtual environment for MISP
Group:		Internet Applications
License:	GPLv3

%description python-virtualenv
The python vitualenvironment for MISP

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

git submodule update --init --recursive
git submodule foreach --recursive git config core.filemode false
git config core.filemode false

# patch app/Model/Server.php to show commit ID
patch --ignore-whitespace -p0 < %{PATCH0}

# create python3 virtualenv
python3.8 -m venv --copies $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv

$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U pip setuptools

$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install ordered-set python-dateutil six weakrefmethod
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install $RPM_BUILD_ROOT/var/www/MISP/app/files/scripts/misp-stix

cd $RPM_BUILD_ROOT/var/www/MISP/app/files/scripts/python-cybox
git config core.filemode false
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install .

cd $RPM_BUILD_ROOT/var/www/MISP/app/files/scripts/python-stix
git config core.filemode false
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install .

cd $RPM_BUILD_ROOT/var/www/MISP/app/files/scripts/mixbox
git config core.filemode false
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install .

cd $RPM_BUILD_ROOT/var/www/MISP/app/files/scripts/cti-python-stix2
git config core.filemode false
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install .

cd $RPM_BUILD_ROOT/var/www/MISP/app/files/scripts/python-maec
git config core.filemode false
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install .

$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U zmq
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U redis
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U python-magic
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U plyara
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U pydeep
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U lief

cd $RPM_BUILD_ROOT/var/www/MISP/PyMISP
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U .

# CakePHP
cd $RPM_BUILD_ROOT/var/www/MISP/app
/opt/remi/php74/root/usr/bin/php composer.phar install --no-dev
/opt/remi/php74/root/usr/bin/php composer.phar require supervisorphp/supervisor:^4.0 guzzlehttp/guzzle php-http/message lstrojny/fxmlrpc

cd $RPM_BUILD_ROOT/var/www/MISP
# save commit ID of this installation
git rev-parse HEAD > .git_commit_version

# clean up before PATH rewriting
rm -rf $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/__pycache__

# rewrite PATH in virtualenv
sed -e "s/\/usr\/local\/bin\/python3.8/\/var\/www\/cgi-bin\/misp-virtualenv\/bin\/python3/g" -i $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/*
sed -e "s/\/builddir\/build\/BUILDROOT\/%{name}-%{version}-%{release}.%{_arch}//g" -i $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/*
sed -e "s/\/builddir\/build\/BUILDROOT\/%{name}-%{version}-%{release}.%{_arch}//g" -i $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/lib/python3.8/site-packages/pymisp-%{pymispver}.dist-info/direct_url.json
sed -e "s/\/builddir\/build\/BUILDROOT\/%{name}-%{version}-%{release}.%{_arch}//g" -i $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/lib/python3.8/site-packages/misp_stix-%{mispstixver}.dist-info/direct_url.json

# path fix for python3
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" . $RPM_BUILD_ROOT/var/www/MISP/*

# cleanup
rm -rf .git .github .gitchangelog.rc .gitignore .gitmodules .travis.yml
find . -name \.git | xargs -i rm -rf {}

mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/conf.d/
mkdir -p $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system
mkdir -p $RPM_BUILD_ROOT/usr/local/sbin
install -m 755 %{SOURCE6} $RPM_BUILD_ROOT/usr/local/sbin
chmod g+w $RPM_BUILD_ROOT/var/www/MISP/app/Config
mkdir -p $RPM_BUILD_ROOT/etc/supervisord.d
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT/etc/supervisord.d

%files python-virtualenv
%defattr(-,apache,apache,-)
/var/www/cgi-bin/misp-virtualenv
%exclude /var/www/cgi-bin/misp-virtualenv/*.pyc

%files
%defattr(-,apache,apache,-)
%config(noreplace) /var/www/MISP/app/Plugin/CakeResque/Config/config.php
/var/www/MISP
%config(noreplace) /etc/httpd/conf.d/misp.conf
%config(noreplace) /etc/supervisord.d/misp-workers.ini
/usr/share/MISP/policy/selinux/misp-*.pp
%{_sysconfdir}/systemd/system/misp-workers.service
%defattr(-,root,root,-)
/usr/local/sbin/start-misp-workers.sh
# exclude test files whicht get detected by AV solutions
%exclude /var/www/MISP/PyMISP/tests
%exclude /var/www/MISP/*.pyc

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
semodule -i /usr/share/MISP/policy/selinux/misp-workers8.pp

%changelog
* Fri Apr 14 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.170
- update to 2.4.170

* Wed Mar 15 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.169
- update to 2.4.169

* Wed Feb 15 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.168
- update to 2.4.168

* Fri Dec 30 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.167
- update to 2.4.167

* Mon Dec 05 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.166
- update to 2.4.166

* Mon Nov 14 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.165
- update to 2.4.165

* Wed Oct 19 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.164
- update to 2.4.164

* Fri Sep 30 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.163
- update to 2.4.163

* Fri Aug 19 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.161
- update to 2.4.161

* Mon Aug 08 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.160
- update to 2.4.160

* Tue May 31 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.159
- update to 2.4.159

* Tue Apr 26 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.158
- update to 2.4.158

* Fri Mar 25 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.157
- update to 2.4.157

* Sun Mar 20 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.156
- update to 2.4.156

* Thu Mar 10 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.155
- update to 2.4.155
- first version for RHEL8
