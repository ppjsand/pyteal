// begin_generated_IBM_copyright_prolog
//
// This is an automatically generated copyright prolog.
// After initializing,  DO NOT MODIFY OR MOVE
// ================================================================
//
// (C) Copyright IBM Corp.  2001,2011
// Eclipse Public License (EPL)
//
// ================================================================
//
// end_generated_IBM_copyright_prolog
#ifndef __PTHREAD_MUTEX_H__
#define __PTHREAD_MUTEX_H__

#include <memory.h>
#include <pthread.h>
#include <errno.h>
#include <assert.h>


#ifdef DEBUG_MUTEX
#include <stdio.h>
#include <stdlib.h>
#include <execinfo.h>


/* Obtain a backtrace and print it to stdout. */
inline void print_backtrace()
{
  void *array[20];
  size_t size;
  char **strings;
  size_t i;
  
  size = backtrace (array, 20);
  strings = backtrace_symbols (array, size);
  
  printf ("Obtained %zd stack frames.\n", size);
  
  for (i = 0; i < size; i++)
    printf ("%s\n", strings[i]);

  free (strings);
}
#define pthread_mutex_assert(cond) if (!(cond)) { print_backtrace(); this->dump(); }
#else
#define pthread_mutex_assert(cond) assert(cond)
#endif



namespace TEAL {
  //////////////////////////////////////////////////////////////////
  /*!
  // Wrapper class for thread mutexs.  
  //
  // this class handles mutex initialization, destruction, lock 
  // unlock and trylock.
  //
  // The There is also an PthreadAutoMutex class which is intended
  // to be implemted either as an automatic variable or an std::auto_ptr class
  // 
  // This class handles unlocking the mutex should the application exit 
  // the function without unlocking the mutex.
  //
  // Mutexes must be initialized before being able to lock and unlock them.
  //
  // Prior to initialization, attributes of the mutex can be selected.
  */


  class PthreadMutex
  {
   public:
    PthreadMutex(unsigned initializer) {
      init(initializer);
    }
    PthreadMutex() {
      init(PTHREAD_MUTEX_ERRORCHECK);
    }        
    virtual ~PthreadMutex() {
      pthread_mutex_destroy(&m_Mutex);
      pthread_mutexattr_destroy(&m_Attribute);
    }
    void init(int initializer) {
      int rc = 0;
      memset(&m_Mutex, 0, sizeof(m_Mutex));       // we crash if this is not cleared out...
      rc = pthread_mutexattr_init(&m_Attribute);
      pthread_mutex_assert(rc == 0);
      rc = pthread_mutexattr_settype(&m_Attribute, initializer);
      pthread_mutex_assert(rc == 0);
      rc = pthread_mutex_init(&m_Mutex, &m_Attribute);
      pthread_mutex_assert(rc == 0);
    }    
    
    //////////////////////////////////////////////////////////////////
    /*!
    // Locks the mutex pointer for this object.
    //
    // Once locked, this will attempt hold the mutex object
    // and unlock it in its destructor.
    // inputs:
    //     pMutex -- mutex to lock.
    // outputs:
    //     returns the value of
    //    
    //
    // Lock the mutex..
    // 
    // Routine is used by a thread to acquire a lock on the specified mutex variable. 
    // If the mutex is already locked by another thread, this call will block the 
    // calling thread until the mutex is unlocked.     
    // 
    // @returns -- If successful, the pthread_mutex_lock and pthread_mutex_unlock 
    //               functions return zero. Otherwise, an error number is returned to 
    //               indicate the error.
    //          EBUSY   The mutex could not be acquired because it was already locked.
    //          EINVAL  The value specified by mutex does not refer to an initialised mutex
    //                  object.
    //          EDEADLK The current thread already owns the mutex and the mutex type is
    //                  pthread_mutex_errorcheck.
    //          EPERM   The current thread does not own the mutex and the mutex type is not
    //                  pthread_mutex_normal.
    // NOTES:
    //
    // Mutex type is always the default mutex type, so the same thread should not call
    // this twice.
    // 
    // If a signal is delivered to a thread waiting for a mutex, upon return from the
    // signal handler the thread resumes waiting for the mutex as if it was not
    // interrupted    
    */
    int Lock()
    {
      int rc = pthread_mutex_lock(&m_Mutex);
      pthread_mutex_assert(rc == 0);
      if (rc == 0)
        m_lockedBy = pthread_self();
      return rc;
    }
    
    //////////////////////////////////////////////////////////////////////////
    /*!
    //
    // The function TryLock is identical to Lock except that
    // if the mutex object referenced by mutex is currently locked (by any thread,
    // including the current thread), the call returns immediately.
    //
    // @returns-- 0 if successful, error codes if not.
    //
    //          EBUSY   The mutex could not be acquired because it was already locked.
    //          EINVAL  The value specified by mutex does not refer to an initialised mutex
    //                  object.
    //          EDEADLK The current thread already owns the mutex and the mutex type is
    //                  pthread_mutex_errorcheck.
    */
    int TryLock()
    {
      int rc = pthread_mutex_trylock(&m_Mutex);
      if (rc == 0)
        m_lockedBy = pthread_self();
      return rc;
    }
    
    ///////////////////////////////////////////////////////////////////////////
    /*!
    //
    // The Unlock function releases the mutex object referenced by mutex.
    // The manner in which a mutex is released is dependent upon the mutex's type
    // attribute. If there are threads blocked on the mutex object referenced by mutex
    // when pthread_mutex_unlock is called, resulting in the mutex becoming available,
    // the scheduling policy is used to determine which thread shall acquire the mutex.
    // (In the case of PTHREAD_MUTEX_RECURSIVE mutexes, the mutex becomes available when
    // the count reaches zero and the calling thread no longer has any locks on this
    // mutex).
    // 
    // @param   assert_rc0 -- true if we should assert on a non-zero return code
    // @returns-- 0 if successful, error codes if not.
    //          EINVAL	The mutex parameter is not valid.
    //          EPERM	The calling thread does not own the mutex lock.
    */
    int Unlock(bool assert_rc0=true) {
      int rc = pthread_mutex_unlock(&m_Mutex);
      pthread_mutex_assert(!assert_rc0 || rc == 0);
      return rc;
    }

    ///////////////////////////////////////////////////////////////////////////
    /*!
    // return the raw mutex object
    //
    // @returns -- a reference to the raw mutex object..
    */
    pthread_mutex_t &GetRawMutex() {
      return(m_Mutex); };
   protected:

   private:
    pthread_t m_lockedBy;	                    // who holds the lock
    pthread_mutex_t m_Mutex;                        // actual mutex structure...
    pthread_mutexattr_t m_Attribute;
#ifdef DEBUG_MUTEX
    inline void dump()
    {
      printf("mutex: %p\n", this);
      printf("  m_lockedBy: %08x\n", (unsigned) m_lockedBy);
      printf("  m_Mutex\n");
      printf("    __lock:  %d\n", m_Mutex.__data.__lock);
      printf("    __count: %d\n", m_Mutex.__data.__count);
      printf("    __owner: %d\n", m_Mutex.__data.__owner);
      printf("    __kind:  %d\n", m_Mutex.__data.__kind);
      printf("    __nusers:%d\n", m_Mutex.__data.__nusers);
    }
#endif
    // the following is to prevent accidental bitwise copying of instances of this class
    PthreadMutex(const PthreadMutex&);
    PthreadMutex& operator=(const PthreadMutex&);
  };



  ///////////////////////////////////////////////////////////////////////////////
  //
  // Helper class (similar to auto pointer, makes sure that we unlock
  // this mutex when the destructor for this function is called.
  //
  //    
  class PthreadMutexHolder
  {
   public:
    PthreadMutexHolder() {
      m_pMutex = NULL; }
    ~PthreadMutexHolder() {
      if (m_pMutex)
        m_pMutex->Unlock();
    }
    /////////////////////////////////////////////////////////
    /*!
    // Unlock the mutex we are holding.
    // @return   value from the pthread_mutex_unlock call.
    */
    int Unlock()
    {
      int nRet = 0;
      if (m_pMutex)
        nRet = m_pMutex->Unlock();
      m_pMutex = NULL;
      return(nRet);
    }

    ///////////////////////////////////////////////////////
    /*!
    // Locks the mutex pointer for this object.
    //
    // Once locked, this will attempt hold the mutex object
    // and unlock it in its destructor.
    //
    // @param    pMutex -- mutex to lock.
    // @return   the return code from pthread_mutex_lock
    */   
    int Lock(PthreadMutex *pMutex) {
      int nRet = 0;
        
      if (m_pMutex)                   // if we were holding a previous lock
        m_pMutex->Unlock();         // unlock it...
      if (pMutex)
        {
          m_pMutex = pMutex;             // point to the mutex to lock.
          nRet = m_pMutex->Lock();       // lock the mutex..
        }
      else
	{
          m_pMutex = NULL;
          nRet = EINVAL;
	}
      return(nRet);
    };

    ///////////////////////////////////////////////////////
    /*!
    // The function TryLock is identical to Lock except that
    // if the mutex object referenced by mutex is currently locked (by any thread,
    // including the current thread), the call returns immediately.
    //
    // Once locked, this will attempt hold the mutex object
    // and unlock it in its destructor.
    //
    // @param    pMutex -- mutex to lock.
    // @return   the return code from pthread_mutex_trylock
    */   
    int TryLock(PthreadMutex *pMutex) {
      int nRet = 0;
        
      if (m_pMutex)                   // if we were holding a previous lock
        m_pMutex->Unlock();         // unlock it...
      if (pMutex)
        {
          m_pMutex = pMutex;             // point to the mutex to lock.
          nRet = m_pMutex->TryLock();    // lock the mutex..
          if (nRet != 0)
            m_pMutex = NULL;
        }
      else
	{
          m_pMutex = NULL;
          nRet = EINVAL;
	}
        
      return(nRet);
    };
   protected:

   private:
    PthreadMutex *m_pMutex;
  };

} // namespace TEAL

#endif


