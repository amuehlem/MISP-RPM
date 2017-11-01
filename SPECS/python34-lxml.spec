%define pythondir /usr/lib/python3.4/site-packages

Name:		python34-lxml
Version:	4.1.0
Release:	1%{?dist}
Summary:    libxml for python34

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.python.org/pypi/libtaxii
Source0:    fake-tgz.tgz
Source1:	lxml-%{version}-cp34-cp34m-manylinux1_x86_64.whl

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
mv lxml $RPM_BUILD_ROOT/%{pythondir}
mv lxml-%{version}.dist-info $RPM_BUILD_ROOT/%{pythondir}

%files
%{pythondir}/lxml
%{pythondir}/lxml-%{version}.dist-info

%changelog
* Mon Oct 23 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 4.1.0
- first version
