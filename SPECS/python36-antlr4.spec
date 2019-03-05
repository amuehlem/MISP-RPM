%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-antlr4
Version:	4.7.2
Release:	1%{?dist}
Summary:	Antlr4 runtime for python

Group:		Development/Languages
License:	BSD
URL:		https://pypi.org/project/antlr4-python3-runtime/
Source0:	antlr4-python3-runtime-%{version}.tar.gz
BuildArch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Antlr4 runtime for python

%prep
%setup -q -n antlr4-python3-runtime-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/antlr4
%{pylibdir}/antlr4_python3_runtime-%{version}-py%{pybasever}.egg-info

%changelog
* Tue Mar 5 2019 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 4.7.2
- first version for python36
