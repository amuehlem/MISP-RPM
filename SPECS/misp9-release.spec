Name:       	misp-release	
Version:	1.1
Release:	2%{?dist}
Summary:	configuration for MISP repositories for EL9

Group:		System Environment/Base
License:	GPLv2
URL:		https://cruncher.switch.ch/repos/
Source0:	misp9.repo
Source1:    	RPM-GPG-KEY-KOJI-SWITCH-EL9
Source2:	RPM-GPG-KEY-KOJI-MISPPROJECT-EL9

BuildArch:  	noarch

%description
Configuration for MISP repositories (Mariadb and MISP) for EL9

%prep
%setup -q -c -T

%build

%install
rm -rf $RPM_BUILD_ROOT

install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/misp.repo
install -dm 744 $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg
install -pm 644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg

%files
%defattr(-,root,root,-)
%config /etc/yum.repos.d/*
/etc/pki/rpm-gpg/RPM-GPG-KEY-KOJI-SWITCH-EL9
/etc/pki/rpm-gpg/RPM-GPG-KEY-KOJI-MISPPROJECT-EL9

%changelog
* Tue May 21 2024 Andreas Muehlemann <amuehlem@gmail.com> - 1.1-2
- new download URL misp-project.ch
- new GPG key
- update to MariaDB 11.4

* Tue Nov 28 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0.5
- update to MariaDB 10.11

* Thu Jun 29 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0
- first version for EL9
