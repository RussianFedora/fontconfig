%define fcpackage_version 2_1
%define relno %(echo %fcpackage_version | sed -e 's#_#.#')

%define freetype_version 2.1.2-7

Summary: Font configuration and customization library
Name: fontconfig
Version: %relno
Release: 9
License: MIT
Group: System Environment/Libraries
Source: http://fontconfig.org/release/fcpackage.%{fcpackage_version}.tar.gz
URL: http://fontconfig.org
BuildRoot: %{_tmppath}/%{name}-%{version}-root

Patch1: fontconfig-2.0-defaultconfig.patch
Patch4: fontconfig-2.1-slighthint.patch
# Remove /usr/X11R6 dirs from fonts.conf, we'll add them back
Patch5: fontconfig-fontdir.patch
# Blacklist certain fonts that freetype can't handle
Patch11: fontconfig-0.0.1.020826.1330-blacklist.patch
# Fix caching of directories 
# (http://www.fontconfig.org/cgi-bin/bugzilla/show_bug.cgi?id=8)
Patch12: fontconfig-2.1-dircache.patch
# Ignore .fulldir entries from earlier versions 'dircache' fix.
Patch13: fontconfig-2.1-fulldir.patch

BuildRequires: freetype-devel >= %{freetype_version}
BuildRequires: expat-devel
BuildRequires: perl

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
%patch5 -p1 -b .slighthint
%patch11 -p1 -b .blacklist
%patch12 -p1 -b .dircache
%patch13 -p1 -b .fulldir

%build

%configure
make

# Only look for fonts in the Type1/OTF subdirectories
# of /usr/X11R6/lib/fonts; the fonts in the TTF directory 
# duplicate those in the Type1 directory
perl -ni -e '
if (m@^\s+<dir>/usr/share/fonts</dir>\s+$@) {
  for $i (qw(/usr/share/fonts /usr/X11R6/lib/X11/fonts/Type1 /usr/X11R6/lib/X11/fonts/OTF)) {
    print "\t<dir>$i</dir>\n";
  }
} else {
  print;
}' fonts.conf

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
%{_mandir}/man3/fontconfig.3*

%files devel
%defattr(-, root, root)
%{_libdir}/libfontconfig.so
%{_libdir}/pkgconfig
%{_includedir}/fontconfig
%{_bindir}/fontconfig-config

%changelog
* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- debuginfo rebuild

* Mon Feb 24 2003 Owen Taylor <otaylor@redhat.com> 2.1-8
- Fix segfault in fc-cache from .dircache patch

* Mon Feb 24 2003 Owen Taylor <otaylor@redhat.com>
- Back out patch that wrote fonts.conf entries that crash RH-8.0 
  gnome-terminal, go with patch from fontconfig CVS instead.
  (#84863)

* Tue Feb 11 2003 Owen Taylor <otaylor@redhat.com>
- Move fontconfig man page to main package, since it contains non-devel 
  information (#76189)
- Look in the OTF subdirectory of /usr/X11R6/lib/fonts as well
  so we find Syriac fonts (#82627)

* Thu Feb  6 2003 Matt Wilson <msw@redhat.com> 2.1-5
- modified fontconfig-0.0.1.020626.1517-fontdir.patch to hard code
  /usr/X11R6/lib/X11/fonts instead of using $(X_FONT_DIR).  This is
  because on lib64 machines, fonts are not in /usr/X11R6/lib64/....

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Owen Taylor <otaylor@redhat.com>
- Try a different tack when fixing cache problem

* Tue Jan 14 2003 Owen Taylor <otaylor@redhat.com>
- Try to fix bug where empty cache entries would be found in 
  ~/.fonts.cache-1 during scanning (#81335)

* Thu Nov 21 2002 Mike A. Harris <mharris@redhat.com> 2.1-1
- Updated to version 2.1
- Updated slighthint patch to fontconfig-2.1-slighthint.patch
- Updated freetype version required to 2.1.2-7

* Mon Sep  2 2002 Owen Taylor <otaylor@redhat.com>
- Version 2.0
- Correct capitalization/spacing for ZYSong18030 name (#73272)

* Fri Aug 30 2002 Owen Taylor <otaylor@redhat.com>
- Blacklist fonts from ghostscript-fonts that don't render correctly

* Mon Aug 26 2002 Owen Taylor <otaylor@redhat.com>
- Upgrade to fcpackage rc3
- Fix bug in comparisons for xx_XX language tags
- Compensate for a minor config file change in rc3

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

