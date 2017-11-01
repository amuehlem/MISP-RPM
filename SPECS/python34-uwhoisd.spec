Name:		python34-uwhoisd
Version:	0.0.7
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
cd uwhoisd
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/uwhoisd
/usr/lib/python3.4/site-packages/uwhoisd
/usr/lib/python3.4/site-packages/uwhoisd-%{version}-py3.4.egg-info

%changelog
* Mon Jan 02 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.0.7
- first version
