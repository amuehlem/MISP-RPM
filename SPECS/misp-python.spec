%global _turn_off_bytecompile 1
%global __requires_exclude ^/usr/local/bin/python
%undefine _missing_build_ids_terminate_build

Name:		misp-python
Version:	3.9.9
Release: 	6%{?dist}
Summary:	Interpreter of the Python programming language

License:	Python
URL:		https://www.python.org/
Source0:	https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tgz

BuildRequires:	misp-gcc, misp-gcc-libs, openssl-devel
BuildRequires:	libffi-devel
Requires:	openssl

%description
Python is an accessible, high-level, dynamically typed, interpreted programming
language, designed with an emphasis on code readability.
It includes an extensive standard library, and has a vast ecosystem of
third-party libraries.

%prep
%setup -q -n Python-%{version}

%build
export PATH=/var/www/cgi-bin/misp-helpers/bin:$PATH
export LD_LIBRARY_PATH=/var/www/cgi-bin/misp-helpers/lib64:$LD_LIBRARY_PATH
export CMAKE_MAKE_PROGRAM=/var/www/cgi-bin/misp-helpers/bin/cmake
./configure --prefix=/var/www/cgi-bin/misp-python --enable-optimization --with-ssl
make %{?_smp_mflags}

%install
%make_install DESTDIR=$RPM_BUILD_ROOT

%files
%doc
%license
/var/www/cgi-bin/misp-python

%changelog
* Fri Mar 25 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 3.9.9
- changed to gcc version 9

* Wed Jan 05 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 3.9.9
- first version
