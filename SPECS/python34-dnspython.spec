%define pythondir /usr/lib/python3.4/site-packages

Name:		python34-dnspython
Version:	1.15.0
Release:	1%{?dist}
Summary:    libxml for python34

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.python.org/pypi/libtaxii
Source0:    fake-tgz.tgz
Source1:	dnspython-%{version}-py2.py3-none-any.whl

BuildRequires:	python34-devel, python34-setuptools
BuildRequires:  python34-pip, unzip
Requires:	python34, python34-pip

%description
libxml for python34

%prep
%setup -q -n fake-tgz

%build
# intentianally left empty

%install
unzip %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT/%{pythondir}
mv dns $RPM_BUILD_ROOT/%{pythondir}
mv dnspython-%{version}.dist-info $RPM_BUILD_ROOT/%{pythondir}

%files
%{pythondir}/dns
%{pythondir}/dnspython-%{version}.dist-info

%changelog
* Wed Oct 25 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.15.0
- first version
