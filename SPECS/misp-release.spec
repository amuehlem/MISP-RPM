Name:       misp-release	
Version:	1.0
Release:	5%{?dist}
Summary:	configuration for MISP repositories

Group:		System Environment/Base
License:	GPLv2
URL:		https://koji.misp.ch/
Source0:	misp.repo
Source1:    RPM-GPG-KEY-KOJI-SWITCH

BuildArch:  noarch

%description
Configuration for MISP repositories (Mariadb and MISP)


%prep
%setup -q -c -T

%build

%install
rm -rf $RPM_BUILD_ROOT

install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/misp.repo
install -dm 744 $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/RPM-GPG-KEY-KOJI-SWITCH

%changelog
* Sat Mar 3 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0-4
- added GPG key RPM-GPG-KEY-KOJI-SWITCH

* Wed Oct 18 2017 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0
- first version
