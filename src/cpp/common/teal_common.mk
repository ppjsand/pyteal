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
LDFLAGS = -lpthread -ldl --eh-frame-hdr
INCFLAGS = -I../../include -I../../unixODBC -I..

SHAREDC++_LIBRARIES = libteal_common.so
libteal_common.so_SHAREDC++_OFILES = \
DbModule.o \
DbInterface.o \
DbEvent.o \
DbCommonBaseEvent.o \
DbGpfsInfo.o \
Logging.o \
Semaphore.o \
RmcNotifier.o \
teal_connect_api.o \
teal_helpers.o \
teal_common_info.o

teal_common_info.o: teal_common_info.cc
teal_common_info.cc::
	@echo "char teal_common_build_name[] = \"\$$NAME: $(TEAL_RPM_NAME)  "`date +%c`" "`whoami`" \$$\";" > teal_common_info.cc

EXPLIB_TARGETS = export_libteal_common.so
ILIST = libteal_common.so

