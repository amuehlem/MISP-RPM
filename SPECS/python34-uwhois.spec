Name:		python34-uwhois
Version:	0.5
Release:	1%{?dist}
Summary:	Python extension for interfacing uwhois

Group:		Development/Languages
License:	PHP
URL:		https://github.com/Rafiot/uwhoisd
Source0:	fake-tgz.tgz

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools, git
Requires:	python34

%description
Python extension for uwhois

%prep
%setup -q -n fake-tgz

%build
# intentianally left empty

%install
git clone https://github.com/Rafiot/uwhoisd.git
cd uwhoisd/client
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/uwhois
/usr/lib/python3.4/site-packages/uwhois
/usr/lib/python3.4/site-packages/uwhois-%{version}-py3.4.egg-info

%changelog
* Thu Nov 02 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.5
- first version
