%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-pip
Version:	10.0.1
Release:	4%{?dist}
Summary:	The PyPA recommended tool for installing Python packages.

Group:		Development/Languages
License:	MIT License
URL:		https://pypi.org/project/pip/
Source0:	pip-10.0.1.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-setuptools	
Requires:	    python36

%description
The PyPA recommended tool for installing Python packages.

%prep
%setup -q -n pip-%{version}


%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%doc
%{pylibdir}/pip-%{version}-py%{pybasever}.egg-info
%{pylibdir}/pip
%exclude %{_bindir}/pip
%{_bindir}/pip%{pymajorver}
%{_bindir}/pip%{pybasever}

%changelog
* Fri Jul 6 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 10.0.1
- first version for python36
