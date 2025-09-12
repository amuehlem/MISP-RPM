%global __python %{__python3}
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global _python_bytecompile_extra 0
%define _binaries_in_noarch_packages_terminate_build 0
# disable mangling of shebangs #!
%define __brp_mangle_shebangs /usr/bin/true
# exclude for requirements
%global __requires_exclude ^/opt/python/cp3.*

%define pymispver 2.4.198

Name:		misp
Version:	2.4.204
Release: 	1%{?dist}
Summary:	MISP - malware information sharing platform

Group:		Internet Applications
License:	GPLv3
URL:		http://www.misp-project.org/
Source0:	fake-tgz.tgz
Source1:        misp.conf
Source2:        misp-httpd.pp
Source3:        misp-bash.pp
Source4:        misp-ps.pp
Source5:        misp-workers.service
Source6:        start-misp-workers.sh
Source7:	misp-workers.ini
Patch0:         MISP-AppModel.php.patch

BuildRequires:	/usr/bin/pathfix.py
BuildRequires:	git, misp-python, libxslt-devel, zlib-devel
BuildRequires:	php74-php, php74-php-cli, php74-php-xml, php74-php-mbstring
BuildRequires:	ssdeep-devel, cmake3, bash-completion, gcc
BuildRequires:	libcaca-devel

Requires:	httpd, mod_ssl, redis, libxslt, zlib
Requires:	misp-python, misp-python-virtualenv = %{version}-%{release}
Requires:	php74-php, php74-php-cli, php74-php-gd, php74-php-pdo
Requires:	php74-php-mysqlnd, php74-php-mbstring, php74-php-xml
Requires:       php74-php-bcmath, php74-php-opcache, php74-php-json
Requires:       php74-php-pecl-zip, php74-php-pecl-redis5, php74-php-intl
Requires:       php74-php-pecl-gnupg, php74-php-pecl-ssdeep, php74-php-process
Requires:	php74-php-brotli, php74-php-pecl-rdkafka, php74-php-pecl-apcu
Requires:	php74-php-pecl-simdjson
Requires:	gtcaca, faup, supervisor

%package python-virtualenv
Summary:        the python virtual environment for MISP
Group:          Internet Applications
License:        GPLv3

%description python-virtualenv
The python vitualenvironment for MISP

%description
MISP - malware information sharing platform
The MISP threat sharing platform is a free and open source software 
helping information sharing of threat intelligence including cyber 
security indicators.

A threat intelligence platform for gathering, sharing, storing and 
correlating Indicators of Compromise of targeted attacks, threat 
intelligence, financial fraud information, vulnerability information or 
even counter-terrorism information. 

%prep
%setup -q -n fake-tgz

%build
# intentionally left blank

%install
mkdir -p $RPM_BUILD_ROOT/var/www
git clone https://github.com/MISP/MISP.git $RPM_BUILD_ROOT/var/www/MISP
cd $RPM_BUILD_ROOT/var/www/MISP
git checkout v%{version}
git submodule sync
git submodule update --init --recursive
git submodule foreach --recursive git config core.filemode false
git config core.filemode false

# patch app/Model/Server.php to show commit ID
patch --ignore-whitespace -p0 < %{PATCH0}

# create python3 virtualenv
/var/www/cgi-bin/misp-python/bin/python3 -m venv --copies $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv

mkdir -p $RPM_BUILD_ROOT/usr/share/httpd/.cache

$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U pip setuptools

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
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U pymisp==%{pymispver}
# fix openssl 1.1.1 issue
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install --force-reinstall -v "urllib3==1.26.14"


# CakePHP
cd $RPM_BUILD_ROOT/var/www/MISP/app
/opt/remi/php74/root/usr/bin/php composer.phar install
/opt/remi/php74/root/usr/bin/php composer.phar require --with-all-dependencies supervisorphp/supervisor:^4.0 guzzlehttp/guzzle php-http/message php-http/message-factory lstrojny/fxmlrpc jakub-onderka/openid-connect-php

cd $RPM_BUILD_ROOT/var/www/MISP
# save commit ID of this installation
git rev-parse HEAD > .git_commit_version

# clean up before PATH rewriting
rm -rf $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/__pycache__

# rewrite PATH in virtualenv
sed -e "s/\/usr\/local\/bin\/python3.9/\/var\/www\/cgi-bin\/misp-virtualenv\/bin\/python3/g" -i $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/*
sed -e "s|%{buildroot}||g" -i $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/*
sed -e "s|%{buildroot}||g" -i $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/lib/python3.9/site-packages/*/direct_url.json

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
%exclude %{_libdir}/debug
%exclude /usr/lib/debug/.build-id
%exclude /usr/lib/debug/var/www/MISP/PyMISP/tests/viper-test-files/test_files/tmux.debug
# exclude test files whicht get detected by AV solutions
%exclude /var/www/MISP/PyMISP/tests

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
systemctl restart supervisor

%changelog
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
- update to 2.4.174

* Fri Jul 21 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.173.1
- added missing php-http/message-factory to composer install command

* Tue Jul 11 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.173
- update to 2.4.173

* Thu Jun 15 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.172
- update to 2.4.172

* Tue Jun 06 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.171
- update to 2.4.171
- portability improvements recommended by Guillaume Rousse

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
- udpate to 2.4.157

* Sun Mar 20 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.156
- update to 2.4.156

* Fri Mar 4 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.155
- update to 2.4.155
- added requirement for misp-python, because of pymisp needing python >= 3.7

* Mon Feb 7 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.153
- update to 2.4.153
- added supervisor for background tasks
- added php-apcu and php-process as requirements
 
* Mon Jan 10 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.152
- new build to solve MISP issues #8057

* Mon Dec 27 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.152
- update to 2.4.152

* Thu Dec 02 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.151
- update to 2.4.151

* Thu Oct 14 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.150
- update to 2.4.150

* Mon Sep 13 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.148-2
- update to include some important patches

* Wed Aug 11 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.148
- update to 2.4.148

* Wed Jul 28 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.147
- update to 2.4.147

* Tue Jul 6 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.146
- update to 2.4.146

* Wed Jun 30 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.145
- update to 2.4.145

* Tue Jun 8 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.144
- update to 2.4.144

* Fri May 21 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.143
- update to 2.4.143

* Sat Apr 24 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.141
- new build process to put all python modules into a virtual environment
