# ==================
# Top-level metadata
# ==================

Name: python36
Summary: Interpreter of the Python programming language
URL: https://www.python.org/

%global pybasever 3.6

# pybasever without the dot:
%global pyshortver 36

Version: %{pybasever}.8
Release: 1%{?dist}
License: Python

Obsoletes: python34


# ==================================
# Conditionals controlling the build
# ==================================

# Run the test suite in %%check
%global run_selftest_suite 0

# Extra build for debugging the interpreter or C-API extensions
# (the -debug subpackages)
%global with_debug_build 1

# Support for the GDB debugger
%global with_gdb_hooks 1

# The dbm.gnu module (key-value database)
%global with_gdbm 1

# Change from yes to no to turn this off
%global with_computed_gotos yes

# Support for the Valgrind debugger/profiler
%ifnarch s390 %{mips} riscv64
%global with_valgrind 1
%else
# Some arches don't have valgrind, disable support for it there.
%global with_valgrind 0
%endif

%if 0%{?rhel} && 0%{?rhel} < 7
%global with_system_expat 0
%else
%global with_system_expat 1
%endif

# Bundle latest wheels of setuptools and/or pip.
#global setuptools_version 39.0.1
#global pip_version 9.0.3


# =====================
# General global macros
# =====================

%global pylibdir %{_libdir}/python%{pybasever}
%global dynload_dir %{pylibdir}/lib-dynload

# ABIFLAGS, LDVERSION and SOABI are in the upstream configure.ac
# See PEP 3149 for some background: http://www.python.org/dev/peps/pep-3149/
%global ABIFLAGS_optimized m
%global ABIFLAGS_debug     dm

%global LDVERSION_optimized %{pybasever}%{ABIFLAGS_optimized}
%global LDVERSION_debug     %{pybasever}%{ABIFLAGS_debug}

%global SOABI_optimized cpython-%{pyshortver}%{ABIFLAGS_optimized}-%{_arch}-linux%{_gnu}
%global SOABI_debug     cpython-%{pyshortver}%{ABIFLAGS_debug}-%{_arch}-linux%{_gnu}

# All bytecode files are in a __pycache__ subdirectory, with a name
# reflecting the version of the bytecode.
# See PEP 3147: http://www.python.org/dev/peps/pep-3147/
# For example,
#   foo/bar.py
# has bytecode at:
#   foo/__pycache__/bar.cpython-%%{pyshortver}.pyc
#   foo/__pycache__/bar.cpython-%%{pyshortver}.opt-1.pyc
#   foo/__pycache__/bar.cpython-%%{pyshortver}.opt-2.pyc
%global bytecode_suffixes .cpython-%{pyshortver}*.pyc

# Python's configure script defines SOVERSION, and this is used in the Makefile
# to determine INSTSONAME, the name of the libpython DSO:
#   LDLIBRARY='libpython$(VERSION).so'
#   INSTSONAME="$LDLIBRARY".$SOVERSION
# We mirror this here in order to make it easier to add the -gdb.py hooks.
# (if these get out of sync, the payload of the libs subpackage will fail
# and halt the build)
%global py_SOVERSION 1.0
%global py_INSTSONAME_optimized libpython%{LDVERSION_optimized}.so.%{py_SOVERSION}
%global py_INSTSONAME_debug     libpython%{LDVERSION_debug}.so.%{py_SOVERSION}

# We want to byte-compile the .py files within the packages using the new
# python3 binary.
#
# Unfortunately, rpmbuild's infrastructure requires us to jump through some
# hoops to avoid byte-compiling with the system python 2 version:
#   /usr/lib/rpm/redhat/macros sets up build policy that (amongst other things)
# defines __os_install_post.  In particular, "brp-python-bytecompile" is
# invoked without an argument thus using the wrong version of python
# (/usr/bin/python, rather than the freshly built python), thus leading to
# numerous syntax errors, and incorrect magic numbers in the .pyc files.  We
# thus override __os_install_post to avoid invoking this script:
%global __os_install_post /usr/lib/rpm%{?rhel:/redhat}/brp-compress \
  %{!?__debug_package:/usr/lib/rpm%{?rhel:/redhat}/brp-strip %{__strip}} \
  %{!?__debug_package:/usr/lib/rpm%{?rhel:/redhat}/brp-strip-comment-note %{__strip} %{__objdump}} \
  /usr/lib/rpm%{?rhel:/redhat}/brp-strip-static-archive %{__strip} \
  /usr/lib/rpm%{?rhel:/redhat}/brp-python-hardlink
# to remove the invocation of brp-python-bytecompile, whilst keeping the
# invocation of brp-python-hardlink (since this should still work for python3
# pyc/pyo files)


# =======================
# Build-time requirements
# =======================

# (keep this list alphabetized)

BuildRequires: autoconf%{?el6:268}
BuildRequires: bluez-libs-devel
BuildRequires: bzip2
BuildRequires: bzip2-devel

# expat 2.1.0 added the symbol XML_SetHashSalt without bumping SONAME.  We use
# it (in pyexpat) in order to enable the fix in Python-3.2.3 for CVE-2012-0876:
%if 0%{?with_system_expat}
BuildRequires: expat-devel >= 2.1.0
%endif

BuildRequires: findutils
BuildRequires: gcc-c++
%if 0%{?with_gdbm}
BuildRequires: gdbm-devel
%endif
BuildRequires: glibc-devel
BuildRequires: gmp-devel
BuildRequires: libffi-devel
BuildRequires: libGL-devel
BuildRequires: libX11-devel
BuildRequires: ncurses-devel
# workaround http://bugs.python.org/issue19804 (test_uuid requires ifconfig)
BuildRequires: net-tools
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: readline-devel
BuildRequires: sqlite-devel

BuildRequires: tar
BuildRequires: tcl-devel
BuildRequires: tix-devel
BuildRequires: tk-devel

%if 0%{?with_valgrind}
BuildRequires: valgrind-devel
%endif

BuildRequires: xz-devel
BuildRequires: zlib-devel

BuildRequires: /usr/bin/dtrace


# =======================
# Source code and patches
# =======================

Source: https://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz

# Supply an RPM macro "py_byte_compile" for the python3-devel subpackage
# to enable specfiles to selectively byte-compile individual files and paths
# with different Python runtimes as necessary:
Source3: macros.pybytecompile%{pybasever}

# A simple script to check timestamps of bytecode files
# Run in check section with Python that is currently being built
# Written by bkabrda
Source8: check-pyc-and-pyo-timestamps.py

# Supply various useful macros for building python 3.X modules:
#  __python3Xu, python3Xu_sitelib, python3Xu_sitearch
Source10: macros.python%{pybasever}

%if %{defined setuptools_version}
Source20: https://files.pythonhosted.org/packages/py2.py3/s/setuptools/setuptools-%{setuptools_version}-py2.py3-none-any.whl
%endif
%if %{defined pip_version}
Source21: https://files.pythonhosted.org/packages/py2.py3/p/pip/pip-%{pip_version}-py2.py3-none-any.whl
%endif

# 00001 #
# Fixup distutils/unixccompiler.py to remove standard library path from rpath:
# Was Patch0 in ivazquez' python3000 specfile:
Patch1:         00001-rpath.patch

# 00102 #
# Change the various install paths to use /usr/lib64/ instead or /usr/lib
# Only used when "%%{_lib}" == "lib64"
# Not yet sent upstream.
Patch102: 00102-lib64.patch

# 00111 #
# Patch the Makefile.pre.in so that the generated Makefile doesn't try to build
# a libpythonMAJOR.MINOR.a
# See https://bugzilla.redhat.com/show_bug.cgi?id=556092
# Downstream only: not appropriate for upstream
Patch111: 00111-no-static-lib.patch

# 00132 #
# Add non-standard hooks to unittest for use in the "check" phase below, when
# running selftests within the build:
#   @unittest._skipInRpmBuild(reason)
# for tests that hang or fail intermittently within the build environment, and:
#   @unittest._expectedFailureInRpmBuild
# for tests that always fail within the build environment
#
# The hooks only take effect if WITHIN_PYTHON_RPM_BUILD is set in the
# environment, which we set manually in the appropriate portion of the "check"
# phase below (and which potentially other python-* rpms could set, to reuse
# these unittest hooks in their own "check" phases)
Patch132: 00132-add-rpmbuild-hooks-to-unittest.patch

# 00155 #
# Avoid allocating thunks in ctypes unless absolutely necessary, to avoid
# generating SELinux denials on "import ctypes" and "import uuid" when
# embedding Python within httpd
# See https://bugzilla.redhat.com/show_bug.cgi?id=814391
Patch155: 00155-avoid-ctypes-thunks.patch

# 00160 #
# Python 3.3 added os.SEEK_DATA and os.SEEK_HOLE, which may be present in the
# header files in the build chroot, but may not be supported in the running
# kernel, hence we disable this test in an rpm build.
# Adding these was upstream issue http://bugs.python.org/issue10142
# Not yet sent upstream
Patch160: 00160-disable-test_fs_holes-in-rpm-build.patch

# 00163 #
# Some tests within test_socket fail intermittently when run inside Koji;
# disable them using unittest._skipInRpmBuild
# Not yet sent upstream
Patch163: 00163-disable-parts-of-test_socket-in-rpm-build.patch

# 00170 #
# In debug builds, try to print repr() when a C-level assert fails in the
# garbage collector (typically indicating a reference-counting error
# somewhere else e.g in an extension module)
# The new macros/functions within gcmodule.c are hidden to avoid exposing
# them within the extension API.
# Sent upstream: http://bugs.python.org/issue9263
# See https://bugzilla.redhat.com/show_bug.cgi?id=614680
Patch170: 00170-gc-assertions.patch

# 00178 #
# Don't duplicate various FLAGS in sysconfig values
# http://bugs.python.org/issue17679
# Does not affect python2 AFAICS (different sysconfig values initialization)
Patch178: 00178-dont-duplicate-flags-in-sysconfig.patch

# 00205 #
# LIBPL variable in makefile takes LIBPL from configure.ac
# but the LIBPL variable defined there doesn't respect libdir macro
Patch205: 00205-make-libpl-respect-lib64.patch

# 00274 #
# Upstream uses Debian-style architecture naming. Change to match Fedora.
Patch274: 00274-fix-arch-names.patch

# 00900 #
Patch900: 00900-skip-tan0064-32bit.patch

# (New patches go here ^^^)
#
# When adding new patches to "python" and "python3" in Fedora, EL, etc.,
# please try to keep the patch numbers in-sync between all specfiles.
#
# More information, and a patch number catalog, is at:
#
#     https://fedoraproject.org/wiki/SIGs/Python/PythonPatches


# ==========================================
# Descriptions, and metadata for subpackages
# ==========================================

# Packages with Python modules in standard locations automatically
# depend on python(abi). Provide that here.
Provides: python(abi) = %{pybasever}

Requires: %{name}-libs%{?_isa} = %{version}-%{release}


# The description used both for the SRPM and the main `python3` subpackage:
%description
Python is an accessible, high-level, dynamically typed, interpreted programming
language, designed with an emphasis on code readability.
It includes an extensive standard library, and has a vast ecosystem of
third-party libraries.

The %{name} package provides the "python%{pybasever}" executable: the reference
interpreter for the Python language, version 3.
The majority of its standard library is provided in the %{name}-libs package,
which should be installed automatically along with %{name}.
The remaining parts of the Python standard library are broken out into the
%{name}-tkinter and %{name}-test packages, which may need to be installed
separately.

Documentation for Python is provided in the %{name}-docs package.

Packages containing additional libraries for Python are generally named with
the "%{name}-" prefix.


%package libs
Summary:        Python runtime libraries

Obsoletes: python34-libs


%description libs
This package contains runtime libraries for use by Python:
- the majority of the Python standard library
- a dynamically linked library for use by applications that embed Python as
  a scripting language, and by the main "python3" executable


%package devel
Summary: Libraries and header files needed for Python development
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Conflicts: %{name} < %{version}-%{release}

%description devel
This package contains the header files and configuration needed to compile
Python extension modules (typically written in C or C++), to embed Python
into other programs, and to make binary distributions for Python libraries.

It also contains the necessary macros to build RPM packages with Python modules.


%package tools
Summary: A collection of tools included with Python including 2to3 and idle
Requires: %{name} = %{version}-%{release}
Requires: %{name}-tkinter = %{version}-%{release}

%description tools
This package contains several tools included with Python, including:
- 2to3, an automatic source converter from Python 2.X
- idle, a basic graphical development environment


%package tkinter
Summary: A GUI toolkit for Python
Requires: %{name} = %{version}-%{release}

%description tkinter
The Tkinter (Tk interface) library is a graphical user interface toolkit for
the Python programming language.


%package test
Summary: The self-test suite for the main %{name} package
Requires: %{name} = %{version}-%{release}
Requires: %{name}-tools = %{version}-%{release}


%description test
The self-test suite for the Python interpreter.

This is only useful to test Python itself. For testing general Python code,
you should use the unittest module from %{name}-libs, or a library such as
%{name}-pytest or %{name}-nose.


%if 0%{?with_debug_build}
%package debug
Summary: Debug version of the Python runtime

# The debug build is an all-in-one package version of the regular build, and
# shares the same .py/.pyc files and directories as the regular build. Hence
# we depend on all of the subpackages of the regular build:
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}-test%{?_isa} = %{version}-%{release}
Requires: %{name}-tkinter%{?_isa} = %{version}-%{release}
Requires: %{name}-tools%{?_isa} = %{version}-%{release}

%description debug
%{name}-debug provides a version of the Python runtime with numerous debugging
features enabled, aimed at advanced Python users such as developers of Python
extension modules.

This version uses more memory and will be slower than the regular Python build,
but is useful for tracking down reference-counting issues and other bugs.

The bytecode format is unchanged, so that .pyc files are compatible between
this and the standard version of Python, but the debugging features mean that
C/C++ extension modules are ABI-incompatible and must be built for each version
separately.

The debug build shares installation directories with the standard Python
runtime, so that .py and .pyc files can be shared.
Compiled extension modules use a special ABI flag ("d") in the filename,
so extensions for both versions can co-exist in the same directory.
%endif # with_debug_build


# ======================================================
# The prep phase of the build:
# ======================================================

%prep
%setup -q -n Python-%{version}%{?prerel}

# Remove bundled libraries to ensure that we're using the system copy.
%if 0%{?with_system_expat}
rm -r Modules/expat
%endif
rm -r Modules/zlib

%if %{defined setuptools_version}
sed -r -e '/^_SETUPTOOLS_VERSION =/ s/"[0-9.]+"/"%{setuptools_version}"/' -i Lib/ensurepip/__init__.py
rm Lib/ensurepip/_bundled/setuptools-*.whl
cp -a %{SOURCE20} Lib/ensurepip/_bundled/
%endif
%if %{defined pip_version}
sed -r -e '/^_PIP_VERSION =/ s/"[0-9.]+"/"%{pip_version}"/' -i Lib/ensurepip/__init__.py
rm Lib/ensurepip/_bundled/pip-*.whl
cp -a %{SOURCE21} Lib/ensurepip/_bundled/
%endif

#
# Apply patches:
#
%patch1 -p1

%if "%{_lib}" == "lib64"
%patch102 -p1
%endif
%patch111 -p1
%patch132 -p1
%patch155 -p1
%patch160 -p1
%patch163 -p1
%patch170 -p1
%patch178 -p1

%patch205 -p1

%patch274 -p1
%patch900 -p1

# Remove files that should be generated by the build
# (This is after patching, so that we can use patches directly from upstream)
rm configure pyconfig.h.in


# ======================================================
# Configuring and building the code:
# ======================================================

%build

# Regenerate the configure script and pyconfig.h.in
autoconf%{?el6:268}
autoheader%{?el6:268}

# Remember the current directory (which has sources and the configure script),
# so we can refer to it after we "cd" elsewhere.
topdir=$(pwd)

# Set common compiler/linker flags
export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC -fwrapv"
export CXXFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC -fwrapv"
export CPPFLAGS="$(pkg-config --cflags-only-I libffi)"
export OPT="$RPM_OPT_FLAGS -D_GNU_SOURCE -fPIC -fwrapv"
export LINKCC="gcc"
export CFLAGS="$CFLAGS $(pkg-config --cflags openssl)"
export LDFLAGS="$RPM_LD_FLAGS $(pkg-config --libs-only-L openssl)"

# We can build several different configurations of Python: regular and debug.
# Define a common function that does one build:
BuildPython() {
  ConfName=$1
  BinaryName=$2
  SymlinkName=$3
  ExtraConfigArgs=$4
  PathFixWithThisBinary=$5
  MoreCFlags=$6

  # Each build is done in its own directory
  ConfDir=build/$ConfName
  echo STARTING: BUILD OF PYTHON FOR CONFIGURATION: $ConfName - %{_bindir}/$BinaryName
  mkdir -p $ConfDir
  pushd $ConfDir

  # Normally, %%configure looks for the "configure" script in the current
  # directory.
  # Since we changed directories, we need to tell %%configure where to look.
  %global _configure $topdir/configure

%configure \
  --enable-ipv6 \
  --enable-shared \
  --with-computed-gotos=%{with_computed_gotos} \
  --with-dbmliborder=gdbm:ndbm:bdb \
  --enable-unicode=ucs4 \
%if 0%{?with_system_expat}
  --with-system-expat \
%endif
  --with-system-ffi \
  --enable-loadable-sqlite-extensions \
  --with-dtrace \
%if 0%{?with_valgrind}
  --with-valgrind \
%endif
  $ExtraConfigArgs \
  %{nil}

  # Invoke the build
  make EXTRA_CFLAGS="$CFLAGS $MoreCFlags" %{?_smp_mflags}

  popd
  echo FINISHED: BUILD OF PYTHON FOR CONFIGURATION: $ConfDir
}

# Call the above to build each configuration.

%if 0%{?with_debug_build}
BuildPython debug \
  python-debug \
  python%{pybasever}-debug \
  "--without-ensurepip --with-pydebug" \
  false \
  "-O0"
%endif # with_debug_build

BuildPython optimized \
  python \
  python%{pybasever} \
  "--without-ensurepip" \
  true

# ======================================================
# Installing the built code:
# ======================================================

%install

# As in %%build, remember the current directory
topdir=$(pwd)

# We install a collection of hooks for gdb that make it easier to debug
# executables linked against libpython3* (such as /usr/bin/python3 itself)
#
# These hooks are implemented in Python itself (though they are for the version
# of python that gdb is linked with)
#
# gdb-archer looks for them in the same path as the ELF file or its .debug
# file, with a -gdb.py suffix.
# We put them next to the debug file, because ldconfig would complain if
# it found non-library files directly in /usr/lib/
# (see https://bugzilla.redhat.com/show_bug.cgi?id=562980)
#
# We'll put these files in the debuginfo package by installing them to e.g.:
#  /usr/lib/debug/usr/lib/libpython3.2.so.1.0.debug-gdb.py
# (note that the debug path is /usr/lib/debug for both 32/64 bit)
#
# See https://fedoraproject.org/wiki/Features/EasierPythonDebugging for more
# information

%if 0%{?with_gdb_hooks}
DirHoldingGdbPy=%{_prefix}/lib/debug/%{_libdir}
mkdir -p %{buildroot}$DirHoldingGdbPy
%endif # with_gdb_hooks

# Use a common function to do an install for all our configurations:
InstallPython() {

  ConfName=$1
  PyInstSoName=$2
  MoreCFlags=$3

  # Switch to the directory with this configuration's built files
  ConfDir=build/$ConfName
  echo STARTING: INSTALL OF PYTHON FOR CONFIGURATION: $ConfName
  mkdir -p $ConfDir
  pushd $ConfDir

  make \
    DESTDIR=%{buildroot} \
    INSTALL="install -p" \
    EXTRA_CFLAGS="$MoreCFlags" \
    altinstall

  popd

%if 0%{?with_gdb_hooks}
  # See comment on $DirHoldingGdbPy above
  PathOfGdbPy=$DirHoldingGdbPy/$PyInstSoName-%{version}-%{release}.%{_arch}.debug-gdb.py
  cp Tools/gdb/libpython.py %{buildroot}$PathOfGdbPy
%endif # with_gdb_hooks

  echo FINISHED: INSTALL OF PYTHON FOR CONFIGURATION: $ConfName
}

# Install the "debug" build first; any common files will be overridden with
# later builds
%if 0%{?with_debug_build}
InstallPython debug \
  %{py_INSTSONAME_debug} \
  -O0

# altinstall only creates pkgconfig/python-3.X.pc, not the version with ABIFAGS,
#  so we need to move the debug .pc file to not overwrite it by optimized install
mv \
  %{buildroot}%{_libdir}/pkgconfig/python-%{pybasever}.pc \
  %{buildroot}%{_libdir}/pkgconfig/python-%{LDVERSION_debug}.pc

%endif # with_debug_build

# Now the optimized build:
InstallPython optimized \
  %{py_INSTSONAME_optimized}

# Install directories for additional packages
install -d -m 0755 %{buildroot}%{pylibdir}/site-packages/__pycache__
%if "%{_lib}" == "lib64"
# The 64-bit version needs to create "site-packages" in /usr/lib/ (for
# pure-Python modules) as well as in /usr/lib64/ (for packages with extension
# modules).
# Note that rpmlint will complain about hardcoded library path;
# this is intentional.
install -d -m 0755 %{buildroot}%{_prefix}/lib/python%{pybasever}/site-packages/__pycache__
%endif

# Development tools
install -m755 -d %{buildroot}%{pylibdir}/Tools
install Tools/README %{buildroot}%{pylibdir}/Tools/
cp -ar Tools/freeze %{buildroot}%{pylibdir}/Tools/
cp -ar Tools/i18n %{buildroot}%{pylibdir}/Tools/
cp -ar Tools/pynche %{buildroot}%{pylibdir}/Tools/
cp -ar Tools/scripts %{buildroot}%{pylibdir}/Tools/

# Documentation tools
install -m755 -d %{buildroot}%{pylibdir}/Doc
cp -ar Doc/tools %{buildroot}%{pylibdir}/Doc/

# Demo scripts
cp -ar Tools/demo %{buildroot}%{pylibdir}/Tools/

# Make python3-devel multilib-ready (bug #192747, #139911)
%global _pyconfig32_h pyconfig-32.h
%global _pyconfig64_h pyconfig-64.h

%ifarch %{power64} s390x x86_64 ia64 alpha sparc64 aarch64 %{mips64} riscv64
%global _pyconfig_h %{_pyconfig64_h}
%else
%global _pyconfig_h %{_pyconfig32_h}
%endif

# ABIFLAGS, LDVERSION and SOABI are in the upstream Makefile
%global ABIFLAGS_optimized m
%global ABIFLAGS_debug     dm

%global LDVERSION_optimized %{pybasever}%{ABIFLAGS_optimized}
%global LDVERSION_debug     %{pybasever}%{ABIFLAGS_debug}

%global SOABI_optimized cpython-%{pyshortver}%{ABIFLAGS_optimized}-%{_arch}-linux%{_gnu}
%global SOABI_debug     cpython-%{pyshortver}%{ABIFLAGS_debug}-%{_arch}-linux%{_gnu}

%if 0%{?with_debug_build}
%global PyIncludeDirs python%{LDVERSION_optimized} python%{LDVERSION_debug}

%else
%global PyIncludeDirs python%{LDVERSION_optimized}
%endif

for PyIncludeDir in %{PyIncludeDirs} ; do
  mv %{buildroot}%{_includedir}/$PyIncludeDir/pyconfig.h \
     %{buildroot}%{_includedir}/$PyIncludeDir/%{_pyconfig_h}
  cat > %{buildroot}%{_includedir}/$PyIncludeDir/pyconfig.h << EOF
#include <bits/wordsize.h>

#if __WORDSIZE == 32
#include "%{_pyconfig32_h}"
#elif __WORDSIZE == 64
#include "%{_pyconfig64_h}"
#else
#error "Unknown word size"
#endif
EOF
done

# Make sure distutils looks at the right pyconfig.h file
# See https://bugzilla.redhat.com/show_bug.cgi?id=201434
# Similar for sysconfig: sysconfig.get_config_h_filename tries to locate
# pyconfig.h so it can be parsed, and needs to do this at runtime in site.py
# when python starts up (see https://bugzilla.redhat.com/show_bug.cgi?id=653058)
#
# Split this out so it goes directly to the pyconfig-32.h/pyconfig-64.h
# variants:
sed -i -e "s/'pyconfig.h'/'%{_pyconfig_h}'/" \
  %{buildroot}%{pylibdir}/distutils/sysconfig.py \
  %{buildroot}%{pylibdir}/sysconfig.py

# Switch all shebangs to refer to the specific Python version.
# This currently only covers files matching ^[a-zA-Z0-9_]+\.py$,
# so handle files named using other naming scheme separately.
LD_LIBRARY_PATH=./build/optimized ./build/optimized/python \
  Tools/scripts/pathfix.py \
  -i "%{_bindir}/python%{pybasever}" \
  %{buildroot} %{buildroot}%{pylibdir}/Tools/scripts/*-*.py \
  %{buildroot}%{pylibdir}/Tools/pynche/{pynche,pynche.pyw}
# not covered, also redundant and useless:
rm %{buildroot}%{pylibdir}/Tools/scripts/{2to3,idle3,pydoc3,pyvenv}

# Remove shebang lines from .py files that aren't executable, and
# remove executability from .py files that don't have a shebang line:
find %{buildroot} -name \*.py \
  \( \( \! -perm /u+x,g+x,o+x -exec sed -e '/^#!/Q 0' -e 'Q 1' {} \; \
  -print -exec sed -i '1d' {} \; \) -o \( \
  -perm /u+x,g+x,o+x ! -exec grep -m 1 -q '^#!' {} \; \
  -exec chmod a-x {} \; \) \)

# Remove executable flag from files that shouldn't have it:
chmod a-x \
  %{buildroot}%{pylibdir}/Tools/README

# Get rid of DOS batch files:
find %{buildroot} -name \*.bat -exec rm {} \;

# Get rid of backup files:
find %{buildroot}/ -name "*~" -exec rm -f {} \;
find . -name "*~" -exec rm -f {} \;

# Get rid of a stray copy of the license:
rm %{buildroot}%{pylibdir}/LICENSE.txt

# Do bytecompilation with the newly installed interpreter.
# This is similar to the script in macros.pybytecompile
# compile *.pyc
find %{buildroot} -type f -a -name "*.py" -print0 | \
    LD_LIBRARY_PATH="%{buildroot}%{dynload_dir}/:%{buildroot}%{_libdir}" \
    PYTHONPATH="%{buildroot}%{_libdir}/python%{pybasever} %{buildroot}%{_libdir}/python%{pybasever}/site-packages" \
    xargs -0 %{buildroot}%{_bindir}/python%{pybasever} -O -c 'import py_compile, sys; [py_compile.compile(f, dfile=f.partition("%{buildroot}")[2], optimize=opt) for opt in range(3) for f in sys.argv[1:]]' || :

# Fixup permissions for shared libraries from non-standard 555 to standard 755:
find %{buildroot} -perm 555 -exec chmod 755 {} \;

# Install macros for rpm:
mkdir -p %{buildroot}/%{rpmmacrodir}
install -m 644 %{SOURCE3} %{buildroot}/%{rpmmacrodir}
install -m 644 %{SOURCE10} %{buildroot}/%{rpmmacrodir}

# Create "/usr/bin/python3-debug", a symlink to the python3 debug binary, to
# avoid the user having to know the precise version and ABI flags.
# See e.g. https://bugzilla.redhat.com/show_bug.cgi?id=676748
%if 0%{?with_debug_build}
ln -s \
  %{_bindir}/python%{LDVERSION_debug} \
  %{buildroot}%{_bindir}/python%{pybasever}-debug
%endif

# Rename the script that differs on different arches to arch specific name
mv %{buildroot}%{_bindir}/python%{LDVERSION_optimized}-{,`uname -m`-}config
echo -e '#!/bin/sh\nexec `dirname $0`/python%{LDVERSION_optimized}-`uname -m`-config "$@"' > \
  %{buildroot}%{_bindir}/python%{LDVERSION_optimized}-config
echo '[ $? -eq 127 ] && echo "Could not find python%{LDVERSION_optimized}-`uname -m`-config. Look around to see available arches." >&2' >> \
  %{buildroot}%{_bindir}/python%{LDVERSION_optimized}-config
  chmod +x %{buildroot}%{_bindir}/python%{LDVERSION_optimized}-config

# make altinstall doesn't create python3.X-config, but we want it
#  (we don't want to have just python3.Xm-config, that's a bit confusing)
ln -s \
  %{_bindir}/python%{LDVERSION_optimized}-config \
  %{buildroot}%{_bindir}/python%{pybasever}-config
# make altinstall doesn't create python-3.Xm.pc, only python-3.X.pc, but we want both
ln -s \
  %{_libdir}/pkgconfig/python-%{pybasever}.pc \
  %{buildroot}%{_libdir}/pkgconfig/python-%{LDVERSION_optimized}.pc

# remove libpython3.so non-main python to not cause collision
rm -f %{buildroot}%{_libdir}/libpython3.so

# add symlink for /usr/bin/python3
ln -s %{_bindir}/python%{pybasever} %{buildroot}%{_bindir}/python3

# ======================================================
# Checks for packaging issues
# ======================================================

%check

# first of all, check timestamps of bytecode files
find %{buildroot} -type f -a -name "*.py" -print0 | \
    LD_LIBRARY_PATH="%{buildroot}%{dynload_dir}/:%{buildroot}%{_libdir}" \
    PYTHONPATH="%{buildroot}%{_libdir}/python%{pybasever} %{buildroot}%{_libdir}/python%{pybasever}/site-packages" \
    xargs -0 %{buildroot}%{_bindir}/python%{pybasever} %{SOURCE8}

# Ensure that the curses module was linked against libncursesw.so, rather than
# libncurses.so
# See https://bugzilla.redhat.com/show_bug.cgi?id=539917
ldd %{buildroot}/%{dynload_dir}/_curses*.so \
    | grep curses \
    | grep libncurses.so && (echo "_curses.so linked against libncurses.so" ; exit 1)

# Ensure that the debug modules are linked against the debug libpython, and
# likewise for the optimized modules and libpython:
for Module in %{buildroot}/%{dynload_dir}/*.so ; do
    case $Module in
    *.%{SOABI_debug})
        ldd $Module | grep %{py_INSTSONAME_optimized} &&
            (echo Debug module $Module linked against optimized %{py_INSTSONAME_optimized} ; exit 1)

        ;;
    *.%{SOABI_optimized})
        ldd $Module | grep %{py_INSTSONAME_debug} &&
            (echo Optimized module $Module linked against debug %{py_INSTSONAME_debug} ; exit 1)
        ;;
    esac
done

# ======================================================
# Running the upstream test suite
# ======================================================

# In some scenarios a larger stack is needed to avoid testInfiniteRecursion
# from segfaulting.  This was previously seen on ppc64 (rhbz#1292462), and more
# recently on EL6.
%if 0%{?rhel} && 0%{?rhel} < 7
  ulimit -a
  ulimit -s 16384
%endif


topdir=$(pwd)
CheckPython() {
  ConfName=$1
  ConfDir=$(pwd)/build/$ConfName

  echo STARTING: CHECKING OF PYTHON FOR CONFIGURATION: $ConfName

  # Note that we're running the tests using the version of the code in the
  # builddir, not in the buildroot.

  # Run the upstream test suite, setting "WITHIN_PYTHON_RPM_BUILD" so that the
  # our non-standard decorators take effect on the relevant tests:
  #   @unittest._skipInRpmBuild(reason)
  #   @unittest._expectedFailureInRpmBuild
  # test_faulthandler.test_register_chain currently fails on ppc64le and
  #   aarch64, see upstream bug http://bugs.python.org/issue21131
  WITHIN_PYTHON_RPM_BUILD= \
  LD_LIBRARY_PATH=$ConfDir $ConfDir/python -m test.regrtest \
    --verbose --findleaks \
    -x test_distutils \
    -x test_bdist_rpm \
    -x test_resource \
    %if 0%{?rhel} && 0%{?rhel} < 7
    -x test_zlib \
    %endif
    %ifarch ppc64le aarch64
    -x test_faulthandler \
    %endif
    %ifarch %{mips64}
    -x test_ctypes \
    %endif
    %ifarch %{power64} s390 s390x armv7hl aarch64 %{mips}
    -x test_gdb
    %endif

  echo FINISHED: CHECKING OF PYTHON FOR CONFIGURATION: $ConfName

}

%if 0%{run_selftest_suite}

# Check each of the configurations:
%if 0%{?with_debug_build}
CheckPython debug
%endif # with_debug_build
CheckPython optimized

%endif # run_selftest_suite


# ======================================================
# Scriptlets
# ======================================================

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%files
%license LICENSE
%doc README.rst
%{_bindir}/pydoc*
%{_bindir}/python%{pybasever}
%{_bindir}/python%{pybasever}m
%{_bindir}/pyvenv-%{pybasever}
%{_bindir}/python3
%{_mandir}/*/*

%files libs
%license LICENSE
%doc README.rst

%dir %{pylibdir}
%dir %{dynload_dir}

%{pylibdir}/lib2to3
%exclude %{pylibdir}/lib2to3/tests

%dir %{pylibdir}/unittest/
%dir %{pylibdir}/unittest/__pycache__/
%{pylibdir}/unittest/*.py
%{pylibdir}/unittest/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/asyncio/
%dir %{pylibdir}/asyncio/__pycache__/
%{pylibdir}/asyncio/*.py
%{pylibdir}/asyncio/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/venv/
%dir %{pylibdir}/venv/__pycache__/
%{pylibdir}/venv/*.py
%{pylibdir}/venv/__pycache__/*%{bytecode_suffixes}
%{pylibdir}/venv/scripts

%{pylibdir}/wsgiref
%{pylibdir}/xmlrpc

%dir %{pylibdir}/ensurepip/
%dir %{pylibdir}/ensurepip/__pycache__/
%{pylibdir}/ensurepip/*.py
%{pylibdir}/ensurepip/__pycache__/*%{bytecode_suffixes}
%{pylibdir}/ensurepip/_bundled

%{pylibdir}/idlelib

%dir %{pylibdir}/test/
%dir %{pylibdir}/test/__pycache__/
%dir %{pylibdir}/test/support/
%dir %{pylibdir}/test/support/__pycache__/
%{pylibdir}/test/__init__.py
%{pylibdir}/test/__pycache__/__init__%{bytecode_suffixes}
%{pylibdir}/test/support/__init__.py
%{pylibdir}/test/support/__pycache__/__init__%{bytecode_suffixes}

%dir %{pylibdir}/concurrent/
%dir %{pylibdir}/concurrent/__pycache__/
%{pylibdir}/concurrent/*.py
%{pylibdir}/concurrent/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/concurrent/futures/
%dir %{pylibdir}/concurrent/futures/__pycache__/
%{pylibdir}/concurrent/futures/*.py
%{pylibdir}/concurrent/futures/__pycache__/*%{bytecode_suffixes}

%{pylibdir}/pydoc_data

%{dynload_dir}/_blake2.%{SOABI_optimized}.so
%{dynload_dir}/_md5.%{SOABI_optimized}.so
%{dynload_dir}/_sha1.%{SOABI_optimized}.so
%{dynload_dir}/_sha256.%{SOABI_optimized}.so
%{dynload_dir}/_sha3.%{SOABI_optimized}.so
%{dynload_dir}/_sha512.%{SOABI_optimized}.so

%{dynload_dir}/_asyncio.%{SOABI_optimized}.so
%{dynload_dir}/_bisect.%{SOABI_optimized}.so
%{dynload_dir}/_bz2.%{SOABI_optimized}.so
%{dynload_dir}/_codecs_cn.%{SOABI_optimized}.so
%{dynload_dir}/_codecs_hk.%{SOABI_optimized}.so
%{dynload_dir}/_codecs_iso2022.%{SOABI_optimized}.so
%{dynload_dir}/_codecs_jp.%{SOABI_optimized}.so
%{dynload_dir}/_codecs_kr.%{SOABI_optimized}.so
%{dynload_dir}/_codecs_tw.%{SOABI_optimized}.so
%{dynload_dir}/_crypt.%{SOABI_optimized}.so
%{dynload_dir}/_csv.%{SOABI_optimized}.so
%{dynload_dir}/_ctypes.%{SOABI_optimized}.so
%{dynload_dir}/_curses.%{SOABI_optimized}.so
%{dynload_dir}/_curses_panel.%{SOABI_optimized}.so
%{dynload_dir}/_dbm.%{SOABI_optimized}.so
%{dynload_dir}/_decimal.%{SOABI_optimized}.so
%{dynload_dir}/_elementtree.%{SOABI_optimized}.so
%if 0%{?with_gdbm}
%{dynload_dir}/_gdbm.%{SOABI_optimized}.so
%endif
%{dynload_dir}/_hashlib.%{SOABI_optimized}.so
%{dynload_dir}/_heapq.%{SOABI_optimized}.so
%{dynload_dir}/_json.%{SOABI_optimized}.so
%{dynload_dir}/_lsprof.%{SOABI_optimized}.so
%{dynload_dir}/_lzma.%{SOABI_optimized}.so
%{dynload_dir}/_multibytecodec.%{SOABI_optimized}.so
%{dynload_dir}/_multiprocessing.%{SOABI_optimized}.so
%{dynload_dir}/_opcode.%{SOABI_optimized}.so
%{dynload_dir}/_pickle.%{SOABI_optimized}.so
%{dynload_dir}/_posixsubprocess.%{SOABI_optimized}.so
%{dynload_dir}/_random.%{SOABI_optimized}.so
%{dynload_dir}/_socket.%{SOABI_optimized}.so
%{dynload_dir}/_sqlite3.%{SOABI_optimized}.so
%{dynload_dir}/_ssl.%{SOABI_optimized}.so
%{dynload_dir}/_struct.%{SOABI_optimized}.so
%{dynload_dir}/array.%{SOABI_optimized}.so
%{dynload_dir}/audioop.%{SOABI_optimized}.so
%{dynload_dir}/binascii.%{SOABI_optimized}.so
%{dynload_dir}/cmath.%{SOABI_optimized}.so
%{dynload_dir}/_datetime.%{SOABI_optimized}.so
%{dynload_dir}/fcntl.%{SOABI_optimized}.so
%{dynload_dir}/grp.%{SOABI_optimized}.so
%{dynload_dir}/math.%{SOABI_optimized}.so
%{dynload_dir}/mmap.%{SOABI_optimized}.so
%{dynload_dir}/nis.%{SOABI_optimized}.so
%{dynload_dir}/ossaudiodev.%{SOABI_optimized}.so
%{dynload_dir}/parser.%{SOABI_optimized}.so
%{dynload_dir}/pyexpat.%{SOABI_optimized}.so
%{dynload_dir}/readline.%{SOABI_optimized}.so
%{dynload_dir}/resource.%{SOABI_optimized}.so
%{dynload_dir}/select.%{SOABI_optimized}.so
%{dynload_dir}/spwd.%{SOABI_optimized}.so
%{dynload_dir}/syslog.%{SOABI_optimized}.so
%{dynload_dir}/termios.%{SOABI_optimized}.so
%{dynload_dir}/_testmultiphase.%{SOABI_optimized}.so
%{dynload_dir}/unicodedata.%{SOABI_optimized}.so
%{dynload_dir}/xxlimited.%{SOABI_optimized}.so
%{dynload_dir}/zlib.%{SOABI_optimized}.so

%dir %{pylibdir}/site-packages/
%dir %{pylibdir}/site-packages/__pycache__/
%{pylibdir}/site-packages/README.txt
%{pylibdir}/*.py
%dir %{pylibdir}/__pycache__/
%{pylibdir}/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/collections/
%dir %{pylibdir}/collections/__pycache__/
%{pylibdir}/collections/*.py
%{pylibdir}/collections/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/ctypes/
%dir %{pylibdir}/ctypes/__pycache__/
%{pylibdir}/ctypes/*.py
%{pylibdir}/ctypes/__pycache__/*%{bytecode_suffixes}
%{pylibdir}/ctypes/macholib

%{pylibdir}/curses

%dir %{pylibdir}/dbm/
%dir %{pylibdir}/dbm/__pycache__/
%{pylibdir}/dbm/*.py
%{pylibdir}/dbm/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/distutils/
%dir %{pylibdir}/distutils/__pycache__/
%{pylibdir}/distutils/*.py
%{pylibdir}/distutils/__pycache__/*%{bytecode_suffixes}
%{pylibdir}/distutils/README
%{pylibdir}/distutils/command
%exclude %{pylibdir}/distutils/command/wininst-*.exe

%dir %{pylibdir}/email/
%dir %{pylibdir}/email/__pycache__/
%{pylibdir}/email/*.py
%{pylibdir}/email/__pycache__/*%{bytecode_suffixes}
%{pylibdir}/email/mime
%doc %{pylibdir}/email/architecture.rst

%{pylibdir}/encodings

%{pylibdir}/html
%{pylibdir}/http

%dir %{pylibdir}/importlib/
%dir %{pylibdir}/importlib/__pycache__/
%{pylibdir}/importlib/*.py
%{pylibdir}/importlib/__pycache__/*%{bytecode_suffixes}

%dir %{pylibdir}/json/
%dir %{pylibdir}/json/__pycache__/
%{pylibdir}/json/*.py
%{pylibdir}/json/__pycache__/*%{bytecode_suffixes}

%{pylibdir}/logging
%{pylibdir}/multiprocessing

%dir %{pylibdir}/sqlite3/
%dir %{pylibdir}/sqlite3/__pycache__/
%{pylibdir}/sqlite3/*.py
%{pylibdir}/sqlite3/__pycache__/*%{bytecode_suffixes}

%exclude %{pylibdir}/turtle.py
%exclude %{pylibdir}/__pycache__/turtle*%{bytecode_suffixes}

%{pylibdir}/urllib
%{pylibdir}/xml

%if "%{_lib}" == "lib64"
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}/site-packages
%attr(0755,root,root) %dir %{_prefix}/lib/python%{pybasever}/site-packages/__pycache__/
%endif

# "Makefile" and the config-32/64.h file are needed by
# distutils/sysconfig.py:_init_posix(), so we include them in the core
# package, along with their parent directories (bug 531901):
%dir %{pylibdir}/config-%{LDVERSION_optimized}-%{_arch}-linux%{_gnu}/
%{pylibdir}/config-%{LDVERSION_optimized}-%{_arch}-linux%{_gnu}/Makefile
%dir %{_includedir}/python%{LDVERSION_optimized}/
%{_includedir}/python%{LDVERSION_optimized}/%{_pyconfig_h}

%{_libdir}/%{py_INSTSONAME_optimized}

%files devel
%{pylibdir}/config-%{LDVERSION_optimized}-%{_arch}-linux%{_gnu}/*
%exclude %{pylibdir}/config-%{LDVERSION_optimized}-%{_arch}-linux%{_gnu}/Makefile
%{pylibdir}/distutils/command/wininst-*.exe
%{_includedir}/python%{LDVERSION_optimized}/*.h
%exclude %{_includedir}/python%{LDVERSION_optimized}/%{_pyconfig_h}
%doc Misc/README.valgrind Misc/valgrind-python.supp Misc/gdbinit
%{_bindir}/python%{pybasever}-config
%{_bindir}/python%{LDVERSION_optimized}-config
%{_bindir}/python%{LDVERSION_optimized}-*-config
%{_libdir}/libpython%{LDVERSION_optimized}.so
%{_libdir}/pkgconfig/python-%{LDVERSION_optimized}.pc
%{_libdir}/pkgconfig/python-%{pybasever}.pc
/%{rpmmacrodir}/macros.pybytecompile%{pybasever}
/%{rpmmacrodir}/macros.python%{pybasever}

%files tools
%{_bindir}/2to3-%{pybasever}
%{_bindir}/idle*
%{pylibdir}/Tools
%doc %{pylibdir}/Doc

%files tkinter
%{pylibdir}/tkinter
%exclude %{pylibdir}/tkinter/test
%{dynload_dir}/_tkinter.%{SOABI_optimized}.so
%{pylibdir}/turtle.py
%{pylibdir}/__pycache__/turtle*%{bytecode_suffixes}
%dir %{pylibdir}/turtledemo
%{pylibdir}/turtledemo/*.py
%{pylibdir}/turtledemo/*.cfg
%dir %{pylibdir}/turtledemo/__pycache__/
%{pylibdir}/turtledemo/__pycache__/*%{bytecode_suffixes}

%files test
%{pylibdir}/ctypes/test
%{pylibdir}/distutils/tests
%{pylibdir}/sqlite3/test
%{pylibdir}/test
%{dynload_dir}/_ctypes_test.%{SOABI_optimized}.so
%{dynload_dir}/_testbuffer.%{SOABI_optimized}.so
%{dynload_dir}/_testcapi.%{SOABI_optimized}.so
%{dynload_dir}/_testimportmultiple.%{SOABI_optimized}.so
%{pylibdir}/lib2to3/tests
%{pylibdir}/tkinter/test
%{pylibdir}/unittest/test


# We don't bother splitting the debug build out into further subpackages:
# if you need it, you're probably a developer.

# Hence the manifest is the combination of analogous files in the manifests of
# all of the other subpackages

%if 0%{?with_debug_build}
%files debug

# Analog of the core subpackage's files:
%{_bindir}/python%{LDVERSION_debug}
%{_bindir}/python%{pybasever}-debug

# Analog of the -libs subpackage's files:
# ...with debug builds of the built-in "extension" modules:

%{dynload_dir}/_blake2.%{SOABI_debug}.so
%{dynload_dir}/_md5.%{SOABI_debug}.so
%{dynload_dir}/_sha1.%{SOABI_debug}.so
%{dynload_dir}/_sha256.%{SOABI_debug}.so
%{dynload_dir}/_sha3.%{SOABI_debug}.so
%{dynload_dir}/_sha512.%{SOABI_debug}.so

%{dynload_dir}/_asyncio.%{SOABI_debug}.so
%{dynload_dir}/_bisect.%{SOABI_debug}.so
%{dynload_dir}/_bz2.%{SOABI_debug}.so
%{dynload_dir}/_codecs_cn.%{SOABI_debug}.so
%{dynload_dir}/_codecs_hk.%{SOABI_debug}.so
%{dynload_dir}/_codecs_iso2022.%{SOABI_debug}.so
%{dynload_dir}/_codecs_jp.%{SOABI_debug}.so
%{dynload_dir}/_codecs_kr.%{SOABI_debug}.so
%{dynload_dir}/_codecs_tw.%{SOABI_debug}.so
%{dynload_dir}/_crypt.%{SOABI_debug}.so
%{dynload_dir}/_csv.%{SOABI_debug}.so
%{dynload_dir}/_ctypes.%{SOABI_debug}.so
%{dynload_dir}/_curses.%{SOABI_debug}.so
%{dynload_dir}/_curses_panel.%{SOABI_debug}.so
%{dynload_dir}/_dbm.%{SOABI_debug}.so
%{dynload_dir}/_decimal.%{SOABI_debug}.so
%{dynload_dir}/_elementtree.%{SOABI_debug}.so
%if 0%{?with_gdbm}
%{dynload_dir}/_gdbm.%{SOABI_debug}.so
%endif
%{dynload_dir}/_hashlib.%{SOABI_debug}.so
%{dynload_dir}/_heapq.%{SOABI_debug}.so
%{dynload_dir}/_json.%{SOABI_debug}.so
%{dynload_dir}/_lsprof.%{SOABI_debug}.so
%{dynload_dir}/_lzma.%{SOABI_debug}.so
%{dynload_dir}/_multibytecodec.%{SOABI_debug}.so
%{dynload_dir}/_multiprocessing.%{SOABI_debug}.so
%{dynload_dir}/_opcode.%{SOABI_debug}.so
%{dynload_dir}/_pickle.%{SOABI_debug}.so
%{dynload_dir}/_posixsubprocess.%{SOABI_debug}.so
%{dynload_dir}/_random.%{SOABI_debug}.so
%{dynload_dir}/_socket.%{SOABI_debug}.so
%{dynload_dir}/_sqlite3.%{SOABI_debug}.so
%{dynload_dir}/_ssl.%{SOABI_debug}.so
%{dynload_dir}/_struct.%{SOABI_debug}.so
%{dynload_dir}/array.%{SOABI_debug}.so
%{dynload_dir}/audioop.%{SOABI_debug}.so
%{dynload_dir}/binascii.%{SOABI_debug}.so
%{dynload_dir}/cmath.%{SOABI_debug}.so
%{dynload_dir}/_datetime.%{SOABI_debug}.so
%{dynload_dir}/fcntl.%{SOABI_debug}.so
%{dynload_dir}/grp.%{SOABI_debug}.so
%{dynload_dir}/math.%{SOABI_debug}.so
%{dynload_dir}/mmap.%{SOABI_debug}.so
%{dynload_dir}/nis.%{SOABI_debug}.so
%{dynload_dir}/ossaudiodev.%{SOABI_debug}.so
%{dynload_dir}/parser.%{SOABI_debug}.so
%{dynload_dir}/pyexpat.%{SOABI_debug}.so
%{dynload_dir}/readline.%{SOABI_debug}.so
%{dynload_dir}/resource.%{SOABI_debug}.so
%{dynload_dir}/select.%{SOABI_debug}.so
%{dynload_dir}/spwd.%{SOABI_debug}.so
%{dynload_dir}/syslog.%{SOABI_debug}.so
%{dynload_dir}/termios.%{SOABI_debug}.so
%{dynload_dir}/_testmultiphase.%{SOABI_debug}.so
%{dynload_dir}/unicodedata.%{SOABI_debug}.so
%{dynload_dir}/zlib.%{SOABI_debug}.so

# No need to split things out the "Makefile" and the config-32/64.h file as we
# do for the regular build above (bug 531901), since they're all in one package
# now; they're listed below, under "-devel":

%{_libdir}/libpython%{LDVERSION_debug}.so
%{_libdir}/%{py_INSTSONAME_debug}

# Analog of the -devel subpackage's files:
%{pylibdir}/config-%{LDVERSION_debug}-%{_arch}-linux%{_gnu}
%{_includedir}/python%{LDVERSION_debug}
%{_bindir}/python%{LDVERSION_debug}-config
%{_libdir}/pkgconfig/python-%{LDVERSION_debug}.pc

# Analog of the -tools subpackage's files:
#  None for now; we could build precanned versions that have the appropriate
# shebang if needed

# Analog  of the tkinter subpackage's files:
%{dynload_dir}/_tkinter.%{SOABI_debug}.so

# Analog  of the -test subpackage's files:
%{dynload_dir}/_ctypes_test.%{SOABI_debug}.so
%{dynload_dir}/_testbuffer.%{SOABI_debug}.so
%{dynload_dir}/_testcapi.%{SOABI_debug}.so
%{dynload_dir}/_testimportmultiple.%{SOABI_debug}.so

%endif # with_debug_build

# We put the debug-gdb.py file inside /usr/lib/debug to avoid noise from ldconfig
# See https://bugzilla.redhat.com/show_bug.cgi?id=562980
#
# The /usr/lib/rpm/redhat/macros defines %%__debug_package to use
# debugfiles.list, and it appears that everything below /usr/lib/debug and
# (/usr/src/debug) gets added to this file (via LISTFILES) in
# /usr/lib/rpm/find-debuginfo.sh
#
# Hence by installing it below /usr/lib/debug we ensure it is added to the
# -debuginfo subpackage
# (if it doesn't, then the rpmbuild ought to fail since the debug-gdb.py
# payload file would be unpackaged)


# ======================================================
# Finally, the changelog:
# ======================================================

%changelog
* Thu Jul 05 2018 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 3.6.5
- Port from IUS

* Mon Apr 09 2018 Carl George <carl@george.computer> - 3.6.5-1.ius
- Latest upstream
- Fix deprecation warning on using imp in check-pyc-and-pyo-timestamps.py (Fedora)
- Skip test_zlib on el6

* Tue Dec 19 2017 Ben Harper <ben.harper@rackspace.com> - 3.6.4-1.ius
- Latest upstream
- Remove Patch277 and Patch279, fixed upstream

* Wed Oct 11 2017 Carl George <carl@george.computer> - 3.6.3-1.ius
- Latest upstream
- Skip test_bdist_rpm using test config rather than a patch (removes patch 137) (Fedora)
- Add patch277 to fix two hanging tests from test_subprocess (Fedora)
- Fix memory corruption due to allocator mix rhbz#1498207 (Fedora)
- Use a larger stack size on EL6
- Conditionalize systemtap-devel BuildRequires (Fedora)
- Drop patches 157 and 188
- Merge lib64 patches (104 into 102) (Fedora)
- Merge patches 180, 206, 243, 5001 (architecture naming) into new patch 274 (Fedora)
- Run autotools to generate the configure script before building (Fedora)
- Use bundled expat on EL6
- Move windows executables to the devel subpackage (rhbz#1426257) (Fedora)
- Drop patch252, as it was deemed unnecessary and could possibly collide with `pip --editable` option (Fedora)
- Use autoconf268 on EL6

* Tue Jul 18 2017 Carl George <carl.george@rackspace.com> - 3.6.2-1.ius
- Latest upstream
- Rebase patch180
- Remove patch249, resolved upstream pybt#28787
- Remove patch258, resolved upstream pybt#29324

* Thu Apr 06 2017 Carl George <carl.george@rackspace.com> - 3.6.1-2.ius
- EL6 support
- Remove minimum sqlite version (pybt#10740 and pybt#29098)
- Require correct version of expat{,-devel}
- Install the Makefile in its proper location (rhbz#1438219) (Fedora)
- Skip tan0064 in test_math and test_cmath on 32bit

* Wed Mar 22 2017 Carl George <carl.george@rackspace.com> - 3.6.1-1.ius
- Latest upstream
- Add --executable option to install.py command (Fedora)
- Fix syntax error in %%py_byte_compile macro (rhbz#1433569) (Fedora)
- Skip test_aead_aes_gcm during rpmbuild (Fedora)

* Thu Jan 19 2017 Carl George <carl.george@rackspace.com> - 3.6.0-2.ius
- Don't blow up on EL7 kernel (random generator) (rhbz#1410175) (Fedora)
- Define HAVE_LONG_LONG as 1 for backwards compatibility (Fedora)
- Fix error check, so that Random.seed actually uses OS randomness (rhbz#1412275) (Fedora)

* Wed Dec 28 2016 Carl George <carl.george@rackspace.com> - 3.6.0-1.ius
- Port from Fedora to IUS
- Remove rewheel
- Undo https://fedoraproject.org/wiki/Changes/System_Python
- Import altinstall changes from EPEL's python34
- Cleanup libpython* files
- Add macros to optionally include the latest wheels of setuptools and pip
- Set minimum sqlite version
- Patch186 merged upstream

* Tue Dec 27 2016 Charalampos Stratakis <cstratak@redhat.com> - 3.6.0-1
- Update to Python 3.6.0 final

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 3.6.0-0.6.rc1
- Enable rewheel

* Wed Dec 07 2016 Charalampos Stratakis <cstratak@redhat.com> - 3.6.0-0.5.rc1
- Update to Python 3.6.0 release candidate 1

* Mon Dec 05 2016 Charalampos Stratakis <cstratak@redhat.com> - 3.6.0-0.4.b4
- Update to Python 3.6.0 beta 4

* Mon Dec 05 2016 Charalampos Stratakis <cstratak@redhat.com> - 3.5.2-7
- Set to work with pip version 9.0.1

* Wed Oct 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 3.5.2-6
- Use proper patch numbering and base upstream branch for
porting ssl and hashlib modules to OpenSSL 1.1.0
- Drop hashlib patch for now
- Add riscv64 arch to 64bit and no-valgrind arches

* Tue Oct 11 2016 Tomáš Mráz <tmraz@redhat.com> - 3.5.2-5
- Make it build with OpenSSL-1.1.0 based on upstream patch

* Wed Sep 14 2016 Charalampos Stratakis <cstratak@redhat.com> - 3.5.2-4
- Obsolete and Provide python35 package

* Mon Sep 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 3.5.2-3
- Update %%py_byte_compile macro
- Remove unused configure flags (rhbz#1374357)

* Fri Sep 09 2016 Tomas Orsava <torsava@redhat.com> - 3.5.2-2
- Updated .pyc 'bytecompilation with the newly installed interpreter' to also
  recompile optimized .pyc files
- Removed .pyo 'bytecompilation with the newly installed interpreter', as .pyo
  files are no more
- Resolves rhbz#1373635

* Mon Aug 15 2016 Tomas Orsava <torsava@redhat.com> - 3.5.2-1
- Rebased to version 3.5.2
- Set to work with pip version 8.1.2
- Removed patches 207, 237, 241 as fixes are already contained in Python 3.5.2
- Removed arch or environment specific patches 194, 196, 203, and 208
  as test builds indicate they are no longer needed
- Updated patches 102, 146, and 242 to work with the new Python codebase
- Removed patches 200, 201, 5000 which weren't even being applied

* Tue Aug 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 3.5.1-15
- Fix for CVE-2016-1000110 HTTPoxy attack
- SPEC file cleanup

* Mon Aug 01 2016 Michal Toman <mtoman@fedoraproject.org> - 3.5.1-14
- Build properly on MIPS

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.1-13
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jul 08 2016 Charalampos Stratakis <cstratak@redhat.com> - 3.5.1-12
- Refactor patch for properly fixing CVE-2016-5636

* Fri Jul 08 2016 Charalampos Stratakis <cstratak@redhat.com> - 3.5.1-11
- Fix test_pyexpat failure with Expat version of 2.2.0

* Fri Jul 08 2016 Miro Hrončok <mhroncok@redhat.com> - 3.5.1-10
- Move xml module to system-python-libs

* Thu Jun 16 2016 Tomas Orsava <torsava@redhat.com> - 3.5.1-9
- Fix for: CVE-2016-0772 python: smtplib StartTLS stripping attack
- Raise an error when STARTTLS fails
- rhbz#1303647: https://bugzilla.redhat.com/show_bug.cgi?id=1303647
- rhbz#1346345: https://bugzilla.redhat.com/show_bug.cgi?id=1346345
- Fixed upstream: https://hg.python.org/cpython/rev/d590114c2394

* Mon Jun 13 2016 Charalampos Stratakis <cstratak@redhat.com> - 3.5.1-8
- Added patch for fixing possible integer overflow and heap corruption in zipimporter.get_data()

* Fri Mar 04 2016 Miro Hrončok <mhroncok@redhat.com> - 3.5.1-7
- Move distutils to system-python-libs

* Wed Feb 24 2016 Robert Kuska <rkuska@redhat.com> - 3.5.1-6
- Provide python3-enum34

* Fri Feb 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.5.1-5
- Provide System Python packages and macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 13 2016 Orion Poplwski <orion@cora.nwra.com> - 3.5.1-2
- Drop python3 macros, require python/python3-rpm-macros

* Mon Dec 14 2015 Robert Kuska <rkuska@redhat.com> - 3.5.1-1
- Update to 3.5.1
- Removed patch 199 and 207 (upstream)

* Sun Nov 15 2015 Robert Kuska <rkuska@redhat.com> - 3.5.0-5
- Remove versioned libpython from devel package

* Fri Nov 13 2015 Than Ngo <than@redhat.com> 3.5.0-4
- add correct arch for ppc64/ppc64le to fix build failure

* Wed Nov 11 2015 Robert Kuska <rkuska@redhat.com> - 3.5.0-3
- Hide the private _Py_atomic_xxx symbols from public header

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 3.5.0-2
- Rebuild with wheel set to 1

* Tue Sep 15 2015 Matej Stuchlik <mstuchli@redhat.com> - 3.5.0-1
- Update to 3.5.0

* Mon Jun 29 2015 Thomas Spura <tomspur@fedoraproject.org> - 3.4.3-4
- python3-devel: Require python-macros for version independant macros such as
  python_provide. See fpc#281 and fpc#534.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 17 2015 Matej Stuchlik <mstuchli@redhat.com> - 3.4.3-4
- Use 1024bit DH key in test_ssl
- Use -O0 when compiling -debug build
- Update pip version variable to the version we actually ship

* Wed Jun 17 2015 Matej Stuchlik <mstuchli@redhat.com> - 3.4.3-3
- Make relocating Python by changing _prefix actually work
Resolves: rhbz#1231801

* Mon May  4 2015 Peter Robinson <pbrobinson@fedoraproject.org> 3.4.3-2
- Disable test_gdb on aarch64 (rhbz#1196181), it joins all other non x86 arches

* Thu Mar 12 2015 Matej Stuchlik <mstuchli@redhat.com> - 3.4.3-1
- Updated to 3.4.3
- BuildPython now accepts additional build options
- Temporarily disabled test_gdb on arm (rhbz#1196181)

* Wed Feb 25 2015 Matej Stuchlik <mstuchli@redhat.com> - 3.4.2-7
- Fixed undefined behaviour in faulthandler which caused test to hang on x86_64
  (http://bugs.python.org/issue23433)

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 3.4.2-6
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Tue Feb 17 2015 Ville Skyttä <ville.skytta@iki.fi> - 3.4.2-5
- Own systemtap dirs (#710733)

* Mon Jan 12 2015 Dan Horák <dan[at]danny.cz> - 3.4.2-4
- build with valgrind on ppc64le
- disable test_gdb on s390(x) until rhbz#1181034 is resolved

* Tue Dec 16 2014 Robert Kuska <rkuska@redhat.com> - 3.4.2-3
- New patches: 170 (gc asserts), 200 (gettext headers),
  201 (gdbm memory leak)

* Thu Dec 11 2014 Robert Kuska <rkuska@redhat.com> - 3.4.2-2
- OpenSSL disabled SSLv3 in SSLv23 method

* Thu Nov 13 2014 Matej Stuchlik <mstuchli@redhat.com> - 3.4.2-1
- Update to 3.4.2
- Refreshed patches: 156 (gdb autoload)
- Removed: 195 (Werror declaration), 197 (CVE-2014-4650)

* Mon Nov 03 2014 Slavek Kabrda <bkabrda@redhat.com> - 3.4.1-16
- Fix CVE-2014-4650 - CGIHTTPServer URL handling
Resolves: rhbz#1113529

* Sun Sep 07 2014 Karsten Hopp <karsten@redhat.com> 3.4.1-15
- exclude test_gdb on ppc* (rhbz#1132488)

* Thu Aug 21 2014 Slavek Kabrda <bkabrda@redhat.com> - 3.4.1-14
- Update rewheel patch with fix from https://github.com/bkabrda/rewheel/pull/1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun  8 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.4.1-12
- aarch64 has valgrind, just list those that don't support it

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun 04 2014 Karsten Hopp <karsten@redhat.com> 3.4.1-10
- bump release and rebuild to link with the correct tcl/tk libs on ppcle

* Tue Jun 03 2014 Matej Stuchlik <mstuchli@redhat.com> - 3.4.1-9
- Change paths to bundled projects in rewheel patch

* Fri May 30 2014 Miro Hrončok <mhroncok@redhat.com> - 3.4.1-8
- In config script, use uname -m to write the arch

* Thu May 29 2014 Dan Horák <dan[at]danny.cz> - 3.4.1-7
- update the arch list where valgrind exists - %%power64 includes also
    ppc64le which is not supported yet

* Thu May 29 2014 Miro Hrončok <mhroncok@redhat.com> - 3.4.1-6
- Forward arguments to the arch specific config script
Resolves: rhbz#1102683

* Wed May 28 2014 Miro Hrončok <mhroncok@redhat.com> - 3.4.1-5
- Rename python3.Xm-config script to arch specific.
Resolves: rhbz#1091815

* Tue May 27 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 3.4.1-4
- Use python3-*, not python-* runtime requires on setuptools and pip
- rebuild for tcl-8.6

* Tue May 27 2014 Matej Stuchlik <mstuchli@redhat.com> - 3.4.1-3
- Update the rewheel module

* Mon May 26 2014 Miro Hrončok <mhroncok@redhat.com> - 3.4.1-2
- Fix multilib dependencies.
Resolves: rhbz#1091815

* Sun May 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 3.4.1-1
- Update to Python 3.4.1

* Sun May 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 3.4.0-8
- Fix test_gdb failure on ppc64le
Resolves: rhbz#1095355

* Thu May 22 2014 Miro Hrončok <mhroncok@redhat.com> - 3.4.0-7
- Add macro %%python3_version_nodots

* Sun May 18 2014 Matej Stuchlik <mstuchli@redhat.com> - 3.4.0-6
- Disable test_faulthandler, test_gdb on aarch64
Resolves: rhbz#1045193

* Fri May 16 2014 Matej Stuchlik <mstuchli@redhat.com> - 3.4.0-5
- Don't add Werror=declaration-after-statement for extension
  modules through setup.py (PyBT#21121)

* Mon May 12 2014 Matej Stuchlik <mstuchli@redhat.com> - 3.4.0-4
- Add setuptools and pip to Requires

* Tue Apr 29 2014 Matej Stuchlik <mstuchli@redhat.com> - 3.4.0-3
- Point __os_install_post to correct brp-* files

* Tue Apr 15 2014 Matej Stuchlik <mstuchli@redhat.com> - 3.4.0-2
- Temporarily disable tests requiring SIGHUP (rhbz#1088233)

* Tue Apr 15 2014 Matej Stuchlik <mstuchli@redhat.com> - 3.4.0-1
- Update to Python 3.4 final
- Add patch adding the rewheel module
- Merge patches from master

* Wed Jan 08 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 3.4.0-0.1.b2
- Update to Python 3.4 beta 2.
- Refreshed patches: 55 (systemtap), 146 (hashlib-fips), 154 (test_gdb noise)
- Dropped patches: 114 (statvfs constants), 177 (platform unicode)

* Mon Nov 25 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 3.4.0-0.1.b1
- Update to Python 3.4 beta 1.
- Refreshed patches: 102 (lib64), 111 (no static lib), 125 (less verbose COUNT
ALLOCS), 141 (fix COUNT_ALLOCS in test_module), 146 (hashlib fips),
157 (UID+GID overflows), 173 (ENOPROTOOPT in bind_port)
- Removed patch 00187 (remove pthread atfork; upstreamed)

* Mon Nov 04 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 3.4.0-0.1.a4
- Update to Python 3.4 alpha 4.
- Refreshed patches: 55 (systemtap), 102 (lib64), 111 (no static lib),
114 (statvfs flags), 132 (unittest rpmbuild hooks), 134 (fix COUNT_ALLOCS in
test_sys), 143 (tsc on ppc64), 146 (hashlib fips), 153 (test gdb noise),
157 (UID+GID overflows), 173 (ENOPROTOOPT in bind_port), 186 (dont raise
from py_compile)
- Removed patches: 129 (test_subprocess nonreadable dir - no longer fails in
Koji), 142 (the mock issue that caused this is fixed)
- Added patch 187 (remove thread atfork) - will be in next version
- Refreshed script for checking pyc and pyo timestamps with new ignored files.
- The fips patch is disabled for now until upstream makes a final decision
what to do with sha3 implementation for 3.4.0.

* Wed Oct 30 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 3.3.2-7
- Bytecompile all *.py files properly during build (rhbz#1023607)

* Fri Aug 23 2013 Matej Stuchlik <mstuchli@redhat.com> - 3.3.2-6
- Added fix for CVE-2013-4238 (rhbz#996399)

* Fri Jul 26 2013 Dennis Gilmore <dennis@ausil.us> - 3.3.2-5
- fix up indentation in arm patch

* Fri Jul 26 2013 Dennis Gilmore <dennis@ausil.us> - 3.3.2-4
- disable a test that fails on arm
- enable valgrind support on arm arches

* Tue Jul 02 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 3.3.2-3
- Fix build with libffi containing multilib wrapper for ffi.h (rhbz#979696).

* Mon May 20 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 3.3.2-2
- Add patch for CVE-2013-2099 (rhbz#963261).

* Thu May 16 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 3.3.2-1
- Updated to Python 3.3.2.
- Refreshed patches: 153 (gdb test noise)
- Dropped patches: 175 (configure -Wformat, fixed upstream), 182 (gdb
test threads)
- Synced patch numbers with python.spec.

* Thu May  9 2013 David Malcolm <dmalcolm@redhat.com> - 3.3.1-4
- fix test.test_gdb.PyBtTests.test_threads on ppc64 (patch 181; rhbz#960010)

* Thu May 02 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 3.3.1-3
- Add patch that enables building on ppc64p7 (replace the sed, so that
we get consistent with python2 spec and it's more obvious that we're doing it.

* Wed Apr 24 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 3.3.1-2
- Add fix for gdb tests failing on arm, rhbz#951802.

* Tue Apr 09 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 3.3.1-1
- Updated to Python 3.3.1.
- Refreshed patches: 55 (systemtap), 111 (no static lib), 146 (hashlib fips),
153 (fix test_gdb noise), 157 (uid, gid overflow - fixed upstream, just
keeping few more downstream tests)
- Removed patches: 3 (audiotest.au made it to upstream tarball)
- Removed workaround for http://bugs.python.org/issue14774, discussed in
http://bugs.python.org/issue15298 and fixed in revision 24d52d3060e8.

* Mon Mar 25 2013 David Malcolm <dmalcolm@redhat.com> - 3.3.0-10
- fix gcc 4.8 incompatibility (rhbz#927358); regenerate autotool intermediates

* Mon Mar 25 2013 David Malcolm <dmalcolm@redhat.com> - 3.3.0-9
- renumber patches to keep them in sync with python.spec

* Fri Mar 15 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 3.3.0-8
- Fix error in platform.platform() when non-ascii byte strings are decoded to
  unicode (rhbz#922149)

* Thu Mar 14 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 3.3.0-7
- Fix up shared library extension (rhbz#889784)

* Thu Mar 07 2013 Karsten Hopp <karsten@redhat.com> 3.3.0-6
- add ppc64p7 build target, optimized for Power7

* Mon Mar  4 2013 David Malcolm <dmalcolm@redhat.com> - 3.3.0-5
- add workaround for ENOPROTOOPT seen running selftests in Koji
(rhbz#913732)

* Mon Mar  4 2013 David Malcolm <dmalcolm@redhat.com> - 3.3.0-4
- remove config flag from /etc/rpm/macros.{python3|pybytecompile}

* Mon Feb 11 2013 David Malcolm <dmalcolm@redhat.com> - 3.3.0-3
- add aarch64 (rhbz#909783)

* Thu Nov 29 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.0-2
- add BR on bluez-libs-devel (rhbz#879720)

* Sat Sep 29 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.0-1
- 3.3.0rc3 -> 3.3.0; drop alphatag

* Mon Sep 24 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.0-0.6.rc3
- 3.3.0rc2 -> 3.3.0rc3

* Mon Sep 10 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.0-0.5.rc2
- 3.3.0rc1 -> 3.3.0rc2; refresh patch 55

* Mon Aug 27 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.0-0.4.rc1
- 3.3.0b2 -> 3.3.0rc1; refresh patches 3, 55

* Mon Aug 13 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.0-0.3.b2
- 3.3b1 -> 3.3b2; drop upstreamed patch 152; refresh patches 3, 102, 111,
134, 153, 160; regenenerate autotools patch; rework systemtap patch to work
correctly when LANG=C (patch 55); importlib.test was moved to
test.test_importlib upstream

* Mon Aug 13 2012 Karsten Hopp <karsten@redhat.com> 3.3.0-0.2.b1
- disable some failing checks on PPC* (rhbz#846849)

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.0-0.1.b1
- 3.2 -> 3.3: https://fedoraproject.org/wiki/Features/Python_3.3
- 3.3.0b1: refresh patches 3, 55, 102, 111, 113, 114, 134, 157; drop upstream
patch 147; regenenerate autotools patch; drop "--with-wide-unicode" from
configure (PEP 393); "plat-linux2" -> "plat-linux" (upstream issue 12326);
"bz2" -> "_bz2" and "crypt" -> "_crypt"; egg-info files are no longer shipped
for stdlib (upstream issues 10645 and 12218); email/test moved to
test/test_email; add /usr/bin/pyvenv[-3.3] and venv module (PEP 405); add
_decimal and _lzma modules; make collections modules explicit in payload again
(upstream issue 11085); add _testbuffer module to tests subpackage (added in
upstream commit 3f9b3b6f7ff0); fix test failures (patches 160 and 161);
workaround erroneously shared _sysconfigdata.py upstream issue #14774; fix
distutils.sysconfig traceback (patch 162); add BuildRequires: xz-devel (for
_lzma module); skip some tests within test_socket (patch 163)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 20 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.0-0.1.b1

* Fri Jun 22 2012 David Malcolm <dmalcolm@redhat.com> - 3.2.3-10
- use macro for power64 (rhbz#834653)

* Mon Jun 18 2012 David Malcolm <dmalcolm@redhat.com> - 3.2.3-9
- fix missing include in uid/gid handling patch (patch 157; rhbz#830405)

* Wed May 30 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 3.2.3-8
- fix tapset for debug build

* Tue May 15 2012 David Malcolm <dmalcolm@redhat.com> - 3.2.3-7
- update uid/gid handling to avoid int overflows seen with uid/gid
values >= 2^31 on 32-bit architectures (patch 157; rhbz#697470)

* Fri May  4 2012 David Malcolm <dmalcolm@redhat.com> - 3.2.3-6
- renumber autotools patch from 300 to 5000
- specfile cleanups

* Mon Apr 30 2012 David Malcolm <dmalcolm@redhat.com> - 3.2.3-5
- fix test_gdb.py (patch 156; rhbz#817072)

* Fri Apr 20 2012 David Malcolm <dmalcolm@redhat.com> - 3.2.3-4
- avoid allocating thunks in ctypes unless absolutely necessary, to avoid
generating SELinux denials on "import ctypes" and "import uuid" when embedding
Python within httpd (patch 155; rhbz#814391)

* Fri Apr 20 2012 David Malcolm <dmalcolm@redhat.com> - 3.2.3-3
- add explicit version requirements on expat to avoid linkage problems with
XML_SetHashSalt

* Thu Apr 12 2012 David Malcolm <dmalcolm@redhat.com> - 3.2.3-2
- fix test_gdb (patch 153)

* Wed Apr 11 2012 David Malcolm <dmalcolm@redhat.com> - 3.2.3-1
- 3.2.3; refresh patch 102 (lib64); drop upstream patches 148 (gdbm magic
values), 149 (__pycache__ fix); add patch 152 (test_gdb regex)

* Thu Feb  9 2012 Thomas Spura <tomspur@fedoraproject.org> - 3.2.2-13
- use newly installed python for byte compiling (now for real)

* Sun Feb  5 2012 Thomas Spura <tomspur@fedoraproject.org> - 3.2.2-12
- use newly installed python for byte compiling (#787498)

* Wed Jan  4 2012 Ville Skyttä <ville.skytta@iki.fi> - 3.2.2-11
- Build with $RPM_LD_FLAGS (#756863).
- Use xz-compressed source tarball.

* Wed Dec 07 2011 Karsten Hopp <karsten@redhat.com> 3.2.2-10
- disable rAssertAlmostEqual in test_cmath on PPC (#750811)

* Mon Oct 17 2011 Rex Dieter <rdieter@fedoraproject.org> - 3.2.2-9
- python3-devel missing autogenerated pkgconfig() provides (#746751)

* Mon Oct 10 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.2-8
- cherrypick fix for distutils not using __pycache__ when byte-compiling
files (rhbz#722578)

* Fri Sep 30 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.2-7
- re-enable gdbm (patch 148; rhbz#742242)

* Fri Sep 16 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.2-6
- add a sys._debugmallocstats() function (patch 147)

* Wed Sep 14 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.2-5
- support OpenSSL FIPS mode in _hashlib and hashlib; don't build the _md5 and
_sha* modules, relying on _hashlib in hashlib (rhbz#563986; patch 146)

* Tue Sep 13 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.2-4
- disable gdbm module to prepare for gdbm soname bump

* Mon Sep 12 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.2-3
- renumber and rename patches for consistency with python.spec (8 to 55, 106
to 104, 6 to 111, 104 to 113, 105 to 114, 125, 131, 130 to 143)

* Sat Sep 10 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.2-2
- rewrite of "check", introducing downstream-only hooks for skipping specific
cases in an rpmbuild (patch 132), and fixing/skipping failing tests in a more
fine-grained manner than before; (patches 106, 133-142 sparsely, moving
patches for consistency with python.spec: 128 to 134, 126 to 135, 127 to 141)

* Tue Sep  6 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.2-1
- 3.2.2

* Thu Sep  1 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.1-7
- run selftests with "--verbose"
- disable parts of test_io on ppc (rhbz#732998)

* Wed Aug 31 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.1-6
- use "--findleaks --verbose3" when running test suite

* Tue Aug 23 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.1-5
- re-enable and fix the --with-tsc option on ppc64, and rework it on 32-bit
ppc to avoid aliasing violations (patch 130; rhbz#698726)

* Tue Aug 23 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.1-4
- don't use --with-tsc on ppc64 debug builds (rhbz#698726)

* Thu Aug 18 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.1-3
- add %%python3_version to the rpm macros (rhbz#719082)

* Mon Jul 11 2011 Dennis Gilmore <dennis@ausil.us> - 3.2.1-2
- disable some tests on sparc arches

* Mon Jul 11 2011 David Malcolm <dmalcolm@redhat.com> - 3.2.1-1
- 3.2.1; refresh lib64 patch (102), subprocess unit test patch (129), disabling
of static library build (due to Modules/_testembed; patch 6), autotool
intermediates (patch 300)

* Fri Jul  8 2011 David Malcolm <dmalcolm@redhat.com> - 3.2-5
- use the gdb hooks from the upstream tarball, rather than keeping our own copy

* Fri Jul  8 2011 David Malcolm <dmalcolm@redhat.com> - 3.2-4
- don't run test_openpty and test_pty in %%check

* Fri Jul  8 2011 David Malcolm <dmalcolm@redhat.com> - 3.2-3
- cleanup of BuildRequires; add comment headings to specfile sections

* Tue Apr 19 2011 David Malcolm <dmalcolm@redhat.com> - 3.2-2
- fix the libpython.stp systemtap tapset (rhbz#697730)

* Mon Feb 21 2011 David Malcolm <dmalcolm@redhat.com> - 3.2-1
- 3.2
- drop alphatag
- regenerate autotool patch

* Mon Feb 14 2011 David Malcolm <dmalcolm@redhat.com> - 3.2-0.13.rc3
- add a /usr/bin/python3-debug symlink within the debug subpackage

* Mon Feb 14 2011 David Malcolm <dmalcolm@redhat.com> - 3.2-0.12.rc3
- 3.2rc3
- regenerate autotool patch

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-0.11.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 31 2011 David Malcolm <dmalcolm@redhat.com> - 3.2-0.10.rc2
- 3.2rc2

* Mon Jan 17 2011 David Malcolm <dmalcolm@redhat.com> - 3.2-0.9.rc1
- 3.2rc1
- rework patch 6 (static lib removal)
- remove upstreamed patch 130 (ppc debug build)
- regenerate patch 300 (autotool intermediates)
- updated packaging to reflect upstream rewrite of "Demo" (issue 7962)
- added libpython3.so and 2to3-3.2

* Wed Jan  5 2011 David Malcolm <dmalcolm@redhat.com> - 3.2-0.8.b2
- set EXTRA_CFLAGS to our CFLAGS, rather than overriding OPT, fixing a linker
error with dynamic annotations (when configured using --with-valgrind)
- fix the ppc build of the debug configuration (patch 130; rhbz#661510)

* Tue Jan  4 2011 David Malcolm <dmalcolm@redhat.com> - 3.2-0.7.b2
- add --with-valgrind to configuration (on architectures that support this)

* Wed Dec 29 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-0.6.b2
- work around test_subprocess failure seen in koji (patch 129)

* Tue Dec 28 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-0.5.b2
- 3.2b2
- rework patch 3 (removal of mimeaudio tests), patch 6 (no static libs),
patch 8 (systemtap), patch 102 (lib64)
- remove patch 4 (rendered redundant by upstream r85537), patch 103 (PEP 3149),
patch 110 (upstreamed expat fix), patch 111 (parallel build fix for grammar
fixed upstream)
- regenerate patch 300 (autotool intermediates)
- workaround COUNT_ALLOCS weakref issues in test suite (patch 126, patch 127,
patch 128)
- stop using runtest.sh in %%check (dropped by upstream), replacing with
regrtest; fixup list of failing tests
- introduce "pyshortver", "SOABI_optimized" and "SOABI_debug" macros
- rework manifests of shared libraries to use "SOABI_" macros, reflecting
PEP 3149
- drop itertools, operator and _collections modules from the manifests as py3k
commit r84058 moved these inside libpython; json/tests moved to test/json_tests
- move turtle code into the tkinter subpackage

* Wed Nov 17 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-0.5.a1
- fix sysconfig to not rely on the -devel subpackage (rhbz#653058)

* Thu Sep  9 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-0.4.a1
- move most of the content of the core package to the libs subpackage, given
that the libs aren't meaningfully usable without the standard libraries

* Wed Sep  8 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-0.3.a1
- Move test.support to core package (rhbz#596258)
- Add various missing __pycache__ directories to payload

* Sun Aug 22 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 3.2-0.2.a1
- Add __pycache__ directory for site-packages

* Sun Aug 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 3.2-0.1.a1
- on 64bit "stdlib" was still "/usr/lib/python*" (modify *lib64.patch)
- make find-provides-without-python-sonames.sh 64bit aware

* Sat Aug 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.2-0.0.a1
- 3.2a1; add alphatag
- rework %%files in the light of PEP 3147 (__pycache__)
- drop our configuration patch to Setup.dist (patch 0): setup.py should do a
better job of things, and the %%files explicitly lists our modules (r82746
appears to break the old way of doing things).  This leads to various modules
changing from "foomodule.so" to "foo.so".  It also leads to the optimized build
dropping the _sha1, _sha256 and _sha512 modules, but these are provided by
_hashlib; _weakref becomes a builtin module; xxsubtype goes away (it's only for
testing/devel purposes)
- fixup patches 3, 4, 6, 8, 102, 103, 105, 111 for the rebase
- remove upstream patches: 7 (system expat), 106, 107, 108 (audioop reformat
plus CVE-2010-1634 and CVE-2010-2089), 109 (CVE-2008-5983)
- add machinery for rebuilding "configure" and friends, using the correct
version of autoconf (patch 300)
- patch the debug build's usage of COUNT_ALLOCS to be less verbose (patch 125)
- "modulator" was removed upstream
- drop "-b" from patch applications affecting .py files to avoid littering the
installation tree

* Thu Aug 19 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 3.1.2-13
- Turn on computed-gotos.
- Fix for parallel make and graminit.c

* Fri Jul  2 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-12
- rebuild

* Fri Jul  2 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-11
- Fix an incompatibility between pyexpat and the system expat-2.0.1 that led to
a segfault running test_pyexpat.py (patch 110; upstream issue 9054; rhbz#610312)

* Fri Jun  4 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-10
- ensure that the compiler is invoked with "-fwrapv" (rhbz#594819)
- reformat whitespace in audioop.c (patch 106)
- CVE-2010-1634: fix various integer overflow checks in the audioop
module (patch 107)
- CVE-2010-2089: further checks within the audioop module (patch 108)
- CVE-2008-5983: the new PySys_SetArgvEx entry point from r81399 (patch 109)

* Thu May 27 2010 Dan Horák <dan[at]danny.cz> - 3.1.2-9
- reading the timestamp counter is available only on some arches (see Python/ceval.c)

* Wed May 26 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-8
- add flags for statvfs.f_flag to the constant list in posixmodule (i.e. "os")
(patch 105)

* Tue May 25 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-7
- add configure-time support for COUNT_ALLOCS and CALL_PROFILE debug options
(patch 104); enable them and the WITH_TSC option within the debug build

* Mon May 24 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-6
- build and install two different configurations of Python 3: debug and
standard, packaging the debug build in a new "python3-debug" subpackage
(patch 103)

* Tue Apr 13 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-5
- exclude test_http_cookies when running selftests, due to hang seen on
http://koji.fedoraproject.org/koji/taskinfo?taskID=2088463 (cancelled after
11 hours)
- update python-gdb.py from v5 to py3k version submitted upstream

* Wed Mar 31 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-4
- update python-gdb.py from v4 to v5 (improving performance and stability,
adding commands)

* Thu Mar 25 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-3
- update python-gdb.py from v3 to v4 (fixing infinite recursion on reference
cycles and tracebacks on bytes 0x80-0xff in strings, adding handlers for sets
and exceptions)

* Wed Mar 24 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-2
- refresh gdb hooks to v3 (reworking how they are packaged)

* Sun Mar 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-1
- update to 3.1.2: http://www.python.org/download/releases/3.1.2/
- drop upstreamed patch 2 (.pyc permissions handling)
- drop upstream patch 5 (fix for the test_tk and test_ttk_* selftests)
- drop upstreamed patch 200 (path-fixing script)

* Sat Mar 20 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-28
- fix typo in libpython.stp (rhbz:575336)

* Fri Mar 12 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-27
- add pyfuntop.stp example (source 7)
- convert usage of $$RPM_BUILD_ROOT to %%{buildroot} throughout, for
consistency with python.spec

* Mon Feb 15 2010 Thomas Spura <tomspur@fedoraproject.org> - 3.1.1-26
- rebuild for new package of redhat-rpm-config (rhbz:564527)
- use 'install -p' when running 'make install'

* Fri Feb 12 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-25
- split configure options into multiple lines for easy of editing
- add systemtap static markers (wcohen, mjw, dmalcolm; patch 8), a systemtap
tapset defining "python.function.entry" and "python.function.return" to make
the markers easy to use (dmalcolm; source 5), and an example of using the
tapset to the docs (dmalcolm; source 6) (rhbz:545179)

* Mon Feb  8 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-24
- move the -gdb.py file from %%{_libdir}/INSTSONAME-gdb.py to
%%{_prefix}/lib/debug/%%{_libdir}/INSTSONAME.debug-gdb.py to avoid noise from
ldconfig (bug 562980), and which should also ensure it becomes part of the
debuginfo subpackage, rather than the libs subpackage
- introduce %%{py_SOVERSION} and %%{py_INSTSONAME} to reflect the upstream
configure script, and to avoid fragile scripts that try to figure this out
dynamically (e.g. for the -gdb.py change)

* Mon Feb  8 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-23
- add gdb hooks for easier debugging (Source 4)

* Thu Jan 28 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-22
- update python-3.1.1-config.patch to remove downstream customization of build
of pyexpat and elementtree modules
- add patch adapted from upstream (patch 7) to add support for building against
system expat; add --with-system-expat to "configure" invocation
- remove embedded copies of expat and zlib from source tree during "prep"

* Mon Jan 25 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-21
- introduce %%{dynload_dir} macro
- explicitly list all lib-dynload files, rather than dynamically gathering the
payload into a temporary text file, so that we can be sure what we are
shipping
- introduce a macros.pybytecompile source file, to help with packaging python3
modules (Source3; written by Toshio)
- rename "2to3-3" to "python3-2to3" to better reflect python 3 module packaging
plans

* Mon Jan 25 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-20
- change python-3.1.1-config.patch to remove our downstream change to curses
configuration in Modules/Setup.dist, so that the curses modules are built using
setup.py with the downstream default (linking against libncursesw.so, rather
than libncurses.so), rather than within the Makefile; add a test to %%install
to verify the dso files that the curses module is linked against the correct
DSO (bug 539917; changes _cursesmodule.so -> _curses.so)

* Fri Jan 22 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-19
- add %%py3dir macro to macros.python3 (to be used during unified python 2/3
builds for setting up the python3 copy of the source tree)

* Wed Jan 20 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-18
- move lib2to3 from -tools subpackage to main package (bug 556667)

* Sun Jan 17 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-17
- patch Makefile.pre.in to avoid building static library (patch 6, bug 556092)

* Fri Jan 15 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-16
- use the %%{_isa} macro to ensure that the python-devel dependency on python
is for the correct multilib arch (#555943)
- delete bundled copy of libffi to make sure we use the system one

* Fri Jan 15 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-15
- fix the URLs output by pydoc so they point at python.org's 3.1 build of the
docs, rather than the 2.6 build

* Wed Jan 13 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-14
- replace references to /usr with %%{_prefix}; replace references to
/usr/include with %%{_includedir} (Toshio)

* Mon Jan 11 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-13
- fix permission on find-provides-without-python-sonames.sh from 775 to 755

* Mon Jan 11 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-12
- remove build-time requirements on tix and tk, since we already have
build-time requirements on the -devel subpackages for each of these (Thomas
Spura)
- replace usage of %%define with %%global (Thomas Spura)
- remove forcing of CC=gcc as this old workaround for bug 109268 appears to
longer be necessary
- move various test files from the "tools"/"tkinter" subpackages to the "test"
subpackage

* Thu Jan  7 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.1-11
- add %%check section (thanks to Thomas Spura)
- update patch 4 to use correct shebang line
- get rid of stray patch file from buildroot

* Tue Nov 17 2009 Andrew McNabb <amcnabb@mcnabbs.org> - 3.1.1-10
- switched a few instances of "find |xargs" to "find -exec" for consistency.
- made the description of __os_install_post more accurate.

* Wed Nov  4 2009 David Malcolm <dmalcolm@redhat.com> - 3.1.1-9
- add macros.python3 to the -devel subpackage, containing common macros for use
when packaging python3 modules

* Tue Nov  3 2009 David Malcolm <dmalcolm@redhat.com> - 3.1.1-8
- add a provides of "python(abi)" (see bug 532118)
- fix issues identified by a.badger in package review (bug 526126, comment 39):
  - use "3" thoughout metadata, rather than "3.*"
  - remove conditional around "pkg-config openssl"
  - use standard cleanup of RPM_BUILD_ROOT
  - replace hardcoded references to /usr with _prefix macro
  - stop removing egg-info files
  - use /usr/bin/python3.1 rather than /use/bin/env python3.1 when fixing
up shebang lines
  - stop attempting to remove no-longer-present .cvsignore files
  - move the post/postun sections above the "files" sections

* Thu Oct 29 2009 David Malcolm <dmalcolm@redhat.com> - 3.1.1-7
- remove commented-away patch 51 (python-2.6-distutils_rpm.patch): the -O1
flag is used by default in the upstream code
- "Makefile" and the config-32/64.h file are needed by distutils/sysconfig.py
_init_posix(), so we include them in the core package, along with their parent
directories (bug 531901)

* Tue Oct 27 2009 David Malcolm <dmalcolm@redhat.com> - 3.1.1-6
- reword description, based on suggestion by amcnabb
- fix the test_email and test_imp selftests (patch 3 and patch 4 respectively)
- fix the test_tk and test_ttk_* selftests (patch 5)
- fix up the specfile's handling of shebang/perms to avoid corrupting
test_httpservers.py (sed command suggested by amcnabb)

* Thu Oct 22 2009 David Malcolm <dmalcolm@redhat.com> - 3.1.1-5
- fixup importlib/_bootstrap.py so that it correctly handles being unable to
open .pyc files for writing (patch 2, upstream issue 7187)
- actually apply the rpath patch (patch 1)

* Thu Oct 22 2009 David Malcolm <dmalcolm@redhat.com> - 3.1.1-4
- update patch0's setup of the crypt module to link it against libcrypt
- update patch0 to comment "datetimemodule" back out, so that it is built
using setup.py (see Setup, option 3), thus linking it statically against
timemodule.c and thus avoiding a run-time "undefined symbol:
_PyTime_DoubleToTimet" failure on "import datetime"

* Wed Oct 21 2009 David Malcolm <dmalcolm@redhat.com> - 3.1.1-3
- remove executable flag from various files that shouldn't have it
- fix end-of-line encodings
- fix a character encoding

* Tue Oct 20 2009 David Malcolm <dmalcolm@redhat.com> - 3.1.1-2
- disable invocation of brp-python-bytecompile in postprocessing, since
it would be with the wrong version of python (adapted from ivazquez'
python3000 specfile)
- use a custom implementation of __find_provides in order to filter out bogus
provides lines for the various .so modules
- fixup distutils/unixccompiler.py to remove standard library path from rpath
(patch 1, was Patch0 in ivazquez' python3000 specfile)
- split out libraries into a -libs subpackage
- update summaries and descriptions, basing content on ivazquez' specfile
- fixup executable permissions on .py, .xpm and .xbm files, based on work in
ivazquez's specfile
- get rid of DOS batch files
- fixup permissions for shared libraries from non-standard 555 to standard 755
- move /usr/bin/python*-config to the -devel subpackage
- mark various directories as being documentation

* Thu Sep 24 2009 Andrew McNabb <amcnabb@mcnabbs.org> 3.1.1-1
- Initial package for Python 3.

