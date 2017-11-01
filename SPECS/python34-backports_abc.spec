%define pythondir /usr/lib/python3.4/site-packages

Name:		python34-backports_abc
Version:	0.5
Release:	1%{?dist}
Summary:    libtaxii for python

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.python.org/pypi/libtaxii
Source0:    fake-tgz.tgz
Source1:	backports_abc-%{version}-py2.py3-none-any.whl

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
mv backports_abc.py $RPM_BUILD_ROOT/%{pythondir}
mv backports_abc-%{version}.dist-info $RPM_BUILD_ROOT/%{pythondir}

%files
%{pythondir}/backports_abc.py
%{pythondir}/backports_abc-%{version}.dist-info

%changelog
* Wed Oct 25 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.5
- first version
