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

# global definitions
%define pymispver 2.5.17.2
%define mispstixver 2025.9.25

# RHEL version dependencies
%define phpbasever php83
%define pythonvershort python3.12
%define pythonver python3.12
%define pythonbin python3.12

%if 0%{?rhel} == 8
%define pythonver python3.12
%define pythonvershort python3.12
%define pythonbin python3.12
%endif
%if 0%{?rhel} == 9
%define pythonver python3.12
%define pythonvershort python3.12
%define pythonbin python3.12
%endif
%if 0%{?rhel} == 10
%define pythonver python3.12
%define pythonvershort python3
%define pythonbin python3
%endif

Name:		misp
Version:	2.5.27
release:	1%{?dist}
Summary:	MISP - malware information sharing platform

Group:		Internet Applications
License:	GPLv3
URL:		http://www.misp-project.org/
Source1:	misp.conf
Source2:	misp-httpd.pp
Source3:	misp-bash.pp
Source4:	misp-ps.pp
Source5:	misp-workers.service
Source6:	start-misp-workers.sh
Source7:	misp-workers.ini
Source8:	misp-workers8.pp
Source9:	misp-worker-status-supervisord.pp
Patch0:		MISP-AppModel.php.patch
Patch1:		misp-2.4.177-fix-composer-config.patch

BuildRequires:	git, %{pythonvershort}-devel, %{pythonvershort}-pip
BuildRequires:	libxslt-devel, zlib-devel
BuildRequires:	%{phpbasever}-php, %{phpbasever}-php-cli, %{phpbasever}-php-xml
BuildRequires:	%{phpbasever}-php-mbstring
BuildRequires:	ssdeep-devel
BuildRequires:	cmake3, bash-completion, gcc

%if 0%{?rhel} < 9
BuildRequires:  /usr/bin/pathfix.py
%endif

Requires:	httpd, mod_ssl, libxslt, zlib
# requires either mod_php or php-fpm
Requires:	(%{phpbasever}-php or %{phpbasever}-php-fpm)
Requires:	%{phpbasever}-php-cli, %{phpbasever}-php-gd, %{phpbasever}-php-pdo
Requires:	%{phpbasever}-php-mysqlnd, %{phpbasever}-php-mbstring, %{phpbasever}-php-xml
Requires:	%{phpbasever}-php-bcmath, %{phpbasever}-php-opcache, %{phpbasever}-php-json
Requires:	%{phpbasever}-php-pecl-zip, %{phpbasever}-php-pecl-redis6, %{phpbasever}-php-intl
Requires:	%{phpbasever}-php-pecl-gnupg, %{phpbasever}-php-pecl-ssdeep, %{phpbasever}-php-process
Requires:	%{phpbasever}-php-pecl-apcu, %{phpbasever}-php-brotli, %{phpbasever}-php-pecl-rdkafka
Requires:	%{phpbasever}-php-pecl-simdjson
Requires:	supervisor, faup, gtcaca
Requires:	misp-python-virtualenv = %{version}-%{release}

# redis / valkey depending on rhel version
%if 0%{?rhel} < 10
Requires:  redis
%endif
%if 0%{?rhel} > 9
Requires:  valkey
%endif

%package python-virtualenv
Summary:	the python virtual environment for MISP
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
mkdir -p $RPM_BUILD_ROOT/var/www/MISP
cp -r MISP/app $RPM_BUILD_ROOT/var/www/MISP
cp -r MISP/PyMISP $RPM_BUILD_ROOT/var/www/MISP
cp -r MISP/format $RPM_BUILD_ROOT/var/www/MISP
cp -r MISP/tools $RPM_BUILD_ROOT/var/www/MISP
cp -r MISP/*.json $RPM_BUILD_ROOT/var/www/MISP
cp -r MISP/.git $RPM_BUILD_ROOT/var/www/MISP
mkdir -p $RPM_BUILD_ROOT/var/www/MISP/INSTALL
cp MISP/INSTALL/*.sql $RPM_BUILD_ROOT/var/www/MISP/INSTALL

# create initial configuartion files
cd  $RPM_BUILD_ROOT/var/www/MISP/app/Config
mv bootstrap.default.php bootstrap.php
mv config.default.php config.php
mv core.default.php core.php
mv database.default.php database.php

# create python3 virtualenv
%{pythonbin} -m venv --copies $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv

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
/opt/remi/%{phpbasever}/root/usr/bin/php composer.phar install --no-dev
/opt/remi/%{phpbasever}/root/usr/bin/php composer.phar require --with-all-dependencies supervisorphp/supervisor:^4.0 guzzlehttp/guzzle php-http/message php-http/message-factory lstrojny/fxmlrpc jakub-onderka/openid-connect-php

cd $RPM_BUILD_ROOT/var/www/MISP

# clean up before PATH rewriting
rm -rf $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/__pycache__

# rewrite PATH in virtualenv
sed -e "s|%{buildroot}||g" -i $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/pyvenv.cfg
sed -e "s|%{buildroot}||g" -i $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/*
sed -e "s|%{buildroot}||g" -i $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/lib/%{pythonver}/site-packages/*/direct_url.json

# path fix for python3 for RHEL8
%if 0%{?rhel} < 9
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" . $RPM_BUILD_ROOT/var/www/MISP/*
%endif

%py3_shebang_fix $RPM_BUILD_ROOT/var/www/MISP

# save commit ID of this installation
git rev-parse HEAD > .git_commit_version

# cleanup
pushd $RPM_BUILD_ROOT
find . -not -name '.git_commit_version' -name .git* | xargs rm -rf
find . -type f -name empty | xargs rm -f

rm -f var/www/MISP/app/Makefile
rm -f var/www/MISP/app/update_thirdparty.sh
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
%doc MISP/docs
%license MISP/LICENSE
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
/var/www/MISP
/usr/share/MISP/policy/selinux/misp-*.pp
%{_sysconfdir}/systemd/system/misp-workers.service
/usr/local/sbin/start-misp-workers.sh
# exclude test files whicht get detected by AV solutions
%exclude /var/www/MISP/PyMISP/tests
%exclude /var/www/MISP/*.pyc

%post
SELINUXSTATUS=$(getenforce);
if [ SELINUXSTATUS != 'Disabled' ]; then
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
fi

%changelog
* Mon Dec 1 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.27
- update to 2.5.27

* Thu Nov 20 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.26
- update to 2.5.26

* Fri Nov 14 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.25
- update to 2.5.25

* Mon Nov 3 2025 Andreas Muehoemann <amuehlem@gmail.com> - 2.5.24
- update to 2.5.24

* Wed Oct 15 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.23
- update to 2.5.23

* Sat Oct 4 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.22
- update to 2.5.22

* Thu Sep 11 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.21
- update to 2.5.21

* Thu Aug 28 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.20
- update to 2.5.20

* Mon Aug 25 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.19
- update to 2.5.19, one spec file for RHEL8/RHEL9/RHEL10, thank you  guillomovitch!
- update to python3.12 for RHEL8/9

* Sat Aug 9 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.18
- update to 2.5.18

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
