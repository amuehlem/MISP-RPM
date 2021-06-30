%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

%define __requires_exclude ^/opt/python/(.*)$

Name:			lief-python
Version:		0.11.4
Release: 		1%{?dist}
Summary:		Python extension for LIEF

License:		Apache
URL:			https://github.com/lief-project/
Source0:		fake-tgz.tgz
Source1:		lief-%{version}-cp36-cp36m-manylinux1_x86_64.whl

BuildRequires:		python36, python36-setuptools, python36-pip
BuildRequires:		cmake3
Requires:		python36

%description
Python extension for LIEF

%prep
%setup -q -n fake-tgz


%build

%install
mkdir -p $RPM_BUILD_ROOT%{pylibdir}
unzip -d $RPM_BUILD_ROOT%{pylibdir} %{SOURCE1}

%files
%{pylibdir}/lief.cpython-36m-x86_64-linux-gnu.so
%{pylibdir}/lief-%{version}.data
%{pylibdir}/lief-%{version}.dist-info

%changelog
* Wed Mar 31 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.11.4
- first version using pip to install
