__author__ = 'asifj'
import json
import re
import csv

class Querybuilder:

    def build_common_query(self, tablename):
        # OS value will be Platform Meta data field and baseproductname will be get from csv and platform will be series like M series or E series.
        tmp = ""
        ifile  = open('..\\Baseproduct-mapping.csv', "rb")
        reader = csv.reader(ifile)
        for row in reader:
            if row[0].strip()==self.product.strip():
                self.base_product_name = row[1].strip()
        if self.node==None or self.node=='NULL':
            tmp = "devicenode is NULL"
        else:
            tmp = "devicenode='" + str(self.node) + "'"
        self.common_query = "select * from "+tablename+" where \
            hostname='" + str(self.host_name) + "' and serialnumber='" + str(self.serial_number) + "' and \
            product='" + str(self.product) + "' and baseproduct='" + str(self.base_product_name) + "' and \
            os='" + str(self.platform) + "' and aiscriptversion='" + str(self.aiscript_version) + "' and \
            softwarerelease='" + str(self.software_release) + "' and collectortype='PHC' and \
            spaceversion='" + str(self.space_version) + "' and "+str(tmp)+" and\
            basesoftwarerlease='" + str(self.base_software_release) + "' and spaceversion='" + str(self.space_version) + "' and \
            servicenowversion='" + str(self.servicenow_version) + "' and softwarerelease='" + str(self.software_release) + "' and \
            collector_time between '" + str(self.phdct_utc) + "' and '" + str(self.phdct_utc) + "' "
        '''
        self.common_query = "select * from "+tablename+" where \
            hostname='" + str(self.host_name) + "' and serialnumber='" + str(self.serial_number) + "' and \
            product='" + str(self.product) + "' and baseproduct='" + str(self.base_product_name) + "' and \
            platform is NULL and os='"+self.platform+"' and aiscriptversion='" + str(self.aiscript_version) + "' and \
            softwarerelease='" + str(self.software_release) + "' and collectortype='PHC' and \
            spaceversion='" + str(self.space_version) + "' and "+str(tmp)+" and\
            basesoftwarerlease='" + str(self.base_software_release) + "' and spaceversion='" + str(self.space_version) + "' and \
            servicenowversion='" + str(self.servicenow_version) + "' and softwarerelease='" + str(self.software_release) + "' and \
            collector_time between '" + str(self.phdct_utc) + "' and '" + str(self.phdct_utc) + "' "'''

    def build_arp_data_query(self, arp_data):
        totalarpentries = arp_data.get("total_entries", 0)
        self.command_query = ""
        self.command_query =" and totalarpentries="+str(totalarpentries)+"  order by collector_time"

    def build_buff_data_query(self, buff_data):
        chassisname = buff_data.get("chassisname", "")
        currentMbufs = buff_data.get("mbufs in use (current/cache/total)",0)[0]
        cacheMbufs = buff_data.get("mbufs in use (current/cache/total)",0)[1]
        totalMbufs = buff_data.get("mbufs in use (current/cache/total)",0)[2]

        currentMbufClusters = buff_data.get("mbuf clusters in use (current/cache/total/max)", 0)[0]
        cacheMbufClusters = buff_data.get("mbuf clusters in use (current/cache/total/max)", 0)[1]
        totalMbufClusters = buff_data.get("mbuf clusters in use (current/cache/total/max)", 0)[2]

        reqsForMbufsDenied = buff_data.get("requests for mbufs denied (mbufs/clusters/mbuf+clusters)", 0)[0]
        reqsForClustersDenied = buff_data.get("requests for mbufs denied (mbufs/clusters/mbuf+clusters)", 0)[0]
        reqsForMbufsPlusClustersDenied = buff_data.get("requests for mbufs denied (mbufs/clusters/mbuf+clusters)", 0)[0]

        reqsForMbufsDelayed = buff_data.get("mbuf requests delayed", 0)[0]
        reqsForClustersDelayed = buff_data.get("cluster requests delayed", 0)[0]

        self.command_query = ""
        self.command_query =" and chassisname"+str(" is NULL" if chassisname=="" else "='"+str(chassisname)+"'" )+" and currentmbufs="+str(currentMbufs)+" and cachembufs="+str(cacheMbufs)+" and \
                            totalmbufs="+str(totalMbufs)+" and currentmbufclusters="+str(currentMbufClusters)+" and \
                            cachembufclusters="+str(cacheMbufClusters)+" and totalmbufclusters="+str(totalMbufClusters)+" \
                            and reqsformbufsdenied="+str(reqsForMbufsDenied)+" and reqsforclustersdenied="+str(reqsForClustersDenied)+" " \
                            " and reqsformbufsplusclustersdenied="+str(reqsForMbufsPlusClustersDenied)+" " \
                            " order by collector_time"
        #print self.command_query

    def build_ch_alarm_query(self, ch_alarm_data):
        chassisname = ch_alarm_data.get('chassisname', "NULL")
        alarm_class = ch_alarm_data.get('alarm_class', "NULL")
        alarm_text = ch_alarm_data.get('alarm_description', "NULL")
        alarm_time = ch_alarm_data.get('alarm_time', "NULL")
        self.command_query = ""
        self.command_query =" and chassisname"+str(" is NULL" if chassisname=="NULL" else "='"+str(chassisname)+"'" )+" \
                            and alarmclass"+str(" is NULL" if alarm_class=="NULL" else "='"+str(alarm_class)+"'" )+" \
                            and alarmtext"+str(" is NULL" if alarm_text=="NULL" else "='"+str(alarm_text)+"'" )+" \
                            and alarmtime"+str(" is NULL" if alarm_time=="NULL" else "='"+str(alarm_time)+"'" )+" order by collector_time"

    def build_fab_map_data_query(self, ch_fab_map_data):
        fabricmap = ch_fab_map_data.get('fabricmap', "NULL")
        mapstatus = ch_fab_map_data.get('mapstatus', "NULL")
        self.command_query = ""
        self.command_query =" and fabricmap='"+str(fabricmap)+"' and mapstatus='"+str(mapstatus)+"' order by collector_time"

    def build_ch_fab_sum_data_query(self, ch_fab_sum_data):
        plane = ch_fab_sum_data.get("plane","")
        state = ch_fab_sum_data.get("state","")
        uptime = ch_fab_sum_data.get("uptime","")
        self.command_query = ""
        self.command_query = " and plane="+str(plane)+" and state='"+str(state)+"' and uptime='"+str(uptime)+"' order by collector_time"

    def build_ch_fpc_pic_data_query(self, ch_fpc_pic_data):
        rename = ch_fpc_pic_data.get('chassisname', "NULL")
        slot = ch_fpc_pic_data.get('slot', "NULL")
        pic_state = ch_fpc_pic_data.get('pic_state', "NULL")
        pic_slot = ch_fpc_pic_data.get('pic_slot', "NULL")
        description = ch_fpc_pic_data.get('description', "NULL")
        pic = ch_fpc_pic_data.get('pic', "NULL")
        state = ch_fpc_pic_data.get('state', "NULL")
        pic_type = ch_fpc_pic_data.get('pic_type', "NULL")
        self.command_query = ""
        self.command_query =" and `rename`"+str(" is NULL" if rename=="NULL" else "='"+str(rename)+"'" )+" \
                            and fpcslot"+str(" is NULL" if slot=="NULL" else "='"+str(slot)+"'" )+" \
                            and picstate"+str(" is NULL" if pic_state=="NULL" else "='"+str(pic_state)+"'" )+" \
                            and picslot"+str(" is NULL" if pic_slot=="NULL" else "='"+str(pic_slot)+"'" )+" \
                            and fpcdesc"+str(" is NULL" if description=="NULL" else "='"+str(description)+"'" )+" \
                            and picstate"+str(" is NULL" if state=="NULL" else "='"+str(state)+"'" )+" \
                            and pictype"+str(" is NULL" if pic_type=="NULL" else "='"+str(pic_type)+"'" )+" \
                            order by collector_time"

    def build_ch_hard_data_query(self, k):
        parttype = ""
        self.command_query = ""
        q = ""
        m = re.match(r'([\S|\s]+)(\d)$', str(self.ch_hard_data[k]["item"]), re.M | re.I)
        if m:
            #print m.groups()
            parttype = m.groups()[0].strip()
            if len(parttype.split(" "))>1:
                parttype = parttype.split(" ")[1]
            slot = m.groups()[1]
            if parttype=="PIC":
                q = "and slot is NULL and pic_slot="+str(slot)+""
            else:
                q = "and slot="+str(slot)+" and pic_slot is NULL"
            if parttype=="Xcvr":
                parttype = parttype.upper()
                q = "and slot is NULL and pic_slot is NULL and sfp_slot="+str(slot)+""
        else:
            parttype = k
            slot = "NULL"
            q = "and slot is "+str(slot)+""
        q = q + " and partrev='"+str(self.ch_hard_data[k]["version"].upper().strip())+"' \
            and partasnum='"+str(self.ch_hard_data[k]["part_number"]).strip()+"' " \
            "and partserial='"+str(self.ch_hard_data[k]["serial_number"]).strip()+"' \
             and partdesc='"+str(self.ch_hard_data[k]["description"]).strip()+"'"
        self.command_query = q

    def build_env_data_query(self, env_data):
        tempc = ""
        chassispartstatus = env_data.get('status','')
        chassisname = env_data.get('chassisname','')
        chassispart = env_data.get('chassispart', '')

        self.command_query = ""
        m = re.match(r'(\d+).*', env_data['measurement'].strip(), re.I | re.M)
        if m:
            #print "hi"
            tempc = m.groups(0)[0]
            self.command_query = " and chassispartstatus='"+str(chassispartstatus)+"' and \
            chassispart='"+str(chassispart)+"' and chassisname='"+str(chassisname)+"' \
            and tempc='"+str(tempc)+"'"

    def build_eth_sw_err_age_msg_data_query(self, eth_sw_err_age_msg_data):
        erroragemessages = eth_sw_err_age_msg_data.get('erroragemessages', 0)
        self.command_query = ""
        self.command_query = " and erroragemessages="+str(erroragemessages)+""

    def build_eth_sw_stat_maclrnerr_data_query(self, eth_sw_stat_maclrnerr_data):
        learnerrors = eth_sw_stat_maclrnerr_data.get('learnerrors', 0)
        self.command_query = ""
        self.command_query = " and learnerrors="+str(learnerrors)+""

    def build_eth_sw_tbl_summ_data_query(self, eth_sw_tbl_summ_data):
        totalentries = eth_sw_tbl_summ_data.get('totalentries', 0)
        self.command_query = ""
        self.command_query = " and totalentries="+str(totalentries)+""

    def build_stp_stats_data_query(self, stp_stats_data):
        numberoftopologychanges = stp_stats_data.get('numberoftopologychanges', 0)
        timesincelasttopologychange = stp_stats_data.get('timesincelasttopologychange', 0)
        self.command_query = ""
        self.command_query = " and numberoftopologychanges="+str(numberoftopologychanges)+" and timesincelasttopologychange="+str(timesincelasttopologychange)+""

    def build_fan_data_query(self, fan_data):
        chassisname = fan_data.get("chassisname", "").strip()
        fanloc = fan_data.get("fanloc", "").strip()
        fanstatus = fan_data.get("fanstatus", "").strip()
        fanspeed = fan_data.get("fanspeed", "").strip()
        self.command_query = ""
        self.command_query = " and chassisname='"+chassisname+"' and fanloc='"+str(fanloc)+"' and \
            fanstatus='"+str(fanstatus)+"' and fanspeed='"+str(fanspeed)+"' order by collector_time"

    def build_fpc_data_query(self, fpc_data):
        slot = fpc_data.get('slot', 0)
        cpu_int = fpc_data.get('cpu_interrupt', 0)
        cpu_total = fpc_data.get("cpu_total", 0)
        tempc = fpc_data.get('temperature', 0)
        state = fpc_data.get('state', "")
        mem_heap = fpc_data.get('memory_dram_size', 0)
        mem_buffer = fpc_data.get('memory_buffer_utilization', 0)
        mem_heap = fpc_data.get('memory_heap_utilization', 0)
        self.command_query = ""

        self.command_query =" and slot="+str(slot)+" and cpu_int="+str(cpu_int)+" and cputotal="+str(cpu_total)+" and \
                            tempc="+str(tempc)+" and state='"+str(state)+"' and mem_heap="+str(mem_heap)+" and \
                            mem_buffer="+str(mem_buffer)+" order by collector_time"

    def build_ipsec_stats_data_query(self, ipsec_stats_data):
        chassisname = ipsec_stats_data.get('chassisname', "NULL")
        ah_authentication_failures = ipsec_stats_data.get('ah_authentication_failures', "NULL")
        esp_authentication_failures = ipsec_stats_data.get('esp_authentication_failures', "NULL")
        esp_decryption_failures = ipsec_stats_data.get('esp_decryption_failures', "NULL")
        bad_headers = ipsec_stats_data.get('bad_headers', "NULL")
        bad_trailers = ipsec_stats_data.get('bad_trailers', "NULL")
        replay_errors = ipsec_stats_data.get('replay_errors', "NULL")
        self.command_query = ""
        self.command_query =" and `rename`"+str(" is NULL" if chassisname=="NULL" else "='"+str(chassisname)+"'" )+" \
                            and ah_authentication_failures"+str(" is NULL" if ah_authentication_failures=="NULL" else "='"+str(ah_authentication_failures)+"'" )+" \
                            and esp_authentication_failures"+str(" is NULL" if esp_authentication_failures=="NULL" else "='"+str(esp_authentication_failures)+"'" )+" \
                            and esp_decryption_failures"+str(" is NULL" if esp_decryption_failures=="NULL" else "='"+str(esp_decryption_failures)+"'" )+" \
                            and bad_headers"+str(" is NULL" if bad_headers=="NULL" else "='"+str(bad_headers)+"'" )+" \
                            and bad_trailers"+str(" is NULL" if bad_trailers=="NULL" else "='"+str(bad_trailers)+"'" )+" \
                            and replay_errors"+str(" is NULL" if replay_errors=="NULL" else "='"+str(replay_errors)+"'" )+" \
                            order by collector_time"

    def build_krt_q_query(self, krt_q):
        routetbladd = krt_q.get("Routing table add queue", 0)
        indadddelchange = krt_q.get("Interface add/delete/change queue", 0)
        indirectnhaddchange = krt_q.get("Indirect next hop add/change", 0)
        mplsadd = krt_q.get("MPLS add queue", 0)
        indirectnhdel = krt_q.get("Indirect next hop delete", 0)
        highpridel = krt_q.get("High-priority deletion queue", 0)
        highprichange = krt_q.get("High-priority change queue", 0)
        highpriadd = krt_q.get("High-priority add queue", 0)
        tnormalpriindnh = krt_q.get("Normal-priority indirect next hop queue", 0)
        normalpridel = krt_q.get("Normal-priority deletion queue", 0)
        normalpricompnhdel = krt_q.get("Normal-priority composite next hop deletion queue", 0)
        normalprichange = krt_q.get("Normal-priority change queue", 0)
        normalpriadd = krt_q.get("Normal-priority add queue", 0)
        routingtbldel = krt_q.get("Routing table delete queue", 0)
        self.command_query = ""
        self.command_query = " and routetbladd="+str(routetbladd)+" and \
            indadddelchange="+str(indadddelchange)+" and mplsadd="+str(mplsadd)+" and \
            mplsadd="+str(mplsadd)+" and indirectnhdel="+str(indirectnhdel)+" and \
            highpridel="+str(highpridel)+" and highprichange="+str(highprichange)+" and \
            highpriadd="+str(highpriadd)+" and tnormalpriindnh="+str(tnormalpriindnh)+" and \
            normalpridel="+str(normalpridel)+" and normalpricompnhdel="+str(normalpricompnhdel)+" and \
            normalprichange="+str(normalprichange)+" and normalpriadd="+str(normalpriadd)+" and \
            routingtbldel="+str(routingtbldel)+" \
            order by collector_time"

    def build_krt_st_query(self, krt_st):
        installjob = krt_st.get("Install Job is", "")
        numOpsQueued = krt_st.get("Number of operations queued", 0)
        rteTableAdds = krt_st.get("Routing table adds", 0)
        intfRoutes = krt_st.get("Interface routes", 0)
        indNhAddsChanges = krt_st.get("Indirect Next Hop Adds/Changes", 0)[0]
        indNhDeletes = krt_st.get("Indirect Next Hop Adds/Changes", 0)[1]
        mplsAdds = krt_st.get("MPLS Adds", 0)[0]
        highPriAdds = krt_st.get("High pri Adds", 0)[0]
        highPriChanges = krt_st.get("High pri Adds", 0)[1]
        highPriDeletes = krt_st.get("High pri Adds", 0)[2]
        normalPriIndirects = krt_st.get("Normal pri Indirects", 0)
        normalPriAdds = krt_st.get("Normal pri Adds", 0)[0]
        normalPriChanges = krt_st.get("Normal pri Adds", 0)[1]
        normalPriDeletes = krt_st.get("Normal pri Adds", 0)[2]
        rteTableDeletes = krt_st.get("Routing Table deletes", 0)
        numOpsDeferred = krt_st.get("Number of operations deferred", 0)
        numOpsCanceled = krt_st.get("Number of operations canceled", 0)
        timeUntilNxtQueRun = krt_st.get("Time until next queue run", 0)
        rtesLrndFrmKernel = krt_st.get("Routes learned from kernel", 0)
        rtngSktTimeUntlNextScan = krt_st.get("Time until next scan", 0)
        self.command_query = ""
        self.command_query = " and installjob='"+installjob+"' and numopsqueued="+str(numOpsQueued)+" and \
                            rteTableAdds="+str(rteTableAdds)+" and intfroutes="+str(intfRoutes)+" and \
                            indnhaddschanges="+str(indNhAddsChanges)+" and indnhdeletes="+str(indNhDeletes)+" and \
                            mplsadds="+str(mplsAdds)+" and highpriadds="+str(highPriAdds)+" and highpriadds="+str(highPriAdds)+" \
                            and highprichanges="+str(highPriChanges)+" and highprideletes="+str(highPriDeletes)+" \
                            and normalpriindirects="+str(normalPriIndirects)+" and normalprichanges="+str(normalPriChanges)+" \
                            and normalpriadds="+str(normalPriAdds)+" and normalprideletes="+str(normalPriDeletes)+" and \
                            rteTableDeletes="+str(rteTableDeletes)+" and numopsdeferred="+str(numOpsDeferred)+" and \
                            numopscanceled="+str(numOpsCanceled)+" and timeuntilnxtquerun="+str(timeUntilNxtQueRun)+" and \
                            rteslrndfrmkernel="+str(rtesLrndFrmKernel)+" and rtngskttimeuntlnextscan="+str(rtngSktTimeUntlNextScan)+" \
                            order by collector_time"

    def build_mpc_jnh_summ_data_query(self, mpc_jnh_summ_data):
        print json.dumps(mpc_jnh_summ_data, indent=4)
        self.command_query = ""

    def build_nhdb_zones_query(self, nhdb_zones):
        device = nhdb_zones.get("device","")
        state = nhdb_zones.get("devicenum","")
        nhdbchip = nhdb_zones.get("nhdbchip","")
        nhdbstart = nhdb_zones.get("nhdbstart","")
        nhdbsize1 = nhdb_zones.get("nhdbsize1","")
        nhdbrsvd = nhdb_zones.get("nhdbrsvd","")
        nhdbused = nhdb_zones.get("nhdbused","")
        nhdbhiwater = nhdb_zones.get("nhdbhiwater","")
        nhdbtotal = nhdb_zones.get("nhdbtotal","")
        nhdbsize2 = nhdb_zones.get("nhdbsize2","")
        nhdbname = nhdb_zones.get("nhdbname","")
        self.command_query = ""
        
        query = " order by collector_time"

    def build_pfe_st_notif_data_query(self, pfe_st_notif_data):
        print json.dumps(pfe_st_notif_data, indent=4)
        discard_failed = pfe_st_notif_data.get("discard_failed", 0)
        dontfrag_failed = pfe_st_notif_data.get("dontfrag_failed", 0)
        illegal = pfe_st_notif_data.get("illegal", 0)
        sample_failed = pfe_st_notif_data.get("sample_failed", 0)
        option_failed = pfe_st_notif_data.get("option_failed", 0)
        nexthop_failed = pfe_st_notif_data.get("nexthop_failed", 0)
        illegal_failed = pfe_st_notif_data.get("illegal_failed", 0)
        poison_failed = pfe_st_notif_data.get("poison_failed", 0)
        dma_failure = pfe_st_notif_data.get("dma_failure", 0)
        redirect_failed = pfe_st_notif_data.get("redirect_failed", 0)
        cfdf_failed = pfe_st_notif_data.get("cfdf_failed", 0)
        reject_failed = pfe_st_notif_data.get("reject_failed", 0)
        unclass_failed = pfe_st_notif_data.get("unclass_failed", 0)
        mempkt_failed = pfe_st_notif_data.get("mempkt_failed", 0)
        autoconf_failed = pfe_st_notif_data.get("autoconf_failed", 0)
        self.command_query = ""
        self.command_query = " and discard_failed="+str(discard_failed)+" and dontfrag_failed="+str(dontfrag_failed)+" \
                            and illegal="+str(illegal)+" and sample_failed="+str(sample_failed)+" and \
                            option_failed="+str(option_failed)+" and nexthop_failed="+str(nexthop_failed)+" and \
                            illegal_failed="+str(illegal_failed)+" and poison_failed="+str(poison_failed)+" and \
                            dma_failure="+str(dma_failure)+" and redirect_failed="+str(redirect_failed)+" and \
                            cfdf_failed="+str(cfdf_failed)+" and reject_failed="+str(reject_failed)+" and \
                            unclass_failed="+str(unclass_failed)+" and mempkt_failed="+str(mempkt_failed)+" \
                            and autoconf_failed="+str(autoconf_failed)+""

    def build_pfe_tr_data_query(self, pfe_tr_data):
        inputpackets = pfe_tr_data.get("Input  packets", 0)
        inputpps = pfe_tr_data.get("Input  packets PPS", 0)
        outputpackets = pfe_tr_data.get("Output packets", 0)
        outputpps = pfe_tr_data.get("Output packets PPS", 0)
        localpacketsinput = pfe_tr_data.get("Local packets input", 0)
        localpacketsoutput = pfe_tr_data.get("Local packets output", 0)
        swinputctlplanedrops = pfe_tr_data.get("Software input control plane drops", 0)
        swinputhighdrops = pfe_tr_data.get("Software input high drops", 0)
        swinputmediumdrops = pfe_tr_data.get("Software input medium drops", 0)
        swinputlowdrops = pfe_tr_data.get("Software input low drops", 0)
        swoutputdrops = pfe_tr_data.get("Software output drops", 0)
        hwinputdrops = pfe_tr_data.get("Hardware input drops", 0)
        normaldiscard = pfe_tr_data.get("Normal discard", 0)
        extendeddiscard = pfe_tr_data.get("Extended discard", 0)
        invalidinterface = pfe_tr_data.get("Invalid interface", 0)
        infocelldrops = pfe_tr_data.get("Info cell drops", 0)
        fabricdrops = pfe_tr_data.get("Fabric drops", 0)
        timeout = pfe_tr_data.get("Timeout", 0)
        truncatedkey = pfe_tr_data.get("Truncated key", 0)
        bitstotest = pfe_tr_data.get("Bits to test", 0)
        dataerror = pfe_tr_data.get("Data error", 0)
        stackunderflow = pfe_tr_data.get("Stack underflow", 0)
        stackoverflow = pfe_tr_data.get("Stack overflow", 0)
        hdlckeepalives = pfe_tr_data.get("HDLC keepalives", 0)
        atmoam = pfe_tr_data.get("ATM OAM", 0)
        frlmi = pfe_tr_data.get("Frame Relay LMI", 0)
        ppplcpncp = pfe_tr_data.get("PPP LCP/NCP", 0)
        ospfhello = pfe_tr_data.get("OSPF hello", 0)
        ospf3hello = pfe_tr_data.get("OSPF3 hello", 0)
        rsvphello = pfe_tr_data.get("RSVP hello", 0)
        ldphello = pfe_tr_data.get("LDP hello", 0)
        bfd = pfe_tr_data.get("BFD", 0)
        isisiih = pfe_tr_data.get("IS-IS IIH", 0)
        lacp = pfe_tr_data.get("LACP", 0)
        arp = pfe_tr_data.get("ARP", 0)
        etheroam = pfe_tr_data.get("ETHER OAM", 0)
        unknown = pfe_tr_data.get("Unknown", 0)
        mtuerrorinputchksm = pfe_tr_data.get("Input Checksum", 0)
        mtuerroroutputmtu = pfe_tr_data.get("Output MTU", 0)

        self.command_query = ""

        self.command_query = " and inputpackets="+str(inputpackets)+" and inputpps="+str(inputpps)+"  and outputpackets="+str(outputpackets)+"  \
                            and outputpps="+str(outputpps)+"  and localpacketsinput="+str(localpacketsinput)+"  and \
                            localpacketsoutput="+str(localpacketsoutput)+"  and swinputctlplanedrops="+str(swinputctlplanedrops)+"  \
                            and swinputhighdrops="+str(swinputhighdrops)+"  and swinputhighdrops="+str(swinputhighdrops)+"  and \
                            swinputmediumdrops="+str(swinputmediumdrops)+"  and swinputlowdrops="+str(swinputlowdrops)+"  and \
                            swoutputdrops="+str(swoutputdrops)+"  and hwinputdrops="+str(hwinputdrops)+"  and normaldiscard="+str(normaldiscard)+"  \
                            and extendeddiscard="+str(extendeddiscard)+"  and invalidinterface="+str(invalidinterface)+" \
                            and infocelldrops="+str(infocelldrops)+"  and fabricdrops="+str(fabricdrops)+"  and timeout="+str(timeout)+" \
                            and truncatedkey="+str(truncatedkey)+"  and bitstotest="+str(bitstotest)+"  and dataerror="+str(dataerror)+" \
                            and stackunderflow="+str(stackunderflow)+"  and stackoverflow="+str(stackoverflow)+"  and hdlckeepalives="+str(hdlckeepalives)+" \
                            and atmoam="+str(atmoam)+"  and frlmi="+str(frlmi)+"  and ppplcpncp="+str(ppplcpncp)+"  and ospfhello="+str(ospfhello)+"  \
                            and ospf3hello="+str(ospf3hello)+"  and rsvphello="+str(rsvphello)+"  and ldphello="+str(ldphello)+"  \
                            and bfd="+str(bfd)+"  and isisiih="+str(isisiih)+"  and lacp="+str(lacp)+"  and arp="+str(arp)+" \
                            and etheroam="+str(etheroam)+"  and unknown="+str(unknown)+"  and mtuerrorinputchksm="+str(mtuerrorinputchksm)+" \
                            and mtuerroroutputmtu="+str(mtuerroroutputmtu)+" order by collector_time"

    def build_proc_mem_data_query(self, proc_mem_data):
        #print json.dumps(proc_mem_data, indent=4)
        chassisname = proc_mem_data.get("chassisname", "NULL")
        activemem = proc_mem_data.get("activemem","")
        inactmem = proc_mem_data.get("inactmem","")
        wiredmem = proc_mem_data.get("wiredmem","")
        cachemem = proc_mem_data.get("cachemem","")
        bufmem = proc_mem_data.get("bufmem","")
        freemem = proc_mem_data.get("freemem","")
        usedmem = proc_mem_data.get("usedmem","")
        totalmem = proc_mem_data.get("totalmem","")
        usedmempercentage = proc_mem_data.get("usedmempercentage","")
        swap_total = proc_mem_data.get("swap_total", 0)
        swap_free = proc_mem_data.get("swap_free", 0)
        self.command_query = ""
        if chassisname=="" or chassisname=="NULL":
            self.command_query = " and chassisname is NULL and activemem='"+str(activemem)+"' and \
                inactmem='"+str(inactmem)+"' and wiredmem='"+str(wiredmem)+"' and  \
                cachemem='"+str(cachemem)+"' and bufmem='"+str(bufmem)+"' and  freemem='"+str(freemem)+"' and  \
                swap_total='"+str(swap_total)+"' and swap_free='"+str(swap_free)+"' and  \
                usedmem="+str(usedmem)+" and totalmem="+str(totalmem)+" and \
                usedmempercentage="+str(usedmempercentage)+" order by collector_time"
        else:
            self.command_query = " and chassisname='"+chassisname+"' and activemem='"+str(activemem)+"' and \
                inactmem='"+str(inactmem)+"' and wiredmem='"+str(wiredmem)+"' and  \
                cachemem='"+str(cachemem)+"' and bufmem='"+str(bufmem)+"' and  freemem='"+str(freemem)+"' and  \
                swap_total='"+str(swap_total)+"' and swap_free='"+str(swap_free)+"' and  \
                usedmem="+str(usedmem)+" and totalmem="+str(totalmem)+" and \
                usedmempercentage="+str(usedmempercentage)+" order by collector_time"


    def build_ps_data_query(self, ps_data):
        chassisname = ps_data.get("chassisname","")
        pid = ps_data.get("pid","")
        username = ps_data.get("username","")
        thr = ps_data.get("thr","")
        pri = ps_data.get("pri","")
        nice = ps_data.get("nice","")
        size = ps_data.get("size","")
        if size[-1:]=='K':
            size = size[:-1]
            size = int(size) * 1000
        elif size[-1:]=='M':
            size = size[:-1]
            size = int(size) * 1000 * 1000
        res = ps_data.get("res","")
        if res[-1:]=='K':
            res = res[:-1]
            res = int(res) * 1000
        elif res[-1:]=='M':
            res = res[:-1]
            res = int(res) * 1000 * 1000
        state = ps_data.get("state","")
        time = ps_data.get("time","")
        wcpu = ps_data.get("wcpu","")
        command = ps_data.get("command","")
        self.command_query = ""
        m = re.match(r'(chassisd)|(dfwd)|(mib2d)|(pfed)|(rpd)|(sampled)|(snmpd)|(dswd)|(dcd)|(cosd)|(mgd)|(ksyncd)|(ppmd)|(rtspd)|(l2ald)', command.strip(), re.M | re.I)
        result_set = ""
        query_status = 0
        self.command_query = ""
        if m:
            #print m.groups()
            self.command_query = " and pid="+str(pid)+" and \
                username='"+str(username)+"' and thr="+str(thr)+" and pri="+str(pri)+" and \
                nice="+str(nice)+" and size='"+str(size)+"' and res='"+str(res)+"' and state='"+str(state)+"' and time='"+str(time)+"' and \
                wcpu="+str(wcpu)+" and command='"+str(command)+"' order by collector_time"

    def build_pwr_data_query(self, pwr_data):
        chassisname = pwr_data.get("chassisname", "NULL").strip()
        powersupply = pwr_data.get("item","").strip()
        status = pwr_data.get("status","").strip()
        self.command_query = ""
        if chassisname == "NULL":
            self.command_query = " and powersupply='"+str(powersupply)+"' and \
            status='"+str(status)+"' and chassisname is NULL order by collector_time"
        else:
            self.command_query = " and powersupply='"+str(powersupply)+"' and \
            status='"+str(status)+"' and chassisname='"+str(chassisname)+"' order by collector_time"

    def build_re_data_query(self, re_data):
        self.command_query = ""
        tmp = ""
        rename = re_data.get('rename', "")
        slot = re_data.get('slot', "NULL")
        if slot=="NULL":
            tmp += " and slot is NULL "
        else:
            tmp += " and slot=" + str(slot) + ""

        cpu_system = re_data.get('cpu_system', 0)
        tmp += " and cpu_system="+str(cpu_system)+""
        cpu_interrupt = re_data.get('cpu_interrupt', 0)
        tmp += " and cpu_interrupt="+str(cpu_interrupt)+""
        cpu_idle = re_data.get('cpu_idle', 0)
        tmp += " and cpu_idle="+str(cpu_idle)+""
        cpu_user = re_data.get('cpu_user', 0)
        tmp += " and cpu_user="+str(cpu_user)+""
        cpu_background = re_data.get('cpu_background', 0)
        tmp += " and cpu_background="+str(cpu_background)+""
        model = re_data.get('model', "NULL")
        if model=="NULL":
            tmp += " and model is NULL "
        else:
            tmp += " and model='"+str(model)+"' "
        serial_number = re_data.get('serial_number', "NULL")
        if serial_number=="NULL":
            tmp += " and serial_number is NULL "
        else:
            tmp += " and serial_number='"+str(serial_number)+"' "
        start_time = re_data.get('start_time', "NULL")
        if start_time=="NULL":
            tmp += " and start_time is NULL "
        else:
            tmp += " and start_time='"+str(start_time)+"' "
        up_time = re_data.get('up_time', "NULL")
        if up_time=="NULL":
            tmp += " and up_time is NULL "
        else:
            tmp += " and up_time='"+str(up_time)+"' "
        load_average_one = re_data.get('load_average_one', "NULL")
        if load_average_one=="NULL":
            tmp += " and load_average_one is NULL "
        else:
            tmp += " and load_average_one='"+str(load_average_one)+"' "
        load_average_five = re_data.get('load_average_five', "NULL")
        if load_average_five=="NULL":
            tmp += " and load_average_five is NULL "
        else:
            tmp += " and load_average_five='"+str(load_average_five)+"' "
        load_average_fifteen = re_data.get('load_average_fifteen', "NULL")
        if load_average_fifteen=="NULL":
            tmp += " and load_average_fifteen is NULL "
        else:
            tmp += " and load_average_fifteen='"+str(load_average_fifteen)+"' "
        mastership_priority = re_data.get('mastership_priority', "NULL")
        if mastership_priority=="NULL":
            tmp += " and mastership_priority is NULL "
        else:
            tmp += " and mastership_priority='"+str(mastership_priority)+"' "
        status1 = re_data.get('status', "NULL")
        if status1=="NULL":
            tmp += " and status is NULL "
        else:
            tmp += " and status='"+str(status1)+"' "
        temperature = re_data.get('temperature', "NULL")
        if temperature=="NULL":
            tmp += " and temperature is NULL "
        else:
            tmp += " and temperature='"+str(temperature)+"' "
        cpu_temperature = re_data.get('cpu_temperature', "NULL")
        if cpu_temperature=="NULL":
            tmp += " and cpu_temperature is NULL "
        else:
            tmp += " and cpu_temperature='"+str(cpu_temperature)+"' "
        memory_dram_size = re_data.get('memory_dram_size', "NULL")
        if memory_dram_size=="NULL":
            tmp += " and memory_dram_size is NULL "
        else:
            tmp += " and memory_dram_size="+str(memory_dram_size)+" "
        memory_buffer_utilization = re_data.get('memory_buffer_utilization', 0)
        tmp += " and memory_buffer_utilization="+str(memory_buffer_utilization)+""
        mastershipstate = re_data.get('mastership_state', "NULL")
        if mastershipstate=="NULL":
            tmp += " and mastershipstate is NULL "
        else:
            tmp += " and mastershipstate='"+str(mastershipstate)+"' "
        totalcpu = int(cpu_user) + int(cpu_background) + int(cpu_system)
        tmp += " and totalcpu="+str(totalcpu)+""

        self.command_query = tmp + " order by collector_time"
        #print self.command_query

    def build_rt_sum_data_query(self, rt_sum_data):
        routetable = rt_sum_data.get("routetable", "NULL")
        destinations = rt_sum_data.get("destinations", 0)
        routes = rt_sum_data.get("routes", 0)
        active = rt_sum_data.get("active", 0)
        holddown = rt_sum_data.get("holddown", 0)
        hidden = rt_sum_data.get("hidden", 0)
        self.command_query = ""
        self.command_query = " and routetable='"+str(routetable)+"' and \
                destinations="+str(destinations)+" and routes="+str(routes)+" and \
                active="+str(active)+" and \
                holddown="+str(holddown)+" and hidden="+str(hidden)+" \
                order by collector_time"

    def build_sec_alg_st_data_query(self, sec_alg_st_data):
        alg_rtsp_status = sec_alg_st_data.get('alg_rtsp_status', "")
        alg_pptp_status = sec_alg_st_data.get('alg_pptp_status', "NULL")
        alg_sip_status = sec_alg_st_data.get('alg_sip_status', "NULL")
        alg_rsh_status = sec_alg_st_data.get('alg_rsh_status', "NULL")
        alg_sunrpc_status = sec_alg_st_data.get('alg_sunrpc_status', "NULL")
        alg_dns_status = sec_alg_st_data.get('alg_dns_status', "NULL")
        alg_h323_status = sec_alg_st_data.get('alg_h323_status', "NULL")
        alg_sccp_status = sec_alg_st_data.get('alg_sccp_status', "NULL")
        alg_msrpc_status = sec_alg_st_data.get('alg_msrpc_status', "NULL")
        alg_talk_status = sec_alg_st_data.get('alg_talk_status', "NULL")
        alg_ftp_status = sec_alg_st_data.get('alg_ftp_status', "NULL")
        alg_sql_status = sec_alg_st_data.get('alg_sql_status', "NULL")
        #alg_ike_esp_nat_status = sec_alg_st_data.get('alg_ike_esp_nat_status', "NULL")
        alg_mgcp_status = sec_alg_st_data.get('alg_mgcp_status', "NULL")
        alg_tftp_status = sec_alg_st_data.get('alg_tftp_status', "NULL")
        self.command_query = ""
        self.command_query =" and alg_rtsp_status"+str(" is NULL" if alg_rtsp_status=="NULL" else "='"+str(alg_rtsp_status)+"'" )+" \
                            and alg_pptp_status"+str(" is NULL" if alg_pptp_status=="NULL" else "='"+str(alg_pptp_status)+"'" )+" \
                            and alg_sip_status"+str(" is NULL" if alg_sip_status=="NULL" else "='"+str(alg_sip_status)+"'" )+" \
                            and alg_rsh_status"+str(" is NULL" if alg_rsh_status=="NULL" else "='"+str(alg_rsh_status)+"'" )+" \
                            and alg_sunrpc_status"+str(" is NULL" if alg_sunrpc_status=="NULL" else "='"+str(alg_sunrpc_status)+"'" )+" \
                            and alg_dns_status"+str(" is NULL" if alg_dns_status=="NULL" else "='"+str(alg_dns_status)+"'" )+" \
                            and alg_h323_status"+str(" is NULL" if alg_h323_status=="NULL" else "='"+str(alg_h323_status)+"'" )+" \
                            and alg_sccp_status"+str(" is NULL" if alg_sccp_status=="NULL" else "='"+str(alg_sccp_status)+"'" )+" \
                            and alg_msrpc_status"+str(" is NULL" if alg_msrpc_status=="NULL" else "='"+str(alg_msrpc_status)+"'" )+" \
                            and alg_talk_status"+str(" is NULL" if alg_talk_status=="NULL" else "='"+str(alg_talk_status)+"'" )+" \
                            and alg_ftp_status"+str(" is NULL" if alg_ftp_status=="NULL" else "='"+str(alg_ftp_status)+"'" )+" \
                            and alg_sql_status"+str(" is NULL" if alg_sql_status=="NULL" else "='"+str(alg_sql_status)+"'" )+" \
                            and alg_mgcp_status"+str(" is NULL" if alg_mgcp_status=="NULL" else "='"+str(alg_mgcp_status)+"'" )+" \
                            and alg_tftp_status"+str(" is NULL" if alg_tftp_status=="NULL" else "='"+str(alg_tftp_status)+"'" )+" \
                            order by collector_time"

    def build_sec_nat_intf_nat_prts_data_query(self, sec_nat_intf_nat_prts_data):
        rename = sec_nat_intf_nat_prts_data.get('rename', "")
        pool_index = sec_nat_intf_nat_prts_data.get('pool_index', "NULL")
        single_ports_available = sec_nat_intf_nat_prts_data.get('single_ports_available', "NULL")
        self.command_query = ""
        self.command_query =" and `rename`"+str(" is NULL" if rename=="" else "='"+str(rename)+"'" )+" \
                            and pool_index"+str(" is NULL" if pool_index=="NULL" else "='"+str(pool_index)+"'" )+" \
                            and single_ports_available"+str(" is NULL" if single_ports_available=="NULL" else "='"+str(single_ports_available)+"'" )+" \
                            order by collector_time"

    def build_sec_utm_aspam_stats_data_query(self, sec_utm_aspam_stats_data):
        dns_errors = sec_utm_aspam_stats_data.get('dns_errors', "NULL")
        timeout_errors = sec_utm_aspam_stats_data.get('timeout_errors', "NULL")
        return_errors = sec_utm_aspam_stats_data.get('return_errors', "NULL")
        invalid_parameter_errors = sec_utm_aspam_stats_data.get('invalid_parameter_errors', "NULL")
        self.command_query = ""
        self.command_query =" and dns_errors"+str(" is NULL" if dns_errors=="NULL" else "='"+str(dns_errors)+"'" )+" \
                            and timeout_errors"+str(" is NULL" if timeout_errors=="NULL" else "='"+str(timeout_errors)+"'" )+" \
                            and return_errors"+str(" is NULL" if return_errors=="NULL" else "='"+str(return_errors)+"'" )+" \
                            and invalid_parameter_errors"+str(" is NULL" if invalid_parameter_errors=="NULL" else "='"+str(invalid_parameter_errors)+"'" )+" \
                            order by collector_time"

    def build_sec_utm_av_st_data_query(self, sec_utm_av_st_data):
        anti_virus_signature_version = sec_utm_av_st_data.get('anti_virus_signature_version', "")
        self.command_query = ""
        self.command_query =" and anti_virus_signature_version"+str(" is NULL" if anti_virus_signature_version=="" else "='"+str(anti_virus_signature_version)+"'" )+" \
                            order by collector_time"

    def build_sec_utm_av_stats_data_query(self, sec_utm_av_stats_data):
        out_of_resource_log_and_permit = sec_utm_av_stats_data.get('out_of_resource_log_and_permit', "")
        out_of_resource_block = sec_utm_av_stats_data.get('out_of_resource_block', "NULL")
        timeout_log_and_permit = sec_utm_av_stats_data.get('timeout_log_and_permit', "NULL")
        timeout_block = sec_utm_av_stats_data.get('timeout_block', "NULL")
        too_many_requests_log_and_permit = sec_utm_av_stats_data.get('too_many_requests_log_and_permit', "NULL")
        too_many_requests_block = sec_utm_av_stats_data.get('too_many_requests_block', "NULL")

        self.command_query = ""
        self.command_query =" and out_of_resource_log_and_permit"+str(" is NULL" if out_of_resource_log_and_permit=="" else "='"+str(out_of_resource_log_and_permit)+"'" )+" \
                            and out_of_resource_block"+str(" is NULL" if out_of_resource_block=="NULL" else "='"+str(out_of_resource_block)+"'" )+" \
                            and timeout_log_and_permit"+str(" is NULL" if timeout_log_and_permit=="NULL" else "='"+str(timeout_log_and_permit)+"'" )+" \
                            and timeout_block"+str(" is NULL" if timeout_block=="NULL" else "='"+str(timeout_block)+"'" )+" \
                            and too_many_requests_log_and_permit"+str(" is NULL" if too_many_requests_log_and_permit=="NULL" else "='"+str(too_many_requests_log_and_permit)+"'" )+" \
                            and too_many_requests_block"+str(" is NULL" if too_many_requests_block=="NULL" else "='"+str(too_many_requests_block)+"'" )+" \
                            order by collector_time"

    def build_sec_utm_st_data_query(self, sec_utm_st_data):
        utmd_status = sec_utm_st_data.get('running', "NULL")
        if utmd_status=="":
            utmd_status = "running"
        self.command_query = ""
        self.command_query =" and utmd_status"+str(" is NULL" if utmd_status=="NULL" else "='"+str(utmd_status)+"'" )+" \
                            order by collector_time"

    def build_sec_utm_web_st_data_query(self, sec_utm_web_st_data):
        web_filtering_server_status = sec_utm_web_st_data.get('web_filtering_server_status', "NULL")
        self.command_query = ""
        self.command_query =" and web_filtering_server_status"+str(" is NULL" if web_filtering_server_status=="" else "='"+str(web_filtering_server_status)+"'" )+" \
                            order by collector_time"

    def build_sec_utm_web_stat_data_query(self, sec_utm_web_stat_data):
        fallback_block_too_many_requests = sec_utm_web_stat_data.get('fallback_block_too_many_requests', "")
        self.command_query = ""
        self.command_query =" and fallback_block_too_many_requests"+str(" is NULL" if fallback_block_too_many_requests=="" else "='"+str(fallback_block_too_many_requests)+"'" )+" \
                            order by collector_time"

    def build_sh_mem_frag_data_query(self, sh_mem_frag_data):
        alloctype = sh_mem_frag_data[0].strip()
        pages_in_use = sh_mem_frag_data[1].strip()
        pages_needed = sh_mem_frag_data[2].strip()
        frag = sh_mem_frag_data[3].strip()
        self.command_query = ""
        self.command_query = " and alloctype='"+str(alloctype)+"' and frag="+str(frag)+" and pages_in_use="+str(pages_in_use)+" " \
                            "and pages_needed="+str(pages_needed)+" order by collector_time"


    def build_stp_stats_data_query(self, stp_stats_data):
        numberoftopologychanges = stp_stats_data.get('numberoftopologychanges', 0)
        timesincelasttopologychange = stp_stats_data.get('timesincelasttopologychange', 0)
        self.command_query = ""
        self.command_query = " and numberoftopologychanges="+str(numberoftopologychanges)+" and timesincelasttopologychange="+str(timesincelasttopologychange)+""


    def build_sys_cores_data_query(self, sys_cores_data):
        user = sys_cores_data.get("user","").strip()
        size = sys_cores_data.get("size",0)
        date = sys_cores_data.get("date","").strip()
        location = sys_cores_data.get("location","").strip()
        chassisname = sys_cores_data.get("chassisname","NULL").strip()
        self.command_query = ""
        if chassisname=="NULL":
            self.command_query = " and chassisname is NULL and `date`='"+str(date)+"' and `user`='"+user+"' " \
                                "and `size`="+str(size)+" and `location`='"+str(location)+"' order by collector_time"
        else:
            self.command_query = " and chassisname='"+str(chassisname)+"' and `date`='"+str(date)+"' and `user`='"+user+"' " \
                                "and `size`="+str(size)+" and `location`='"+str(location)+"' order by collector_time"

    def build_sys_license_data_query(self, sys_license_data):
        licensename = sys_license_data.get('name', "NULL")
        enddate = sys_license_data.get('end_date', "NULL")
        self.command_query = ""
        self.command_query =" and licensename"+str(" is NULL" if licensename=="NULL" else "='"+str(licensename)+"'" )+" \
                            and enddate"+str(" is NULL" if enddate=="NULL" else "='"+str(enddate)+"'" )+" order by collector_time"

    def build_sys_stats_data_query(self, sys_stats_data):
        chassisname = ""
        icmpratelimitdrops = 0
        icmp6ratelimitnotgen = 0
        deadnexthop = 0
        noroutedrop = 0
        routeralertoptions = 0
        ipfragdropduporspace = 0
        listenqoverflow = 0
        bucketoverflow = 0
        cacheoverflow = 0
        ipfragdropqueueoverflow = 0
        ipfragdropoverlimit = 0
        ipfragdropnobufs = 0
        ipfragdropratelimit = 0
        ipfragdropnoiflist = 0
        ipfragdropsrcintmismatch = 0
        iptrnstredroponmgmt = 0
        tcpsenddropautherror = 0
        tcprcvdropautherror = 0
        tcpdiscardbadchecksum = 0
        tcpdiscardbadheaderoffsetfid = 0
        tcpdiscardtooshort = 0
        tcpbadconnattempt = 0
        tcpdropconnembryonic = 0
        tcpdropconnrexmittimeout = 0
        tcpdropconnpersisttimeout = 0
        tcpdropconnkeepalive = 0
        tcpdrop = 0
        tcpdroprcvpktbadaddress = 0
        tcpdropoosinsufficientmemory = 0
        tcpdropsendpktsautherror = 0
        tcpdroprcvpktsautherror = 0
        tcptimeoutretransmit = 0
        tcptimeoutpersist = 0
        tcptimeoutkeepalive = 0
        arpdiscarded = 0
        arpdenied = 0
        ip6fragdropduporspace = 0
        ip6fragdroptimeout = 0
        ip6packetdropnobufs = 0
        ip6optpacketsdropratelimit = 0
        ip6packetdropsrcintmismatch = 0
        ip6packetdropbadprotocol = 0
        ip6trnstredroponmgmt = 0
        tnpdroprcvhello = 0
        tnpdroprcvfragments = 0
        udpfullsocbufs = 0
        for i in range(0, len(sys_stats_data)):
            ssd = sys_stats_data[i]
            for k, v in ssd.iteritems():
                #print k
                output = ssd[k]
                output = output.split("\n")
                if k=="icmp":
                    for line in output:
                        m = re.match(r"(sfc[0-9]+.*:|lcc[0-9]+.*:)", line, re.M | re.I)
                        if m:
                            chassisname = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+drops due to rate limit", line.strip(), re.M | re.I)
                        if m:
                            icmpratelimitdrops = m.groups(0)[0]
                elif k=="icmp6":
                    for line in output:
                        m = re.match(r"(sfc[0-9]+.*:|lcc[0-9]+.*:)", line, re.M | re.I)
                        if m:
                            chassisname = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+errors not generated because rate limitation", line.strip(), re.M | re.I)
                        if m:
                            icmp6ratelimitnotgen = m.groups(0)[0]
                elif k=="ip":
                    for line in output:
                        m = re.match(r"(sfc[0-9]+.*:|lcc[0-9]+.*:)", line, re.M | re.I)
                        if m:
                            chassisname = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+packets destined to dead next hop", line.strip(), re.M | re.I)
                        if m:
                            deadnexthop = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+output packets discarded due to no route", line.strip(), re.M | re.I)
                        if m:
                            noroutedrop = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+router alert options", line.strip(), re.M | re.I)
                        if m:
                            routeralertoptions = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+fragments dropped \(dup or out of space\)", line.strip(), re.M | re.I)
                        if m:
                            ipfragdropduporspace = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+fragments dropped \(queue overflow\)", line.strip(), re.M | re.I)
                        if m:
                            ipfragdropqueueoverflow = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\t+fragments dropped after timeout", line.strip(), re.M | re.I)
                        if m:
                            ipfragdroptimeout = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\t+fragments dropped due to over limit", line.strip(), re.M | re.I)
                        if m:
                            ipfragdropoverlimit = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\t+output packets dropped due to no bufs", line.strip(), re.M | re.I)
                        if m:
                            ipfragdropnobufs = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+option packets dropped due to rate limit", line.strip(), re.M | re.I)
                        if m:
                            ipfragdropratelimit = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+multicast packets dropped \(no iflist\)", line.strip(), re.M | re.I)
                        if m:
                            ipfragdropnoiflist = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+packets dropped \(src and int don't match\)", line.strip(), re.M | re.I)
                        if m:
                            ipfragdropsrcintmismatch = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+transit re packets dropped on mgmt i\/f/", line.strip(), re.M | re.I)
                        if m:
                            iptrnstredroponmgmt = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+send packets dropped by TCP due to auth errors", line.strip(), re.M | re.I)
                        if m:
                            tcpsenddropautherror = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+rcv packets dropped by TCP due to auth errors", line.strip(), re.M | re.I)
                        if m:
                            tcprcvdropautherror = m.groups(0)[0]
                elif k == "tcp":
                    for line in output:
                        m = re.match(r"(sfc[0-9]+.*:|lcc[0-9]+.*:)", line, re.M | re.I)
                        if m:
                            chassisname = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+listen queue overflows", line.strip(), re.M | re.I)
                        if m:
                            listenqoverflow = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+bucket overflow", line.strip(), re.M | re.I)
                        if m:
                            bucketoverflow = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+cache overflow", line.strip(), re.M | re.I)
                        if m:
                            cacheoverflow = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+send packets dropped by TCP due to auth errors", line.strip(), re.M | re.I)
                        if m:
                            tcpsenddropautherror = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+rcv packets dropped by TCP due to auth errors", line.strip(), re.M | re.I)
                        if m:
                            tcprcvdropautherror = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+discarded for bad checksums", line.strip(), re.M | re.I)
                        if m:
                            tcpdiscardbadchecksum = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+discarded for bad header offset fields", line.strip(), re.M | re.I)
                        if m:
                            tcpdiscardbadheaderoffsetfld = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+discarded because packet too short", line.strip(), re.M | re.I)
                        if m:
                            tcpdiscardtooshort = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+bad connection attempts", line.strip(), re.M | re.I)
                        if m:
                            tcpbadconnattempt = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+embryonic connection[s]?\s+dropped", line.strip(), re.M | re.I)
                        if m:
                            tcpdropconnembryonic = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+connections dropped by rexmit timeout", line.strip(), re.M | re.I)
                        if m:
                            tcpdropconnrexmittimeout = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+connections dropped by retransmit timeout", line.strip(), re.M | re.I)
                        if m:
                            tcpdropconnrexmittimeout = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+connections dropped by persist timeout", line.strip(), re.M | re.I)
                        if m:
                            tcpdropconnpersisttimeout = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+connections dropped by keepalive", line.strip(), re.M | re.I)
                        if m:
                            tcpdropconnkeepalive = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+dropped+", line.strip(), re.M | re.I)
                        if m:
                            tcpdrop = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+rcv packets dropped by TCP due to bad address", line.strip(), re.M | re.I)
                        if m:
                            tcpdroprcvpktbadaddress = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+out-of-sequence segment drops due to insufficient memory", line.strip(), re.M | re.I)
                        if m:
                            tcpdropoosinsufficientmemory = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+send packets dropped by TCP due to auth errors", line.strip(), re.M | re.I)
                        if m:
                            tcpdropsendpktsautherror = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+rcv packets dropped by TCP due to auth errors", line.strip(), re.M | re.I)
                        if m:
                            tcpdroprcvpktsautherror = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+retransmit timeouts", line.strip(), re.M | re.I)
                        if m:
                            tcptimeoutretransmit = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+persist timeouts", line.strip(), re.M | re.I)
                        if m:
                            tcptimeoutpersist = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+keepalive timeouts", line.strip(), re.M | re.I)
                        if m:
                            tcptimeoutkeepalive = m.groups(0)[0]
                elif k=="arp":
                    for line in output:
                        m = re.match(r"(sfc[0-9]+.*:|lcc[0-9]+.*:)", line, re.M | re.I)
                        if m:
                            chassisname = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+packets discarded waiting for resolution", line.strip(), re.M | re.I)
                        if m:
                            arpdiscarded = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+requests for memory denied", line.strip(), re.M | re.I)
                        if m:
                            arpdenied = m.groups(0)[0]
                elif k=="udp":
                    for line in output:
                        m = re.match(r"(sfc[0-9]+.*:|lcc[0-9]+.*:)", line, re.M | re.I)
                        if m:
                            chassisname = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+dropped due to full socket buffers", line.strip(), re.M | re.I)
                        if m:
                            udpfullsocbufs = m.groups(0)[0]
                elif k == "ip6":
                    for line in output:
                        m = re.match(r"([0-9]+)\t+fragments dropped \(dup or out of space\)", line.strip(), re.M | re.I)
                        if m:
                            ip6fragdropduporspace = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+fragments dropped after timeout", line.strip(), re.M | re.I)
                        if m:
                            ip6fragdroptimeout = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+output packets dropped due to no bufs", line.strip(), re.M | re.I)
                        if m:
                            ip6packetdropnobufs = m.groups(0)[0]

                        m = re.match(r"([0-9]+)\s+option packets dropped due to rate limit", line.strip(), re.M | re.I)
                        if m:
                            ip6optpacketsdropratelimit = m.groups(0)[0]

                        m = re.match(r"([0-9]+)\s+packets dropped \(src and int don't match\)", line.strip(), re.M | re.I)
                        if m:
                            ip6packetdropsrcintmismatch = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+packets dropped due to bad protocol", line.strip(), re.M | re.I)
                        if m:
                            ip6packetdropbadprotocol = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+transit re packet\(null\) dropped on mgmt i\/f", line.strip(), re.M | re.I)
                        if m:
                            ip6trnstredroponmgmt = m.groups(0)[0]
                elif k == "udp":
                    for line in output:
                        m = re.match(r"([0-9]+)\s+dropped due to full socket buffers", line.strip(), re.M | re.I)
                        if m:
                            udpfullsocbufs = m.groups(0)[0]
                elif k == "tnp":
                    for line in output:
                        m = re.match(r"([0-9]+)\s+hello packets dropped", line.strip(), re.M | re.I)
                        if m:
                            tnpdroprcvhello = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+fragments dropped", line.strip(), re.M | re.I)
                        if m:
                            tnpdroprcvfragments = m.groups(0)[0]
                        m = re.match(r"([0-9]+)\s+fragments dropped", line.strip(), re.M | re.I)
                        if m:
                            udpfullsocbufs = m.groups(0)[0]
                        m = re.match(r"", line.strip(), re.M | re.I)

        self.command_query = ""
        self.command_query = " and icmpratelimitdrops="+str(icmpratelimitdrops)+"" \
            " and icmp6ratelimitnotgen="+str(icmp6ratelimitnotgen)+" and deadnexthop="+str(deadnexthop)+"" \
            " and noroutedrop="+str(noroutedrop)+" and routeralertoptions="+str(routeralertoptions)+"" \
            " and ipfragdropduporspace="+str(ipfragdropduporspace)+" and listenqoverflow="+str(listenqoverflow)+"" \
            " and bucketoverflow="+str(bucketoverflow)+"  and cacheoverflow="+str(cacheoverflow)+"" \
            " and ipfragdropqueueoverflow="+str(ipfragdropqueueoverflow)+"  and ipfragdropoverlimit="+str(ipfragdropoverlimit)+"" \
            " and ipfragdropnobufs="+str(ipfragdropnobufs)+"  and ipfragdropratelimit="+str(ipfragdropratelimit)+"" \
            " and ipfragdropnoiflist="+str(ipfragdropnoiflist)+" and ipfragdropsrcintmismatch="+str(ipfragdropsrcintmismatch)+"" \
            " and iptrnstredroponmgmt="+str(iptrnstredroponmgmt)+" and tcpsenddropautherror="+str(tcpsenddropautherror)+"" \
            " and tcprcvdropautherror="+str(tcprcvdropautherror)+" and tcpdiscardbadchecksum="+str(tcpdiscardbadchecksum)+"" \
            " and tcpdiscardbadheaderoffsetfld="+str(tcpdiscardbadheaderoffsetfid)+" and tcpdiscardtooshort="+str(tcpdiscardtooshort)+"" \
            " and tcpbadconnattempt="+str(tcpbadconnattempt)+" and tcpdropconnembryonic="+str(tcpdropconnembryonic)+" " \
            " and tcpdropconnrexmittimeout="+str(tcpdropconnrexmittimeout)+" and tcpdropconnpersisttimeout="+str(tcpdropconnpersisttimeout)+"" \
            " and tcpdropconnkeepalive="+str(tcpdropconnkeepalive)+" and tcpdrop="+str(tcpdrop)+" and tcpdroprcvpktbadaddress="+str(tcpdroprcvpktbadaddress)+"" \
            " and tcpdropoosinsufficientmemory="+str(tcpdropoosinsufficientmemory)+" and tcpdropsendpktsautherror="+str(tcpdropsendpktsautherror)+"" \
            " and tcpdroprcvpktsautherror="+str(tcpdroprcvpktsautherror)+" and tcptimeoutretransmit="+str(tcptimeoutretransmit)+" " \
            " and tcptimeoutpersist="+str(tcptimeoutpersist)+" and tcptimeoutkeepalive="+str(tcptimeoutkeepalive)+" and arpdiscarded="+str(arpdiscarded)+" " \
            " and arpdenied="+str(arpdenied)+" and udpfullsocbufs="+str(udpfullsocbufs)+" and ip6fragdropduporspace="+str(ip6fragdropduporspace)+"" \
            " and ip6fragdroptimeout="+str(ip6fragdroptimeout)+" and ip6packetdropnobufs="+str(ip6packetdropnobufs)+"" \
            " and ip6optpacketsdropratelimit="+str(ip6optpacketsdropratelimit)+" and ip6optpacketsdropratelimit="+str(ip6optpacketsdropratelimit)+"" \
            " and ip6packetdropsrcintmismatch="+str(ip6packetdropsrcintmismatch)+" and ip6packetdropbadprotocol="+str(ip6packetdropbadprotocol)+" " \
            " and ip6trnstredroponmgmt="+str(ip6trnstredroponmgmt)+" and udpfullsocbufs="+str(udpfullsocbufs)+" and tnpdroprcvhello="+str(tnpdroprcvhello)+"" \
            " and tnpdroprcvfragments="+str(tnpdroprcvfragments)+""


    def build_sys_stor_data_query(self, sys_stor_data):
        filesystem = sys_stor_data[0].strip()
        size = sys_stor_data[1].strip()
        used = sys_stor_data[2].strip()
        avail = sys_stor_data[3].strip()
        capacity = sys_stor_data[4].strip()
        mountedon = sys_stor_data[5].strip()
        chassisname = sys_stor_data[6].strip()
        if size[-1:]=="M":
            size = size[:-1]
            if '.' in size:
                size = float(size) * 1000 * 1000
            else:
                size = int(size) * 1000 * 1000
            size = int(size)
        elif size[-1:]=="G":
            size = size[:-1]
            if '.' in size:
                size = float(size) * 1000 * 1000 * 1000
            else:
                size = int(size) * 1000 * 1000 * 1000
            size = int(size)
        elif size[-1:]=="K":
            size = size[:-1]
            if '.' in size:
                size = float(size) * 1000
            else:
                size = int(size) * 1000
            size = int(size)
        elif size[-1:]=="B":
            size = size[:-1]
            if '.' in size:
                size = float(size)
            else:
                size = int(size)
            size = int(size)

        if used[-1:]=="M":
            used = used[:-1]
            if '.' in used:
                used = float(used) * 1000 * 1000
            else:
                used = int(used) * 1000 * 1000
            used = int(used)
        elif used[-1:]=="G":
            used = used[:-1]
            if '.' in used:
                used = float(used) * 1000 * 1000 * 1000
            else:
                used = int(used) * 1000 * 1000 * 1000
            used = int(used)
        elif used[-1:]=="K":
            used = used[:-1]
            if '.' in used:
                used = float(used) * 1000
            else:
                used = int(used) * 1000
            used = int(used)
        elif used[-1:]=="B":
            used = used[:-1]
            if '.' in used:
                used = float(used)
            else:
                used = int(used)
            used = int(used)

        if avail[-1:]=="M":
            avail = avail[:-1]
            if '.' in avail:
                avail = float(avail) * 1000 * 1000
            else:
                avail = int(avail) * 1000 * 1000
            avail = int(avail)
        elif avail[-1:]=="G":
            avail = avail[:-1]
            if '.' in avail:
                avail = float(avail) * 1000 * 1000 * 1000
            else:
                avail = int(avail) * 1000 * 1000 * 1000
            avail = int(avail)
        elif avail[-1:]=="K":
            avail = avail[:-1]
            if '.' in avail:
                avail = float(avail) * 1000
            else:
                avail = int(avail) * 1000
            avail = int(avail)
        elif avail[-1:]=="B":
            avail = avail[:-1]
            if '.' in avail:
                avail = float(avail)
            else:
                avail = int(avail)
            avail = int(avail)

        if capacity[-1:]=="M":
            capacity = capacity[:-1]
            if '.' in capacity:
                capacity = float(capacity) * 1000 * 1000
            else:
                capacity = int(capacity) * 1000 * 1000
            capacity = int(capacity)
        elif capacity[-1:]=="G":
            capacity = capacity[:-1]
            if '.' in capacity:
                capacity = float(capacity) * 1000 * 1000 * 1000
            else:
                capacity = int(capacity) * 1000 * 1000 * 1000
            capacity = int(capacity)
        elif capacity[-1:]=="K":
            capacity = capacity[:-1]
            if '.' in capacity:
                capacity = float(capacity) * 1000
            else:
                capacity = int(capacity) * 1000
            capacity = int(capacity)
        elif capacity[-1:]=="B":
            capacity = capacity[:-1]
            if '.' in capacity:
                capacity = float(capacity)
            else:
                capacity = int(capacity)
            capacity = int(capacity)

        self.command_query = ""
        self.command_query = " and chassisname"+str(" is NULL" if chassisname=="" else "='"+str(chassisname)+"'" )+" and filesystem='"+str(filesystem)+"' and \
            `size`="+str(size)+" and used="+str(used)+" and avail="+str(avail)+" and \
            capacity="+str(capacity)+" and mountedon='"+str(mountedon)+"' order by collector_time"

    def build_sys_ver_data_query(self, sys_ver_data):
        #print json.dumps(sys_ver_data, indent=4)
        chassisname = sys_ver_data.get("chassisname","")
        verbaseosboot = sys_ver_data.get("JUNOS Base OS boot","not found")
        verbaseossoftware = sys_ver_data.get("JUNOS Base OS Software Suite", "not found")
        verkernelsoftware = sys_ver_data.get("JUNOS Kernel Software Suite", "not found")
        vercryptosoftware = sys_ver_data.get("JUNOS Crypto Software Suite", "not found")
        verpfesupportcommon = sys_ver_data.get("JUNOS Packet Forwarding Engine Support (MX Common)", "not found")
        verdoc = sys_ver_data.get("JUNOS Online Documentation", "not found")
        versoftwarerelease = sys_ver_data.get("JUNOS platform Software Suite", "not found")
        verroutingsoftware = sys_ver_data.get("JUNOS Routing Software Suite", "not found")
        verpfesupport = sys_ver_data.get("JUNOS Packet Forwarding Engine Support", "not found")
        firmware_software = sys_ver_data.get("JUNOS Firmware Software Suite", "not found")
        self.command_query = ""
        self.command_query = " and chassisname='"+str(chassisname)+"' and verbaseosboot='"+str(verbaseosboot)+"' and \
            verbaseossoftware='"+str(verbaseossoftware)+"' and verkernelsoftware='"+str(verkernelsoftware)+"' and \
            vercryptosoftware='"+str(vercryptosoftware)+"' and verpfesupportcommon='"+str(verpfesupportcommon)+"' and \
            verdoc='"+str(verdoc)+"' and versoftwarerelease='"+str(versoftwarerelease)+"' and \
            verroutingsoftware='"+str(verroutingsoftware)+"' and verpfesupport='"+str(verpfesupport)+"' order by collector_time"

    def build_sys_vm_swap_query(self, sys_vm_swap):
        chassisname = sys_vm_swap.get("chassisname","")
        swappagerpageins = sys_vm_swap.get("swap pager pageins",0)
        swappagerpagespagedin = sys_vm_swap.get("swap pager pages paged in",0)
        swappagerpageouts = sys_vm_swap.get("swap pager pageouts",0)
        swappagerpagespagedout = sys_vm_swap.get("swap pager pages paged out", 0)
        swappagesused = sys_vm_swap.get("swap pager pageins", 0)
        peakswappagesused = sys_vm_swap.get("peak swap pages used", 0)
        self.command_query = ""
        self.command_query = " and chassisname"+str(" is NULL" if chassisname=="" else "='"+str(chassisname)+"'" )+" \
            and swappagerpageins="+str(swappagerpageins)+" and \
            swappagerpagespagedin ="+str(swappagerpagespagedin)+" and  \
            swappagerpageouts="+str(swappagerpageouts)+" and \
            swappagerpagespagedout="+str(swappagerpagespagedout)+" and swappagesused="+str(swappagesused)+" and \
            peakswappagesused="+str(peakswappagesused)+" order by collector_time"

    def build_task_io_data_query(self, task_io_data):
        taskname = task_io_data.get("taskname","").strip()
        reads = task_io_data.get("reads","").strip()
        writes = task_io_data.get("writes","").strip()
        rcvd = task_io_data.get("rcvd","").strip()
        sent = task_io_data.get("sent","").strip()
        dropped = task_io_data.get("dropped","").strip()

        self.command_query = ""
        self.command_query =" and taskname='"+str(taskname)+"' and reads="+str(reads)+" and \
                            writes="+str(writes)+" and rcvd="+str(rcvd)+" and \
                            sent="+str(sent)+" and dropped="+str(dropped)+" order by collector_time"
        #print self.command_query

    def build_task_mem_data_query(self, task_mem_data):
        memavailable = task_mem_data[2].get("Sizekb","")
        memavailablepercent = task_mem_data[2].get("Percentage","")
        memused = task_mem_data[0].get("Sizekb","")
        memusedpercent = task_mem_data[0].get("Percentage", "")
        maxeverused = task_mem_data[1].get("Sizekb", "")
        maxeverusedpercent = task_mem_data[1].get("Percentage", "")
        maxusedtime = task_mem_data[1].get("When", "")
        self.command_query = ""
        self.command_query = " and memavailable="+str(memavailable)+" and  \
            memavailablepercent="+str(memavailablepercent)+" and  memused="+str(memused)+" and  \
            memusedpercent="+str(memusedpercent)+" and  maxeverused="+str(maxeverused)+" and  \
            maxeverusedpercent="+str(maxeverusedpercent)+" and  maxusedtime='"+str(maxusedtime)+"' \
             order by collector_time"

    def build_ukern_trace_mem_comp_data_query(self, ukern_trace_mem_comp_data):
        name = ukern_trace_mem_comp_data.get("name","")
        bytess = ukern_trace_mem_comp_data.get("bytes","")
        allocs = ukern_trace_mem_comp_data.get("allocs","")
        frees = ukern_trace_mem_comp_data.get("frees", "")
        failures = ukern_trace_mem_comp_data.get("failures", "")
        self.command_query = ""
        self.command_query = " and name='"+str(name)+"' and \
            bytes="+str(bytess)+" and allocs="+str(allocs)+" and \
            frees="+str(frees)+" and failures="+str(failures)+" order by collector_time"

    def build_up_data_query(self, up_data):
        boot_date = up_data.get("system_booted_date","")
        boot_time = up_data.get("system_booted_time","")
        protocols_start_date = up_data.get("protocols_started_date","")
        protocol_start_time = up_data.get("protocols_started_time", "")
        config_date = up_data.get("last_configured_date", "")
        config_time = up_data.get("last_configured_time", "")
        chassisname = up_data.get("chassisname", "")
        self.command_query = ""
        self.command_query =" and boot_date='"+str(boot_date)+"' and \
                boot_time='"+str(boot_time)+"' and protocols_start_date='"+str(protocols_start_date)+"' and \
                protocol_start_time='"+str(protocol_start_time)+"' and config_date='"+str(config_date)+"' and \
                config_time='"+str(config_time)+"' order by collector_time"

    def build_vc_prtcl_adj_data_query(self, vc_prtcl_adj_data):
        interface = vc_prtcl_adj_data.get('interface', "")
        system = vc_prtcl_adj_data.get('system', "")
        hold = vc_prtcl_adj_data.get('state', 0)
        state = vc_prtcl_adj_data.get('hold', "")
        member = vc_prtcl_adj_data.get('member', 0)
        self.command_query = ""
        self.command_query = " and interface='"+str(interface)+"' and state='"+str(state)+"' and system='"+str(system)+"'  and  and hold="+str(hold)+" and member="+str(member)+""

    def build_vc_prtcl_stat_data_query(self, vc_prtcl_stat_data):
        interface = vc_prtcl_stat_data.get('interface', "")
        system = vc_prtcl_stat_data.get('system', "")
        hold = vc_prtcl_stat_data.get('state', 0)
        state = vc_prtcl_stat_data.get('hold', "")
        member = vc_prtcl_stat_data.get('member', 0)
        self.command_query = ""
        self.command_query = " and interface='"+str(interface)+"' and state='"+str(state)+"' and system='"+str(system)+"'  and  and hold="+str(hold)+" and member="+str(member)+""


    def build_vc_stat_data_query(self, vc_stat_data):
        interface = vc_stat_data.get('interface', "")
        system = vc_stat_data.get('system', "")
        hold = vc_stat_data.get('state', 0)
        state = vc_stat_data.get('hold', "")
        member = vc_stat_data.get('member', 0)
        self.command_query = ""
        self.command_query = " and interface='"+str(interface)+"' and state='"+str(state)+"' and system='"+str(system)+"'  and  and hold="+str(hold)+" and member="+str(member)+""

    def build_vc_vcp_stat_data_query(self, vc_vcp_stat_data):
        interface = vc_vcp_stat_data.get('interface', "")
        system = vc_vcp_stat_data.get('system', "")
        hold = vc_vcp_stat_data.get('state', 0)
        state = vc_vcp_stat_data.get('hold', "")
        member = vc_vcp_stat_data.get('member', 0)
        self.command_query = ""
        self.command_query = " and interface='"+str(interface)+"' and state='"+str(state)+"' and system='"+str(system)+"'  and  and hold="+str(hold)+" and member="+str(member)+""