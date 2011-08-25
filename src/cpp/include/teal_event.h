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
 * \file teal_event.h
 * \brief External interfaces for working with TEAL Events
 */

#ifndef _H_TEAL_EVENT_
#define _H_TEAL_EVENT_

// System Includes
#include <limits.h>
#include <time.h>
#include <inttypes.h>

#ifdef __cplusplus
extern "C" {
#endif

  /**
   * \typedef teal_cbe_t
   * \brief Structure type used to hold common base event data to be written to the log.
   */

  /**
   * \brief Represents common base portion of TEAL events to be inserted into the event log.
   *
   * All character pointer fields are presumed to be NULL terminated unless
   * noted on the specific field.
   *
   * Optional fields should be set to NULL if not used.
   */

  typedef struct teal_common_base_event {

    char*               event_id;       /**< REQ: A unique id within the
                                         * Source Component for events that
                                         * occur. This is defined by the
                                         * component. 8 characters.
                                         */

    char*               time_occurred;  /**< REQ: Time the event was
                                           created in the cluster. This
                                           should be the local time value
                                           on the hardware that created
                                           the event. Should be in the format
                                           %Y:%m:%d %H:%M:%S */

    char*               src_comp;       /**< REQ: The component that is
                                           detecting the event. This is a
                                           free-form, user-defined
                                           string.x  128 characters */
    
    char*               src_loc_type;   /**< REQ: Type of location code. 
                                           Up to 2 characters.*/

    char*               src_loc;        /**< REQ: Component location that
                                           created the event in TEAL
                                           Location Code format. 255 characters */

    char*               rpt_comp;       /**< OPT: Component reporting on
                                           behalf of the source
                                           component. If used, then
                                           report_loc_type and report_loc
                                           become required fields. NULL if
                                           not used. 128 characters */

    char*               rpt_loc_type;   /**< OPT: Type of location
                                           code. Ignored if report_comp is
                                           not used. Up to 2 characters. */

    char*               rpt_loc;        /**< OPT: Component location
                                           reporting the event. NULL if
                                           not used. 255 characters */

    unsigned long long* elapsed_time;   /**< OPT: Elapsed time between
                                           identical events of this
                                           time. Required to be set to
                                           zero if not used. */

    int*                event_cnt;      /**< OPT: Count representing number
                                           of events that were conslidated
                                           into this single event. int*/

  } teal_cbe_t;




#ifdef __cplusplus
}
#endif

#endif // _H_TEAL_EVENT_

