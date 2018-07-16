%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-pypssl
Version:	2.1
Release:	1%{?dist}
Summary:	Python API for PSSL.

Group:		Development/Languages
License:	GPLv3
URL:		https://pypi.org/project/pypssl/
Source0:	pypssl-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Internationalized Domain Names in Applications (IDNA)

%prep
%setup -q -n pypssl-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/pypssl
%{pylibdir}/pypssl
%{pylibdir}/pypssl-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.1
- first version for python36
