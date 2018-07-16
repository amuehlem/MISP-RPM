%define pymajorver 3
%define pybasever 3.6
%define pylibdir /usr/%{_lib}/python%{pybasever}/site-packages

Name:		python36-pytesseract
Version:	0.2.2
Release:	1%{?dist}
Summary:	Python-tesseract is a python wrapper for Google's Tesseract-OCR

Group:		Development/Languages
License:	GPLv3
URL:		https://pypi.org/project/pytesseract/
Source0:	pytesseract-%{version}.tar.gz
Buildarch:  noarch

BuildRequires:  python36, python36-devel, python36-setuptools	
Requires:	    python36

%description
Python-tesseract is a python wrapper for Google's Tesseract-OCR

%prep
%setup -q -n pytesseract-%{version}

%build
#intentionally left blank

%install
python3 setup.py install --root=$RPM_BUILD_ROOT

%files
%{_bindir}/pytesseract
%{pylibdir}/pytesseract
%{pylibdir}/pytesseract-%{version}-py%{pybasever}.egg-info

%changelog
* Wed Jul 11 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 0.2.2
- first version for python36
