%global pkg_name         %{name}
%global _root_sysconfdir %{_sysconfdir}
%if 0%{?nfsmountable}
%global metadir          %{_scl_root}/var/lib/pear
%else
%global metadir          %{_localstatedir}/lib/pear
%endif

%global peardir %{_datadir}/pear

%global getoptver 1.4.1
%global arctarver 1.4.2
# https://pear.php.net/bugs/bug.php?id=19367
# Structures_Graph 1.0.4 - incorrect FSF address
%global structver 1.1.1
%global xmlutil   1.3.0
%global manpages  1.10.0

%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_root_sysconfdir}/rpm; echo $d)

#global pearprever dev1

Summary: PHP Extension and Application Repository framework
Name: php-pear
Version: 1.10.1
Release: 1%{?dist}
Epoch: 1
# PEAR, Archive_Tar, XML_Util are BSD
# Console_Getopt is PHP
# Structures_Graph is LGPLv2+
License: BSD and PHP and LGPLv2+
Group: Development/Languages
URL: http://pear.php.net/package/PEAR
Source0: http://download.pear.php.net/package/PEAR-%{version}%{?pearprever}.tgz
# wget https://raw.github.com/pear/pear-core/master/install-pear.php
Source1: install-pear.php
Source3: cleanup.php
Source10: pear.sh
Source11: pecl.sh
Source12: peardev.sh
Source13: macros.pear
Source21: http://pear.php.net/get/Archive_Tar-%{arctarver}.tgz
Source22: http://pear.php.net/get/Console_Getopt-%{getoptver}.tgz
Source23: http://pear.php.net/get/Structures_Graph-%{structver}.tgz
Source24: http://pear.php.net/get/XML_Util-%{xmlutil}.tgz
Source25: http://pear.php.net/get/PEAR_Manpages-%{manpages}.tgz

Patch0:   php-pear-proxy.patch

BuildArch: noarch
BuildRequires: php > 7.0
###BuildRequires: php-cli
###BuildRequires: php-xml
BuildRequires: gnupg

Provides:  php-pear(Console_Getopt) = %{getoptver}
Provides:  php-pear(Archive_Tar) = %{arctarver}
Provides:  php-pear(PEAR) = %{version}
Provides:  php-pear(Structures_Graph) = %{structver}
Provides:  php-pear(XML_Util) = %{xmlutil}
Provides:  php-pear(PEAR_Manpages) = %{manpages}

Provides:  php-composer(pear/console_getopt) = %{getoptver}
Provides:  php-composer(pear/archive_tar) = %{arctarver}
Provides:  php-composer(pear/pear-core-minimal) = %{version}
Provides:  php-composer(pear/structures_graph) = %{structver}
Provides:  php-composer(pear/xml_util) = %{xmlutil}

Requires:  php > 5.4
###Requires:  php-cli
# phpci detected extension
# PEAR (date, spl always builtin):
###Requires:  php-ftp
###Requires:  php-pcre
###Requires:  php-posix
###Requires:  php-tokenizer
###Requires:  php-xml
###Requires:  php-zlib
# Console_Getopt: pcre
# Archive_Tar: pcre, posix, zlib
###Requires:  php-bz2
# Structures_Graph: none
# XML_Util: pcre
# optional: overload and xdebug
%if 0%{?fedora} >= 21 && 0%{!?scl:1}
%global with_html_dir 0
# for /var/www/html ownership
Requires: httpd-filesystem
%else
%global with_html_dir 1
%endif


%description
PEAR is a framework and distribution system for reusable PHP
components.  This package contains the basic PEAR components.

%prep
%setup -cT

# Create a usable PEAR directory (used by install-pear.php)
for archive in %{SOURCE0} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24} %{SOURCE25}
do
    tar xzf  $archive --strip-components 1 || tar xzf  $archive --strip-path 1
    file=${archive##*/}
    [ -f LICENSE ] && mv LICENSE LICENSE-${file%%-*}
    [ -f README ]  && mv README  README-${file%%-*}

    tar xzf $archive 'package*xml'
    [ -f package2.xml ] && mv package2.xml ${file%%-*}.xml \
                        || mv package.xml  ${file%%-*}.xml
done
cp %{SOURCE1} .

# apply patches on used PEAR during install
# PATCH0 applied on installation tree

sed -e 's/@SCL@/%{?scl:php70_}/' \
    -e 's:@METADIR@:%{metadir}:' \
    -e 's:@BINDIR@:%{_bindir}:' \
    %{SOURCE13} | tee macros.pear


%build
# This is an empty build section.


%install
export PHP_PEAR_SYSCONF_DIR=%{_sysconfdir}
export PHP_PEAR_SIG_KEYDIR=%{_sysconfdir}/pearkeys
export PHP_PEAR_SIG_BIN=%{_root_bindir}/gpg
export PHP_PEAR_INSTALL_DIR=%{peardir}

# 1.4.11 tries to write to the cache directory during installation
# so it's not possible to set a sane default via the environment.
# The ${PWD} bit will be stripped via relocate.php later.
export PHP_PEAR_CACHE_DIR=${PWD}%{_localstatedir}/cache/php-pear
export PHP_PEAR_TEMP_DIR=/var/tmp

install -d $RPM_BUILD_ROOT%{peardir} \
           $RPM_BUILD_ROOT%{_localstatedir}/cache/php-pear \
           $RPM_BUILD_ROOT%{_localstatedir}/www/html \
           $RPM_BUILD_ROOT%{metadir}/pkgxml \
           $RPM_BUILD_ROOT%{_docdir}/pecl \
           $RPM_BUILD_ROOT%{_datadir}/tests/pecl \
           $RPM_BUILD_ROOT%{_sysconfdir}/pear

export INSTALL_ROOT=$RPM_BUILD_ROOT

%{_bindir}/php --version

%{_bindir}/php -dmemory_limit=64M -dshort_open_tag=0 -dsafe_mode=0 \
         -d 'error_reporting=E_ALL&~E_DEPRECATED' -ddetect_unicode=0 \
         install-pear.php --force \
                 --dir      %{peardir} \
                 --cache    %{_localstatedir}/cache/php-pear \
                 --config   %{_sysconfdir}/pear \
                 --bin      %{_bindir} \
                 --www      %{_localstatedir}/www/html \
                 --doc      %{_docdir}/pear \
                 --test     %{_datadir}/tests/pear \
                 --data     %{_datadir}/pear-data \
                 --metadata %{metadir} \
                 --man      %{_mandir} \
                 %{SOURCE0} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24} %{SOURCE25}

# Replace /usr/bin/* with simple scripts:
install -m 755 %{SOURCE10} $RPM_BUILD_ROOT%{_bindir}/pear
install -m 755 %{SOURCE11} $RPM_BUILD_ROOT%{_bindir}/pecl
install -m 755 %{SOURCE12} $RPM_BUILD_ROOT%{_bindir}/peardev
# Fix path in SCL
for exe in pear pecl peardev; do
    sed -e 's:/usr:%{_prefix}:' \
        -i $RPM_BUILD_ROOT%{_bindir}/$exe
done

# Sanitize the pear.conf
%{_bindir}/php %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf %{_datadir}

# Display configuration for debug
%{_bindir}/php -r "print_r(unserialize(substr(file_get_contents('$RPM_BUILD_ROOT%{_sysconfdir}/pear.conf'),17)));"


install -m 644 -D macros.pear \
           $RPM_BUILD_ROOT%{macrosdir}/macros.pear

# apply patches on installed PEAR tree
pushd $RPM_BUILD_ROOT%{peardir}
patch --no-backup --fuzz 0 -p1 < %{PATCH0}
popd

# Why this file here ?
rm -rf $RPM_BUILD_ROOT/.depdb* $RPM_BUILD_ROOT/.lock $RPM_BUILD_ROOT/.channels $RPM_BUILD_ROOT/.filemap

# Need for re-registrying XML_Util
install -m 644 *.xml $RPM_BUILD_ROOT%{metadir}/pkgxml

%if 0%{?nfsmountable:1}
install -d \
    $RPM_BUILD_ROOT%{_scl_scripts}/register.content%{_sysconfdir}/pear \
    $RPM_BUILD_ROOT%{_scl_scripts}/register.content%{_localstatedir}/www/html \
    $RPM_BUILD_ROOT%{_scl_scripts}/register.content%{_localstatedir}/cache/php-pear

install -m 644 -D $RPM_BUILD_ROOT%{macrosdir}/macros.pear \
    $RPM_BUILD_ROOT%{_scl_scripts}/register.content%{macrosdir}/macros.pear

install -m 644 -D $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf \
    $RPM_BUILD_ROOT%{_scl_scripts}/register.content%{_sysconfdir}/pear.conf
%endif


%check
# Check that no bogus paths are left in the configuration, or in
# the generated registry files.
grep $RPM_BUILD_ROOT $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf && exit 1
grep %{_libdir} $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf && exit 1
grep '"/tmp"' $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf && exit 1
grep /usr/local $RPM_BUILD_ROOT%{_sysconfdir}/pear.conf && exit 1
grep -rl $RPM_BUILD_ROOT $RPM_BUILD_ROOT && exit 1


%postun
if [ $1 -eq 0 -a -d %{metadir}/.registry ] ; then
  rm -rf %{metadir}/.registry
fi


%files
%{peardir}
%dir %{metadir}
%{metadir}/.channels
%verify(not mtime size md5) %{metadir}/.depdb
%verify(not mtime)          %{metadir}/.depdblock
%verify(not mtime size md5) %{metadir}/.filemap
%verify(not mtime)          %{metadir}/.lock
%if 0%{?nfsmountable}
%dir %{_scl_root}/var
%dir %{_scl_root}/var/lib
%endif
%{metadir}/.registry
%{metadir}/pkgxml
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/pear.conf
%{macrosdir}/macros.pear
%dir %{_localstatedir}/cache/php-pear
%if %{with_html_dir}
%endif
%dir %{_sysconfdir}/pear
%{!?_licensedir:%global license %%doc}
%license LICENSE*
%doc README*
%dir %{_docdir}/pear
%doc %{_docdir}/pear/*
%dir %{_docdir}/pecl
%dir %{_datadir}/tests
%dir %{_datadir}/tests/pecl
%{_datadir}/tests/pear
%{_datadir}/pear-data
%if 0%{?scl:1}
%dir %{_localstatedir}/www
%endif
%{_mandir}/man1/pear.1*
%{_mandir}/man1/pecl.1*
%{_mandir}/man1/peardev.1*
%{_mandir}/man5/pear.conf.5*
%{?nfsmountable:%{_scl_scripts}/register.content/*}
%exclude %{_localstatedir}/www/html

%changelog
* Wed Dec 28 2016 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1:1.10.1-3
- first version

