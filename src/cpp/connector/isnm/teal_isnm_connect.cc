// begin_generated_IBM_copyright_prolog
//
// This is an automatically generated copyright prolog.
// After initializing,  DO NOT MODIFY OR MOVE
// ================================================================
//
// (C) Copyright IBM Corp.  2010,2011
// Eclipse Public License (EPL)
//
// ================================================================
//
// end_generated_IBM_copyright_prolog

/**
 * \file teal_connect_api.c
 * \brief Implementation for C API used by connectors.
 */




#include "teal_isnm_connect.h"
#include "teal_connect_internal.h"
#include "DbInterface.h"
#include "DbIsnmEvent.h"
#include "DbCommonBaseEvent.h"
#include "Semaphore.h"
#include <stdexcept>


#ifdef __cpluplus
extern "C" {
#endif


  TEAL_ERR_T teal_isnm_write_event_format2(teal_connector_handle handle,
                                          teal_cbe_t *common_event,
                                          teal_isnm_ext_event_t *isnm_ext_event)
  {
    TEAL_ERR_T ret = TEAL_SUCCESS;

    // Pull needed items out of the handle.
    if(handle == NULL) {
      return TEAL_ERR_ARG;
    }
    TEAL::teal_connect_handle_t* conn_handle = static_cast<TEAL::teal_connect_handle_t*>(handle);

    TEAL::DbInterface *pDbInterface = conn_handle->dbi;

    if(pDbInterface == 0) {
      return TEAL_ERR_CONN_HANDLE;
    }

    TEAL::Notifier *pNotifier = conn_handle->notifier;

    // Generate format string.
    // fmtLL is a local static variable used in a way so that
    // we should only have to calculate the format string the
    // first time through the function.
    static unsigned long long fmtLL = 0;
    if(fmtLL == 0) {
      fmtLL |= (unsigned long long)(conn_handle->comp_id)[0] << 56;
      fmtLL |= (unsigned long long)(conn_handle->comp_id)[1] << 48;
      fmtLL |= (unsigned long long)(conn_handle->comp_id)[2] << 40;
      fmtLL |= (unsigned long long)(conn_handle->comp_id)[3] << 32;
      // DB table
      fmtLL |= 1ULL << 31;
      // Version is 01
      fmtLL |= 1ULL << 16;
      // Table is 2
      fmtLL |= 2ULL;
    }

    try {
		pDbInterface->connect();
		try {
			TEAL::DbCommonBaseEvent cbe(*pDbInterface, common_event, fmtLL, 0, NULL);
			TEAL::DbIsnmEvent ie(*pDbInterface, isnm_ext_event);
			pDbInterface->insertRecord(cbe);
			pDbInterface->insertRecord(ie);
			pDbInterface->commit();
			pNotifier->post();
		} catch (TEAL::DbException& dbe) {
			pDbInterface->rollback();
			ret = TEAL_ERR_CONN_WRITE;
		} catch (std::invalid_argument& iae) {
			TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "ISNM_CONN",
					"teal_isnm_write_event_format2: ");
			TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "ISNM_CONN",
					iae.what());

			pDbInterface->rollback();
			ret = TEAL_ERR_ARG;
		}
		pDbInterface->disconnect();
	} catch (TEAL::DbException &dbe) {
		TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "ISNM_CONN",
				"teal_isnm_write_event_format2: ");
		TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "ISNM_CONN",
				dbe.what());
		ret = TEAL_ERR_CONN_GEN;
	} catch (...) {
		TEAL::getLog().printForced(TEAL::TEAL_LOG_ERROR, "ISNM_CONN",
				"teal_isnm_write_event_format2: DB disconnect - unknown error");
		ret = TEAL_ERR_CONN_GEN;
	}

	return ret;
  }


#ifdef __cpluplus
}
#endif
