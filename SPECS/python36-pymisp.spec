Name:		python36-pymisp
Version:	2.4.90
Release:	1%{?dist}
Summary:	Python interface to MISP

Group:		Development/Languages
License:	PyMISP License
URL:		https://github.com/MISP/PyMISP/
Source0:	fake-tgz.tgz

BuildRequires:	python36-devel
BuildRequires:  git
Requires:       python36

%description
Python interface to MISP

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
git clone https://github.com/MISP/PyMISP.git
cd PyMISP
git submodule update --init
pip3 install --install-option='--prefix=$RPM_BUILD_ROOT/usr' -I .

%files
/usr/lib/python3.6/site-packages/*
/usr/bin/*

%changelog
* Wed Apr 25 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.90
- first version for python36
