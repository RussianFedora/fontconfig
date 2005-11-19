%define freetype_version 2.1.4

Summary: Font configuration and customization library
Name: fontconfig
Version: 2.3.92.cvs20051119
Release: 1
License: MIT
Group: System Environment/Libraries
Source: http://fontconfig.org/release/fontconfig-%{version}.tar.gz
URL: http://fontconfig.org
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Source1: 40-blacklist-fonts.conf
Source2: 50-no-hint-fonts.conf

Patch1: fontconfig-2.3.91-defaultconfig.patch
Patch2: fontconfig-2.3.91-crosscheck.patch
Patch3: fontconfig-2.3.92-ft-internals.patch

BuildRequires: freetype-devel >= %{freetype_version}
BuildRequires: expat-devel
BuildRequires: perl
BuildRequires: docbook-utils-pdf >= 0.6.14
BuildRequires: elinks >= 0.10.3

PreReq: freetype >= %{freetype_version}
# Hebrew fonts referenced in fonts.conf changed names in fonts-hebrew-0.100
Conflicts: fonts-hebrew < 0.100
# Conflict with pre-modular X fonts, because they moved and we 
# reference the new path in %%configure
Conflicts: fonts-xorg-base, fonts-xorg-syriac

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
%setup -q

%patch1 -p1 -b .defaultconfig
%patch2 -p1 -b .crosscheck
%patch3 -p1 -b .ft-internals

%build
# Patch3 patches src/Makefile.am
automake
%configure --with-add-fonts=/usr/share/X11/fonts/Type1,/usr/share/X11/fonts/OTF

# Work around weird elinks bug where elinks refuses to open the
# temporary html file generated by jade because it thinks it's a
# special file.  Only happens in beehive.
export ELINKS_CONFDIR=$PWD/elinks-conf
mkdir -p $ELINKS_CONFDIR
echo "set protocol.file.allow_special_files = 1" > $ELINKS_CONFDIR/elinks.conf

make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d

# move installed doc files back to build directory to package themm
# in the right place
mv $RPM_BUILD_ROOT%{_docdir}/fontconfig/* .
rmdir $RPM_BUILD_ROOT%{_docdir}/fontconfig/

# All font packages depend on this package, so we create
# and own /usr/share/fonts
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts

# Remove unpackaged files
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

# Force regeneration of all fontconfig cache files
# The check for existance is needed on dual-arch installs (the second
#  copy of fontconfig might install the binary instead of the first)
# The redirect is because fc-cache is giving warnings about ~/fonts.cache-1
# The HOME setting is to avoid problems if HOME hasn't been reset
if [ -x /usr/bin/fc-cache ] ; then
  HOME=/root /usr/bin/fc-cache -f 2>/dev/null
fi

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%doc README AUTHORS COPYING 
%doc fontconfig-user.txt fontconfig-user.html
%{_libdir}/libfontconfig.so.*
%{_bindir}/fc-cache
%{_bindir}/fc-list
%{_bindir}/fc-match
%{_bindir}/fc-cat
%dir %{_sysconfdir}/fonts
%dir %{_sysconfdir}/fonts/conf.d
%dir %{_datadir}/fonts
%{_sysconfdir}/fonts/fonts.dtd
%config %{_sysconfdir}/fonts/fonts.conf
%config %{_sysconfdir}/fonts/conf.d/*.conf

%{_mandir}/man1/*
%{_mandir}/man5/*

%files devel
%defattr(-, root, root)
%doc fontconfig-devel.txt fontconfig-devel
%{_libdir}/libfontconfig.so
%{_libdir}/libfontconfig.a
%{_libdir}/pkgconfig
%{_includedir}/fontconfig
%{_mandir}/man3/*

%changelog
* Sat Nov 19 2005 Matthias Clasen <mclasen@redhat.com> - 2.3.92.cvs20051119-1
- Update to a newer cvs snapshot
- Don't use freetype internals

* Wed Nov 16 2005 Bill Nottingham <notting@redhat.com> - 2.3.93-3
- modular X moved fonts from /usr/X11R6/lib/X11/fonts to
  /usr/share/X11/fonts, adjust %%configure accordingly and 
  conflict with older font packages

* Wed Nov  9 2005 Carl Worth <cworth@redhat.com> - 2.3.92-2
- Remove inadvertent rejection of Luxi Mono from 40-blacklist-fonts.conf.
  Fixes #172437

* Fri Nov  4 2005 Matthias Clasen <mclasen@redhat.com> - 2.3.92-1
- Update to 2.3.92

* Fri Oct 31 2005 Matthias Clasen <mclasen@redhat.com> - 2.3.91.cvs20051031-1
- Update to a newer cvs snapshot
- Add a patch which should help to understand broken cache problems

* Fri Oct 21 2005 Matthias Clasen <mclasen@redhat.com> - 2.3.91.cvs20051017-2
- Add new Chinese fonts
- Fix the 40-blacklist-fonts.conf file to use the documented
  fonts.conf syntax, and exclude the Hershey fonts by family
  name.

* Fri Oct 14 2005 Matthias Clasen <mclasen@redhat.com> - 2.3.91.cvs20051017-1
- Update to the mmap branch of fontconfig

* Fri Jul 22 2005 Kristian Høgsberg <krh@redhat.com> - 2.3.2-1
- Update to fontconfig-2.3.2.  Drop

	fontconfig-2.1-slighthint.patch,
	fontconfig-2.2.3-timestamp.patch,
	fontconfig-2.2.3-names.patch,
	fontconfig-2.2.3-ta-pa-orth.patch, and
	fontconfig-2.2.3-timestamp.patch,

  as they are now merged upstream.

- Fold fontconfig-2.2.3-add-sazanami.patch into
  fontconfig-2.3.2-defaultconfig.patch and split rules to disable CJK
  hinting out into /etc/fonts/conf.d/50-no-hint-fonts.conf.

- Drop fontconfig-0.0.1.020826.1330-blacklist.patch and use the new
  rejectfont directive to reject those fonts in 40-blacklist-fonts.conf.

- Add fontconfig-2.3.2-only-parse-conf-files.patch to avoid parsing
  .rpmsave files.

- Renable s390 documentation now that #97079 has been fixed and add
  BuildRequires: for docbook-utils and docbook-utils-pdf.

- Drop code to iconv and custom install man pages, upstream does the
  right thing now.

- Add workaround from hell to make elinks cooperate so we can build
  txt documentation.

* Tue Apr 19 2005 David Zeuthen <davidz@redhat.com> - 2.2.3-13
- Add another font family name Sazanami Gothic/Mincho (#148748)

* Fri Mar  4 2005 David Zeuthen <davidz@redhat.com> - 2.2.3-12
- Rebuild

* Fri Mar  4 2005 David Zeuthen <davidz@redhat.com> - 2.2.3-11
- Rebuild

* Fri Mar  4 2005 David Zeuthen <davidz@redhat.com> - 2.2.3-10
- Rebuild

* Fri Mar  4 2005 David Zeuthen <davidz@redhat.com> - 2.2.3-9
- Disable docs for s390 for now

* Fri Mar  4 2005 David Zeuthen <davidz@redhat.com> - 2.2.3-8
- Rebuild

* Wed Dec  1 2004 Owen Taylor <otaylor@redhat.com> - 2.2.3-6
- Sleep a second before the exit of fc-cache to fix problems with fast 
  serial installs of fonts (#140335)
- Turn off hinting for Lohit Hindi/Bengali/Punjabi (#139816)

* Tue Oct 19 2004 Owen Taylor <otaylor@redhat.com> - 2.2.3-5
- Add Lohit fonts for Indic languages (#134492)
- Add Punjabi converage, fix Tamil coverage

* Wed Sep 22 2004 Owen Taylor <otaylor@redhat.com> - 2.2.3-4
- Update fonts-hebrew names to include CLM suffix

* Thu Sep  2 2004 Owen Taylor <otaylor@redhat.com> - 2.2.3-3
- Backport code from head branch of fontconfig CVS to parse names 
  for postscript fonts (fixes #127500, J. J. Ramsey)
- Own /usr/share/fonts (#110956, David K. Levine)
- Add KacstQura to serif/sans-serif/monospace aliases (#101182)

* Mon Aug 16 2004 Owen Taylor <otaylor@redhat.com> - 2.2.3-2
- Don't run fc-cache if the binary isn't there (#128072, tracked
  down by Jay Turner)

* Tue Aug  3 2004 Owen Taylor <otaylor@redhat.com> - 2.2.3-1
- Upgrade to 2.2.3
- Convert man pages to UTF-8 (#108730, Peter van Egdom)
- Renable docs on s390

* Mon Jul 26 2004 Owen Taylor <otaylor@redhat.com> - 2.2.1-12
- Rebuild for RHEL
- Back freetype required version down to 2.1.4

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Apr 19 2004 Owen Taylor <otaylor@redhat.com> 2.2.1-10
- Require recent freetype (#109592, Peter Oliver)
- Remove fonts.conf timestamp to fix multiarch conflict (#118182)
- Disable hinting for Mukti Narrow (#120915, Sayamindu Dasgupta)

* Wed Mar 10 2004 Owen Taylor <otaylor@redhat.com> 2.2.1-8.1
- Rebuild

* Wed Mar 10 2004 Owen Taylor <otaylor@redhat.com> 2.2.1-8.0
- Add Albany/Cumberland/Thorndale as fallbacks for Microsoft core fonts and 
  as non-preferred alternatives for Sans/Serif/Monospace
- Fix FreeType includes for recent FreeType

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Sep 22 2003 Owen Taylor <otaylor@redhat.com> 2.2.1-6.0
- Should have been passing --with-add-fonts, not --with-add-dirs to 
  configure ... caused wrong version of Luxi to be used. (#100862)

* Fri Sep 19 2003 Owen Taylor <otaylor@redhat.com> 2.2.1-5.0
- Tweak fonts.conf to get right hinting for CJK fonts (#97337)

* Tue Jun 17 2003 Bill Nottingham <notting@redhat.com> 2.2.1-3
- handle null config->cache correctly

* Thu Jun 12 2003 Owen Taylor <otaylor@redhat.com> 2.2.1-2
- Update default config to include Hebrew fonts (#90501, Dov Grobgeld)

* Tue Jun 10 2003 Owen Taylor <otaylor@redhat.com> 2.2.1-2
- As a workaround disable doc builds on s390

* Mon Jun  9 2003 Owen Taylor <otaylor@redhat.com> 2.2.1-1
- Version 2.2.1

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

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

