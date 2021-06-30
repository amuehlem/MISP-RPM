%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-pyonyphe
Version:	1.0
Release:	2%{?dist}
Summary:	Client python for https://www.onyphe.io

Group:		Development/Languages
License:	MIT License
URL:		https://github.com/sebdraven/pyonyphe
Source0:	fake-tgz.tgz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
BuildRequires:  git
Requires:	    python36

%description
Client python for https://www.onyphe.io

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
git clone https://github.com/sebdraven/pyonyphe.git
cd pyonyphe
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/onyphe
%{pylibdir}/pyonyphe-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 18 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0
- first version for python36
