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
 * \file Semaphore.h
 * C++ wrapper over the SysV semop interface.
 */



#ifndef _H_SEMAPHORE_
#define _H_SEMAPHORE_

// System Includes
#include <errno.h>
#include <sys/sem.h>
#include <string>
#include <cstdio>
#include <cstring>
#include <errno.h>
#include <stdexcept>

#include "Notifier.h"
#include "TealException.h"
#include "Logging.h"


namespace TEAL {


  /*
   * \brief A class for exceptions generated by the Semaphore class.
   */
  class SemaphoreException : public std::exception
  {
   public:
    /**
     * \brief Constructor
     *
     * \param i The errno value.
     */
    SemaphoreException(int i)
    {
      ivErrnoVal = i;
    }

    ~SemaphoreException()  throw() {}

    /**
     * \brief Return a string representation of the exception.
     *
     * \retval A C-style string representing the exception.
     */
    virtual const char *what() const throw()
    {
      return strerror(ivErrnoVal);
    }

    /**
     * \brief Helper function to retrieve ivErrnoVal member.
     *
     * \retval The ivErrnoVal value.
     */
    int getErrnoVal() const {
      return ivErrnoVal;
    }

   private:
    int ivErrnoVal;

  };


  /**
   * \brief A class to wrap the SysV semop/semctl interface.
   */

  class Semaphore : public Notifier
  {

   public:

    /**
     * \brief The role the semaphore is playing. Changes how the semaphore is created.
     */
    enum Role {
      CLIENT,                   /**< The semaphore is initialized as a client. */
      SERVER                    /**< The semaphore is initialized as a server. */
    };

    /**
     * \brief Construct the basic items needed for the semaphore.
     *
     * Gather together the information needed to create the key and
     * call semget to create the semaphore for use.
     * By default, a CLIENT mode semaphore is created.
     *
     * \parm name A string used as part of token creation.
     *
     * \parm projId An integer identifier for the project. Used as part of token creation.
     *
     * \parm role An enumeration representing the role of this semaphore. Defaults to CLIENT.
     *
     */

    Semaphore(Role role = SERVER,
              const std::string& name = "/var/log/teal" ,
              int ProjId = 0x646c6100);

    /**
     * \brief post a value to the semaphore.
     */

    void post();

    /**
     * \brief Wait on the semaphore, then process it.
     *
     * \retval
     */

    int wait();

   private:
    std::string ivName;
    int ivProjId;
    int ivId;
    key_t ivKey;

  };

} // namespace TEAL

#endif // _H_SEMAPHORE
