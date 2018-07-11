%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-tornado
Version:	5.0.2
Release:	1%{?dist}
Summary:	Tornado is a Python web framework and asynchronous networking library, originally developed at FriendFeed.

Group:		Development/Languages
License:	Apache Software License (http://www.apache.org/licenses/LICENSE-2.0)
URL:		https://pypi.org/project/tornado/
Source0:	tornado-5.0.2.tar.gz

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Tornado is a Python web framework and asynchronous networking library, originally developed at FriendFeed.

%prep
%setup -q -n tornado-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{pylibdir}/tornado
%{pylibdir}/tornado-%{version}-py%{pybasever}.egg-info

%changelog
* Tue Jul 10 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 5.0.2
- first version for python36
