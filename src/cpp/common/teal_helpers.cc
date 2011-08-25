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
 * \file teal_helpers.cc
 * \brief Utility function used by TEAL connector API.
 *
 *
 * \todo Insert copyright/license header
 */

#include "teal_helpers.h"
#include "Semaphore.h"
#include "RmcNotifier.h"

#include <unistd.h>
#include <sys/stat.h>

namespace TEAL {

  TEAL_ERR_T processxCATConfFile(const std::string& path,
                                 std::string &connectionString)
  {

    std::fstream confFile;

    confFile.open(path.c_str());
    if(!confFile) {
      std::string msg("Unable to open: ");
      msg = msg + path;
      TEAL::getLog().print(TEAL_LOG_DEBUG, "TEAL_COMMON", msg);
      return TEAL_ERR_SYS_FILE;
    }
    // Read in the line.
    std::string strToParse,retValue;
    getline(confFile,strToParse);
    confFile.close();
    if(strToParse[0] == 'm') {

      // MySQL format: "mysql:dbname=<databasename>;host=<dbhost>|<dbuser>|<dbpasswd>"
      std::string::size_type idx1,idx2;
      idx1 = strToParse.find("dbname=");
      idx1 = idx1 + strlen("dbname=");
      idx2 = strToParse.find(';',idx1);
      std::string dbName = strToParse.substr(idx1,idx2-idx1);
      idx1 = strToParse.find("host=");
      idx1 = idx1 + strlen("host=");
      std::string host = strToParse.substr(idx1);
      replace(host.begin(),host.end(),'|','\n');
      std::istringstream strm(host);
      std::string hostName, user, passwd;
      strm >> hostName >> user >> passwd;
      connectionString = "DRIVER={MySQL};DATABASE="+dbName+";UID=" + user +";PWD=" + passwd + ";SERVER=" + hostName;
      std::string printableConnStr = "DRIVER={MySQL};DATABASE="+dbName+";UID=" + user + ";SERVER=" + hostName;
      std::ostringstream prtStrm;
      prtStrm << "DB Connection String: " << printableConnStr;
      TEAL::getLog().print(TEAL::TEAL_LOG_DEBUG, "TEAL_COMMON", prtStrm.str().c_str());
      return TEAL_SUCCESS;

    } else if(strToParse[0] == 'D') {

      // DB/2 format: "DB2:<databasename>|<instancename>|<instancepassword>"
      std::string::size_type idx1;
      idx1 = strToParse.find(':');
      std::string toProcess = strToParse.substr(idx1+1);
      replace(toProcess.begin(),toProcess.end(),'|','\n');
      std::istringstream strm(toProcess);
      std::string dbName,instanceName, instancePasswd;
      strm >> dbName >> instanceName >> instancePasswd;
      // 'DRIVER={DB2};DSN=bgdb0;UID=bgpsysdb;PWD=db24bgp'
      connectionString = "DRIVER={DB2};DSN="+dbName+";UID="+instanceName+";PWD="+instancePasswd;
      std::string printableConnStr = "DRIVER={DB2};DSN="+dbName+";UID="+instanceName+";PWD=";
      std::ostringstream prtStrm;
      prtStrm << "DB Connection String: " << printableConnStr;
      TEAL::getLog().print(TEAL::TEAL_LOG_DEBUG,"TEAL_COMMON",prtStrm.str().c_str());
      return TEAL_SUCCESS;

    } else {

      connectionString = "";
      return TEAL_ERR_SYS_GEN;

    }

    return TEAL_SUCCESS;

  }

  /**
   * Create the notifier for the process. The notifier used is determined
   * by the presence of an xCAT file indicating that it is running on a
   * service node
   */
  Notifier* create_notifier()
  {
	  struct stat statbuf;
	  int rc = stat("/etc/xCATMN",&statbuf);
	  if ((rc == 0) && S_ISREG(statbuf.st_mode)) {
		  return new Semaphore();
	  } else {
		  return new RmcNotifier();
	  }
  }

  char * write_pstr(char *target, const char *source, int field_len)
  {
    int strLen;
    unsigned char cnt;
    strLen = strlen(source);
    cnt = strLen;
    memcpy(target,&cnt,sizeof(unsigned char));
    target += sizeof(unsigned char);
    memcpy(target,source,strLen);
    target += strLen;
    target += (field_len - strLen);
    return target;
  }

} // namespace TEAL
