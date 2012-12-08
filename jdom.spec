%define gcj_support 0

Name:           jdom
Version:        1.1.1
Release:	%mkrel 4
Epoch:          0
Summary:        Java alternative to DOM and SAX
License:        Apache License-like
URL:            http://www.jdom.org/
Group:          Development/Java
Source0:        http://jdom.org/dist/binary/%{name}-%{version}.tar.gz
Patch0:         %{name}-crosslink.patch
Patch1:         %{name}-1.0-OSGiManifest.patch
BuildRequires:  java-rpmbuild >= 0:1.5
BuildRequires:  java-javadoc
BuildRequires:	xalan-j2
BuildRequires:  ant
BuildRequires:	jaxen
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
Requires:	xalan-j2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
JDOM is, quite simply, a Java representation of an XML document. JDOM
provides a way to represent that document for easy and efficient
reading, manipulation, and writing. It has a straightforward API, is a
lightweight and fast, and is optimized for the Java programmer. It's an
alternative to DOM and SAX, although it integrates well with both DOM
and SAX.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

%package demo
Summary:        Demos for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{name}.


%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p0
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
find . -name "*.class" -exec rm -f {} \;


%build
export CLASSPATH=$(build-classpath xml-commons-apis xalan-j2 jaxen)
sed -e 's|<property name="build.compiler".*||' build.xml > tempf; cp tempf build.xml; rm tempf
%ant -Dj2se.apidoc=%{_javadocdir}/java package javadoc-link


%install
rm -rf %{buildroot}

# jars
mkdir -p %{buildroot}%{_javadir}
cp -p build/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr build/apidocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

# demo
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -pr samples %{buildroot}%{_datadir}/%{name}

%{gcj_compile}

%clean
%{__rm} -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc CHANGES.txt COMMITTERS.txt LICENSE.txt README.txt TODO.txt
%{_javadir}/%{name}*.jar
%{gcj_files}

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}
%doc %{_javadocdir}/%{name}-%{version}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}




%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0:1.1.1-3mdv2011.0
+ Revision: 665823
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.1.1-2mdv2011.0
+ Revision: 606079
- rebuild

* Sun Feb 21 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 0:1.1.1-1mdv2010.1
+ Revision: 508889
- update to new version 1.1.1
- rediff patch0
- spec file clean
- add missing buildrequires on xalan-j and jaxen

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 0:1.0-5.5.3mdv2010.0
+ Revision: 425458
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 0:1.0-5.5.2mdv2009.1
+ Revision: 351302
- rebuild

* Sun Aug 10 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.0-5.5.1mdv2009.0
+ Revision: 270173
- update OSGi manifest

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 0:1.0-5.0.2mdv2009.0
+ Revision: 136503
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.0-5.0.2mdv2008.1
+ Revision: 120938
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Mon Dec 10 2007 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.0-5.0.1mdv2008.1
+ Revision: 116965
- remove javadoc post/postun

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.0-4.5mdv2008.0
+ Revision: 87431
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sat Sep 08 2007 Pascal Terjan <pterjan@mandriva.org> 0:1.0-4.4mdv2008.0
+ Revision: 82693
- update to new version


* Thu Mar 15 2007 Christiaan Welvaart <spturtle@mandriva.org> 1.0-4.3mdv2007.1
+ Revision: 144241
- rebuild for 2007.1
- Import jdom

* Thu Aug 10 2006 David Walluck <walluck@mandriva.org> 0:1.0-4.1mdv2007.0
- add javadoc %%postun

* Sun Jul 23 2006 David Walluck <walluck@mandriva.org> 0:1.0-3.1mdv2007.0
- fix BuildRequires
- drop xalan-j2 (Build)Requires

* Sun Jun 04 2006 David Walluck <walluck@mandriva.org> 0:1.0-1.2.2mdv2007.0
- rebuild for libgcj.so.7

* Mon Feb 27 2006 David Walluck <walluck@mandriva.org> 0:1.0-1.2.1mdk
- add native libraries

* Sat May 28 2005 David Walluck <walluck@mandriva.org> 0:1.0-1.1mdk
- release

* Wed Oct 20 2004 Fernando Nasser <fnasser@redhat.com> - 0:1.0-1jpp_1rh
- First Red Hat build

* Sun Sep 19 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0-1jpp
- Upgrade to 1.0 final

* Wed Sep 08 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.rc1.1jpp
- Upgrade to 1.0-rc1

* Tue Aug 24 2004 Randy Watler <rwatler at finali.com> - 0:1.0-0.b9.4jpp
- Rebuild with ant-1.6.2

* Tue Jul 20 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0-0.b9.3jpp
- Add non-versioned javadoc dir symlink.
- Crosslink with local J2SE javadocs.

