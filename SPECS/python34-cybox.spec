%define pythondir /usr/lib/python3.4/site-packages

Name:		python34-cybox
Version:	2.1.0.14
Release:	1%{?dist}
Summary:	Python extension for interfacing cybox

Group:		Development/Languages
License:	BSD
URL:		https://github.com/CybOXProject/
Source0:	fake-tgz.tgz
Source1:    cybox-%{version}-py2.py3-none-any.whl

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools, git
BuildRequires:  unzip
Requires:	python34

%description
Python extension for cybox

%prep
%setup -q -n fake-tgz

%build
# intentianally left empty

%install
unzip %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT/%{pythondir}
mv cybox $RPM_BUILD_ROOT/%{pythondir}
mv cybox-%{version}.dist-info $RPM_BUILD_ROOT/%{pythondir}

%files
/usr/lib/python3.4/site-packages/cybox
/usr/lib/python3.4/site-packages/cybox-%{version}.dist-info

%changelog
* Mon Jan 02 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.1.0.12
- first version
