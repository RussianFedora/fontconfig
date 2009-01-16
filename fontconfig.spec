%define freetype_version 2.1.4

Summary: Font configuration and customization library
Name: fontconfig
Version: 2.6.90
Release: 2.git.63.g6bb4b9a%{?dist}
License: MIT
Group: System Environment/Libraries
Source: http://fontconfig.org/release/fontconfig-%{version}.tar.gz
URL: http://fontconfig.org
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Source1: 25-no-bitmap-fedora.conf

BuildRequires: gawk
BuildRequires: expat-devel
BuildRequires: freetype-devel >= %{freetype_version}
BuildRequires: perl

PreReq: freetype >= %{freetype_version}, coreutils
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
Requires: fontconfig = %{version}-%{release}
Requires: freetype-devel >= %{freetype_version}
Requires: pkgconfig

%description devel
The fontconfig-devel package includes the header files,
and developer docs for the fontconfig package.

Install fontconfig-devel if you want to develop programs which 
will use fontconfig.

%prep
%setup -q

%build

# We don't want to rebuild the docs, but we want to install the included ones.
export HASDOCBOOK=no

%configure --with-add-fonts=/usr/share/X11/fonts/Type1,/usr/share/X11/fonts/TTF,/usr/local/share/fonts

make
make check

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
ln -s ../conf.avail/25-unhint-nonlatin.conf $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d

# move installed doc files back to build directory to package themm
# in the right place
mv $RPM_BUILD_ROOT%{_docdir}/fontconfig/* .
rmdir $RPM_BUILD_ROOT%{_docdir}/fontconfig/

# All font packages depend on this package, so we create
# and own /usr/share/fonts
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts

# Remove unpackaged files
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

umask 0022

mkdir -p %{_localstatedir}/cache/fontconfig
# Remove stale caches
rm -f %{_localstatedir}/cache/fontconfig/????????????????????????????????.cache-2
rm -f %{_localstatedir}/cache/fontconfig/stamp

# Force regeneration of all fontconfig cache files
# The check for existance is needed on dual-arch installs (the second
#  copy of fontconfig might install the binary instead of the first)
# The HOME setting is to avoid problems if HOME hasn't been reset
if [ -x /usr/bin/fc-cache ] && /usr/bin/fc-cache --version 2>&1 | grep -q %{version} ; then
  HOME=/root /usr/bin/fc-cache -f
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
%dir %{_sysconfdir}/fonts/conf.avail
%dir %{_datadir}/fonts
%{_sysconfdir}/fonts/fonts.dtd
%config %{_sysconfdir}/fonts/fonts.conf
%doc %{_sysconfdir}/fonts/conf.d/README
%config %{_sysconfdir}/fonts/conf.avail/*.conf
%config(noreplace) %{_sysconfdir}/fonts/conf.d/*.conf
%dir %{_localstatedir}/cache/fontconfig

%{_mandir}/man1/*
%{_mandir}/man5/*

%files devel
%defattr(-, root, root)
%doc fontconfig-devel.txt fontconfig-devel
%{_libdir}/libfontconfig.so
%{_libdir}/pkgconfig/*
%{_includedir}/fontconfig
%{_mandir}/man3/*

%changelog
* Fri Jan 16 2009 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.90-2.git.63.g6bb4b9a
- Update to 2.6.90-1.git.63.g6bb4b9a
- Remove upstreamed patch

* Mon Oct 20 2008 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.0-3
- Add fontconfig-2.6.0-indic.patch
- Resolves: #464470

* Sat Jun 01 2008 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.0-2
- Fix build.

* Sat May 31 2008 Behdad Esfahbod <besfahbo@redhat.com> - 2.6.0-1
- Update to 2.6.0.

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.5.0-2
- Autorebuild for GCC 4.3

* Thu Nov 13 2007 Behdad Esfahbod <besfahbo@redhat.com> - 2.5.0-1
- Update to 2.5.0.

* Thu Nov 06 2007 Behdad Esfahbod <besfahbo@redhat.com> - 2.4.92-1
- Update to 2.4.92.
- Mark /etc/fonts/conf.d/* as config(noreplace).
- Remove most of our conf file, all upstreamed except for
  75-blacklist-fedora.conf that I'm happily dropping.  Who has
  Hershey fonts these days...
- ln upstream'ed 25-unhint-nonlatin.conf from conf.avail in conf.d
- Add 25-no-bitmap-fedora.conf which is the tiny remaining bit
  of conf that didn't end up upstream.  Can get rid of it in the
  future, but not just yet.

* Thu Oct 25 2007 Behdad Esfahbod <besfahbo@redhat.com> - 2.4.91-1
- Update to 2.4.91.
- Add /usr/local/share/fonts to default config. (#147004)
- Don't rebuild docs, to fix multilib conflicts. (#313011)
- Remove docbook and elinks BuildRequires and stuff as we don't
  rebuild docs.

* Wed Aug 22 2007 Adam Jackson <ajax@redhat.com> - 2.4.2-5
- Rebuild for PPC toolchain bug
- Add BuildRequires: gawk

* Sun Jun 17 2007 Matthias Clasen <mclasen@redhat.com> - 2.4.2-4
- /etc/fonts/conf.d is now owned by filesystem

* Fri May 11 2007 Matthias Clasen <mclasen@redhat.com> - 2.4.2-3
- Add Liberation fonts to 30-aliases-fedora.conf

* Fri Jan 12 2007 Behdad Esfahbod <besfahbo@redhat.com> - 2.4.2-2
- Change /usr/share/X11/fonts/OTF to /usr/share/X11/fonts/TTF
- Resolves: #220809

* Tue Dec  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.4.2-1
- Update to 2.4.2

* Wed Oct  4 2006 Matthias Clasen <mclasen@redhat.com> - 2.4.1-4
- Fix a multilib upgrade problem (#208151)

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.4.1-3
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.4.1-2
- Update 30-aliases-fedora.conf to correctly alias MS and StarOffice
  fonts. (#207460)

* Fri Sep 15 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.4.1-1
- Update to 2.4.1, a public API was dropped from 2.4.0
- Remove upstreamed patch

* Mon Sep 11 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.4.0-1
- Update to 2.4.0
- Rename/order our configuration stuff to match the new scheme.
  Breaks expected :-(

* Thu Sep 07 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.3.97-3
- Add missing file.  Previous update didn't go through

* Thu Sep 07 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.3.97-2
- Add fontconfig-2.3.97-ppc64.patch, for ppc64 arch signature

* Thu Sep 07 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.3.97-1
- update to 2.3.97
- Drop upstreamed patches
- Regenerate defaultconfig patch
- Don't touch stamp as it was not ever needed

* Thu Aug 17 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.3.95-11
- inclusion of zhong yi font and rearranged font prefer list. (bug# 201300)

* Fri Aug 11 2006 Ray Strode <rstrode@redhat.com> - 2.3.95-10
- use "%5x" instead of " %4x" to support 64k instead of
  clamping.  Idea from Behdad.

* Fri Aug 11 2006 Ray Strode <rstrode@redhat.com> - 2.3.95-9
- tweak last patch to give a more reasonable page size
  value if 64k page size is in effect.

* Fri Aug 11 2006 Ray Strode <rstrode@redhat.com> - 2.3.95-8
- maybe fix buffer overflow (bug 202152).

* Fri Aug 11 2006 Ray Strode <rstrode@redhat.com> - 2.3.95-7
- Update configs to provide better openoffice/staroffice
  compatibility (bug 200723)

* Thu Jul 27 2006 Behdad Esfahbod <besfahbo@redhat.com> - 2.3.95-6
- Do umask 0022 in post
- Update configs to reflect addition of new Indic fonts (#200381, #200397)

* Tue Jul 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.95-5
- Plug a small memory leak

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.3.95-4.1.1
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.3.95-4.1
- rebuild

* Fri Jun  2 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.95-4
- Fix the handling of TTF font collections

* Thu May 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.95-3
- Apply a patch by David Turner to speed up cache generation

* Wed Apr 26 2006 Bill Nottingham <notting@redhat.com> - 2.3.95-2
- fix fonts.conf typo

* Wed Apr 26 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.95-1
- Update to 2.3.95

* Fri Feb 24 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.94-1
- Update to 2.3.94

* Wed Feb 11 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.93.cvs20060211-1
- Newer cvs snapshot

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.3.93.cvs20060208-1.1
- bump again for double-long bug on ppc(64)

* Wed Feb  8 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.93.cvs20060208-1
- Newer cvs snapshot

* Tue Feb  7 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.93.cvs20060207-1
- Newer cvs snapshot
- Drop upstreamed patches, pick up some new ones

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.3.93.cvs20060131-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb  2 2006 Ray Strode <rstrode@redhat.com> - 2.3.93.cvs20060131-3
- Move user cache to a subdirectory (bug 160275)

* Thu Feb  2 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.93.cvs20060131-2
- Accumulated patches

* Tue Jan 31 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.93.cvs20060131-1
- Newer cvs snapshot

* Tue Jan 24 2006 Matthias Clasen <mclasen@redhat.com> - 2.3.93.cvs20060124-1
- Newer cvs snapshot

* Tue Jan 17 2006 Ray Strode <rstrode@redhat.com> - 2.3.93-4
- apply patch from Tim Mayberry to correct aliasing and disable
  hinting for the two Chinese font names AR PL ShanHeiSun Uni 
  and AR PL Zenkai Uni

* Tue Jan 10 2006 Bill Nottingham <notting@redhat.com> - 2.3.93-3
- prereq coreutils for mkdir/touch in %%post

* Wed Dec 21 2005 Carl Worth <cworth@redhat.com> - 2.3.93-2
- Fix to create /var/cache/fontconfig/stamp in the post install stage.

* Wed Dec 21 2005 Carl Worth <cworth@redhat.com> - 2.3.93-1
- New upstream version.

* Tue Dec 13 2005 Carl Worth <cworth@redhat.com> - 2.3.92.cvs20051129-3
- Disable hinting for Lohit Gujarati

* Fri Dec  9 2005 Carl Worth <cworth@redhat.com> - 2.3.92.cvs20051129-2
- Add two new Chinese font names to the default fonts.conf file:
  	AR PL ShanHeiSun Uni
  	AR PL Zenkai Uni

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Nov 28 2005 Matthias Clasen <mclasen@redhat.com> - 2.3.92.cvs20051129-1
- Update to a newer cvs snapshot

* Sat Nov 19 2005 Matthias Clasen <mclasen@redhat.com> - 2.3.92.cvs20051119-1
- Update to a newer cvs snapshot

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

