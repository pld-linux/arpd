Summary:	User-space arp daemon
Summary(pl):	Demon arpd
Name:		arpd
Version:	1.0.2
Release:	7
License:	GPL
Group:		Daemons
#Source0:	http://www.loran.com/~layes/arpd/%{name}-%{version}.tar.gz  (origin, but 404)
Source0:	ftp://ftp.slackware.org:/pub/slackware/slackware-4.0/source/n/tcpip1/%{name}-%{version}.tar.gz
Source1:	%{name}-init
Patch0:		%{name}-%{version}.debian-patch
Patch1:		%{name}-%{version}.pld-patch
Patch2:		%{name}-makefile-patch
Patch3:		%{name}-more_tables.patch
Patch4:		%{name}-uid.patch
#URL:		http://www.loran.com/~layes/arpd/
Prereq:		/sbin/chkconfig
Prereq:		rc-scripts >= 0.2.0
Prereq:		fileutils
Requires:	dev >= 2.8.0-4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The ARP daemon moves the management of the ARP (Address Resolution
Protocol) table from kernel to user space. It is useful for sites with
LARGE network segments (256+ systems per segment), because the kernel
hash tables are not optimized to handle this situation. To use the ARP
daemon your kernel needs to have ARPD and NETLINK support enabled. The
standard kernels of PLD lack this support. It shouldn't be run without
that! This version can alocate 4096 entries.

%description -l pl
Demon ARP przekazuje zarz±dzanie tablic± ARP (Address Resolution
Protocol) z kernel'a do przestrzeni u¿ytkownika. Jest to bardzo
u¿yteczne dla miejsc o du¿ych segmentach sieci (256+ systemów na
segment), poniewa¿ tablice w j±drze nie s± zoptymalizowane na takie
sytuacje. Aby u¿ywaæ tego demona musisz mieæ ARPD support oraz NETLINK
support uaktywnione w j±drze. Uwaga! Stanadardowe j±dro PLD nie ma
supportu ARPD. Demon nie powinien byæ startowany bez tego! Ta wersja
potrafi zaakceptowaæ 4096 pozycji.

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
install -d $RPM_BUILD_ROOT/{usr/sbin,etc/rc.d/init.d}

install arpd $RPM_BUILD_ROOT%{_sbindir}/arpd
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/arpd

gzip -9nf CHANGES

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add arpd
if [ -f /var/lock/subsys/arpd ]; then
	/etc/rc.d/init.d/arpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/arpd start\" to start arpd daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/arpd ]; then
		/etc/rc.d/init.d/arpd stop 1>&2
	fi
	/sbin/chkconfig --del arpd
fi


%files
%defattr(644,root,root,755)
%doc *.gz README.html
%attr(754,root,root) %{_sbindir}/arpd
%attr(754,root,root) /etc/rc.d/init.d/arpd
