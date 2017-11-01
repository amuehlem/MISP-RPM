Name:		misp-stix-converter
Version:	0.2.10
Release:	1%{?dist}
Summary:    MISP to STIX and back again

Group:		Development/Languages
License:	GPLv3
URL:		https://github.com/MISP/MISP-STIX-Converter
Source0:	fake-tgz.tgz

BuildArch:  noarch
BuildRequires:	python34-devel, python34-setuptools, git
BuildRequires:  python34-pip
Requires:	python34, python34-pip

%description
MISP to STIX and back again

%prep
%setup -q -n fake-tgz

%build
# intentianally left empty

%install
git clone https://github.com/MISP/MISP-STIX-Converter
cd MISP-STIX-Converter
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
/usr/lib/python3.4/site-packages/misp_stix_converter-%{version}-py3.4.egg-info
/usr/lib/python3.4/site-packages/misp_stix_converter
/usr/bin/misp-to-stix.py
/usr/bin/stix-to-misp.py

%changelog
* Fri Oct 20 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0
- first version
