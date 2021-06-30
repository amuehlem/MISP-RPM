%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/lib/python%{pybasever}/site-packages

Name:		python36-yara
Version:	1.7.7
Release:	2%{?dist}
Summary:	Compile YARA rules to test against files or strings

Group:		Development/Languages
License:	Apache Software License
URL:		https://pypi.org/project/yara/
Source0:    yara-%{version}.tar.gz

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36, misp-pcre

%description
Compile YARA rules to test against files or strings

%prep
%setup -q -n yara-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/yara-ctypes
/usr/lib/libyara.so
%{pylibdir}/yara
%{pylibdir}/yara-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 18 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.7.7
- first version for python36
