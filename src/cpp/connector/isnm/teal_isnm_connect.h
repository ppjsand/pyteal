/* begin_generated_IBM_copyright_prolog                             */
/*                                                                  */
/* This is an automatically generated copyright prolog.             */
/* After initializing,  DO NOT MODIFY OR MOVE                       */
/* ================================================================ */
/*                                                                  */
/* (C) Copyright IBM Corp.  2010,2011                               */
/* Eclipse Public License (EPL)                                     */
/*                                                                  */
/* ================================================================ */
/*                                                                  */
/* end_generated_IBM_copyright_prolog                               */
/**
 * \file teal_cnm_event.h
 * \brief External interfaces for working with ISNM specific event information.
 */

#ifndef _H_TEAL_ISNM_CONNECT_
#define _H_TEAL_ISNM_CONNECT_

// System Includes
#include <limits.h>
#include <time.h>
#include <inttypes.h>

#include "teal_connect_api.h"

#ifdef __cplusplus
extern "C" {
#endif

  /**
   * \typedef teal_isnm_event_t
   * \brief Structure type used to hold common base event data to be written
   *        to the log.
   */

  /**
   * \brief Represents extension information used by ISNM.
   *
   * All character pointer fields are presumed to be NULL terminated unless
   * noted on the specific field.
   *
   * Optional fields should be set to NULL if not used.
   */

  typedef struct teal_isnm_ext_event {

    char*        eed_loc_info;			///< Extended Error Data Location   	[64]
    char*        encl_mtms;            	///< Enclosure MTMS                 	[20]
    char*        pwr_ctrl_mtms;        	///< Power Enclosure MTMS           	[20]
    char*        neighbor_loc_code;    	///< Neighbor Location Code         	[256]
    char*        neighbor_loc_type;    	///< Neighbor Location Code Type    	[2]
    char*        recovery_file_path;   	///< Recovery File Path             	[32]

    char*        isnm_raw_data;        	///< Raw Data, ISNM Error Log Entry 	[1024]
    unsigned int isnm_raw_data_len;    	///< Raw Data Length

    char* 		 local_port;		   	///< Local port service location 		[256]
    char* 		 local_torrent;  		///< Local Torrent service location 	[256]
    char* 		 local_planar;          ///< Local Planar service location 		[256]
    char* 		 local_om1;				///< Local Optical Module location 		[256]
    char* 		 local_om2;				///< Local Optical Module location 		[256]
    char* 		 nbr_port;				///< Neighbor port service location 	[256]
    char* 		 nbr_torrent;			///< Neighbor Torrent service location 	[256]
    char*        nbr_planar;			///< Neighbor Planar service location 	[256]
    char*        nbr_om1;				///< Neighbor Optical Module location 	[256]
    char*        nbr_om2;				///< Neighbor Optical Module location 	[256]
    unsigned long long* global_counter; ///< Global counter for network

  } teal_isnm_ext_event_t;


  /**
   *
   * \brief Write common and ISNM specific event data to the event log.
   *
   * Data written via this API will be processed  by TEAL and made available
   * by field name within the GEAR analyzer rules.
   *
   * \param[in] handle A connector handle returned by teal_open_connector
   * \param[in] common_event The commone TEAL event data structure.
   * \param[in] isnm_ext_event The ISNM event data structure.
   *
   * \retval A TEAL_ERR_T encoded return value.
   */

  TEAL_ERR_T teal_isnm_write_event_format2(teal_connector_handle handle,
                                           teal_cbe_t *common_event,
                                           teal_isnm_ext_event_t *isnm_ext_event);




#ifdef __cplusplus
}
#endif

#endif // _H_TEAL_ISNM_CONNECT_

