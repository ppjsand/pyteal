/* begin_generated_IBM_copyright_prolog                             */
/*                                                                  */
/* This is an automatically generated copyright prolog.             */
/* After initializing,  DO NOT MODIFY OR MOVE                       */
/* ================================================================ */
/*                                                                  */
/* (C) Copyright IBM Corp.  2011                                    */
/* Eclipse Public License (EPL)                                     */
/*                                                                  */
/* ================================================================ */
/*                                                                  */
/* end_generated_IBM_copyright_prolog                               */
#ifndef _THREAD_H
#define _THREAD_H

#include <pthread.h>


using namespace std;

class Thread 
{
    private:

    protected:
        bool         launched;
        bool         running;
        pthread_t    thread;
        void        *data;
        pthread_mutex_t mutex;
        pthread_cond_t cond;        

    public:
        Thread();
        virtual ~Thread();
        bool sendSignal();
        bool start(void* (*runner)(void*) ,void* in);
        bool join();
        void schedule(void (*task)(void),int interval);//lauch runner every interval seconds
        
        bool isLaunched() { return launched; }
        bool getState() { return running; }

};

#endif

