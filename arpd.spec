Summary:	User-space arp daemon
Summary(pl):	Demon arpd
Name:		arpd
Version:	1.0.2
Release:	10
License:	GPL
Group:		Daemons
# origin, but 404
#Source0:	http://www.loran.com/~layes/arpd/%{name}-%{version}.tar.gz
# working (copy of original package):
#Source0:	http://www.funet.fi/pub/Linux/PEOPLE/Linus/net-source/base/%{name}-%{version}.tar.gz
# but in CVS we probably have some renamed source from Debian (with .orig inside)
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	4b445f5698342c873068a86a18bc3d6a
Source1:	%{name}-init
Patch0:		%{name}-%{version}.debian-patch
Patch1:		%{name}-%{version}.pld-patch
Patch2:		%{name}-makefile-patch
Patch3:		%{name}-more_tables.patch
Patch4:		%{name}-uid.patch
#URL:		http://www.loran.com/~layes/arpd/
Prereq:		fileutils
Prereq:		rc-scripts >= 0.2.0
Requires(post,preun):	/sbin/chkconfig
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
%doc CHANGES README.html
%attr(754,root,root) %{_sbindir}/arpd
%attr(754,root,root) /etc/rc.d/init.d/arpd
