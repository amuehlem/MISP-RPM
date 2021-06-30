%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-pytz
Version:	2021.1
Release:	1%{?dist}
Summary:	World timezone definitions, modern and historical

Group:		Development/Languages
License:	MIT License
URL:		https://pypi.org/project/pytz/
Source0:	fake-tgz.tgz
Source1:    	pytz-%{version}-py2.py3-none-any.whl
Buildarch:  	noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
World timezone definitions, modern and historical

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
unzip %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT/%{pylibdir}
mv pytz $RPM_BUILD_ROOT/%{pylibdir}
mv pytz-%{version}.dist-info $RPM_BUILD_ROOT/%{pylibdir}

%files
%{pylibdir}/pytz
%{pylibdir}/pytz-%{version}.dist-info

%changelog
* Wed Mar 31 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2021.1
- update to 2021.1

* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2018.5
- first version for python36
