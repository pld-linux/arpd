Summary:	User-space arp daemon
Summary(pl):	Demon arpd
Name:		arpd
Version:	1.0.2
Release:	4
License:	GPL
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}-init
Patch0:		%{name}-%{version}.debian-patch
Patch1:		%{name}-%{version}.pld-patch
Patch2:		%{name}-makefile-patch
Patch3:		%{name}-more_tables.patch
Patch4:		%{name}-uid.patch
Prereq:		/sbin/chkconfig
Prereq:		rc-scripts >= 0.2.0
Prereq:		fileutils
Requires:	dev >= 2.8.0-3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The ARP daemon moves the management of the ARP (Address Resolution
Protocol) table from kernel to user space. It is useful for sites with
LARGE network segments (256+ systems per segment), because the kernel
hash tables are not optimized to handle this situation. To use the ARP
daemon your kernel needs to have ARPD and NETLINK support enabled. The
standard kernels of PLD lack this support. It shouldn't be run without
that!! This version can alocate 2048 entries.

%description -l pl
Demon ARP przekazuje zarz±dzanie tablic± ARP (Address Resolution
Protocol) z kernel'a do przestrzeni u¿ytkownika. Jest to bardzo
u¿yteczne dla miejsc o du¿ych segmentach sieci (256+ systemów na
segment), poniewa¿ tablice w j±drze nie s± zoptymalizowane na takie
sytuacje. Aby u¿ywaæ tego demona musisz mieæ ARPD support oraz NETLINK
support uaktywnione w j±drze. Uwaga! Stanadardowe j±dro PLD nie ma
supportu ARPD!!. Demon nie powinien byæ startowany bez tego!! Ta
wersja potrafi zaakceptowaæ 2048 pozycji.

%prep
%setup  -q -n %{name}-%{version}.orig
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3
%patch4 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{usr/sbin,etc/rc.d/init.d,/var/lib/arpd}

install arpd $RPM_BUILD_ROOT%{_sbindir}/arpd
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/arpd

gzip -9nf CHANGES

%pre
USER=arpd; UID=40; HOMEDIR=/var/lib/arpd; COMMENT="arpd user"
GROUP=daemon; %useradd

%post
if [ ! -L /dev/arpd ]; then
	echo "Moving /dev/arpd to /var/lib/arpd/arpd and making symlink"
	mv -f /dev/arpd /var/lib/arpd
	chown arpd /var/lib/arpd/arpd
	ln -s /var/lib/arpd/arpd dev/arpd
fi
echo "You need arpd kernel support. The standard kernels of PLD lack this support!!"
DESC="arpd daemon"; %chkconfig_post

%preun
%chkconfig_preun
if [ "$1" = "0" ]; then
	echo "Moving /var/lib/arpd/arpd to /dev/arpd and removing symlink"
	rm -f /dev/arpd
	mv -f /var/lib/arpd/arpd /dev/arpd
	chown root:root /dev/arpd
fi

%postun
USER=arpd; %userdel

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz README.html
%attr(754,root,root) %{_sbindir}/arpd
%attr(754,root,root) /etc/rc.d/init.d/arpd
%dir %attr(750,arpd,root) /var/lib/arpd
