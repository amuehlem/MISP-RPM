%global __python %{__python3}
%global _python_bytecompile_extra 0
%global debug_package %{nil}
%define _build_id_links none
%define _binaries_in_noarch_packages_terminate_build 0
# disable mangling of shebangs #!
%define __brp_mangle_shebangs /usr/bin/true
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

# exclude for requirements
%global __requires_exclude ^/opt/python/cp3.*

%define pymispver 2.4.198
%define mispstixver 2025.02.14
%define pythonver python3.9
%define pythonver_short python39

Name:	    	misp
Version:	2.4.210
release:	2%{?dist}
Summary:	MISP - malware information sharing platform

Group:		Internet Applications
License:	GPLv3
URL:		http://www.misp-project.org/
Source1:    	misp.conf
Source2:    	misp-httpd.pp
Source3:    	misp-bash.pp
Source4:    	misp-ps.pp
Source5:    	misp-workers.service
Source6:    	start-misp-workers.sh
Source7:	misp-workers.ini
Source8:	misp-workers8.pp
Source9:	misp-worker-status-supervisord.pp
Patch0:     	MISP-AppModel.php.patch
Patch1:		pymisp.patch

BuildRequires:	/usr/bin/pathfix.py
BuildRequires:  git, python3-devel, python3-pip
BuildRequires:  libxslt-devel, zlib-devel
BuildRequires:  php74-php, php74-php-cli, php74-php-xml
BuildRequires:	php74-php-mbstring
BuildRequires:	ssdeep-devel
BuildRequires:	cmake3, bash-completion
Requires:	httpd, mod_ssl, redis, libxslt, zlib
Requires:       php74-php, php74-php-cli, php74-php-gd, php74-php-pdo
Requires:       php74-php-mysqlnd, php74-php-mbstring, php74-php-xml
Requires:	php74-php-bcmath, php74-php-opcache, php74-php-json
Requires:	php74-php-pecl-zip, php74-php-pecl-redis6, php74-php-intl
Requires:	php74-php-pecl-gnupg, php74-php-pecl-ssdeep, php74-php-process
Requires:	php74-php-pecl-apcu, php74-php-brotli, php74-php-pecl-rdkafka
Requires:	php74-php-pecl-simdjson, php74-php-fpm
Requires:	supervisor, faup, gtcaca
Requires:	misp-python-virtualenv = %{version}-%{release}

%package python-virtualenv
Summary: 	the python virtual environment for MISP
Group:		Internet Applications
License:	GPLv3

%description python-virtualenv
The python vitualenvironment for MISP

%description
MISP - malware information sharing platform & threat sharing

%prep
%setup -q -T -c

git clone https://github.com/MISP/MISP.git
cd MISP
git checkout v%{version}
git submodule update --init --recursive
git submodule foreach --recursive git config core.filemode false
git config core.filemode false

# patch app/Model/Server.php to show commit ID
patch --ignore-whitespace -p0 < %{PATCH0}


%build
# intentionally left blank
%install
mkdir -p $RPM_BUILD_ROOT/var/www
cp -r MISP $RPM_BUILD_ROOT/var/www/MISP

# create initial configuartion files
cd  $RPM_BUILD_ROOT/var/www/MISP/app/Config
cp bootstrap.default.php bootstrap.php
cp config.default.php config.php
cp core.default.php core.php
cp database.default.php database.php

# create python3 virtualenv
python3 -m venv --copies $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv

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
git clone https://github.com/MISP/PyMISP.git
cd $RPM_BUILD_ROOT/var/www/MISP/PyMISP/PyMISP
git checkout v%{pymispver}
git submodule update --init
#patch -p1 < %{PATCH1}
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U .
#$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U pymisp==%{pymispver}

# CakePHP
cd $RPM_BUILD_ROOT/var/www/MISP/app
/opt/remi/php74/root/usr/bin/php composer.phar install --no-dev
/opt/remi/php74/root/usr/bin/php composer.phar require --with-all-dependencies supervisorphp/supervisor:^4.0 guzzlehttp/guzzle php-http/message php-http/message-factory lstrojny/fxmlrpc

cd $RPM_BUILD_ROOT/var/www/MISP
# save commit ID of this installation
git rev-parse HEAD > .git_commit_version

# clean up before PATH rewriting
rm -rf $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/__pycache__

# rewrite PATH in virtualenv
sed -e "s|%{buildroot}||g" -i $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/*
sed -e "s|%{buildroot}||g" -i $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/lib/%{pythonver}/site-packages/*/direct_url.json

# path fix for python3
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" . $RPM_BUILD_ROOT/var/www/MISP/*

# cleanup
rm -rf .git .github .gitchangelog.rc .gitignore .gitmodules .travis.yml
find . -name \.git | xargs -i rm -rf {}

# delete files not needed at runtime under web root
pushd $RPM_BUILD_ROOT/var/www/MISP
# developement
rm -rf build
rm -f build-deb.sh
rm -f requirements.txt
rm -f app/composer.*
rm -f app/Makefile
rm -f app/update_thirdparty.sh

# documentation
rm -f AUTHORS
rm -f CITATION.cff
rm -f code_of_conduct.md
rm -f CODINGSTYLE.md
rm -f CONTRIBUTING.md
rm -f GITWORKFLOW.md
rm -f LICENSE
rm -f README.debian
rm -f README.md
rm -f ROADMAP.md
rm -f SECURITY.md
popd

mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/conf.d/
mkdir -p $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
install -m 644 %{SOURCE9} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
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
%defattr(-,root,root,-)
%doc MISP/{AUTHORS,CITATION.cff,code_of_conduct.md,CODINGSTYLE.md,CONTRIBUTING.md,GITWORKFLOW.md,README.md,ROADMAP.md,SECURITY.md}
%license MISP/LICENSE
/var/www/MISP
# configuration directory: read or read/write permission, through group ownership
%dir %attr(0775,root,apache) /var/www/MISP/app/Config
%config(noreplace) %attr(0640,root,apache) /var/www/MISP/app/Config/bootstrap.php
%config(noreplace) %attr(0660,root,apache) /var/www/MISP/app/Config/config.php
%config(noreplace) %attr(0640,root,apache) /var/www/MISP/app/Config/core.php
%config(noreplace) %attr(0640,root,apache) /var/www/MISP/app/Config/database.php
%config(noreplace) %attr(0640,root,apache) /var/www/MISP/app/Config/email.php
%config(noreplace) %attr(0640,root,apache) /var/www/MISP/app/Config/routes.php
%config(noreplace) /var/www/MISP/app/Plugin/CakeResque/Config/config.php
# data directories: full read/write access, through user ownership
%attr(-,apache,apache) /var/www/MISP/app/tmp
%attr(-,apache,apache) /var/www/MISP/app/files
%attr(-,apache,apache) /var/www/MISP/app/Plugin/CakeResque/tmp
%config(noreplace) /etc/httpd/conf.d/misp.conf
%config(noreplace) /etc/supervisord.d/misp-workers.ini
/usr/share/MISP/policy/selinux/misp-*.pp
%{_sysconfdir}/systemd/system/misp-workers.service
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
semodule -i /usr/share/MISP/policy/selinux/misp-worker-status-supervisord.pp

%changelog
* Wed May 14 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.210
- update to 2.4.210

* Wed Mar 26 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.207
- update to 2.4.207

* Tue Mar 25 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.206
- update to 2.4.206

* Mon Feb 24 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.205
- update to 2.4.205

* Fri Jan 17 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.204
- update to 2.4.204

* Fri Jan 17 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.203
- update to 2.4.203

* Mon Jan 6 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.202
- update to 2.4.202

* Tue Dec 17 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.201
- update to 2.4.201

* Fri Nov 22 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.200
- update to 2.4.200

* Mon Oct 21 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.199
- added new selinux policy for misp-worker-status-supervisord
- update to 2.4.199

* Wed Sep 18 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.198
- update to 2.4.198

* Tue Sep 3 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.197
- update to 2.4.197

* Thu Aug 22 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.196
- update to 2.4.196

* Fri Aug 9 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.195
- update to 2.4.195

* Thu Jun 27 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.194
- update to 2.4.194

* Mon Jun 10 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.193
- update to 2.4.193
- removing MariaDB-Server as dependency

* Mon May 6 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.192
- update to 2.4.192

* Mon Apr 22 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.191
- update to 2.4.191

* Fri Apr 12 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.289
- update to 2.4.189

* Thu Mar 28 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.188
- update to 2.4.188

* Mon Mar 11 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.187
- update to 2.4.187

* Fri Feb 23 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.185
- update to 2.4.185

* Thu Feb 8 2024 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.184
- update to 2.4.184

* Thu Jan 18 2024 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.183
- update to 2.4.183

* Tue Dec 19 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.182
- update to 2.4.182

* Mon Nov 27 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.179
- update to 2.4.179

* Fri Nov 03 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.178
- update to 2.4.178

* Mon Oct 09 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.177
- update to 2.4.177

* Thu Sep 21 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.176
- update to 2.4.176

* Wed Aug 30 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.175
- update to 2.4.175

* Wed Aug 16 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.174
- First version for RHEL9
