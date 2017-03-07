%{?_javapackages_macros:%_javapackages_macros}

Summary:	A transparent threading solution for non-freezing Swing applications
Name:		spin
Version:	1.5
Release:	1
License:	LGPLv2
Group:		Development/Java
URL:		http://spin.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}-all.zip
BuildArch:	noarch

BuildRequires:	maven-local
BuildRequires:	mvn(cglib:cglib)
BuildRequires:	mvn(junit:junit)
BuildRequires:	mvn(org.apache.maven.plugins:maven-assembly-plugin)
BuildRequires:	x11-server-xvfb

%description
Transparent threading solution for non-freezing Swing applications.

%files -f .mfiles
%doc license.txt

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}
Group:		Documentation

%description javadoc
API documentation for %{name}.

%files javadoc -f .mfiles-javadoc
%doc license.txt

#----------------------------------------------------------------------------

%prep
%setup -q

# Delete all pre-built binaries
find . -name "*.jar" -delete
find . -name "*.class" -delete

# Fix dependence name
%pom_xpath_replace "pom:dependency[pom:groupId[./text()='cglib']]/pom:artifactId" "
	<artifactId>cglib</artifactId>" .

# Fix missing version
%pom_xpath_inject "pom:plugin[pom:artifactId[./text()='maven-compiler-plugin']]" "
	<version>any</version>" .
%pom_xpath_inject "pom:plugin[pom:artifactId[./text()='maven-assembly-plugin']]" "
	<version>any</version>" .

# Fix jar-not-indexed warning
%pom_add_plugin :maven-jar-plugin . "<configuration>
	<archive>
		<index>true</index>
	</archive>
</configuration>"

# Fix Jar name
%mvn_file :%{name} %{name}-%{version} %{name}

%build
xvfb-run -a %mvn_build -- -Dproject.build.sourceEncoding=UTF-8 

%install
%mvn_install

