%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-libtaxii
Version:	1.1.111
Release:	1%{?dist}
Summary:	A Python library for handling TAXII Messages and invoking TAXII Services.

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/libtaxii/
Source0:	fake-tgz.tgz
Source1:    libtaxii-%{version}-py2.py3-none-any.whl
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
A Python library for handling TAXII Messages and invoking TAXII Services.

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
unzip %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT/%{pylibdir}
mv libtaxii $RPM_BUILD_ROOT/%{pylibdir}
mv libtaxii-%{version}.dist-info $RPM_BUILD_ROOT/%{pylibdir}

%files
%{pylibdir}/libtaxii
%{pylibdir}/libtaxii-%{version}.dist-info

%changelog
* Fri Jul 6 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.1.111
- first version for python36
