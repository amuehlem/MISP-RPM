%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-lxml
Version:    	4.5.2
Release:	3%{?dist}
Summary:	Powerful and Pythonic XML processing library combining libxml2/libxslt with the ElementTree API.

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/lxml/
Source0:	fake-tgz.tgz
Source1:    	lxml-%{version}-cp36-cp36m-manylinux1_x86_64.whl

BuildRequires:  python36, python36-devel, python36-setuptools	
BuildRequires:  unzip
Requires:	python36

%description
Powerful and Pythonic XML processing library combining libxml2/libxslt with the ElementTree API.

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
unzip %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT/%{pylibdir}
mv lxml $RPM_BUILD_ROOT/%{pylibdir}
mv lxml-%{version}.dist-info $RPM_BUILD_ROOT/%{pylibdir}

%files
%{pylibdir}/lxml
%{pylibdir}/lxml-%{version}.dist-info

%changelog
* Wed Sep 16 2020 Andreas Muehlemann <andreas.muehlemann@swithc.ch> - 4.5.2
- update to 4.5.2

* Fri Jul 6 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 4.2.3
- first version for python36
