%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-stix2_patterns
Version:	0.6.0
Release:	2%{?dist}
Summary:	Validate STIX 2 Patterns

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/stix2_patterns/
Source0:	fake-tgz.tgz
Source1:    stix2_patterns-%{version}-py2.py3-none-any.whl
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Validate STIX 2 Patterns

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
unzip %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT/%{pylibdir}
mv stix2patterns $RPM_BUILD_ROOT/%{pylibdir}
mv stix2_patterns-%{version}.dist-info $RPM_BUILD_ROOT/%{pylibdir}
ln -s /%{pylibdir}/stix2patterns $RPM_BUILD_ROOT/%{pylibdir}/stix2_patterns

%files
%{pylibdir}/stix2patterns
%{pylibdir}/stix2_patterns
%{pylibdir}/stix2_patterns-%{version}.dist-info

%changelog
* Wed Jul 18 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.6.0
- first version for python36
