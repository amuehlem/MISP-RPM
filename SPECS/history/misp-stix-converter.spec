%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		misp-stix-converter
Version:    0.2.10
Release:	2%{?dist}
Summary:	MISP to STIX and back again

Group:		Development/Languages
License:	BSD License
URL:		https://github.com/MISP/MISP-STIX-Converter
Source0:	fake-tgz.tgz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
BuildRequires:  git
Requires:	    python36

%description
MISP to STIX and back again

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
git clone https://github.com/MISP/MISP-STIX-Converter
cd MISP-STIX-Converter
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/misp-to-stix.py
%{_bindir}/stix-to-misp.py
%{pylibdir}/misp_stix_converter
%{pylibdir}/misp_stix_converter-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.2.10
- first version for python36
