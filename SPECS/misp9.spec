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

%define pymispver 2.5.17
%define mispstixver 2025.8.4
%define pythonver python3.9
%define pythonver_short python39
%define python_bin python3
%define phpbasever php83

%define noarch_install_dir %{_datadir}/misp
%define arch_install_dir %{_libdir}/misp

Name:	    	misp
Version:	2.5.17
release:	1%{?dist}
Summary:	MISP - malware information sharing platform

Group:		Internet Applications
License:	GPLv3
URL:		http://www.misp-project.org/
Source2:    	misp-httpd.pp
Source3:    	misp-bash.pp
Source4:    	misp-ps.pp
Source8:	misp-workers8.pp
Source9:	misp-worker-status-supervisord.pp
Patch0:     	MISP-AppModel.php.patch
Patch1:     	misp-2.4.177-fix-composer-config.patch

BuildRequires:	/usr/bin/pathfix.py
BuildRequires:  git, python3-devel, python3-pip
BuildRequires:  libxslt-devel, zlib-devel
BuildRequires:  %{phpbasever}-php, %{phpbasever}-php-cli, %{phpbasever}-php-xml
BuildRequires:	%{phpbasever}-php-mbstring
BuildRequires:	ssdeep-devel
BuildRequires:	cmake3, bash-completion, gcc
Requires:	httpd, mod_ssl, redis, libxslt, zlib
# requires either mod_php or php-fpm
Requires:       (%{phpbasever}-php or %{phpbasever}-php-fpm)
Requires:       %{phpbasever}-php-cli, %{phpbasever}-php-gd, %{phpbasever}-php-pdo
Requires:       %{phpbasever}-php-mysqlnd, %{phpbasever}-php-mbstring, %{phpbasever}-php-xml
Requires:	%{phpbasever}-php-bcmath, %{phpbasever}-php-opcache, %{phpbasever}-php-json
Requires:	%{phpbasever}-php-pecl-zip, %{phpbasever}-php-pecl-redis6, %{phpbasever}-php-intl
Requires:	%{phpbasever}-php-pecl-gnupg, %{phpbasever}-php-pecl-ssdeep, %{phpbasever}-php-process
Requires:	%{phpbasever}-php-pecl-apcu, %{phpbasever}-php-brotli, %{phpbasever}-php-pecl-rdkafka
Requires:	%{phpbasever}-php-pecl-simdjson
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
# patch app/composer.json to avoid user interaction during build
patch --ignore-whitespace -p0 < %{PATCH1}


%build
# intentionally left blank
%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}
cp -r MISP $RPM_BUILD_ROOT%{noarch_install_dir}

# FHS compliance:
# move configuration files under %{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
mv $RPM_BUILD_ROOT%{noarch_install_dir}/app/Config $RPM_BUILD_ROOT%{_sysconfdir}/misp

# move log files under %{_localstatedir}/log
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/log
mv $RPM_BUILD_ROOT%{noarch_install_dir}/app/tmp/logs $RPM_BUILD_ROOT%{_localstatedir}/log/misp
rm -f $RPM_BUILD_ROOT%{_localstatedir}/log/misp/empty

# move other variable files under %{_sharedstatedir}
mkdir -p $RPM_BUILD_ROOT%{_sharedstatedir}/misp
mv $RPM_BUILD_ROOT%{noarch_install_dir}/app/tmp/cache $RPM_BUILD_ROOT%{_sharedstatedir}/misp/cache
mv $RPM_BUILD_ROOT%{noarch_install_dir}/app/tmp/cached_exports $RPM_BUILD_ROOT%{_sharedstatedir}/misp/cached_exports
mv $RPM_BUILD_ROOT%{noarch_install_dir}/app/tmp/files $RPM_BUILD_ROOT%{_sharedstatedir}/misp/files
mv $RPM_BUILD_ROOT%{noarch_install_dir}/app/tmp/sessions $RPM_BUILD_ROOT%{_sharedstatedir}/misp/sessions
mv $RPM_BUILD_ROOT%{noarch_install_dir}/app/tmp/yara $RPM_BUILD_ROOT%{_sharedstatedir}/misp/yara

# emulate original setup through symlinks
pushd $RPM_BUILD_ROOT%{noarch_install_dir}/app
ln -s ../../../..%{_sysconfdir}/misp Config
ln -s ../../../..%{_localstatedir}/log/misp tmp/logs
ln -s ../../../..%{_sharedstatedir}/misp/cache tmp/cache
ln -s ../../../..%{_sharedstatedir}/misp/cached_exports tmp/cached_exports
ln -s ../../../..%{_sharedstatedir}/misp/files tmp/files
ln -s ../../../..%{_sharedstatedir}/misp/sessions tmp/sessions
ln -s ../../../..%{_sharedstatedir}/misp/yara tmp/yara
popd

# create initial configuration files
pushd $RPM_BUILD_ROOT%{_sysconfdir}/misp
cp bootstrap.default.php bootstrap.php
cp config.default.php config.php
cp core.default.php core.php
cp database.default.php database.php
popd

# create python3 virtualenv
mkdir -p $RPM_BUILD_ROOT%{_libdir}
%{python_bin} -m venv --copies $RPM_BUILD_ROOT%{arch_install_dir}

$RPM_BUILD_ROOT%{arch_install_dir}/bin/pip install -U pip setuptools

$RPM_BUILD_ROOT%{arch_install_dir}/bin/pip install ordered-set python-dateutil six weakrefmethod
$RPM_BUILD_ROOT%{arch_install_dir}/bin/pip install $RPM_BUILD_ROOT%{noarch_install_dir}/app/files/scripts/misp-stix

cd $RPM_BUILD_ROOT%{noarch_install_dir}/app/files/scripts/python-cybox
git config core.filemode false
$RPM_BUILD_ROOT%{arch_install_dir}/bin/pip install .

cd $RPM_BUILD_ROOT%{noarch_install_dir}/app/files/scripts/python-stix
git config core.filemode false
$RPM_BUILD_ROOT%{arch_install_dir}/bin/pip install .

cd $RPM_BUILD_ROOT%{noarch_install_dir}/app/files/scripts/mixbox
git config core.filemode false
$RPM_BUILD_ROOT%{arch_install_dir}/bin/pip install .

cd $RPM_BUILD_ROOT%{noarch_install_dir}/app/files/scripts/cti-python-stix2
git config core.filemode false
$RPM_BUILD_ROOT%{arch_install_dir}/bin/pip install .

cd $RPM_BUILD_ROOT%{noarch_install_dir}/app/files/scripts/python-maec
git config core.filemode false
$RPM_BUILD_ROOT%{arch_install_dir}/bin/pip install .

$RPM_BUILD_ROOT%{arch_install_dir}/bin/pip install -U zmq
$RPM_BUILD_ROOT%{arch_install_dir}/bin/pip install -U redis
$RPM_BUILD_ROOT%{arch_install_dir}/bin/pip install -U python-magic
$RPM_BUILD_ROOT%{arch_install_dir}/bin/pip install -U plyara
$RPM_BUILD_ROOT%{arch_install_dir}/bin/pip install -U pydeep
$RPM_BUILD_ROOT%{arch_install_dir}/bin/pip install -U lief

cd $RPM_BUILD_ROOT%{noarch_install_dir}/PyMISP
$RPM_BUILD_ROOT%{arch_install_dir}/bin/pip install -U .

# CakePHP
cd $RPM_BUILD_ROOT%{noarch_install_dir}/app
/opt/remi/%{phpbasever}/root/usr/bin/php composer.phar install --no-dev
/opt/remi/%{phpbasever}/root/usr/bin/php composer.phar require --with-all-dependencies supervisorphp/supervisor:^4.0 guzzlehttp/guzzle php-http/message php-http/message-factory lstrojny/fxmlrpc jakub-onderka/openid-connect-php

cd $RPM_BUILD_ROOT%{noarch_install_dir}
# save commit ID of this installation
git rev-parse HEAD > .git_commit_version

# clean up before PATH rewriting
rm -rf $RPM_BUILD_ROOT%{arch_install_dir}/bin/__pycache__

# rewrite PATH in virtualenv
sed -e "s|%{buildroot}||g" -i $RPM_BUILD_ROOT%{arch_install_dir}/bin/*
sed -e "s|%{buildroot}||g" -i $RPM_BUILD_ROOT%{arch_install_dir}/lib/%{pythonver}/site-packages/*/direct_url.json

# path fix for python3
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" . $RPM_BUILD_ROOT%{noarch_install_dir}/*

# cleanup
rm -rf .git .github .gitchangelog.rc .gitignore .gitmodules .travis.yml
find . -name \.git | xargs -i rm -rf {}

# delete files not needed at runtime under web root
pushd $RPM_BUILD_ROOT%{noarch_install_dir}
# developement
rm -f .coveragerc
rm -rf build
rm -f build-deb.sh
rm -rf debian
rm -rf misp-vagrant
rm -f Pipfile
rm -rf travis
rm -rf tests
rm -f requirements.txt
#rm -f app/composer.*
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

# useless installation files, excepted mysql schema
rm -rf INSTALL
mkdir INSTALL
cp $RPM_BUILD_DIR/%{name}-%{version}/MISP/INSTALL/MYSQL.sql INSTALL
popd

mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d
cat > $RPM_BUILD_ROOT/etc/httpd/conf.d/misp.conf <<EOF
<VirtualHost *:80>

    Alias /misp %{noarch_install_dir}/app/webroot

    <Directory %{noarch_install_dir}/app/webroot>
        Options -Indexes
        AllowOverride all
        Order allow,deny
        allow from all
    </Directory>

    ErrorLog /var/log/httpd/misp.error.log
    CustomLog /var/log/httpd/misp.access.log combined

</VirtualHost>
EOF
mkdir -p $RPM_BUILD_ROOT%{noarch_install_dir}/policy/selinux
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{noarch_install_dir}/policy/selinux/
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{noarch_install_dir}/policy/selinux/
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{noarch_install_dir}/policy/selinux/
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{noarch_install_dir}/policy/selinux/
install -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{noarch_install_dir}/policy/selinux/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system
cat > $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/misp-workers.service <<EOF
[Unit]
Description=MISP workers
After=network.target remote-fs.target nss-lookup.target httpd.service mariadb.service redis.service

[Service]
Type=forking
ExecStart=%{noarch_install_dir}/app/Console/worker/start.sh
User=apache
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

mkdir -p $RPM_BUILD_ROOT/usr/local/sbin
cat > $RPM_BUILD_ROOT/usr/local/sbin/start-misp-workers.sh <<EOF
#!/bin/bash

su -s /bin/bash apache -c '%{noarch_install_dir}/app/Console/worker/start.sh'
EOF
chmod 755 $RPM_BUILD_ROOT/usr/local/sbin/start-misp-workers.sh

chmod g+w $RPM_BUILD_ROOT%{_sysconfdir}/misp

mkdir -p $RPM_BUILD_ROOT/etc/supervisord.d
cat > $RPM_BUILD_ROOT/etc/supervisord.d/misp-workers.ini <<EOF
[group:misp-workers]
programs=default,email,cache,prio,update

[program:default]
directory=%{noarch_install_dir}
command=%{noarch_install_dir}/app/Console/cake start_worker default
process_name=%(program_name)s_%(process_num)02d
numprocs=5
autostart=true
autorestart=true
redirect_stderr=false
stderr_logfile=%{_localstatedir}/log/misp/misp-workers-errors.log
stdout_logfile=%{_localstatedir}/log/misp/misp-workers.log
directory=%{noarch_install_dir}
user=apache

[program:prio]
directory=%{noarch_install_dir}
command=%{noarch_install_dir}/app/Console/cake start_worker prio
process_name=%(program_name)s_%(process_num)02d
numprocs=5
autostart=true
autorestart=true
redirect_stderr=false
stderr_logfile=%{_localstatedir}/log/misp/misp-workers-errors.log
stdout_logfile=%{_localstatedir}/log/misp/misp-workers.log
directory=%{noarch_install_dir}
user=apache

[program:email]
directory=%{noarch_install_dir}
command=%{noarch_install_dir}/app/Console/cake start_worker email
process_name=%(program_name)s_%(process_num)02d
numprocs=5
autostart=true
autorestart=true
redirect_stderr=false
stderr_logfile=%{_localstatedir}/log/misp/misp-workers-errors.log
stdout_logfile=%{_localstatedir}/log/misp/misp-workers.log
directory=%{noarch_install_dir}
user=apache

[program:update]
directory=%{noarch_install_dir}
command=%{noarch_install_dir}/app/Console/cake start_worker update
process_name=%(program_name)s_%(process_num)02d
numprocs=1
autostart=true
autorestart=true
redirect_stderr=false
stderr_logfile=%{_localstatedir}/log/misp/misp-workers-errors.log
stdout_logfile=%{_localstatedir}/log/misp/misp-workers.log
directory=%{noarch_install_dir}
user=apache

[program:cache]
directory=%{noarch_install_dir}
command=%{noarch_install_dir}/app/Console/cake start_worker cache
process_name=%(program_name)s_%(process_num)02d
numprocs=5
autostart=true
autorestart=true
redirect_stderr=false
stderr_logfile=%{_localstatedir}/log/misp/misp-workers-errors.log
stdout_logfile=%{_localstatedir}/log/misp/misp-workers.log
user=apache
EOF

%files python-virtualenv
%defattr(-,apache,apache,-)
%{arch_install_dir}
%exclude %{arch_install_dir}/*.pyc

%files
%defattr(-,root,root,-)
%doc MISP/{AUTHORS,CITATION.cff,code_of_conduct.md,CODINGSTYLE.md,CONTRIBUTING.md,GITWORKFLOW.md,README.md,ROADMAP.md,SECURITY.md}
%license MISP/LICENSE
%{noarch_install_dir}
# configuration directory: read or read/write permission, through group ownership
%dir %attr(0775,root,apache) %{_sysconfdir}/misp
%config(noreplace) %attr(0640,root,apache) %{_sysconfdir}/misp/bootstrap.php
%config(noreplace) %attr(0660,root,apache) %{_sysconfdir}/misp/config.php
%config(noreplace) %attr(0640,root,apache) %{_sysconfdir}/misp/core.php
%config(noreplace) %attr(0640,root,apache) %{_sysconfdir}/misp/database.php
%config(noreplace) %attr(0640,root,apache) %{_sysconfdir}/misp/email.php
%config(noreplace) %attr(0640,root,apache) %{_sysconfdir}/misp/routes.php
%config(noreplace) %{noarch_install_dir}/app/Plugin/CakeResque/Config/config.php
%{_sysconfdir}/misp/bootstrap.default.php
%{_sysconfdir}/misp/config.default.php
%{_sysconfdir}/misp/core.default.php
%{_sysconfdir}/misp/database.default.php
# data directories: full read/write access, through user ownership
%attr(-,apache,apache) %{_sharedstatedir}/misp
%attr(-,apache,apache) %{_localstatedir}/log/misp
%attr(-,apache,apache) %{noarch_install_dir}/app/Plugin/CakeResque/tmp
%config(noreplace) /etc/httpd/conf.d/misp.conf
%config(noreplace) /etc/supervisord.d/misp-workers.ini
%{_sysconfdir}/systemd/system/misp-workers.service
/usr/local/sbin/start-misp-workers.sh
# exclude test files whicht get detected by AV solutions
%exclude %{noarch_install_dir}/PyMISP/tests
%exclude %{noarch_install_dir}/*.pyc

%post
chcon -t httpd_sys_rw_content_t %{noarch_install_dir}/app/files
chcon -t httpd_sys_rw_content_t %{noarch_install_dir}/app/files/terms
chcon -t httpd_sys_rw_content_t %{noarch_install_dir}/app/files/scripts/tmp
chcon -t httpd_sys_rw_content_t %{noarch_install_dir}/app/Plugin/CakeResque/tmp
chcon -R -t httpd_sys_rw_content_t %{_sharedstatedir}/misp
chcon -R -t httpd_sys_rw_content_t %{noarch_install_dir}/app/webroot/img/orgs
chcon -R -t httpd_sys_rw_content_t %{noarch_install_dir}/app/webroot/img/custom
setsebool -P httpd_can_network_connect 1
setsebool -P httpd_unified 1
semanage fcontext -a -t httpd_sys_rw_content_t '%{_sharedstatedir}/misp/'
restorecon -v '%{_sharedstatedir}/misp/'
semanage fcontext -a -t httpd_sys_rw_content_t '%{_sharedstatedir}/misp/cache/'
restorecon -v '%{_sharedstatedir}/misp/cache/'
semanage fcontext -a -t httpd_sys_rw_content_t '%{_sharedstatedir}/misp/cache/feeds'
restorecon -v '%{_sharedstatedir}/misp/cache/feeds'
semanage fcontext -a -t httpd_sys_rw_content_t '%{_sharedstatedir}/misp/cache/models'
restorecon -v '%{_sharedstatedir}/misp/cache/models'
semanage fcontext -a -t httpd_sys_rw_content_t '%{_sharedstatedir}/misp/cache/persistent'
restorecon -v '%{_sharedstatedir}/misp/cache/persistent'
semanage fcontext -a -t httpd_sys_rw_content_t '%{_sharedstatedir}/misp/cache/views'
restorecon -v '%{_sharedstatedir}/misp/cache/views'
semanage fcontext -a -t httpd_sys_rw_content_t '%{_localstatedir}/log/misp/'
restorecon -v '%{_localstatedir}/log/misp/'
semanage fcontext -a -t httpd_sys_rw_content_t '%{_sysconfdir}/misp/config.php'
restorecon -v '%{_sysconfdir}/misp/config.php'
semanage fcontext -a -t httpd_sys_rw_content_t '%{noarch_install_dir}/app/Lib/cakephp/lib/Cake/Config/config.php'
restorecon -v '%{noarch_install_dir}/app/Lib/cakephp/lib/Cake/Config/config.php'
semanage fcontext -a -t httpd_sys_rw_content_t '%{noarch_install_dir}/app/Plugin/CakeResque/Config/config.default.php'
restorecon -v '%{noarch_install_dir}/app/Plugin/CakeResque/Config/config.php'
semodule -i %{noarch_install_dir}/policy/selinux/misp-httpd.pp
semodule -i %{noarch_install_dir}/policy/selinux/misp-bash.pp
semodule -i %{noarch_install_dir}/policy/selinux/misp-ps.pp
semodule -i %{noarch_install_dir}/policy/selinux/misp-workers8.pp
semodule -i %{noarch_install_dir}/policy/selinux/misp-worker-status-supervisord.pp

%changelog
* Tue Aug 5 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.17
- update to 2.5.17

* Tue Jul 15 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.16
- update to 2.5.16

* Sun Jun 22 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.15
- update to 2.5.15

* Mon Jun 16 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.14
- update to 2.5.14
- including jakub-onderka/openid-connect-php module

* Fri Jun 13 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.13
- update to 2.5.13

* Wed May 14 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.12
- update to 2.5.12

* Mon May 12 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.11
- update to 2.5.11

* Tue Apr 8 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.10
- update to 2.5.10

* Wed Mar 26 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.9
- update to 2.5.9

* Tue Mar 25 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.8
- update to 2.5.8 

* Mon Feb 24 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.7
- update to 2.5.7 

* Fri Jan 17 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.6
- update to 2.5.6

* Fri Jan 17 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.5
- update to 2.5.5

* Mon Jan 6 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.4
- update to 2.5.4

* Tue Dec 17 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.3
- update to 2.5.3

* Fri Nov 22 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.2
- update to 2.5.2

* Mon Oct 21 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.1
- update to 2.5.1

* Thu Oct 10 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.0
- added new selinux policy for misp-worker-status-supervisord
- update to MISP 2.5.0 with php8 support

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
