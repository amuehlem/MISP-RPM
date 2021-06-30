%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-setuptools-rust
Version:	0.12.1
Release:	1%{?dist}
Summary:	Internationalized Domain Names in Applications (IDNA)

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/setuptools-rust/
Source0:	setuptools-rust-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Internationalized Domain Names in Applications (IDNA)

%prep
%setup -q -n setuptools-rust-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/setuptools-rust
%{pylibdir}/setuptools-rust-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Mar 31 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 3.1
- first version for python36
