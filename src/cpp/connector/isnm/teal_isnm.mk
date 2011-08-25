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

VPATH=..

C++TYPE=xlC_r  

SHRLIB_LDFLAGS = -brtl -lteal_common
LDFLAGS = --eh-frame-hdr
LIBS = -lteal_common

INCLUDES = teal_isnm_connect.h

INCFLAGS = -I../../../include -I../../../common -I../../../unixODBC -I..

SHAREDC++_LIBRARIES = libteal_isnm.so
libteal_isnm.so_SHAREDC++_OFILES = teal_isnm_connect.o DbIsnmEvent.o

EXPLIB_TARGETS = export_libteal_isnm.so

ILIST = libteal_isnm.so

