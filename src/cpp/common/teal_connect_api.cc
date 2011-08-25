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

#include "teal_connect_api.h"
#include "teal_connect_internal.h"
#include "teal_helpers.h"
#include "DbInterface.h"
#include "DbCommonBaseEvent.h"
#include "Semaphore.h"

// System headers.
#include <iostream>
#include <sstream>

namespace TEAL {
const char *tealDataDir = "TEAL_DATA_DIR";
const char *tealConfDir = "TEAL_CONF_DIR";
const char *tealLogDir = "TEAL_LOG_DIR";
const char *tealRootDir = "TEAL_ROOT_DIR";
}

#ifdef __cpluplus
extern "C" {
#endif

TEAL_ERR_T teal_open_connector(teal_connector_handle *conn_handle,
							   const char *comp_name,
							   const char *log_dir)
{

	TEAL_ERR_T ret;
	TEAL::teal_connect_handle_t* handle;

	if ((conn_handle == NULL) || (comp_name == NULL) || (log_dir == NULL)) {
		return TEAL_ERR_ARG;
	}

	try {
		// Allocate storage for the connection handle object.
		*conn_handle = NULL;
		handle = new TEAL::teal_connect_handle_t();
	} catch (std::bad_alloc &except) {
		return TEAL_ERR_SYS_MEM;
	}

	// Fill in the component_id field.
	memset(handle->comp_id, '\0', 4);

	if (strlen(comp_name) < 4) {
		strncpy(handle->comp_id, comp_name, strlen(comp_name));
	} else {
		strncpy(handle->comp_id, comp_name, 4);
	}

	// Retrieve necessary database connection information.
	std::string pathToDbConfigFile, connectionString;

	char *p = getenv(TEAL::tealConfDir);
	if (!p) {
		TEAL::getLog().print(TEAL::TEAL_LOG_DEBUG, "TEAL",
				"TEAL_CONF_DIR environment variable not set.");
		pathToDbConfigFile = "/etc/xcat/cfgloc";
	} else {
		pathToDbConfigFile = std::string(p) + "/xcat/cfgloc";
	}

	ret = TEAL::processxCATConfFile(pathToDbConfigFile, connectionString);
	if (ret != TEAL_SUCCESS) {
		std::string tmp = "Unable to process file: " + pathToDbConfigFile;

		TEAL::getLog().printForced(TEAL::TEAL_LOG_CRITICAL, "TEAL_CONN",
				tmp.c_str());
		return ret;
	}

	try {
		handle->dbi = new TEAL::DbInterface(connectionString);
	} catch (std::bad_alloc &except) {
		TEAL::getLog().printForced(TEAL::TEAL_LOG_DEBUG, "TEAL_CONN",
				"Memory Allocation Failure: DbInterface construction.");
		return TEAL_ERR_SYS_MEM;
	} catch (TEAL::DbException &dbe) {
		TEAL::getLog().printForced(TEAL::TEAL_LOG_DEBUG, "TEAL_CONN",
				dbe.what());
		return TEAL_ERR_CONN_INIT;
	} catch (...) {
		TEAL::getLog().printForced(TEAL::TEAL_LOG_CRITICAL, "TEAL_CONN",
				"Unknown error: DbInterface construction");
		return TEAL_ERR_SYS_GEN;
	}

	try {
		handle->notifier = TEAL::create_notifier();
	} catch (std::bad_alloc &except) {
		TEAL::getLog().printForced(TEAL::TEAL_LOG_DEBUG, "TEAL_CONN",
				"Memory Allocation Failure: Semaphore construction.");
		// Delete previously allocated memory
		delete handle->dbi;
		return TEAL_ERR_SYS_MEM;
	} catch (TEAL::SemaphoreException &se) {
		TEAL::getLog().printForced(TEAL::TEAL_LOG_CRITICAL, "TEAL_CONN",
				se.what());
		// Delete previously allocated memory
		delete handle->dbi;

		if (se.getErrnoVal() == ENOMEM) {
			return TEAL_ERR_SYS_MEM;
		} else if (se.getErrnoVal() == ENOENT) {
			return TEAL_ERR_CONN_INIT;
		} else {
			return TEAL_ERR_SYS_GEN;
		}
	} catch (...) {
		TEAL::getLog().printForced(TEAL::TEAL_LOG_CRITICAL, "TEAL_CONN",
				"Unknown error: Semaphore Construction");
		// Delete previously allocated memory
		delete handle->dbi;
		return TEAL_ERR_SYS_GEN;
	}

	TEAL::getLog().print(TEAL::TEAL_LOG_DEBUG, "TEAL_CONN",
			"teal_open_connector() completed.\n");
	*conn_handle = handle;
	return TEAL_SUCCESS;
}

TEAL_ERR_T teal_close_connector(teal_connector_handle conn_handle) {

	if (conn_handle == NULL) {
		return TEAL_ERR_CONN_HANDLE;
	}

	TEAL::teal_connect_handle_t* handle = static_cast<TEAL::teal_connect_handle_t*>(conn_handle);
	delete handle->dbi;
	delete handle->notifier;
	delete handle;

	return TEAL_SUCCESS;
}

TEAL_ERR_T teal_write_event(teal_connector_handle conn_handle,
		teal_cbe_t* event, unsigned raw_data_len, void* raw_data) {
	TEAL_ERR_T rc = TEAL_SUCCESS;

	// Validate the input
	if (conn_handle == NULL) {
		return TEAL_ERR_CONN_HANDLE;
	}
	TEAL::teal_connect_handle_t* handle = static_cast<TEAL::teal_connect_handle_t*>(conn_handle);

	// Pull the items out of our connection handle to do the work
	TEAL::DbInterface* dbi = handle->dbi;
	if (dbi == NULL) {
		return TEAL_ERR_CONN_HANDLE;
	}

	TEAL::Notifier* notifier = handle->notifier;

	// Write the event to the database
	try {
		dbi->connect();
		try {
			TEAL::DbCommonBaseEvent dbEvent(*dbi, event, 0, raw_data_len,
					raw_data);
			dbi->insertRecord(dbEvent);
			dbi->commit();
			notifier->post();
		} catch (std::invalid_argument& iae) {
			dbi->rollback();
			rc = TEAL_ERR_ARG;
		} catch (TEAL::DbException& dbe) {
			dbi->rollback();
			rc = TEAL_ERR_CONN_WRITE;
		}
		dbi->disconnect();
	} catch (TEAL::DbException& dbe) {
		rc = TEAL_ERR_CONN_GEN;
	} catch (...) {
		rc = TEAL_ERR_CONN_GEN;
	}

	return rc;
}

#ifdef __cpluplus
}
#endif
