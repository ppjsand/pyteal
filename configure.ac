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


###############################
# Checks for programs.
###############################

AC_PROG_CXX
AC_PROG_CC
AC_PROG_CPP

########################
# Checks for libraries.
########################


#############################
# Checks for header files.
#############################

AC_CHECK_HEADERS([sql.h sqlext.h],[],AC_MSG_ERROR([Must have SQL header files available]))
#AC_CHECK_HEADER([Python.h],[],AC_MSG_ERROR([Must have python header file available]))

#################################################################
# Checks for typedefs, structures, and compiler characteristics.
#################################################################

###############################
# Checks for library functions.
###############################

###############################
# Endgame
###############################
AC_CONFIG_FILES([Makefile:Makefile.in])

#AC_CONFIG_FILES([Makefile:Makefile.in
#                 Make.rules
#                 ibm/Makefile:ibm/Makefile.in
#                 ibm/teal/Makefile:ibm/teal/Makefile.in
#                 ibm/teal/analyzer/Makefile:ibm/teal/analyzer/Makefile.in
#                 ibm/teal/analyzer/gear/Makefile:ibm/teal/analyzer/gear/Makefile.in
#                 ibm/teal/analyzer/pool/Makefile:ibm/teal/analyzer/pool/Makefile.in
#                 ibm/teal/database/Makefile:ibm/teal/database/Makefile.in
#                 ibm/teal/filter/Makefile:ibm/teal/filter/Makefile.in
#                 ibm/teal/listener/Makefile:ibm/teal/listener/Makefile.in
#                 ibm/teal/monitor/Makefile:ibm/teal/monitor/Makefile.in
#                 ibm/teal/test/Makefile:ibm/teal/test/Makefile.in
#                 ibm/teal/test/ut/Makefile:ibm/teal/test/ut/Makefile.in
#                 ibm/teal/util/Makefile:ibm/teal/util/Makefile.in
#                 ibm/teal/connector/Makefile:ibm/teal/connector/Makefile.in
#                 cpp/Makefile:cpp/Makefile.in
#                 cpp/include/Makefile:cpp/include/Makefile.in
#                 cpp/common/Makefile:cpp/common/Makefile.in
#                 cpp/connector/Makefile:cpp/connector/Makefile.in
#                 cpp/connector/isnm/Makefile:cpp/connector/isnm/Makefile.in
#                 data/Makefile:data/Makefile.in
#                 data/ibm/Makefile:data/ibm/Makefile.in
#                 data/ibm/teal/Makefile:data/ibm/teal/Makefile.in
#                 data/ibm/teal/xml/Makefile:data/ibm/teal/xml/Makefile.in])
#
AC_OUTPUT

