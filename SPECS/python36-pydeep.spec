%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-pydeep
Version:	0.4
Release:	1%{?dist}
Summary:	Python bindings for ssdeep

Group:		Development/Languages
License:	BSD License
URL:		https://pypi.org/project/pydeep/
Source0:	fake-tgz.tgz

BuildRequires:  python36, python36-devel, python36-setuptools	
BuildRequires:  ssdeep-devel, git
Requires:	    python36, ssdeep

%description
Python bindings for ssdeep

%prep
%setup -q -n fake-tgz

%build
#intentionally left blank

%install
git clone https://github.com/kbandla/pydeep.git
cd pydeep
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/pydeep.cpython-36m-x86_64-linux-gnu.so
%{pylibdir}/pydeep-%{version}-py%{pybasever}.egg-info

%changelog
* Thu Jul 12 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.2
- first version for python36
