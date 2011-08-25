// begin_generated_IBM_copyright_prolog
//
// This is an automatically generated copyright prolog.
// After initializing,  DO NOT MODIFY OR MOVE
// ================================================================
//
// (C) Copyright IBM Corp.  2011     
// Eclipse Public License (EPL)
//
// ================================================================
//
// end_generated_IBM_copyright_prolog
#ifndef RMC_NOTIFIER_H_
#define RMC_NOTIFIER_H_

/*--------------------------------------------------------------------*/
/*  Includes                                                          */
/*--------------------------------------------------------------------*/

#include <Notifier.h>
#include <string>

/*--------------------------------------------------------------------*/
/*  User Types                                                        */
/*--------------------------------------------------------------------*/

namespace TEAL {
	class RmcNotifier : public Notifier
	{
		public:
			/**
			 * Constructor
			 *
			 * @param sensorName - the name of the RMC sensor to update
			 */
			RmcNotifier(const char* sensorName = "TealEventNotify");

			virtual ~RmcNotifier();

			void post();

		private:
			/**
			 * Count value to update when updating the RMC sensor
			 */
			unsigned int ivCount;

			/**
			 * The system command used to update the sensor
			 */
			std::string ivCommand;
	};
}

/*--------------------------------------------------------------------*/
/*  Constants                                                         */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Macros                                                            */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Global Variables                                                  */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Function Prototypes                                               */
/*--------------------------------------------------------------------*/


#endif /* RMC_NOTIFIER_H_ */
