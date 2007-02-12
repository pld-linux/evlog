Summary:	Linux Event Logging for Enterprise-Class Systems
Summary(pl.UTF-8):   Linuksowe logowanie zdarzeń dla systemów klasy enterprise
Name:		evlog
Version:	1.6.0
%define	bver	alpha
Release:	0.%{bver}.0.1
License:	LGPL (library), GPL (utils)
Group:		Libraries
Source0:	http://dl.sourceforge.net/evlog/%{name}-%{version}-%{bver}.tar.gz
# Source0-md5:	47142eabd0fdf59faf6b28cd5a748e45
Patch0:		%{name}-ksyms2.4.patch
URL:		http://evlog.sourceforge.net/
BuildRequires:	binutils-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
evlog provides an open-source, platform-independent Event Logging
facility for the Linux Operating system and Linux applications, that
offers capabilities and features required in medium-to-large
Enterprise-class systems.

%description -l pl.UTF-8
evlog dostarcza oparte o otwarty kod źródłowy, niezależne od platformy
udogodnienia związane z logowaniem zdarzeń dla systemu operacyjnego
Linux i aplikacji linuksowych, oferujące możliwości i cechy potrzebne
w średnich i dużych systemach klasy enterprise.

%package devel
Summary:	Header files for evlog libraries
Summary(pl.UTF-8):   Pliki nagłówkowe bibliotek evlog
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for evlog libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek evlog.

%package static
Summary:	Static evlog libraries
Summary(pl.UTF-8):   Statyczne biblioteki evlog
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static evlog libraries.

%description static -l pl.UTF-8
Statyczne biblioteki evlog.

%prep
%setup -q
%patch0 -p1

%build
#%{__libtoolize}
#%{__aclocal}
#%{__autoconf}
#%{__autoheader}
#%{__automake}
# plugins path is ${optdir}/evlog/plugins, so pass %{_libdir}
%configure \
	--with-localstatedir=/var/lib \
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

mv -f $RPM_BUILD_ROOT/%{_lib}/libevlsyslog.{a,la} $RPM_BUILD_ROOT%{_libdir}
ln -sf /%{_lib}/libevlsyslog.so.0.0.0 $RPM_BUILD_ROOT%{_libdir}/libevlsyslog.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES INSTALL README README.ela
%attr(755,root,root) /sbin/*
%attr(755,root,root) /%{_lib}/libevlsyslog.so.*.*.*
%attr(755,root,root) %{_libdir}/libevl.so.*.*.*
%dir %{_libdir}/evlog
%dir %{_libdir}/evlog/plugins
%attr(755,root,root) %{_libdir}/evlog/plugins/*.so
%attr(755,root,root) %{_datadir}/evlog
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/cron.d/evlogmgr.cron
%attr(755,root,root) %dir %{_sysconfdir}/evlog.d
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/evlog.d/*
%attr(754,root,root) /etc/rc.d/init.d/evl*
%attr(750,root,root) /var/lib/evlog
%{_mandir}/man1/evl*.1*

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
