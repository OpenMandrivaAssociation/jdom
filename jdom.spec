%define gcj_support 0

Summary:	Java alternative to DOM and SAX
Name:		jdom
Version:	1.1.1
Release:	8
License:	Apache License-like
Url:		http://www.jdom.org/
Group:		Development/Java
Source0:	http://jdom.org/dist/binary/%{name}-%{version}.tar.gz
Patch0:		%{name}-crosslink.patch
Patch1:		%{name}-1.0-OSGiManifest.patch
%if !%{gcj_support}
BuildArch:	noarch
%else
BuildRequires:	java-gcj-compat-devel
%endif
BuildRequires:	ant
BuildRequires:	java-rpmbuild >= 0:1.5
BuildRequires:	java-javadoc
BuildRequires:	jaxen
BuildRequires:	xalan-j2
Requires:	xalan-j2

%description
JDOM is, quite simply, a Java representation of an XML document. JDOM
provides a way to represent that document for easy and efficient
reading, manipulation, and writing. It has a straightforward API, is a
lightweight and fast, and is optimized for the Java programmer. It's an
alternative to DOM and SAX, although it integrates well with both DOM
and SAX.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description javadoc
Javadoc for %{name}.

%package demo
Summary:	Demos for %{name}
Group:		Development/Java
Requires:	%{name} = %{EVRD}

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -qn %{name}
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

%gcj_compile

%if %{gcj_support}
%post
%update_gcjdb

%postun
%clean_gcjdb
%endif

%files
%doc CHANGES.txt COMMITTERS.txt LICENSE.txt README.txt TODO.txt
%{_javadir}/%{name}*.jar
%{gcj_files}

%files javadoc
%doc %{_javadocdir}/%{name}
%doc %{_javadocdir}/%{name}-%{version}

%files demo
%{_datadir}/%{name}

