%define pythondir /usr/lib/python3.4/site-packages

Name:		python34-libtaxii
Version:	1.1.111
Release:	1%{?dist}
Summary:    libtaxii for python

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.python.org/pypi/libtaxii
Source0:    fake-tgz.tgz
Source1:	libtaxii-%{version}-py2.py3-none-any.whl

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools
BuildRequires:  python34-pip, unzip
Requires:	python34, python34-pip

%description
Python interface to MISP

%prep
%setup -q -n fake-tgz

%build
# intentianally left empty

%install
unzip %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT/%{pythondir}
mv libtaxii $RPM_BUILD_ROOT/%{pythondir}
mv libtaxii-%{version}.dist-info $RPM_BUILD_ROOT/%{pythondir}

%files
%{pythondir}/libtaxii
%{pythondir}/libtaxii-%{version}.dist-info

%changelog
* Fri Oct 20 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0
- first version
