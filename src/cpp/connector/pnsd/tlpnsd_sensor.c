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

/**
 * Detect the PNSD status.
 *
 * This function will
 *
 * 1) Issue the pnsd_stat command
 * 2) Parse the output
 * 3) Calculate the failure percentages
 * 4) Output the percentages to RMC subsystem
 *
 */

/*--------------------------------------------------------------------*/
/*  Includes                                                          */
/*--------------------------------------------------------------------*/

#include <stdio.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <regex.h>
#include <string.h>
#include <stdlib.h>
#include <limits.h>
#include <errno.h>

/*--------------------------------------------------------------------*/
/*  User Types                                                        */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Constants                                                         */
/*--------------------------------------------------------------------*/

//const char* PNSD_STAT = "/usr/bin/pnsd_stat -n";
const char* PNSD_STAT = "pnsd_stat -n";
const char* PNSD_RETRANSMIT = "^ +([0-9]+) retransmitted .*$";
const char* PNSD_SENT_PKT   = "^ +([0-9]+) packets sent .*$";

/*--------------------------------------------------------------------*/
/*  Macros                                                            */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/*  Internal Function Prototypes                                      */
/*--------------------------------------------------------------------*/

int prep_re(const char* re_str, regex_t* reg_prog);

/*--------------------------------------------------------------------*/
/*  Global Variables                                                  */
/*--------------------------------------------------------------------*/

/*--------------------------------------------------------------------*/
/* >>> Function <<<                                                   */
/*--------------------------------------------------------------------*/

int main(int argc, char* argv[])
{
    int rc;
    char data[256];
    char *line;

    regex_t retrans_re;
    regex_t sent_pkt_re;

    unsigned long long retrans_cnt = 0;
    unsigned long long sent_pkt_cnt = 0;

    // Prepare the regular expressions
    rc = prep_re(PNSD_SENT_PKT, &sent_pkt_re);
    if (rc != 0) {
        return rc;
    }

    rc = prep_re(PNSD_RETRANSMIT, &retrans_re);
    if (rc != 0) {
        return rc;
    }

    // Issue the command
    FILE* cmd_out = popen(PNSD_STAT,"r");
    if (!cmd_out) {
        rc = errno;
        perror("Failed to invoke command");
        return rc;
    }

    // Parse the output of the command
    while ((line = fgets(data,sizeof(data),cmd_out)) != NULL) {
        regmatch_t match[2];

        rc = regexec(&retrans_re, line, 2, match, 0);
        if (rc == 0) {
            retrans_cnt = strtoull(&line[match[1].rm_so],0,0);
        }

        rc = regexec(&sent_pkt_re, line, 2, match, 0);
        if (rc == 0) {
            sent_pkt_cnt = strtoull(&line[match[1].rm_so],0,0);
        }
    }

    // Get the status of the command to make sure it executed
    rc = pclose(cmd_out);
    if (rc == -1) {
        rc = errno;
        perror("Failed to execute command");
        return rc;
    } else if (rc > 0) {
        if WIFEXITED(rc) {
            rc = WEXITSTATUS(rc);
        } else {
            rc = -1;
        }
        fprintf(stderr,"Command failed: status = %d\n",rc);
        return rc;
    }

    // Calculate and print out the statistics for RMC
    float ratio;
    if (sent_pkt_cnt == 0) {
    	ratio = 0.0;
    } else {
    	ratio = (float)retrans_cnt/(float)sent_pkt_cnt;
    }

    fprintf(stdout,"Float64=%.2g\n",ratio);

    // Clean up the regular expressions
    regfree(&retrans_re);
    regfree(&sent_pkt_re);

    return rc;
}

/*--------------------------------------------------------------------*/

int prep_re(const char* re_str, regex_t* re_prog)
{
    int rc = regcomp(re_prog, re_str, REG_EXTENDED);
    if (rc != 0) {
        char err_msg[256];
        regerror(rc, re_prog, err_msg, sizeof(err_msg));
        fprintf(stderr,"%s",err_msg);
        return rc;
    }

    return rc;
}


