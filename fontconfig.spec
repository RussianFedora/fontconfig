%define fcpackage_version rc3
%define relno 020826.1330

%define freetype_version 2.1.2-2

Summary: Font configuration and customization library
Name: fontconfig
Version: 0.0.1.%{relno}
Release: 1
License: MIT
Group: System Environment/Libraries
Source: http://keithp.com/fonts/pub/fcpackage.%{fcpackage_version}.tar.gz
URL: http://keithp.com/fonts
BuildRoot: %{_tmppath}/fontconfig-%{PACKAGE_VERSION}-root
Patch1: fontconfig-0.0.1.020811.1151-defaultconfig.patch
Patch4: fontconfig-0.0.1.020811.1151-slighthint.patch
# Only look in /usr/X11R6/lib/fonts/Type1, not in
# all of /usr/X11R6/lib/fonts.
Patch5: fontconfig-0.0.1.020626.1517-fontdir.patch
# Fix groff errors with fontconfig.man
Patch9: fontconfig-0.0.1.020811.1151-manfix.patch

BuildRequires: freetype-devel >= %{freetype_version}
BuildRequires: expat-devel

PreReq: freetype >= %{freetype_version}

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

%prep
%setup -q -n fcpackage.%{fcpackage_version}/fontconfig

%patch1 -p1 -b .defaultconfig
%patch4 -p1 -b .slighthint
%patch5 -p1 -b .fontdir
%patch9 -p1 -b .manfix

%build

# flockfile patch changes configure.in
autoconf
%configure
make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT 
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3
install -m 0644 src/fontconfig.man $RPM_BUILD_ROOT%{_mandir}/man3/fontconfig.3

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

# Force regeneration of all fontconfig cache files.
# The redirect is because fc-cache is giving warnings about ~/fc.cache
# the HOME setting is to avoid problems if HOME hasn't been reset
HOME=/root fc-cache -f 2>/dev/null

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc README AUTHORS COPYING
%{_libdir}/libfontconfig.so.*
%{_bindir}/fc-cache
%{_bindir}/fc-list
%dir %{_sysconfdir}/fonts
%{_sysconfdir}/fonts/fonts.dtd
%config %{_sysconfdir}/fonts/fonts.conf

%files devel
%defattr(-, root, root)
%{_libdir}/libfontconfig.so
%{_libdir}/pkgconfig
%{_includedir}/fontconfig
%{_bindir}/fontconfig-config
%{_mandir}/man3/fontconfig.3*

%changelog
* Mon Aug 26 2002 Owen Taylor <otaylor@redhat.com>
- Upgrade to fcpackage rc3

* Wed Aug 21 2002 Owen Taylor <otaylor@redhat.com>
- Add an explicit PreReq for freetype
- Move fonts we don't ship to the end of the fonts.conf aliases so
  installing them doesn't change the look.

* Wed Aug 21 2002 Owen Taylor <otaylor@redhat.com>
- Memory leak fix when parsing config files
- Set rh_prefer_bitmaps for .ja fonts to key off of in Xft
- Fix some groff warnings for fontconfig.man (#72138)

* Thu Aug 15 2002 Owen Taylor <otaylor@redhat.com>
- Try once more to get the right default Sans-serif font :-(
- Switch the Sans/Monospace aliases for Korean to Gulim, not Dotum

* Wed Aug 14 2002 Owen Taylor <otaylor@redhat.com>
- Fix %%post

* Tue Aug 13 2002 Owen Taylor <otaylor@redhat.com>
- Fix lost Luxi Sans default

* Mon Aug 12 2002 Owen Taylor <otaylor@redhat.com>
- Upgrade to rc2
- Turn off hinting for all CJK fonts
- Fix typo in %%post
- Remove the custom language tag stuff in favor of Keith's standard 
  solution.

* Mon Jul 15 2002 Owen Taylor <otaylor@redhat.com>
- Prefer Luxi Sans to Nimbus Sans again

* Fri Jul 12 2002 Owen Taylor <otaylor@redhat.com>
- Add FC_HINT_STYLE to FcBaseObjectTypes
- Switch Chinese fonts to always using Sung-ti / Ming-ti, and never Kai-ti
- Add ZYSong18030 to aliases (#68428)

* Wed Jul 10 2002 Owen Taylor <otaylor@redhat.com>
- Fix a typo in the langtag patch (caught by Erik van der Poel)

* Wed Jul  3 2002 Owen Taylor <otaylor@redhat.com>
- Add FC_HINT_STYLE tag

* Thu Jun 27 2002 Owen Taylor <otaylor@redhat.com>
- New upstream version, with fix for problems with
  ghostscript-fonts (Fonts don't work for Qt+CJK,
  etc.)

* Wed Jun 26 2002 Owen Taylor <otaylor@redhat.com>
- New upstream version, fixing locale problem

* Mon Jun 24 2002 Owen Taylor <otaylor@redhat.com>
- Add a hack where we set the "language" fontconfig property based on the locale, then 
  we conditionalize base on that in the fonts.conf file.

* Sun Jun 23 2002 Owen Taylor <otaylor@redhat.com>
- New upstream version

* Tue Jun 18 2002 Owen Taylor <otaylor@redhat.com>
- Fix crash from FcObjectSetAdd

* Tue Jun 11 2002 Owen Taylor <otaylor@redhat.com>
- make fonts.conf %%config, not %%config(noreplace)
- Another try at the CJK aliases
- Add some CJK fonts to the config
- Prefer Luxi Mono to Nimbus Mono

* Mon Jun 10 2002 Owen Taylor <otaylor@redhat.com>
- New upstream version
- Fix matching for bitmap fonts

* Mon Jun  3 2002 Owen Taylor <otaylor@redhat.com>
- New version, new upstream mega-tarball

* Tue May 28 2002 Owen Taylor <otaylor@redhat.com>
- Fix problem with FcConfigSort

* Fri May 24 2002 Owen Taylor <otaylor@redhat.com>
- Initial specfile

