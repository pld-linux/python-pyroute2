#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

# NOTES:
# - 'module' should match the Python import path (first component?)
# - 'egg_name' should equal to Python egg name
# - 'pypi_name' must match the Python Package Index name
%define		module		pyroute2
%define		egg_name	pyroute2
%define		pypi_name	pyroute2
Summary:	Python Netlink library
Name:		python-%{module}
Version:	0.5.18
Release:	3
License:	GPLv2+ or Apache v2
Group:		Libraries/Python
# if pypi:
#Source0Download: https://pypi.org/simple/PYPI_NAME/
Source0:	https://pypi.debian.net/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	e9cec0003d98e1b0a4d657b87caf52d5
URL:		https://pyroute2.org/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.5
BuildRequires:	python-setuptools
%if %{with tests}
#BuildRequires:	python-
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools
%if %{with tests}
#BuildRequires:	python3-
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-modules >= 1:2.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python Netlink library.

%package -n python3-%{module}
Summary:	Python Netlink library
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.2

%description -n python3-%{module}
Python Netlink library.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{pypi_name}-%{version}

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python3(\s|$),#!%{__python3}\1,' \
      examples/nftables.py \
      examples/nl80211_scan_dump.py

%build
%if %{with python2}
%py_build
# deprecated target, but sometimes still used: %{?with_tests:test}

%if %{with tests}
%{__python} -m pytest ...
%endif
%endif

%if %{with python3}
%py3_build
# deprecated target, but sometimes still used: %{?with_tests:test}

%if %{with tests}
%{__python3} -m pytest ...
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install
%py_postclean
%endif

%if %{with python3}
%{__rm} -f $RPM_BUILD_ROOT%{_bindir}/pyroute2-cli
%{__rm} -f $RPM_BUILD_ROOT%{_bindir}/ss2
%py3_install
%endif

%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python}|'
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README* CHANGELOG.md
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%{_examplesdir}/python-%{module}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README* CHANGELOG.md
%attr(755,root,root) %{_bindir}/pyroute2-cli
%attr(755,root,root) %{_bindir}/ss2
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/html/*
%endif
