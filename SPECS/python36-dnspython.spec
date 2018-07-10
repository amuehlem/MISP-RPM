%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-dnspython
Version:	1.15.0
Release:	1%{?dist}
Summary:	A DNS toolkit for Python

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/dnspython/
Source0:	fake-tgz.tgz
Source1:    dnspython-%{version}-py2.py3-none-any.whl
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
A DNS toolkit for Python

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
unzip %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT/%{pylibdir}
mv dns $RPM_BUILD_ROOT/%{pylibdir}
mv dnspython-%{version}.dist-info $RPM_BUILD_ROOT/%{pylibdir}

%files
%{pylibdir}/dns
%{pylibdir}/dnspython-%{version}.dist-info

%changelog
* Tue Jul 10 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.15.0
- first version for python36
