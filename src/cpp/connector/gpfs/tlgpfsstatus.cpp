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
#include "teal_gpfs_connect.h"
#include "DbClusterInfo.h"
#include "DbFsInfo.h"
#include "DbDiskInfo.h"
#include "DbStgPoolInfo.h"
#include "DbFsetInfo.h"
#include "DbNodeInfo.h"
#include "DbPdiskInfo.h"
#include "DbVdiskInfo.h"
#include "DbDaInfo.h"
#include "DbRgInfo.h"
#include <iostream>
#include <iomanip>
#include <sstream>

using namespace std;

void usage(const string &processName)
{
  cerr<<"Usage: "<< processName<<"[{options}]"<<endl;
  cerr<<"  [options] can be any of"<<endl;
  cerr<<"    -g                       - print global status of all entities"             <<endl;
  cerr<<"    -c                       - print status of all clusters"                    <<endl;
  cerr<<"    -n                       - print status of all nodes"                       <<endl;
  cerr<<"    -f                       - print status of all file systems"                <<endl;
  cerr<<"    -d                       - print status of all disks"                       <<endl;
  cerr<<"    -s                       - print status of all storage pools"               <<endl;
  cerr<<"    -t                       - print status of all filesets"                    <<endl;
  cerr<<"    -r                       - print status of all recovery groups"             <<endl;
  cerr<<"    -a                       - print status of all declustered arrays"          <<endl;
  cerr<<"    -p                       - print status of all pdisks"                      <<endl;
  cerr<<"    -v                       - print status of all vdisks"                      <<endl;
  cerr<<"    -e \"colName=colValue\"    - expression to filter query result"             <<endl;
  cerr<<"                               all healthy entities: -e \"health=healthy\""     <<endl;
  cerr<<"                               all unhealthy entities: -e \"health=unhealthy\"" <<endl;
  cerr<<"                               unknown status entities: -e \"health=unknown\""  <<endl;
  cerr<<"    -l                       - print detailed status of a entity"               <<endl;
  cerr<<"    -h                       - print this message"                              <<endl;

}


int main(int argc, char *argv[])
{
    if(argc == 1)
    {
        cerr<<"Please specify at least one option!"<<endl;
        usage(argv[0]);
        exit(1);
    }    
    int op;
    bool is_detailed   = false;
    bool is_all        = false;  //query all entities
    bool is_entity     = false;  //only one entity should be queried once
    bool is_expression = false;  // only one expression should be specified once
    string expression  = "";

    bool is_cluster    = false;
    bool is_node       = false;
    bool is_fs         = false;
    bool is_fset       = false;
    bool is_stgpool    = false;
    bool is_disk       = false;
    bool is_rg         = false;
    bool is_da         = false;
    bool is_pdisk      = false;
    bool is_vdisk      = false;

    string colName     = "";
    string colValue    = "";
    while ( (op = getopt(argc, argv, "gcnfdstrapve:lh")) != -1 ) {
        switch (op) {
            case 'g':
                if(is_entity)
                {
                    cerr<<"Option -g can't coexist with other entity options!"<<endl;
                    exit(1);
                }
                is_entity   = true;
                is_all      = true;
                break;
                
            case 'l':
                is_detailed = true;
                break;
                
            case 'c':
                if(is_entity)
                {
                    cerr<<"Only one entity option can be specified once!"<<endl;
                    exit(1);
                }
                is_entity   = true;
                is_cluster  = true;
                break;
                
            case 'n':
                if(is_entity)
                {
                    cerr<<"Only one entity option can be specified once!"<<endl;
                    exit(1);
                }
                is_entity   = true;
                is_node     = true;
                break;
                
            case 's':
                if(is_entity)
                {
                    cerr<<"Only one entity option can be specified once!"<<endl;
                    exit(1);
                }
                is_entity   = true;
                is_stgpool  = true;
                break;
                
            case 'f':
                if(is_entity)
                {
                    cerr<<"Only one entity option can be specified once!"<<endl;
                    exit(1);
                }
                is_entity   = true;
                is_fs       = true;
                break;    
                
            case 't':
                if(is_entity)
                {
                    cerr<<"Only one entity option can be specified once!"<<endl;
                    exit(1);
                }
                is_entity   = true;
                is_fset     = true;
                break;
                
            case 'd':
                if(is_entity)
                {
                    cerr<<"Only one entity option can be specified once!"<<endl;
                    exit(1);
                }
                is_entity   = true;
                is_disk     = true;
                break;

            case 'v':
                if(is_entity)
                {
                    cerr<<"Only one entity option can be specified once!"<<endl;
                    exit(1);
                }
                is_entity   = true;
                is_vdisk    = true;
                break;
                
            case 'p':
                if(is_entity)
                {
                    cerr<<"Only one entity option can be specified once!"<<endl;
                    exit(1);
                }
                is_entity   = true;
                is_pdisk    = true;
                break;    
                
            case 'r':
                if(is_entity)
                {
                    cerr<<"Only one entity option can be specified once!"<<endl;
                    exit(1);
                }
                is_entity   = true;
                is_rg       = true;
                break;
                
            case 'a':
                if(is_entity)
                {
                    cerr<<"Only one entity option can be specified once!"<<endl;
                    exit(1);
                }
                is_entity   = true;
                is_da       = true;
                break;

            case 'e':
                expression = optarg;
                if(expression == "" || expression.find('=') == string::npos)
                {
                    cerr<<"Filter must be like \"colName=colValue\""<<endl;
                    exit(1);
                }
                colName  = expression;
                colValue = expression;
                // split and trim spaces around "="
                colName.erase(colName.begin() + colName.find_first_of('='),colName.end());
                colName.erase(colName.begin(), colName.begin() + colName.find_first_not_of(' '));
                colName.erase(colName.begin() + colName.find_last_not_of(' ') + 1, colName.end());
                colValue.erase(colValue.begin(),colValue.begin() + colValue.find_first_of('=') + 1);
                colValue.erase(colValue.begin(),colValue.begin() + colValue.find_first_not_of(' '));
                // Replace string in "health" field with its real integer value in DB table
                if(!strcmp(colName.c_str(),"health")) 
                {                                    
                    ostringstream stat;
                    if(!strcmp(colValue.c_str(),"healthy"))
                        stat << TEAL::HEALTHY;
                    if(!strcmp(colValue.c_str(),"unknown")) 
                        stat << TEAL::UNKNOWN;
                    if(!strcmp(colValue.c_str(),"unhealthy")) 
                        stat << TEAL::UNHEALTHY;
                    colValue = stat.str();
                }                                    
                colValue.erase(colValue.begin(),colValue.begin() + colValue.find_first_not_of(' '));
                is_expression = true;
                break;

            case 'h':
                usage(argv[0]);
                exit(0);

            default:
                usage(argv[0]);
                exit(1);
        }
    }

    if(is_all && is_expression)
    {
        cerr<<"Option -e can't coexist with -g options!"<<endl;
        exit(1);
    }
    if(!is_entity && is_detailed)
    {
        cerr<<"Option -l should be specified with an entity option!"<<endl;
        exit(1);
    }
    if(!is_entity && is_expression)
    {
        cerr<<"Option -e should be specified with an entity option!"<<endl;
        exit(1);
    }
  
    vector<tlgpfs_cluster_info_t*>* clusters = NULL;
    vector<tlgpfs_node_info_t*>*       nodes = NULL; 
    vector<tlgpfs_fs_info_t*>*            fs = NULL;
    vector<tlgpfs_disk_info_t*>*       disks = NULL;
    vector<tlgpfs_stg_info_t*>*         stgs = NULL;
    vector<tlgpfs_fset_info_t*>*       fsets = NULL;
    vector<tlgpfs_rg_info_t*>*           rgs = NULL;
    vector<tlgpfs_da_info_t*>*           das = NULL;
    vector<tlgpfs_pdisk_info_t*>*     pdisks = NULL;
    vector<tlgpfs_vdisk_info_t*>*     vdisks = NULL;

    if(is_all || (!is_all&&!is_expression))
    {
        colName  = "*";
        colValue = "";
    }
    teal_connector_handle conn_handle = NULL;
    TEAL_ERR_T ret = TEAL_SUCCESS;
    ret = teal_open_connector(&conn_handle,"GPFS","/tmp");
    if(ret != TEAL_SUCCESS)
    {
        cerr<<"open gpfs connector failed with "<< ret<<endl;
        return ret;
    }
    if(is_cluster || is_all)
    {
        cout<<endl;
        cout<<"################################  cluster status  ##################################"<<endl;
        cout<<endl;

        ret = tlgpfs_query_cluster_status(conn_handle,&clusters,colName,colValue);
        if(ret != TEAL_SUCCESS)
            cerr<<"query cluster status error with "<< ret<<endl;
    
        if(clusters && !clusters->empty())
        {
            vector<tlgpfs_cluster_info_t*>::iterator itr;
            
            int i = 0;
            for(itr = clusters->begin(); itr != clusters->end(); itr++,i++)
            {
                cout<<"Cluster "<< i <<":" <<endl;
                cout<<setiosflags(ios::left)<<setw(20)<<"Column Name"<<setiosflags(ios::left)<<setw(40)<<"Column Remarks"<<": Column Value"<<endl;  
                cout<<"------------------------------------------------------------------------------------"<<endl;
                TEAL::DbClusterInfo::printStatus(*itr,is_detailed);
                cout<<endl;
            }
        }
        else
        {
            cerr<<"No corresponding cluster is found."<<endl;
            ret = TEAL_ERR_ARG;
        }
    }
    if(is_node || is_all)
    {
        cout<<endl;
        cout<<"##################################  node status  ###################################"<<endl;
        cout<<endl;

        ret = tlgpfs_query_node_status(conn_handle,&nodes,colName,colValue);
        if(ret != TEAL_SUCCESS)
            cerr<<"query cluster status error with "<< ret<<endl;
    
        if(nodes && !nodes->empty())
        {
            vector<tlgpfs_node_info_t*>::iterator itr;

            int i = 0;
            for(itr = nodes->begin(); itr != nodes->end(); itr++,i++)
            {
                cout<<"Node "<< i <<":" <<endl;
                cout<<setiosflags(ios::left)<<setw(20)<<"Column Name"<<setiosflags(ios::left)<<setw(40)<<"Column Remarks"<<": Column Value"<<endl;  
                cout<<"------------------------------------------------------------------------------------"<<endl;
                TEAL::DbNodeInfo::printStatus(*itr,is_detailed);
                cout<<endl;
            }
        }
        else
        {
            cerr<<"No corresponding node is found."<<endl;
            ret = TEAL_ERR_ARG;
        }
    }

    if(is_fs || is_all)
    {
        cout<<endl;
        cout<<"###############################  file system status  ###############################"<<endl;
        cout<<endl;

        ret = tlgpfs_query_fs_status(conn_handle,&fs,colName,colValue);
        if(ret != TEAL_SUCCESS)
            cerr<<"query fs status error with "<< ret<<endl;
    
        if(fs && !fs->empty())
        {
            vector<tlgpfs_fs_info_t*>::iterator itr;

            int i = 0;
            for(itr = fs->begin(); itr != fs->end(); itr++,i++)
            {
                cout<<"Fs "<< i <<":" <<endl;
                cout<<setiosflags(ios::left)<<setw(20)<<"Column Name"<<setiosflags(ios::left)<<setw(40)<<"Column Remarks"<<": Column Value"<<endl;  
                cout<<"------------------------------------------------------------------------------------"<<endl;
                TEAL::DbFsInfo::printStatus(*itr,is_detailed);
                cout<<endl;
            }
        }
        else
        {
            cerr<<"No corresponding fs is found."<<endl;
            ret = TEAL_ERR_ARG;
        }
    }
    
    if(is_disk || is_all)
    {
        cout<<endl;
        cout<<"####################################  disk status  #################################"<<endl;
        cout<<endl;

        ret = tlgpfs_query_disk_status(conn_handle,&disks,colName,colValue);
        if(ret != TEAL_SUCCESS)
            cerr<<"query disk status error with "<< ret<<endl;
    
        if(disks && !disks->empty())
        {
            vector<tlgpfs_disk_info_t*>::iterator itr;

            int i = 0;
            for(itr = disks->begin(); itr != disks->end(); itr++,i++)
            {
                cout<<"Disk "<< i <<":" <<endl;
                cout<<setiosflags(ios::left)<<setw(20)<<"Column Name"<<setiosflags(ios::left)<<setw(40)<<"Column Remarks"<<": Column Value"<<endl;  
                cout<<"------------------------------------------------------------------------------------"<<endl;
                TEAL::DbDiskInfo::printStatus(*itr,is_detailed);
                cout<<endl;
            }
        }
        else
        {
            cerr<<"No corresponding disk is found."<<endl;
            ret = TEAL_ERR_ARG;
        }
    }
    if(is_stgpool || is_all)
    {
        cout<<endl;
        cout<<"#############################  storage pool status    ##############################"<<endl;
        cout<<endl;

        ret = tlgpfs_query_stg_status(conn_handle,&stgs,colName,colValue);
        if(ret != TEAL_SUCCESS)
            cerr<<"query storage pool status error with "<< ret<<endl;
    
        if(stgs && !stgs->empty())
        {
            vector<tlgpfs_stg_info_t*>::iterator itr;

            int i = 0;
            for(itr = stgs->begin(); itr != stgs->end(); itr++,i++)
            {
                cout<<"Storage pool "<< i <<":" <<endl;
                cout<<setiosflags(ios::left)<<setw(20)<<"Column Name"<<setiosflags(ios::left)<<setw(40)<<"Column Remarks"<<": Column Value"<<endl;
                cout<<"------------------------------------------------------------------------------------"<<endl;
                TEAL::DbStgPoolInfo::printStatus(*itr,is_detailed);
                cout<<endl;
            }
        }
        else
        {
            cerr<<"No corresponding storage pool is found."<<endl;
            ret = TEAL_ERR_ARG;
        }
    }
    if(is_fset || is_all)
    {
        cout<<endl;
        cout<<"################################  file set status  #################################"<<endl;
        cout<<endl;
        
        ret = tlgpfs_query_fset_status(conn_handle,&fsets,colName,colValue);
        if(ret != TEAL_SUCCESS)
            cerr<<"query file set status error with "<< ret <<endl;
    
        if(fsets && !fsets->empty())
        {
            vector<tlgpfs_fset_info_t*>::iterator itr;

            int i = 0;
            for(itr = fsets->begin(); itr != fsets->end(); itr++,i++)
            {
                cout<<"File set "<< i <<":" <<endl;
                cout<<setiosflags(ios::left)<<setw(20)<<"Column Name"<<setiosflags(ios::left)<<setw(40)<<"Column Remarks"<<": Column Value"<<endl;
                cout<<"------------------------------------------------------------------------------------"<<endl;
                TEAL::DbFsetInfo::printStatus(*itr,is_detailed);
                cout<<endl;
            }
        }
        else
        {
            cerr<<"No corresponding file set is found."<<endl;
            ret = TEAL_ERR_ARG;
        }
    }
    
    if(is_rg || is_all)
    {
        cout<<endl;
        cout<<"###########################  recovery group status  ################################"<<endl;
        cout<<endl;
        
        ret = tlgpfs_query_rg_status(conn_handle,&rgs,colName,colValue);
        if(ret != TEAL_SUCCESS)
            cerr<<"query recovery group status error with "<< ret <<endl;
    
        if(rgs && !rgs->empty())
        {
            vector<tlgpfs_rg_info_t*>::iterator itr;

            int i = 0;
            for(itr = rgs->begin(); itr != rgs->end(); itr++,i++)
            {
                cout<<"Recovery group "<< i <<":" <<endl;
                cout<<setiosflags(ios::left)<<setw(20)<<"Column Name"<<setiosflags(ios::left)<<setw(40)<<"Column Remarks"<<": Column Value"<<endl;
                cout<<"------------------------------------------------------------------------------------"<<endl;
                TEAL::DbRgInfo::printStatus(*itr,is_detailed);
                cout<<endl;
            }
        }
        else
        {
            cerr<<"No corresponding recovery group is found."<<endl;
            ret = TEAL_ERR_ARG;
        }
    }

    if(is_da || is_all)
    {
        cout<<endl;
        cout<<"###########################  declustered array status  #############################"<<endl;
        cout<<endl;
        
        ret = tlgpfs_query_da_status(conn_handle,&das,colName,colValue);
        if(ret != TEAL_SUCCESS)
            cerr<<"query declustered array status error with "<< ret <<endl;
    
        if(das && !das->empty())
        {
            vector<tlgpfs_da_info_t*>::iterator itr;

            int i = 0;
            for(itr = das->begin(); itr != das->end(); itr++,i++)
            {
                cout<<"Declustered array "<< i <<":" <<endl;
                cout<<setiosflags(ios::left)<<setw(20)<<"Column Name"<<setiosflags(ios::left)<<setw(40)<<"Column Remarks"<<": Column Value"<<endl;
                cout<<"------------------------------------------------------------------------------------"<<endl;
                TEAL::DbDaInfo::printStatus(*itr,is_detailed);
                cout<<endl;
            }
        }
        else
        {
            cerr<<"No corresponding declustered array is found."<<endl;
            ret = TEAL_ERR_ARG;
        }
    }

    if(is_vdisk || is_all)
    {
        cout<<endl;
        cout<<"############################  Perseus Vdisk status  ################################"<<endl;
        cout<<endl;
        
        ret = tlgpfs_query_vdisk_status(conn_handle,&vdisks,colName,colValue);
        if(ret != TEAL_SUCCESS)
            cerr<<"query vdisk status error with "<< ret <<endl;
    
        if(vdisks && !vdisks->empty())
        {
            vector<tlgpfs_vdisk_info_t*>::iterator itr;

            int i = 0;
            for(itr = vdisks->begin(); itr != vdisks->end(); itr++,i++)
            {
                cout<<"Vdisk "<< i <<":" <<endl;
                cout<<setiosflags(ios::left)<<setw(20)<<"Column Name"<<setiosflags(ios::left)<<setw(40)<<"Column Remarks"<<": Column Value"<<endl;
                cout<<"------------------------------------------------------------------------------------"<<endl;
                TEAL::DbVdiskInfo::printStatus(*itr,is_detailed);
                cout<<endl;
            }
        }
        else
        {
            cerr<<"No corresponding vdisk is found."<<endl;
            ret = TEAL_ERR_ARG;
        }
    }
    
    if(is_pdisk || is_all)
    {
        cout<<endl;
        cout<<"############################  Perseus Pdisk status  ################################"<<endl;
        cout<<endl;
        
        ret = tlgpfs_query_pdisk_status(conn_handle,&pdisks,colName,colValue);
        if(ret != TEAL_SUCCESS)
            cerr<<"query pdisk status error with "<< ret <<endl;
    
        if(pdisks && !pdisks->empty())
        {
            vector<tlgpfs_pdisk_info_t*>::iterator itr;

            int i = 0;
            for(itr = pdisks->begin(); itr != pdisks->end(); itr++,i++)
            {
                cout<<"Pdisk "<< i <<":" <<endl;
                cout<<setiosflags(ios::left)<<setw(20)<<"Column Name"<<setiosflags(ios::left)<<setw(40)<<"Column Remarks"<<": Column Value"<<endl;
                cout<<"------------------------------------------------------------------------------------"<<endl;
                TEAL::DbPdiskInfo::printStatus(*itr,is_detailed);
                cout<<endl;
            }
        }
        else
        {
            cerr<<"No corresponding pdisk is found."<<endl;
            ret = TEAL_ERR_ARG;
        }
    }

    ret = teal_close_connector(conn_handle);
    if(ret != TEAL_SUCCESS)
        cerr<<"close gpfs connector error with "<< ret<<endl;

    return ret;

}

