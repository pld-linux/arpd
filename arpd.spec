Summary:	User-space arp daemon
Summary(pl):	Demon arpd
Name:		arpd
Version:	1.0.2
Release:	5
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
BuildRequires:	fakeroot
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The ARP daemon moves the management of the ARP (Address Resolution
Protocol) table from kernel to user space. It is useful for sites with
LARGE network segments (256+ systems per segment), because the kernel
hash tables are not optimized to handle this situation. To use the ARP
daemon your kernel needs to have ARPD and NETLINK support enabled. The
standard kernels of PLD lack this support. It shouldn't be run without
that!! This version can alocate 2048 entries.

This is version which runs at UID=40.

%description -l pl
Demon ARP przekazuje zarz±dzanie tablic± ARP (Address Resolution
Protocol) z kernel'a do przestrzeni u¿ytkownika. Jest to bardzo
u¿yteczne dla miejsc o du¿ych segmentach sieci (256+ systemów na
segment), poniewa¿ tablice w j±drze nie s± zoptymalizowane na takie
sytuacje. Aby u¿ywaæ tego demona musisz mieæ ARPD support oraz NETLINK
support uaktywnione w j±drze. Uwaga! Stanadardowe j±dro PLD nie ma
supportu ARPD!!. Demon nie powinien byæ startowany bez tego!! Ta
wersja potrafi zaakceptowaæ 2048 pozycji.

Ta wersja pracuje na UID=40.

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

# making device with fakeroot:
cd $RPM_BUILD_ROOT/var/lib/arpd
mknod arpd c 36 8

%pre
if [ -n "`id -u arpd 2>/dev/null`" ]; then
	if [ "`id -u arpd`" != "40" ]; then
		echo "Warning: user arpd haven't uid=40. Correct this before installing arpd." 1>&2
		exit 1
	fi
else
	echo "Adding arpd user (UID=40)"
	/usr/sbin/useradd -u 40 -r -d /var/lib/arpd -s /bin/false -c "arpd user" -g daemon arpd 1>&2
fi

%post
/sbin/chkconfig --add arpd
if [ -f /var/lock/subsys/arpd ]; then
	/etc/rc.d/init.d/arpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/arpd start\" to start arpd daemon."
fi


%preun
/sbin/chkconfig --del arpd
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/arpd ]; then
		/etc/rc.d/init.d/arpd stop 1>&2
	fi
	/sbin/chkconfig --del arpd
fi

%postun
if [ "$1" = "0" ]; then
	echo "Removing arpd user (UID=40)"
	/usr/sbin/userdel arpd
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz README.html
%attr(754,root,root) %{_sbindir}/arpd
%attr(754,root,root) /etc/rc.d/init.d/arpd
%dir %attr(750,arpd,root) /var/lib/arpd/*
