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

#ifndef TEAL_NOTIFIER_H_
#define TEAL_NOTIFIER_H_

/*--------------------------------------------------------------------*/
/*  User Types                                                        */
/*--------------------------------------------------------------------*/

namespace TEAL {
	class Notifier
	{
		public:
			/**
			 * Constructor
			 */
			Notifier() { }

			/**
			 * Destructor
			 */
			virtual ~Notifier() { }

			/**
			 * This method will notify TEAL that an event has been
			 * logged in the event log
			 */
			virtual void post() = 0;
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

#endif /* TEAL_NOTIFIER_H_ */
