%{?scl:%scl_package perl-YAML}

Name:           %{?scl_prefix}perl-YAML
Version:        1.18
Release:        2%{?dist}
Summary:        YAML Ain't Markup Language (tm)
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/YAML/
Source0:        http://search.cpan.org/CPAN/authors/id/T/TI/TINITA/YAML-%{version}.tar.gz
BuildArch:      noarch
# Module Build
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  %{?scl_prefix}perl
BuildRequires:  %{?scl_prefix}perl-generators
BuildRequires:  %{?scl_prefix}perl(ExtUtils::MakeMaker) > 6.75
# Module Runtime
BuildRequires:  %{?scl_prefix}perl(Carp)
BuildRequires:  %{?scl_prefix}perl(constant)
BuildRequires:  %{?scl_prefix}perl(Exporter)
BuildRequires:  %{?scl_prefix}perl(overload)
BuildRequires:  %{?scl_prefix}perl(strict)
BuildRequires:  %{?scl_prefix}perl(warnings)
# Test Suite
# Avoid circular build deps Test::YAML → Test::Base → YAML when bootstrapping
# Test::YAML and its dependencies are too big, skip them on perl_small.
%if !%{defined perl_bootstrap} && !%{defined perl_small}
BuildRequires:  %{?scl_prefix}perl(B::Deparse)
BuildRequires:  %{?scl_prefix}perl(Data::Dumper)
BuildRequires:  %{?scl_prefix}perl(File::Find)
BuildRequires:  %{?scl_prefix}perl(lib)
BuildRequires:  %{?scl_prefix}perl(Test::More) >= 0.88
BuildRequires:  %{?scl_prefix}perl(Test::Pod) >= 1.41
BuildRequires:  %{?scl_prefix}perl(Test::YAML) >= 1.05
BuildRequires:  %{?scl_prefix}perl(utf8)
%endif
# Runtime
Requires:       %{?scl_prefix}perl(:MODULE_COMPAT_%(%{?scl:scl enable %{scl} '}eval "$(perl -V:version)";echo $version%{?scl:'}))
Requires:       %{?scl_prefix}perl(Carp)

# Filter private provides:
# perl(yaml_mapping) perl(yaml_scalar) perl(yaml_sequence)
%if 0%{?rhel} < 7
# RPM 4.8 style
%{?filter_setup:
%filter_from_provides /^%{?scl_prefix}perl(yaml_/d
%?perl_default_filter
}
%else
# RPM 4.9 style
%global __provides_exclude ^%{?scl_prefix}perl\\(yaml_
%endif

%description
The YAML.pm module implements a YAML Loader and Dumper based on the
YAML 1.0 specification. http://www.yaml.org/spec/
YAML is a generic data serialization language that is optimized for
human readability. It can be used to express the data structures of
most modern programming languages, including Perl.
For information on the YAML syntax, please refer to the YAML
specification.

%prep
%setup -q -n YAML-%{version}

%build
%{?scl:scl enable %{scl} '}perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 && make %{?_smp_mflags}%{?scl:'}

%install
%{?scl:scl enable %{scl} '}make install DESTDIR=%{buildroot}%{?scl:'}

%check
# Avoid circular build deps Test::YAML → Test::Base → YAML when bootstrapping
%if !%{defined perl_bootstrap} && !%{defined perl_small}
%{?scl:scl enable %{scl} '}make test%{?scl:'}
%endif

%files
%doc LICENSE
%doc Changes CONTRIBUTING README
%dir %{perl_vendorlib}/YAML/
%dir %{perl_vendorlib}/YAML/Dumper/
%dir %{perl_vendorlib}/YAML/Loader/
%doc %{perl_vendorlib}/YAML.pod
%doc %{perl_vendorlib}/YAML/Any.pod
%doc %{perl_vendorlib}/YAML/Dumper.pod
%doc %{perl_vendorlib}/YAML/Dumper/Base.pod
%doc %{perl_vendorlib}/YAML/Error.pod
%doc %{perl_vendorlib}/YAML/Loader.pod
%doc %{perl_vendorlib}/YAML/Loader/Base.pod
%doc %{perl_vendorlib}/YAML/Marshall.pod
%doc %{perl_vendorlib}/YAML/Node.pod
%doc %{perl_vendorlib}/YAML/Tag.pod
%doc %{perl_vendorlib}/YAML/Types.pod
%{perl_vendorlib}/YAML.pm
%{perl_vendorlib}/YAML/Any.pm
%{perl_vendorlib}/YAML/Dumper.pm
%{perl_vendorlib}/YAML/Dumper/Base.pm
%{perl_vendorlib}/YAML/Error.pm
%{perl_vendorlib}/YAML/Loader.pm
%{perl_vendorlib}/YAML/Loader/Base.pm
%{perl_vendorlib}/YAML/Marshall.pm
%{perl_vendorlib}/YAML/Mo.pm
%{perl_vendorlib}/YAML/Node.pm
%{perl_vendorlib}/YAML/Tag.pm
%{perl_vendorlib}/YAML/Types.pm
%{_mandir}/man3/YAML.3*
%{_mandir}/man3/YAML::Any.3*
%{_mandir}/man3/YAML::Dumper.3*
%{_mandir}/man3/YAML::Dumper::Base.3*
%{_mandir}/man3/YAML::Error.3*
%{_mandir}/man3/YAML::Loader.3*
%{_mandir}/man3/YAML::Loader::Base.3*
%{_mandir}/man3/YAML::Marshall.3*
%{_mandir}/man3/YAML::Node.3*
%{_mandir}/man3/YAML::Tag.3*
%{_mandir}/man3/YAML::Types.3*

%changelog
* Tue Jul 12 2016 Petr Pisar <ppisar@redhat.com> - 1.18-2
- SCL

* Sat Jul  9 2016 Paul Howarth <paul@city-fan.org> - 1.18-1
- Update to 1.18
  - List Test::More as a prereq (GH#161)

* Wed Jul  6 2016 Paul Howarth <paul@city-fan.org> - 1.17-1
- Update to 1.17
  - Use Mo 0.40
- This release by TINITA → update source URL

* Sun Jul  3 2016 Paul Howarth <paul@city-fan.org> - 1.16-1
- Update to 1.16
  - Drop inconsistent $VERSION from YAML::Mo (GH#158)
- BR: perl-generators

* Wed May 18 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-7
- Perl 5.24 re-rebuild of bootstrapped packages

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-6
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-3
- Perl 5.22 re-rebuild of bootstrapped packages

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 1.15-2
- Perl 5.22 rebuild

* Mon Apr 20 2015 Paul Howarth <paul@city-fan.org> - 1.15-1
- Update to 1.15
  - Don't require newlines at end of YAML (GH#149)

* Mon Jan 26 2015 Paul Howarth <paul@city-fan.org> - 1.14-1
- Update to 1.14
  - Add support for QuoteNumericStrings global setting (PR/145)

* Sun Oct 12 2014 Paul Howarth <paul@city-fan.org> - 1.13-1
- Update to 1.13
  - Disable some warnings in YAML::Any (PR/140)

* Wed Sep 24 2014 Paul Howarth <paul@city-fan.org> - 1.12-1
- Update to 1.12
  - Fix parsing of unquoted strings (CPAN RT#97870)
- Classify buildreqs by usage

* Sun Sep 07 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-3
- Perl 5.20 re-rebuild of bootstrapped packages

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.11-2
- Perl 5.20 rebuild

* Tue Sep  2 2014 Paul Howarth <paul@city-fan.org> - 1.11-1
- Update to 1.11
  - Apply PR/139:
    -  Remove die() that can't be called (regex always matches)

* Fri Aug 29 2014 Paul Howarth <paul@city-fan.org> - 1.10-1
- Update to 1.10
  - Apply PR/138:
    - Report an error message mentioning indentation when choking on non-space
      indentation
    - die() should be called as a method of $self

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.09-2
- Perl 5.20 rebuild

* Tue Aug 26 2014 Paul Howarth <paul@city-fan.org> - 1.09-1
- Update to 1.09
  - Add t/000-compile-modules.t
  - Eliminate File::Basename from test/
  - Eliminate spurious trailing whitespace
  - Meta 0.0.2
  - Change testdir to t
  - Add doc examples for YAML::Any (PR/8)
  - Dep on Test::YAML 1.05
  - Replace tabs with spaces

* Tue Aug 12 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1.01-2
- Disable tests when bootstrapping

* Fri Aug  8 2014 Paul Howarth <paul@city-fan.org> - 1.01-1
- Update to 1.01
  - Depend on patched Test::YAML

* Fri Aug  8 2014 Paul Howarth <paul@city-fan.org> - 1.00-1
- Update to 1.00
  - Switch to external Test::Base
  - Fix bad encoding in Pod
- Test::YAML is now unbundled
- Take advantage of new features in recent EU::MM to simplify spec

* Thu Jul 31 2014 Paul Howarth <paul@city-fan.org> - 0.98-1
- Update to 0.98
  - Fix indexing of YAML::Any
  - Change IRC to irc.perl.org#yaml
- Use %%license
- Drop workaround for #1115971

* Thu Jul 17 2014 Paul Howarth <paul@city-fan.org> - 0.97-1
- Update to 0.97
  - Move remaining docs to Swim
- Upstream reinstated all those pod files and manpages again

* Mon Jul 14 2014 Paul Howarth <paul@city-fan.org> - 0.96-1
- Update to 0.96
  - Fix Metadata and add Contributing file
  - Change Kwim to Swim
- Upstream dropped all those pod files and manpages again

* Thu Jul 03 2014 Petr Pisar <ppisar@redhat.com> - 0.95-2
- Inject VERSION into each module (bug #1115971)

* Mon Jun 23 2014 Paul Howarth <paul@city-fan.org> - 0.95-1
- Update to 0.95
  - Fix dumping blessed globs

* Sun Jun 15 2014 Paul Howarth <paul@city-fan.org> - 0.94-1
- Update to 0.94
  - Switch to Zilla::Dist
  - Add badges to doc
  - Fix regression introduced with earlier fix for complex regular
    subexpression recursion limit (GH#18)
  - Fix reference to non-existent sub Carp::Croak (GH#19)
- Enumerate all files so we can mark POD files as %%doc
- Bump Test::More version requirement to 0.88 due to use of done_testing

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.92-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Petr Pisar <ppisar@redhat.com> - 0.92-2
- Do not run release tests on bootstrap (bug #1104137)

* Thu May 29 2014 Paul Howarth <paul@city-fan.org> 0.92-1
- Update to 0.92
  - Metadata fixes (https://github.com/ingydotnet/yaml-pm/pull/23)

* Wed May 28 2014 Paul Howarth <paul@city-fan.org> - 0.91-1
- Update to 0.91
  - Force escaping of single '-'
    (https://github.com/ingydotnet/yaml-pm/pull/22)

* Fri Feb 28 2014 Paul Howarth <paul@city-fan.org> - 0.90-2
- Avoid circular build deps via Module::Build when bootstrapping

* Tue Feb 11 2014 Paul Howarth <paul@city-fan.org> - 0.90-1
- Update to 0.90
  - Revert Mo from 0.38 to 0.31 following a report of it breaking cpan client

* Mon Feb 10 2014 Paul Howarth <paul@city-fan.org> - 0.89-1
- Update to 0.89
  - Synopsis in YAML::Dumper didn't work as expected (CPAN RT#19838)
  - Address complex regular subexpression recursion limit (CPAN RT#90593)
  - Use latest Test::Builder (CPAN RT#90847)
  - Fixed tests to work under parallel testing
  - Switched to dzil release process
- This release by INGY -> update source URL
- Make %%files list more explicit
- Specify all dependencies

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.84-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Petr Pisar <ppisar@redhat.com> - 0.84-6
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.84-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 28 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.84-4
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.84-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Paul Howarth <paul@city-fan.org> - 0.84-2
- Haven't needed to fix documentation character encoding since 0.79
- Drop Test::Base build dependency again to avoid a BR loop (#215637)
- Filter private provides perl(yaml_mapping), perl(yaml_scalar) and
  perl(yaml_sequence)
- Don't need to remove empty directories from the buildroot
- This release by MSTROUT -> update source URL

* Mon Jul 16 2012 Petr Šabata <contyk@redhat.com> - 0.84-1
- 0.84 bump
- Drop command macros
- Drop previously added patch (included in 0.82)

* Fri Jun 22 2012 Jitka Plesnikova <jplesnik@redhat.com> 0.81-4
- Apply patch to for YAML::Any RT#74226

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 0.81-3
- Perl 5.16 rebuild

* Mon Apr 23 2012 Paul Howarth <paul@city-fan.org> - 0.81-2
- R: perl(Carp) and perl(Data::Dumper)
- BR: perl(Carp), perl(constant) and perl(Exporter)
- Release tests no longer shipped, so drop buildreqs for them and don't bother
  setting AUTOMATED_TESTING; run tests even when bootstrapping

* Mon Apr 23 2012 Marcela Mašláňová <mmaslano@redhat.com> - 0.81-1
- Update to 0.81
- Add BR Data::Dumper

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.73-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jun 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.73-2
- Perl mass rebuild
- add perl_bootstrap macro

* Sat May 14 2011 Iain Arnell <iarnell@gmail.com> 0.73-1
- update to latest upstream version
- clean up spec for modern rpmbuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.72-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 08 2010 Steven Pritchard <steve@kspei.com> 0.72-1
- Update to 0.72.

* Wed Aug 18 2010 Paul Howarth <paul@city-fan.org> - 0.71-1
- Update to 0.71 (use UTF-8 encoding in LoadFile/DumpFile: CPAN RT#25434)
- Enable AUTOMATED_TESTING
- BR: perl(Test::CPAN::Meta), perl(Test::MinimumVersion), perl(Test::Pod)
- This release by ADAMK -> update source URL
- Re-code docs as UTF-8

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.70-5
- Mass rebuild with perl-5.12.0

* Thu Feb 25 2010 Marcela Mašláňová <mmaslano@redhat.com> - 0.70-4
- add license

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.70-3
- rebuild against perl 5.10.1

* Wed Oct  7 2009 Marcela Mašláňová <mmaslano@redhat.com> - 0.70-2
- rebuild for push

* Tue Oct 6  2009 Marcela Mašláňová <mmaslano@redhat.com> - 0.70-1
- new upstream version

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.68-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Dec 10 2008 Steven Pritchard <steve@kspei.com> 0.68-1
- Update to 0.68.
- COMPATIBILITY went away.
- ysh moved to YAML::Shell.

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.66-3
- Rebuild for perl 5.10 (again)

* Fri Jan 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.66-2
- rebuild for new perl

* Tue Oct 16 2007 Steven Pritchard <steve@kspei.com> 0.66-1
- Update to 0.66.
- Update License tag.

* Wed Jun 27 2007 Steven Pritchard <steve@kspei.com> 0.65-1
- Update to 0.65.

* Tue Mar 13 2007 Steven Pritchard <steve@kspei.com> 0.62-3
- Use fixperms macro instead of our own chmod incantation.
- Drop Test::Base build dependency to avoid a BR loop (#215637).
- BR ExtUtils::MakeMaker.

* Sat Sep 16 2006 Steven Pritchard <steve@kspei.com> 0.62-2
- Fix find option order.

* Fri Jul 07 2006 Steven Pritchard <steve@kspei.com> 0.62-1
- Update to 0.62.
- Removed Test::YAML (bug #197539).

* Mon Jul 03 2006 Steven Pritchard <steve@kspei.com> 0.61-1
- Update to 0.61.

* Sat May 20 2006 Steven Pritchard <steve@kspei.com> 0.58-3
- Rebuild.

* Tue May 09 2006 Steven Pritchard <steve@kspei.com> 0.58-2
- Drop testmore patch.
- Catch Test::YAML module and man page in file list.

* Thu May 04 2006 Steven Pritchard <steve@kspei.com> 0.58-1
- Update to 0.58.
- Small spec cleanups.

* Thu Apr 14 2005 Ville Skyttä <ville.skytta at iki.fi> - 0.39-2
- 0.39.

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat May 15 2004 Jose Pedro Oliveira <jpo at di.uminho.pt> - 0:0.35-0.fdr.5
- Avoid creation of the perllocal.pod file (make pure_install).

* Sun Apr 25 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.35-0.fdr.4
- Require perl(:MODULE_COMPAT_*).
- Cosmetic tweaks (bug 1383).

* Sun Mar 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.35-0.fdr.3
- Reduce directory ownership bloat.

* Tue Nov 18 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.35-0.fdr.2
- Use INSTALLARCHLIB workaround in %%install.

* Wed Sep  3 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.35-0.fdr.1
- First build.
