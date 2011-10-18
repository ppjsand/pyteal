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
#include <assert.h>
#include <signal.h>

#include "thread.h"
#include "Log.h"
using namespace std;

Thread::Thread()
    : launched(false), running(false), data(NULL)
{
}

Thread::~Thread() 
{
}

bool Thread::start(void* (*runner)(void*) ,void* in)
{
    if (launched) 
        return true;
    
    if (pthread_create(&thread, NULL, runner, in) != 0) 
    {
        running = false;
        return false;
    }
    else 
    {
        launched = true;
        running = true;
        return true;
    }
}

bool Thread::join()
{
    if (!launched)
        return true;
    
    if(pthread_join(thread, NULL)!=0)
        return false;
    running = false;
    launched = false;
    return true;
}

bool Thread::sendSignal()
{
    if(!launched || !running)
        return false;
    if(pthread_cond_signal(&cond) < 0)
        return false;
    return true;
}

void Thread::schedule(void (*task)(void),int interval)
{
    if(interval < 0 || !launched || !running)
        return;
    
    pthread_mutexattr_t mattrs;
    pthread_mutexattr_init(&mattrs);
    pthread_mutexattr_settype(&mattrs, PTHREAD_MUTEX_NORMAL);
    if(pthread_mutex_init(&mutex, &mattrs) ||pthread_cond_init(&cond, NULL))
    {
      return;
    }
    struct timespec to;
    int retval = 0;
    task();
    clock_gettime(CLOCK_REALTIME, &to);
    for(;;)
    {
        to.tv_sec += interval;
    
        if (retval = pthread_mutex_lock(&mutex))
        {
            log_info("pthread_mutex_lock failed!");
    
        }
        if (retval = pthread_cond_timedwait(&cond, &mutex, &to))
        {
            log_info("Polling interval time out, scheduled polling!");
            
        }
        else
        {
            to.tv_sec -= interval;
            log_info("On demand polling!");
        }        
        task();
        if (retval = pthread_mutex_unlock(&mutex))
        {
            log_error("pthread_mutex_unlock failed!");
        }
    }
    return;

}
