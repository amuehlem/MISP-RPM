%global pylibdir /usr/lib/python3.6

Name:		python36
Version:	3.6.4
Release:	1%{?dist}
Summary:	Python programming language

Group:		Development/Languages
License:	Python
URL:		http://www.python.org/
Source0:	Python-3.6.4.tgz

BuildRequires:  autoconf, bzip2-devel, findutils, glibc-devel, gmp-devel, libffi-devel, libGL-devel
BuildRequires:  libX11-devel, ncurses-devel, net-tools, openssl-devel, pkgconfig, readline-devel
BuildRequires:  sqlite-devel, tcl-devel, tix-devel, tk-devel, xz-devel, zlib-devel
Requires:       expat, pkgconfig, zlib

%package devel
Summary:    Libraries and header files needed for Python 3 development
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
This package contains libraries and header files used to build applications
with and native libraries for Python 3

%description
Python is an interpreted, interactive, object-oriented programming
language often compared to Tcl, Perl, Scheme or Java. Python includes
modules, classes, exceptions, very high level dynamic data types and
dynamic typing. Python supports interfaces to many system calls and
libraries, as well as to various windowing systems (X11, Motif, Tk,
Mac and MFC).

Programmers can write new built-in modules for Python in C or C++.
Python can be used as an extension language for applications that need
a programmable interface.


%prep
%setup -q -n Python-%{version}

%build
%configure \
    --enable-ipv6 \
    --enable-shared \
    --with-dbmliborder=gdbm:ndbm:bdb \
    --with-system-expat \
    --with-system-ffi \
    --enable-loadable-sqlite-extensions

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files devel
%{_bindir}/python3-config
%{_bindir}/python3.6-config
%{_bindir}/python3.6m-config
%{_libdir}/pkgconfig/python-3.6.pc
%{_libdir}/pkgconfig/python-3.6m.pc
%{_libdir}/pkgconfig/python3.pc
%{_includedir}/python3.6m/*.h
%exclude %pylibdir/config-3.6m-x86_64-linux-gnu/Makefile
%pylibdir/config-3.6m-x86_64-linux-gnu/*

%files
%{_bindir}/python3
%{_bindir}/python3.6
%{_bindir}/python3.6m
%{_bindir}/pyvenv
%{_bindir}/pyvenv-3.6
%{_bindir}/2to3
%{_bindir}/2to3-3.6
%{_bindir}/easy_install-3.6
%{_bindir}/idle3
%{_bindir}/idle3.6
%{_bindir}/pip3
%{_bindir}/pip3.6
%{_bindir}/pydoc3
%{_bindir}/pydoc3.6
%pylibdir/*
%{_libdir}/*
%{_mandir}/*/*

%changelog
* Wed Jan 17 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 3.6.4
- first version
