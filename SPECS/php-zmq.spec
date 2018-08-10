Name:	    php-zmq	
Version:	1.1.3
Release:	1%{?dist}
Summary:	ZeroMQ binding for PHP

Group:		Development/Languages
License:	BSD License
URL:		http://pecl.php.net/package/zmq
Source0:	zmq-1.1.3.tgz

BuildRequires:	php, zeromq-devel, autoconf, automake
Requires:	    php, zeromq

%description
ZeroMQ is a software library that lets you quickly design and implement a fast message-based applications.

%prep
%setup -q -n zmq-%{version}


%build
phpize
%configure
make %{?_smp_mflags}

%install
make install INSTALL_ROOT=%{buildroot}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/php.d/

# create zmq.ini
cat > $RPM_BUILD_ROOT%{_sysconfdir}/php.d/zmq.ini << EOF
; enable zeromq extension module
extension=zmq.so
EOF

%files
%config(noreplace) %{_sysconfdir}/php.d/zmq.ini
/usr/lib64/php/20170718/zmq.so

%changelog
* Thu Aug 9 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.1.3
- first version
