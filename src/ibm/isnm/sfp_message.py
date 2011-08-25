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

import struct
import array
import time
from datetime import datetime

class SfpMessage(object):
    ''' Base class for all Service Focal Point (SFP) messages
    '''
    def __init__(self, opcode):
        ''' Constructor. Initializes the common packet header
        '''
        self.pkt = array.array('B','\0'*65535)
        self.offset = 0
    
        hdr_fmt = '>IBH'
        hdr_size = struct.calcsize(hdr_fmt)
        struct.pack_into(hdr_fmt,self.pkt,self.offset,0xEAEAEAEA,opcode,hdr_size)
        self.offset += hdr_size

    def finalize(self):
        ''' Finalizes the message by setting the final offset as the length of the message
        '''
        # Re-adjust the packet size based on the data inserted 
        struct.pack_into('>H',self.pkt,5,self.offset)
        
        return self.pkt.tostring()[:self.offset]


class SfpCreateMessage(SfpMessage):
    ''' Create Message
    '''
    def __init__(self):
        ''' Constructor
        '''
        SfpMessage.__init__(self,0x01)

    def build(self, 
              alert, 
              client_name, 
              fru_list, 
              notif_type, 
              enc_mtms, 
              pwr_mtms, 
              neighbor_list,
              eed_location,
              extended_data):
        ''' This method will build the message in the proper order of values. This is the only method
        that should be called by the user
        '''
        self._add_base_alert(alert, client_name)
        self._add_frus(fru_list)
        self._add_svc_info(notif_type, enc_mtms, pwr_mtms)
        self._add_neighbors(neighbor_list)
        self._add_eed_info(eed_location,extended_data)
        
        # Finalize the  message
        return self.finalize() 


    def _add_base_alert(self, alert, client_name):
        client_name_len = len(client_name)
        
        if (alert.event_loc):
            event_loc = str(alert.event_loc)
        else:
            event_loc = '' 
        event_loc_len = len(event_loc)

        if alert.recommendation:
            recommendation = alert.recommendation
        else:
            recommendation = ''
        recommend_len = len(recommendation)

        if alert.src_name:
            src_name = alert.src_name
        else:
            src_name = ''
        src_name_len = len(src_name)

        if alert.reason:
            reason = alert.reason
        else:
            reason = ''
        reason_len = len(reason)

        base_alert_fmt = '>BH{0}sQ8sIH{1}sH{2}sH{3}sH{4}s'.format( 
        #base_alert_fmt = '>BH{0}sI8sIH{1}sH{2}sH{3}sH{4}s'.format(
                                                         client_name_len,
                                                         event_loc_len,
                                                         recommend_len,
                                                         src_name_len,
                                                         reason_len)
        base_alert_size = struct.calcsize(base_alert_fmt)
        struct.pack_into(base_alert_fmt,
                         self.pkt,
                         self.offset,
                         1,
                         client_name_len,
                         client_name,
                         alert.rec_id,
                         self._bcd_timestamp(alert.creation_time),
                         int(alert.alert_id,16),
                         event_loc_len,
                         event_loc,
                         recommend_len,
                         recommendation,
                         src_name_len,
                         src_name,
                         reason_len,
                         reason)
        self.offset += base_alert_size

    def _add_frus(self,fru_list):
        fru_list_len = len(fru_list)
        
        fru_list_fmt = '>H'
        frus = []
        for f in fru_list:
            fru_list_fmt += 'H{0}s'.format(len(f))
            frus.extend([len(f),f])
        fru_list_size = struct.calcsize(fru_list_fmt)

        struct.pack_into(fru_list_fmt,self.pkt,self.offset,fru_list_len,*frus)
        self.offset += fru_list_size

    def _add_svc_info(self, svc_notif, enc_mtms, pwr_mtms):
        if not enc_mtms:
            e_mtms = ' '*21
        else:
            e_mtms = enc_mtms + ' '*(21-len(enc_mtms))

        if not pwr_mtms:
            p_mtms = ' '*21
        else:
            p_mtms = pwr_mtms + ' '*(21-len(pwr_mtms))

        svc_info_fmt = '>21s21sB'
        svc_info_size = struct.calcsize(svc_info_fmt)
        struct.pack_into(svc_info_fmt,self.pkt,self.offset,e_mtms,p_mtms,svc_notif)
        self.offset += svc_info_size

    def _add_neighbors(self, neighbor_list):
        neighbor_list_len = len(neighbor_list)

        neighbor_list_fmt = '>H'
        neighbors = []
        for n in neighbor_list:
            neighbor_list_fmt += 'H{0}s'.format(len(n))
            neighbors.extend([len(n),n])
        neighbor_list_size = struct.calcsize(neighbor_list_fmt)

        struct.pack_into(neighbor_list_fmt,self.pkt,self.offset,neighbor_list_len,*neighbors)
        self.offset += neighbor_list_size

    def _add_eed_info(self, eed_location, extended_data):
        if eed_location is None:
            eed_location = ''
        eed_loc_len = len(eed_location)
            
        if extended_data is None:
            extended_data = ''
        extended_data_len = len(extended_data)

        eed_info_fmt = '>H{0}sH{1}s'.format(eed_loc_len,extended_data_len)
        eed_info_size = struct.calcsize(eed_info_fmt)
        struct.pack_into(eed_info_fmt,self.pkt,self.offset,
                         eed_loc_len,
                         eed_location,
                         extended_data_len,
                         extended_data)
        self.offset += eed_info_size

    def _bcd_timestamp(self, timestamp):
        ''' Convert datetime into UTC BCD value
        '''
        if timestamp is None:
            timestamp = datetime.now()
            
        # Decimal to BCD conversion    
        d2b = lambda v : (v/10)*16+v%10
        
        # This code converts the datetime to a UTC value
        time_fmt = '%Y-%m-%d %H:%M:%S'
        str_today = timestamp.strftime(time_fmt)
        ttime = time.strptime(str_today,time_fmt)
        mtime = time.mktime(ttime)
        gtime = time.gmtime(mtime)
        
        # Get the BCD equivalents of the time parts
        c=d2b(gtime.tm_year/100)
        yr=d2b(gtime.tm_year%100)
        mo=d2b(gtime.tm_mon)
        dy=d2b(gtime.tm_mday)
        h=d2b(gtime.tm_hour)
        m=d2b(gtime.tm_min)
        s=d2b(gtime.tm_sec)
        t=0
        return struct.pack('BBBBBBBB',c,yr,mo,dy,h,m,s,t)
