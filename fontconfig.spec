%define fcpackage_version 02-06-03.01-31
%define relno 020603.0131

%define freetype_version 2.0.9

Summary: Font configuration and customization library
Name: fontconfig
Version: 0.0.1.%{relno}
Release: 3
License: MIT
Group: System Environment/Libraries
Source: http://keithp.com/fonts/pub/fcpackage.%{fcpackage_version}.tar.gz
URL: http://keithp.com/fonts
BuildRoot: %{_tmppath}/fontconfig-%{PACKAGE_VERSION}-root

BuildRequires: freetype-devel >= %{freetype_version}
BuildRequires: expat-devel

%description
Fontconfig is designed to locate fonts within the
system and select them according to requirements specified by 
applications.

%package devel
Summary: Font configuration and customization library
Group: Development/Libraries
Requires: fontconfig = %{PACKAGE_VERSION}
Requires: freetype-devel >= %{freetype_version}

%description devel
The fontconfig-devel package includes the header files,
and developer docs for the fontconfig package.

Install fontconfig-devel if you want to develop programs which 
will use fontconfig.

%changelog
* Fri Jun 07 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Mon Jun  3 2002 Owen Taylor <otaylor@redhat.com>
- New version, new upstream mega-tarball

* Tue May 28 2002 Owen Taylor <otaylor@redhat.com>
- Fix problem with FcConfigSort

* Fri May 24 2002 Owen Taylor <otaylor@redhat.com>
- Initial specfile

%prep
%setup -n fcpackage.%{fcpackage_version}/fontconfig

%build

%configure
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT 
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3
install -m 0644 src/fontconfig.man $RPM_BUILD_ROOT%{_mandir}/man3/fontconfig.3

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc README AUTHORS COPYING
%{_libdir}/libfontconfig.so.*
%{_bindir}/fc-cache
%{_bindir}/fc-list
%dir %{_sysconfdir}/fonts
%{_sysconfdir}/fonts/fonts.dtd
%config(noreplace) %{_sysconfdir}/fonts/fonts.conf

%files devel
%defattr(-, root, root)
%{_libdir}/libfontconfig.so
%{_libdir}/pkgconfig
%{_includedir}/fontconfig
%{_bindir}/fontconfig-config
%{_mandir}/man3/fontconfig.3*
