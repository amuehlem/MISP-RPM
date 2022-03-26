Name:		misp-cmake
Version:	3.22.1
Release: 	1%{?dist}
Summary:	Cross-platform make system

License:	BSD and MIT and zlib
URL:		https://cmake.org/
Source0:	https://github.com/Kitware/CMake/releases/download/v3.22.1/cmake-3.22.1.tar.gz

BuildRequires:	openssl-devel

Requires(post): info
Requires(preun): info

%description
CMake is used to control the software compilation process using simple
platform and compiler independent configuration files. CMake generates
native makefiles and workspaces that can be used in the compiler
environment of your choice. CMake is quite sophisticated: it is possible
to support complex environments requiring system configuration, preprocessor
generation, code generation, and template instantiation.

%prep
%setup -q -n cmake-%{version}

%build
./bootstrap --prefix=/var/www/cgi-bin/misp-helpers
make %{?_smp_mflags}


%install
%make_install DEST_DIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT/var/www/cgi-bin/misp-helpers/share/info/dir

%files
%doc
%license
/var/www/cgi-bin/misp-helpers

%post
/sbin/ldconfig
/sbin/install - info /var/www/cgi-bin/misp-helpers/share/info/%{name}. info /var/www/cgi-bin/misp-helpers/share/info/dir || :

%preun
if [$ 1 = 0 ]; then
/sbin/install - info --delete /var/www/cgi-bin/misp-helpers/share/info/%{name}. info /var/www/cgi-bin/misp-helpers/share/info/dir || :
fi

%changelog
* Fri Jan 07 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 3.22.1
- first version

