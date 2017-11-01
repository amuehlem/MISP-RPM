%define pythondir /usr/lib/python3.4/site-packages

Name:		python34-python_dateutil
Version:	2.6.1
Release:	1%{?dist}
Summary:    python_dateutil for python

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.python.org/pypi/python-dateutil
Source0:    fake-tgz.tgz
Source1:	python_dateutil-%{version}-py2.py3-none-any.whl

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
mv dateutil $RPM_BUILD_ROOT/%{pythondir}
mv python_dateutil-%{version}.dist-info $RPM_BUILD_ROOT/%{pythondir}

%files
%{pythondir}/dateutil
%{pythondir}/python_dateutil-%{version}.dist-info

%changelog
* Tue Oct 24 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.6.1
- first version
