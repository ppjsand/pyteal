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
 * \file Logging.cc
 * \brief C++ Logging support
 */

/// \todo Insert copyright/license header.

#include "Logging.h"
#include <sys/stat.h>
namespace TEAL 
{
 
  Log theLog;
  
  PthreadMutex Log::ivLogMutex;


  std::string mapLevel(const teal_log_level_t& level)
  {
    switch(level) {
      case TEAL_LOG_DEBUG:{
        return std::string("DEBUG");
        break;
      }
      case TEAL_LOG_INFO: {
        return std::string("INFO");
        break;
      }
      case TEAL_LOG_WARN: {
        return std::string("WARNING");
        break;
      }
      case TEAL_LOG_ERROR: {
        return std::string("ERROR");
        break;
      }
      case TEAL_LOG_CRITICAL: {
        return std::string("CRITICAL");
        break;
      }
      case TEAL_LOG_EXCEPT: {
        return std::string("EXCEPTION");
        break;
      }
      default:
        return std::string("??LEVEL");
        break;
    }
    return std::string("??LEVEL");
  }

  Log::Log() : 
    ivRegularStream(0),ivLogStatus(1), ivTimeFormat("%Y-%m-%d %H:%M:%S")
  {
    char *envValue;
    envValue = getenv("TEAL_LOG_DIR");
    if(envValue == 0) {
      envValue = TEAL_LOG_DIR_DEFAULT;
    } else {
      envValue = envValue;
    }
    
    struct stat statbuf;
    int rc = stat(envValue,&statbuf);
    if ((rc != 0) || !S_ISDIR(statbuf.st_mode) ||
        (access(envValue, W_OK) != 0)) {
        envValue = "/tmp";
    }
    ivLogPath = envValue;
    std::string path;
    ivFileName = generateFileName();
    path =  ivLogPath + "/" + ivFileName;
    
    ivFileStream = new std::ofstream(path.c_str(),std::ios::app);
    
    if (!(*ivFileStream)) {
      std::ostringstream msg;      
      msg << "File open failure." << std::endl;
      
      throw LogException(msg.str());
    }
    
    setLogLevel();
  }

  Log::Log(const std::ostream& stream) 
    : ivFileStream(0),ivRegularStream(const_cast<std::ostream*>(&stream)),
      ivLogStatus(1), ivTimeFormat("%Y-%m-%d %H:%M:%S")
  {
    // Check the status of the stream
    if(!(*ivRegularStream)) {
      std::ostringstream msg;
      msg << "Log: stream status: fail." 
          << std::endl;
      throw LogException(msg.str());
    }
    setLogLevel();
  }

  Log::~Log() 
  {
    theStream() << std::endl;

    if(ivFileStream) {
      ivFileStream->close();
      delete ivFileStream;
    }
  }

  void Log::Print(teal_log_level_t severity, 
                  const std::string& compid, 
                  const std::string& msg, char* filename, int lineno) 
  {
    if(severity >= ivMessageLevel) {
      PrintForced(severity,compid,msg, filename, lineno);
    }
  }  

  void Log::PrintForced(teal_log_level_t severity, 
                        const std::string& compid, 
                        const std::string& msg, char* filename, int lineno) 
  {
    // Acquire the Log lock.
    if(ivLogMutex.Lock() == 0) {

      std::ostringstream sTmp;
      if(ivMessageLevel == TEAL_LOG_DEBUG)
      {
          sTmp << generateTimeStamp() << " [" << (int)getpid() << ":" << pthread_self() 
                 << "] " << compid << "(" << filename << ":" << lineno << ")" << " - " << mapLevel(severity) << ": " << msg << std::endl;
      }
      else
      {
          sTmp << generateTimeStamp() << " [" << (int)getpid() << ":" << pthread_self() 
                 << "] "  << compid << " - " << mapLevel(severity) << ": " << msg << std::endl;
      }
      theStream() << sTmp.str();
      
      if(!(theStream())) {
        ivLogStatus = 0;
        theStream().clear();
      } else {
        ivLogStatus = 1;
        theStream().flush(); //print out immediately
      }
    }
    if (ivLogMutex.Unlock() != 0) {
      // Error situation?
      ;
    }
  }


  void Log::setLogLevel(void)
  {

    ivMessageLevel = TEAL_LOG_INFO;

    char *envValue;
    envValue = getenv(logLevelEnvVar.c_str());

    if(envValue != 0) {
      std::string val(envValue);
      if(val == "DEBUG") {
        ivMessageLevel = TEAL_LOG_DEBUG;
      } else if(val == "WARNING") {
        ivMessageLevel = TEAL_LOG_WARN;
      } else if(val == "ERROR") {
        ivMessageLevel = TEAL_LOG_ERROR;
      } else if(val == "CRITICAL") {
        ivMessageLevel = TEAL_LOG_CRITICAL;
      } else if(val == "EXCEPTION") {
        ivMessageLevel = TEAL_LOG_EXCEPT;
      } else {
        ivMessageLevel = TEAL_LOG_INFO;
      }
    }
  }
  std::string Log::generateFileName() 
  {
    std::ostringstream fileName;
 //   fileName << "TEAL_CONN_" << getpid() << ".log";
    fileName << "teal_conn" << ".log";
    return fileName.str();
  }

  std::string Log::generateTimeStamp() const
  {
    struct tm *timeStruct;
    time_t theTime = time(NULL);
    timeStruct = localtime(&theTime);
    
    char buffer[25];
    memset(buffer,'\0',25);
    strftime(buffer,25,ivTimeFormat.c_str(),timeStruct);
    
    return std::string(buffer);
  }
    

} // namespace TEAL


