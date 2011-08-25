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
 * \file Semaphore.cc
 * C++ wrapper over the SysV semop interface. Implementation.
 */

#include "Semaphore.h"

namespace TEAL {

  Semaphore::Semaphore(Role role, const std::string& name, int ProjId) :
    Notifier(), ivName(name), ivProjId(ProjId), ivId(-1)
  {

    key_t key = ftok(ivName.c_str(),ivProjId);
    if (key == (key_t)-1) {
      throw SemaphoreException(errno);
    }

    int semflags = 0;
    if (role == SERVER) {
      semflags = IPC_CREAT | 0620;
    }

    int rc = semget(key,1,semflags);
    if (rc < 0) {
      throw SemaphoreException(errno);
    }

    ivId = rc;
  }


  void Semaphore::post()
  {
    sembuf op = {0,1,0};

    int rc = semop(ivId,&op,1);

    if (rc) {
      std::string error(strerror(errno));
      TEAL::getLog().printForced(TEAL_LOG_ERROR,"TEAL_SEM","Failed to post to semaphore");
      TEAL::getLog().printForced(TEAL_LOG_INFO,"TEAL_SEM",error.c_str());
      if(errno == EINTR) {
        rc = semop(ivId,&op,1);
        if(rc) {
          std::string error(strerror(errno));
          TEAL::getLog().printForced(TEAL_LOG_ERROR,
                                     "TEAL_SEM","Retry failed to post to semaphore");
          TEAL::getLog().printForced(TEAL_LOG_INFO,"TEAL_SEM",error.c_str());

        }

      }
    }
  }


  int Semaphore::wait()
  {
    int rc;
    sembuf op = {0,-1,0};

    while(1) {
      rc = semop(ivId,&op,1);
      if (rc == 0) {
        break;
      } else if ((rc < 0) && (errno != EINTR)) {
        TEAL::getLog().printForced(TEAL_LOG_ERROR,"TEAL_SEM","Failed to wait on semaphore");
        return rc;
      } else {
        // Interrupted, try again
      }
    }

    int count = semctl(ivId, 0, GETVAL);
    if (count < 0) {
      TEAL::getLog().printForced(TEAL_LOG_ERROR,"TEAL_SEM","Failed to retrieve semaphore count");
      return count;
    }
    if (count > 0) {
      std::ostringstream strm;
      strm << "Semaphore count: " << count;
      TEAL::getLog().print(TEAL_LOG_DEBUG,"TEAL_SEM",strm.str().c_str());
      op.sem_op = -count;
      rc = semop(ivId,&op,1);
      if (rc) {
        TEAL::getLog().printForced(TEAL_LOG_ERROR,"TEAL_SEM","Failed to reset semaphore count");
        return rc;
      }
    } else {
      // Only one operation was pending
    }

    return 0;
  }


} // namespace TEAL

