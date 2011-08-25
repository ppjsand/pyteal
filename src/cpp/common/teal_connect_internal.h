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
 * \file teal_connect_internal.h
 *
 * \brief TEAL Connector API, internal-only use functions.
 */



#ifndef _H_TEAL_CONNECT_INTERNAL_
#define _H_TEAL_CONNECT_INTERNAL_

namespace TEAL {

	class Notifier;
	class DbInterface;

	/**
	 * Opaque handle to the TEAL connector.
	 */
	typedef struct teal_connect_handle {
	  char comp_id[4]; /**< 4-byte component identifier that connected*/
	  DbInterface *dbi;
	  Notifier *notifier;
	} teal_connect_handle_t;


  // Part of the internal representation of data is the extended data
  // provided by the user.The data is retrived from a file determined
  // by the comp_format number passed to the constructor. The
  // comp_format is broken down into the following components

  // - 4-byte comp (ascii hex)
  // - 1-byte control, (bit 7 = DB)
  // - 1-byte version,
  // - 2-byte structure id id

  // The comp and version number are used to find the correct file for the definition
  // of the data

  /*
   *
   *     ---------------------------------------------------
   *    |  Component   |ctrl|ver|     structure id          |
   *     ---------------------------------------------------
   *    7              4    3   2                           0 bytes
   *
   *
   *    -----------------------------------------
   *    | 7  | 6  | 5  | 4  | 3  | 2  | 1  | 0  |   ctrl field
   *    -----------------------------------------
   *      ^
   *      |
   *     DB  |<--------------------------------->
   *    Flag            Unused.
   *
   */


  /**
   * \brief The hidden raw data information used by TEAL.
   */
  typedef  struct teal_common_raw_data {

    char*               raw_data;       /**< OPT: Component-owned
                                           data. Non-NULL terminated. */

    unsigned long long* raw_data_fmt;   /**< OPT: Describes
                                           the format of the raw data
                                           field. */


    int                 raw_data_len;   /**< REQ: Length of the raw_data field.
                                           Zero if none passed.
                                        */
  } teal_cbe_raw_t;

} // namespace TEAL
#endif // _H_TEAL_CONNECT_INTERNAL_

