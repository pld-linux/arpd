Summary:	User-space arp daemon
Summary(pl):	Demon arpd
Name:		arpd
Version:	1.0.2
Release:	1
License:	GPL
Group:		Applications/Networking
Group(pl):	Aplikacje/Sieciowe
Group(de):	Applikationen/Netzwerkwesen
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}-init
Patch0:		%{name}-%{version}.debian-patch
Patch1:		%{name}-%{version}.pld-patch
Prereq:		/sbin/chkconfig
Prereq:		rc-scripts >= 0.2.0
Prereq:		fileutils
#BuildRequires:	
BuildRoot:	%{tmpdir}/%{name}-%{version}.orig

%description
User-space arp daemon.
It requires kernel arpd support which isn't supported by standard 
PLD kernel. It shouldn't be run without that!!

%description -l pl
Demon arpd.
Standardowe j±dro ma organiczon± wielko¶æ tablicy arp do 255. Ten demon
likwiduje t± niedogodno¶æ wystêpuj±c± w du¿ych sieciach

Uwaga: wymaga arpd support, którego nie ma w standardowym j±drze PLD!!
Nie powinien byæ startowany bez tego!!

%prep
%setup  -q -n %{name}-%{version}.orig
%patch0 -p1
%patch1 -p1

%build

%{__make}

%install -n -n %{name}-%{version}
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{usr/sbin,etc/rc.d/init.d}
install arpd $RPM_BUILD_ROOT/usr/sbin/arpd
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/arpd

gzip -9nf CHANGES Copyright debian/*

%post
/sbin/chkconfig --add arpd
if [ ! -f /dev/arpd ]; then
	mknod /dev/arpd c 36 8 
fi
echo "Warning!!"
echo "You need arpd kernel support which isn't provided by standard PLD-kernel!!"
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


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%doc README.html debian/*
%attr(754,root,root) /usr/sbin/arpd
%attr(754,root,root) /etc/rc.d/init.d/arpd
