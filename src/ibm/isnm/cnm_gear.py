# begin_generated_IBM_copyright_prolog
#
# This is an automatically generated copyright prolog.
# After initializing,  DO NOT MODIFY OR MOVE
# ================================================================
#
# (C) Copyright IBM Corp.  2010,2011
# Eclipse Public License (EPL)
#
# ================================================================
#
# end_generated_IBM_copyright_prolog

import socket
from ibm.teal.analyzer.gear.external_base_classes import ExtInitAlert
from ibm.teal.registry import get_logger

class CnmInitAlert(ExtInitAlert):
    '''
    This class is responsible for initializing the alert so the service focal point
    listener can get all the information it needs to create its SFP error log packet.

    It will put most of the data into a parsable string in the alert raw_data field
    '''

    def __init__(self):
        '''
        Constructor
        '''
        return


    def update_init_data(self):
	''' This method is called by update_init_data_main which does 
	setup to simplify the coding of this method.  
    
        This method should modify how the alert should be created by 
	modifying self.init_dict which will be filled in prior to it 
	being called and will be returned after this method returns
        
        The flow is to get the FRU list from the metadata then step through it 
         For each FRU, the fru string is split into either 2 or 3 fields.
         Field 1 is the FRU class
         Field 2 is either a symbolic or isolation procedure name or a FRU location
         Field 3 is used if a symbolic procedure or a common FRU is defined.
         The service location, part number, serial number, ECID and CCIN
         are parsed according to FRU class; these are initialized to blank strings, so that
         if a field has no meaning for a particular FRU class, it does not have to be explicitly set.
         Next the FRU list is built.
         Finally, the self.init_dict is modified and returned.
      
      Typically, the only values in the FRU list that are passed back are in the event data or alert metadata. However,
      if data cannot be determined, it may be set to "None" or "".  If a procedure name in the metadata is too long
      (7 characters is the limit), the procedure "HFILONG" will be used instead. If the FRU class is unknown,
      the Isolation procedure "HFI_UFC" will be used and the location will be the metadata.
      If a common part cannot be determined, "HFI_COM" will be used as an isolation procedure.
      If neither the local nor nbr are in common, the data FRU from the 
      metadata will be placed in the location. If the local and nbr are both
      in common, then the local will be placed in the location.

      Two methods are included:
             get_part_info will parse the part info based on the location field from the event. This is passed to it.

             common_fru_check will step through all events related to the alert and look to see if the local or neighbor
             location field of the first event is common among all events. It passes back the location that is common.

	'''
	# Get the FRU list 
	fru_list = self.get_fru_list()

	frus = fru_list.split(',')
	#print frus 		# This is the list of FRUs 
	fruList = ""
	my_event = list(self.init_dict['condition_events'])

	for fru in frus:
	   fru = fru.strip()

           #--------------------------------------------------------              
	   # Here is a list of the fru_list fields in the CNM_GEAR_alert_metadata.xml file
	   #
	   # Isolation Procedures
           #      ISO:[procedure name]
           #      Examples:
	   #          ISO:HFI_LNM
	   #          ISO:HFIGCTR	- HFI Global Counter	
	   #	
	   # Symbolic Procedures:
	   #     SYM:[procedure name]:[svc_location & vpd field]
           #     Examples : 
           #         SYM:HFI_CAB:nbr_port,
	   #         SYM:CBL_CONT:local_port
	   #         SYM:HFI_LRA:common_port
	   #
	   # Field Replaceable Units:
           #      FRU:[svc_location & vpd field]
           #     Examples:	    
           #        FRU:nbr_torrent,
	   #        FRU:local_torrent
	   # 
           #--------------------------------------------------------          
           # Initialize part information
           #--------------------------------------------------------              
           servLoc=""
           partNumber=""
           serNum=""
           ecid=""
           ccin=""

           #--------------------------------------------------------------
           #  Split up the FRU from the metadata into constituent fields
           #--------------------------------------------------------------
           fru_data = fru.split(':')

           # first make sure that you have a FRU Class
           if (len(fru_data) < 2): 
	        get_logger().info('No FRU Class provided in metadata.')
                fruClass="Isolation Procedure"
		# Unknown FRU
                partNumber="HFI_UFC"
                servLoc=fru
           else:
                # Parse FRU part information based on FRU Class
                if fru.startswith('ISO'):
		    get_logger().debug('Found a Isolation Procedure entry')
		
		    fruClass="Isolation Procedure"
		    # MGA changed parantheses in this test
           	    if ( len(fru_data[1]) <= 7 ): 
                        partNumber=fru_data[1]
                    else:
		    	get_logger().info('Invalid Isolation Procedure - too long')
                        partNumber="HFILONG"

                elif fru.startswith('SYM'):
		    get_logger().debug('Found a Symbolic Procedure')
                    fruClass="Symbolic Procedure"
		    # test that fru_data[2] exists; then see if we're looking for a common fru location
                    if len(fru_data) == 3:
                        if fru_data[2].startswith('common'):
                            part = self.common_fru_check(self.get_events(),fru_data[2].replace('common',""))
                            if part is None:
	        	        get_logger().info('No common part found')
                                part_number="HFI_COM"
                                fruClass="Isolation Procedure"
                                servLoc=fru
		            # MGA: both local & nbr match
			    elif part == "both":
                                servLoc, partNumber, ignoreserNum,ignoreecid,ignoreccin = self.get_part_info(my_event[0].raw_data[fru_data[2].replace('common',"local")])
			        part_number="HFI_COM"
				fruClass="Isolation Procedure"
                            else:
                                servLoc, partNumber, ignoreserNum,ignoreecid,ignoreccin = self.get_part_info(my_event[0].raw_data[part])
                        else:
                            # not a common location from multiple events; just get from event[0]
                            servLoc, partNumber, ignoreserNum,ignoreecid,ignoreccin = self.get_part_info(my_event[0].raw_data[fru_data[2]])

	
                    else:
                        servLoc="None"

           	    if ( len(fru_data[1]) <= 7 ): 
		        partNumber=fru_data[1]
                    else:
                        #print 'Invalid Symbolic procedure : too long'
		    	get_logger().info('Invalid Symbolic Procedure - too long')
                        partNumber="HFILONG"
                                
  	        elif fru.startswith('FRU'):
		    get_logger().debug('Found a Field Replaceable Unit (FRU) entry')
                    fruClass="FRU"
                    if fru_data[1].startswith('common'):
                        part = self.common_fru_check(self.get_events(),fru_data[2].replace('common',''))
                        if part is None:
	        	    get_logger().info('No common part found')
                            part_number="HFI_COM"
                            fruClass="Isolation Procedure"
                            servLoc=fru
		        # MGA: both local & nbr match
		        elif part == "both":
                           servLoc, partNumber, ignoreserNum,ignoreecid,ignoreccin = self.get_part_info(my_event[0].raw_data[fru_data[2].replace('common',"local")])
			   part_number="HFI_COM"
			   fruClass="Isolation Procedure"
	
                        else:
                            servLoc, partNumber, serNum,ecid,ccin = self.get_part_info(my_event[0].raw_data[part])
                    else:
                        servLoc, partNumber, serNum,ecid,ccin = self.get_part_info(my_event[0].raw_data[fru_data[1]])
	                                
                else:
                  #Unknown FRU class
		  get_logger().info('Unknown Field Replaceable Unit (FRU) class')
                  fruClass="Isolation Procedure"
                  partNumber="HFI_UFC"
                  servLoc=fru

            # - Done parsing based on FRU class

           #----------------------------------------------------------------
           # Build the FRU list - only if the part info in the event does 
	   # not contain "Ignore"
	   # MGA: Ignore added per review comments on 2/8/2011

           if ( servLoc != 'Ignore' ):
              # strip leading and trailing blanks
              partNumber=partNumber.strip()
              servLoc=servLoc.strip()
              serNum=serNum.strip()
              ecid=ecid.strip()
              ccin=ccin.strip()

              # add fields to the fruList
              fruList += "{ %s,%s,%s,%s,%s,%s }," % (partNumber,fruClass,servLoc,serNum,ecid,ccin)

	    #print 'FRU list = ',fruList
	   else:
	     get_logger().info('Ignore the FRU given in metadata because not available in event log')

	# {Part Number, Class, Physical Location Code, SerialNumber,ECID,CCIN}
	#self.raw_data_dict['non_dict_raw_data'] = fruList
	fruList=fruList.rstrip(',')

	self.raw_data_dict['fru_list'] = fruList
	
	# The following fields need to get placed in the raw data dict
	#
	#   cnm_ext_event		build side
        #
	# eed_loc_info		--> eed_location
	# encl_mtms		--> enc_mtms
	# pwr_ctrl_mtms		--> pwr_mtms
	# neighbor_loc_code	
	# neighbor_loc_type
	#
	#  Parameters for def build call, which will build the SFP message.
	# 	self, alert, client_name, fru_list, notif_type, 
	# 	enc_mtms, pwr_mtms, neighbor_list, eed_location,
	# 	extended_data
	#
	# self.raw_data_dict['alert_id'] = alert_id ???
	# self.raw_data_dict['client_name'] = client_name ???
	self.raw_data_dict['encl_mtms'] = my_event[0].raw_data['encl_mtms']
	self.raw_data_dict['pwr_enc'] = my_event[0].raw_data['pwr_ctrl_mtms']
	self.raw_data_dict['eed_loc'] = my_event[0].raw_data['eed_loc_info']
	#self.raw_data_dict['ext_data'] = my_event[0].raw_data['isnm_raw_data;']

	# The following call will replace the description with a message that 
	# include the local and neighbor frame, supernode, drawer, hub and port 
	# after parsing FR002-SN005-DR2-HB3-LD10
	#
        if my_event[0].raw_data['neighbor_loc'] is not None:
	    self.add_loc_substitutions(my_event[0].raw_data['neighbor_loc'], 'neighbor_')
	    self.raw_data_dict['nbr_loc'] = my_event[0].raw_data['neighbor_loc'].get_location()
	    self.raw_data_dict['nbr_typ'] = my_event[0].raw_data['neighbor_loc'].get_id()
   
	
    # Use this to parse the part info in the part field passed in the event
    # sometimes only the service location is given
    # if more than the service location is given, then all fields must be given
    def get_part_info(self, part_info):
        svc_loc = "Ignore"
        pn = ""
        sn = ""
        ec = ""
        cc = ""
	
        if part_info != None :
           part_data=part_info.split(',')
	             
           svc_loc = part_data[0]
           if len(part_data) == 5:
               pn = part_data[1]
               sn = part_data[2]
               ec = part_data[3]
               cc = part_data[4]
           else:
	       # MGA: per review comments take into account the chance for
	       # missing part data
               if len(part_data) > 1:
                 pn = part_data[1]
   
 	         if len(part_data) > 2:
                   sn = part_data[2]

                   if len(part_data) > 3:
                      ec = part_data[3]

        return svc_loc,pn,sn,ec,cc
	
	
    # Compare locations in events to determine if the first event.s local or neighbor is common
    def common_fru_check(self, event_list, fru):
	''' Find the specified common FRU between all of the events. If there are no common FRUs
	"None" will be returned
	'''
	#print '****',event_list,fru
	local_fru =  'local_'+fru
	nbr_fru = 'nbr_'+fru
	first_event = True
	match_local = True
		        
	for e in event_list:
	    # Get the extended event data from the event
	    ext_data = e.raw_data
	            
	    # Pull out the FRU info for current event
	    # TODO: If the current event does not have one of the
	    #       necessary components, skip it? 
	    # MGA: per review comments, combine the two "try:" & "except:"
	    try:
		local_location = ext_data[local_fru]
		nbr_location = ext_data[nbr_fru]
	    except:
		continue
	                
	    # MGA: per review comments, combine the two "try:", above
	    #try:
	    #	nbr_location = ext_data[nbr_fru]
	    #except:
	    #   continue
	                        
	    if first_event:
		# First event is used for comparison
		first_event = False
	                
		base_local_location = local_location
		match_local = True
	                
		base_nbr_location = nbr_location
		match_nbr = True
	    else:
		# Compare first event with the rest of the events
		if ((base_local_location != local_location) and (base_local_location != nbr_location)):
		    match_local = False

                    # MGA: per review comments
		    # if both local & nbr are False now, return None
		    if ( match_nbr == False ):
		      return None

		if ((base_nbr_location != nbr_location) and (base_nbr_location != local_location)):
		    match_nbr = False

                    # MGA: per review comments
		    # if both local & nbr are False now, return None
		    if ( match_local == False ):
		      return None
	        
	#print 'Local location ',local_location
	#print 'Neighbor location ',nbr_location
	
	if match_nbr:
	    return base_nbr_location

             # match_local covers both match_local and match_local and match_nbr
	if match_local:
	    return base_local_location
            
	if not match_local and not match_nbr:
            #print 'No common location found'
	    return None

        # MGA: per review comments
        # if both the local matches and neighbor matches this suggests
	# that either all of the events are reported at the same location
	# or scoped to the same location. This would suggest that the
	# location scope used for the condition is not appropriate
	# return 'both'
	if match_local and match_nbr:
	    return 'both' 
	            
	return common_location
