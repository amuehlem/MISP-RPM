%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-colorlog
Version:	3.1.4
Release:	1%{?dist}
Summary:	Log formatting with colors!

Group:		Development/Languages
License:	MIT License
URL:		https://pypi.org/project/colorlog/
Source0:	fake-tgz.tgz
Source1:    colorlog-%{version}-py2.py3-none-any.whl
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Log formatting with colors!

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
unzip %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT/%{pylibdir}
mv colorlog $RPM_BUILD_ROOT/%{pylibdir}
mv colorlog-%{version}.dist-info $RPM_BUILD_ROOT/%{pylibdir}

%files
%{pylibdir}/colorlog
%{pylibdir}/colorlog-%{version}.dist-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 3.1.4
- first version for python36
