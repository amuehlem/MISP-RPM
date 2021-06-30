%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-multidict
Version:	4.3.1
Release:	1%{?dist}
Summary:	multidict implementation

Group:		Development/Languages
License:	Apache Software License (Apache 2)
URL:		https://pypi.org/project/multidict/
Source0:	multidict-%{version}.tar.gz

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
multidict implementation

%prep
%setup -q -n multidict-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/multidict
%{pylibdir}/multidict-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 18 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 4.3.1
- first version for python36
