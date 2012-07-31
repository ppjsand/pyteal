# begin_generated_IBM_copyright_prolog
#
# This is an automatically generated copyright prolog.
# After initializing,  DO NOT MODIFY OR MOVE
# ================================================================
#
# (C) Copyright IBM Corp.  2010,2011
# Eclipse Public License (EPL)
#
# ================================================================
#
# end_generated_IBM_copyright_prolog
#                                               -*- Autoconf -*-
#     Autoconf requirements
#     AC_INIT(package, version, bug-report-address)
#     information on the package
#     checks for programs
#     checks for libraries
#     checks for header files
#     checks for types
#     checks for structures
#     checks for compiler characteristics
#     checks for library functions
#     checks for system services
#     AC_CONFIG_FILES([file...])
#     AC_OUTPUT

AC_PREREQ([2.63])
AC_INIT([teal],[1.1.0.0],[ppjsand@users.sf.net],[Toolkit for Event Analysis and Logging],[http://sourceforge.net/projects/pyteal/])
AC_COPYRIGHT('Eclipse Platform License 1.0')
AC_REVISION([$Revision: 1.0 $])

AC_CONFIG_SRCDIR([src/ibm/teal/__init__.py])
AC_PREFIX_DEFAULT([/opt/teal])
AC_CONFIG_AUX_DIR([/usr/share/libtool/config])

AC_CANONICAL_BUILD

###############################
# Options
###############################

# Determine which package to include
AC_ARG_ENABLE([isnm],AC_HELP_STRING([--enable-isnm], [enable isnm connector (default: 1)]),[enable_isnm=$enableval],[enable_isnm=1])
AC_ARG_ENABLE([sfp],AC_HELP_STRING([--enable-sfp], [enable sfp connector (default: 1)]),[enable_sfp=$enableval],[enable_sfp=1])
AC_ARG_ENABLE([ll],AC_HELP_STRING([--enable-ll], [enable loadleveler connector (default: 1)]),[enable_ll=$enableval],[enable_ll=1])
AC_ARG_ENABLE([pnsd],AC_HELP_STRING([--enable-pnsd], [enable PNSD connector (default: 1)]),[enable_pnsd=$enableval],[enable_pnsd=1])
AC_ARG_ENABLE([gpfs],AC_HELP_STRING([--enable-gpfs], [enable GPFS connector (default: 0)]),[enable_gpfs=$enableval],[enable_gpfs=0])
AC_ARG_ENABLE([test],AC_HELP_STRING([--enable-test], [enable testcase package (default: 1)]),[enable_test=$enableval],[enable_test=1])
AC_ARG_ENABLE([ib],AC_HELP_STRING([--enable-ib], [enable IB package (default: 0)]),[enable_test=$enableval],[enable_ib=1])

case "$enable_isnm" in
	"yes"|"1") ENABLE_ISNM=1 ;;
	*) ENABLE_ISNM=0 ;;
esac
case "$enable_sfp" in
	"yes"|"1") ENABLE_SFP=1 ;;
	*) ENABLE_SFP=0 ;;
esac
case "$enable_ll" in
	"yes"|"1") ENABLE_LL=1 ;;
	*) ENABLE_LL=0 ;;
esac
case "$enable_pnsd" in
	"yes"|"1") ENABLE_PNSD=1 ;;
	*) ENABLE_PNSD=0 ;;
esac
case "$enable_gpfs" in
	"yes"|"1") ENABLE_GPFS=1 ;;
	*) ENABLE_GPFS=0 ;;
esac
case "$enable_test" in
	"yes"|"1") ENABLE_TEST=1 ;;
	*) ENABLE_TEST=0 ;;
esac
case "$enable_ib" in
        "yes"|"1") ENABLE_IB=1 ;;
        *) ENABLE_IB=0 ;;
esac


# Determine if 32 or 64 bit platform target
machine="`uname -m`"

if test "$machine" = "ppc64"; then
    BITS="64"
elif test "$machine" = "x86_64"; then
    BITS="64"
else
    BITS="32"
fi

###############################
# Checks for programs.
###############################

AC_PROG_MKDIR_P
AC_PROG_LN_S
AC_PROG_CXX
AC_PROG_CPP
AC_PATH_PROG([PYTHON], [python], false)
if test "$PYTHON" == 'false'; then
	AC_MSG_ERROR([python not found])
else
    python_version="`$PYTHON -V 2>&1 | cut -d' ' -f2`"
    PYTHON_VER=`echo $python_version | sed 's/\(^@<:@0-9@:>@*\.@<:@0-9@:>@*\).*/\1/'`
fi

########################
# Checks for libraries.
########################

#############################
# Checks for header files.
#############################

CPPFLAGS="-I/usr/include/python$PYTHON_VER -I/opt/freeware/include/python$PYTHON_VER"

AC_CHECK_HEADER([Python.h],[], AC_MSG_ERROR([Must have python header files available]))
AC_CHECK_HEADERS([sql.h sqlext.h],[],AC_MSG_ERROR([Must have SQL header files available]))

#################################################################
# Checks for typedefs, structures, and compiler characteristics.
#################################################################

###############################
# Checks for library functions.
###############################

###############################
# Endgame
###############################

AC_CONFIG_FILES([Makefile:Makefile.in
				teal-base.mk
				teal-ll.mk
				teal-pnsd.mk
				teal-sfp.mk
				teal-isnm.mk
				teal-gpfs.mk
				teal-test.mk
				teal-ib.mk])

AC_SUBST(PYTHON_VER)
AC_SUBST(BITS)
AC_SUBST(ENABLE_ISNM)
AC_SUBST(ENABLE_SFP)
AC_SUBST(ENABLE_LL)
AC_SUBST(ENABLE_PNSD)
AC_SUBST(ENABLE_GPFS)
AC_SUBST(ENABLE_TEST)
AC_SUBST(ENABLE_IB)

AC_OUTPUT

