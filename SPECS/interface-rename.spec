Summary:        A program that rename network interfaces to keep them consistent
Name:           interface-rename
Version:        2.0.2
Release:        1
License:        GPLv2+
Group:          System Environment/Base

Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/interface-rename/archive?at=v2.0.2&format=tar.gz&prefix=interface-rename-2.0.2#/interface-rename-2.0.2.tar.gz


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/interface-rename/archive?at=v2.0.2&format=tar.gz&prefix=interface-rename-2.0.2#/interface-rename-2.0.2.tar.gz) = 76ee8cb29338cf9ee113ff07222d623e177ffddb

BuildRoot:      %{_tmppath}/%{name}-%{version}
BuildRequires:  python2-devel
BuildRequires:  systemd
BuildArch:      noarch
Requires:       xcp-python-libs systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
The %{name} package rename network interfaces in order to keep consistent
naming while moving or replacing cards on the machine.

%prep
%autosetup -p1

%install
rm -rf $RPM_BUILD_ROOT

# directories
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
mkdir -p -m755 $RPM_BUILD_ROOT%{_unitdir}
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts/interface-rename-data
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/udev/scripts
mkdir -p -m755 $RPM_BUILD_ROOT/opt/xensource/bin

# files from sources
install -m 755 interface-rename.py $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts/interface-rename.py
install -m 644 systemd/interface-rename.service $RPM_BUILD_ROOT%{_unitdir}/interface-rename.service
install -m 644 60-net.rules $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d
install -m 755 enqueue-interface-rename.sh $RPM_BUILD_ROOT%{_sysconfdir}/udev/scripts
install -m 755 net-rename-sideways.sh $RPM_BUILD_ROOT%{_sysconfdir}/udev/scripts
install -m 644 logrotate-interface-rename $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/interface-rename

# compatibility executable
ln $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/network-scripts/interface-rename.py $RPM_BUILD_ROOT/opt/xensource/bin/interface-rename

# lock files
umask 022
touch $RPM_BUILD_ROOT%{_sysconfdir}/udev/scripts/enqueue-interface-rename.lock
touch $RPM_BUILD_ROOT%{_sysconfdir}/udev/scripts/net-rename-sideways.lock

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post interface-rename.service

%preun
%systemd_preun interface-rename.service

%postun
%systemd_postun interface-rename.service

%files
%defattr(-,root,root,-)
/etc/*
/opt/xensource/bin/*
%{_unitdir}/interface-rename.service

%changelog
* Mon Mar 26 2018 Simon Rowe <simon.rowe@citrix.com> - 2.0.2-1
- CA-286300: start interface-rename even if udev settle timed out

* Tue Dec 29 2015 Salvatore Cambria <salvatore.cambria@citrix.com>
- Switch to systemd service unit
* Wed Jul 17 2013 Frediano Ziglio <frediano.ziglio@citrix.com>
- First packaged version

