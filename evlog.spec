# TODO: PLDify init scripts
Summary:	Linux Event Logging for Enterprise-Class Systems
Summary(pl.UTF-8):	Linuksowe logowanie zdarzeń dla systemów klasy enterprise
Name:		evlog
Version:	1.6.1
Release:	0.1
License:	LGPL v2.1+ (library), GPL v2+ (utils)
Group:		Libraries
Source0:	http://downloads.sourceforge.net/evlog/%{name}-%{version}.tar.gz
# Source0-md5:	b4cf6d696c827bf72b67532950c3bf9f
#Patch0:		%{name}-ksyms2.4.patch
Patch0:		%{name}-am.patch
Patch1:		%{name}-gcc.patch
Patch2:		%{name}-glibc.patch
Patch3:		%{name}-nptl.patch
Patch4:		%{name}-link.patch
Patch5:		%{name}-linux.patch
URL:		http://evlog.sourceforge.net/
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	binutils-devel
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
evlog provides an open-source, platform-independent Event Logging
facility for the Linux Operating system and Linux applications, that
offers capabilities and features required in medium-to-large
Enterprise-class systems.

%description -l pl.UTF-8
evlog dostarcza mającą otwarty kod źródłowy, niezależną od platformy
funkcjonalność logowaniem zdarzeń dla systemu operacyjnego Linux i
aplikacji linuksowych, oferujące możliwości i cechy potrzebne w
średnich i dużych systemach klasy enterprise.

%package devel
Summary:	Header files for evlog libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek evlog
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for evlog libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek evlog.

%package static
Summary:	Static evlog libraries
Summary(pl.UTF-8):	Statyczne biblioteki evlog
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static evlog libraries.

%description static -l pl.UTF-8
Statyczne biblioteki evlog.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%{__sed} -i -e 's/yacc/bison -y/' user/lib/query/Makefile.am

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
# plugins path is ${optdir}/evlog/plugins, so pass %{_libdir}
%configure \
	--with-initdir=/etc/rc.d/init.d \
	--with-localstatedir=/var/lib/evlog \
	--with-optdir=%{_libdir}
%{__make}

%{__make} -C user/cmd/evlogd/tcp_rmtlog_be
%{__make} -C user/cmd/evlogd/udp_rmtlog_be

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C user/cmd/evlogd/tcp_rmtlog_be install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C user/cmd/evlogd/udp_rmtlog_be install \
	DESTDIR=$RPM_BUILD_ROOT

# move devel part to /usr
mv -f $RPM_BUILD_ROOT/%{_lib}/libevlsyslog.{a,la} $RPM_BUILD_ROOT%{_libdir}
%{__rm} $RPM_BUILD_ROOT/%{_lib}/libevlsyslog.so
ln -sf /%{_lib}/libevlsyslog.so.0.0.0 $RPM_BUILD_ROOT%{_libdir}/libevlsyslog.so
%{__sed} -i -e "s,^libdir='/%{_lib}',libdir='%{_libdir}'," $RPM_BUILD_ROOT%{_libdir}/libevlsyslog.la
# dlopened modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/evlog/plugins/*.{la,a}

%{__mv} $RPM_BUILD_ROOT%{_docdir}/{packages/evlog,evlog}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES INSTALL README README.ela
%attr(755,root,root) /sbin/ela_*
%attr(755,root,root) /sbin/evl*
%attr(755,root,root) /sbin/slog_fwd
%attr(755,root,root) /%{_lib}/libevlsyslog.so.*.*.*
%attr(755,root,root) %ghost /%{_lib}/libevlsyslog.so.0
%attr(755,root,root) %{_libdir}/libevl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libevl.so.0
%dir %{_libdir}/evlog
%dir %{_libdir}/evlog/plugins
%attr(755,root,root) %{_libdir}/evlog/plugins/tcp_rmtlog_be.so
%attr(755,root,root) %{_libdir}/evlog/plugins/udp_rmtlog_be.so
%attr(755,root,root) %{_datadir}/evlog
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/evlogmgr.cron
%dir %{_sysconfdir}/evlog.d
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/evlog.d/action_profile
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/evlog.d/action_registry
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/evlog.d/evlhosts
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/evlog.d/evlog.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/evlog.d/evlogrmtd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/evlog.d/facility_registry
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/evlog.d/libevlsyslog.conf
%dir %{_sysconfdir}/evlog.d/plugins
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/evlog.d/plugins/tcp_rmtlog_be.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/evlog.d/plugins/udp_rmtlog_be.conf
%attr(754,root,root) /etc/rc.d/init.d/evlaction
%attr(754,root,root) /etc/rc.d/init.d/evlnotify
%attr(754,root,root) /etc/rc.d/init.d/evlog
%attr(754,root,root) /etc/rc.d/init.d/evlogrmt
%attr(750,root,root) /var/lib/evlog
%{_mandir}/man1/evl*.1*
%dir %{_docdir}/evlog
%{_docdir}/evlog/templates

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libevlsyslog.so
%attr(755,root,root) %{_libdir}/libevl.so
%{_libdir}/libevlsyslog.la
%{_libdir}/libevl.la
%{_includedir}/evl*.h
%{_includedir}/posix_evl*.h
%{_includedir}/linux/evl_log.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libevlsyslog.a
%{_libdir}/libevl.a
