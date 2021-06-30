%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-sigmatools
Version:	0.6
Release:	1%{?dist}
Summary:	Tools for the Generic Signature Format for SIEM Systems

Group:		Development/Languages
License:	LGPLv3
URL:		https://pypi.org/project/sigmatools/
Source0:    fake-tgz.tgz
Source1:	sigmatools-%{version}-py3-none-any.whl
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Tools for the Generic Signature Format for SIEM Systems

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
unzip %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT/%{pylibdir}
mv sigma $RPM_BUILD_ROOT/%{pylibdir}
mv sigmatools-%{version}.data $RPM_BUILD_ROOT/%{pylibdir}
mv sigmatools-%{version}.dist-info $RPM_BUILD_ROOT/%{pylibdir}

%files
%{pylibdir}/sigma
%{pylibdir}/sigmatools-%{version}.data
%{pylibdir}/sigmatools-%{version}.dist-info

%changelog
* Wed Jul 18 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.6
- first version for python36
