%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-furl
Version:	1.2
Release:	1%{?dist}
Summary:	Internationalized Domain Names in Applications (IDNA)

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/furl/
Source0:	furl-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Internationalized Domain Names in Applications (IDNA)

%prep
%setup -q -n furl-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/furl
%{pylibdir}/furl-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.2
- first version for python36
