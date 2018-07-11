%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-uwhois
Version:	0.5
Release:	1%{?dist}
Summary:	A 'Universal WHOIS' proxy server - you query it, it gives back the correct details

Group:		Development/Languages
License:	MIT License
URL:		https://github.com/Rafiot/uwhoisd
Source0:	fake-tgz.tgz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
BuildRequires:  git
Requires:	    python36

%description
A 'Universal WHOIS' proxy server - you query it, it gives back the correct details

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
git clone https://github.com/Rafiot/uwhoisd.git
cd uwhoisd/client
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/uwhois
%{pylibdir}/uwhois
%{pylibdir}/uwhois-%{version}-py%{pybasever}.egg-info

%changelog
* Fri Jul 6 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.5
- first version for python36
