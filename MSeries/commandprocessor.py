__author__ = 'asifj'

# !/usr/bin/env python
# hi

import re
from bs4 import BeautifulSoup
import traceback
import sys
import impala.dbapi
import impala.util
from collections import OrderedDict
import json
import time
import glob
import datetime
import pprint
from tabulate import tabulate
from metadata import metadata
from utils import *
from commands import Commands
from querybuilder import Querybuilder
import csv
import os.path



class CommandProcessor(object, metadata, Utils, Commands, Querybuilder):
    # CommandProcessor
    def __init__(self, file_name):
        # Constructor
        self.file_name = file_name
        self.arp_data = OrderedDict()
        self.ch_alarm_data = OrderedDict()
        self.ch_fpc_pic_data = OrderedDict()
        self.fpc_data = OrderedDict()
        self.ipsec_stats_data = OrderedDict()
        self.jtree_mem = OrderedDict()
        self.up_data = OrderedDict()
        self.vc_prtcl_adj_data = OrderedDict()
        self.vc_prtcl_stat_data = OrderedDict()
        self.vc_stat_data = OrderedDict()
        self.vc_vcp_stat_data = OrderedDict()
        self.sys_ver_data = OrderedDict()
        self.ch_hard_data = OrderedDict()
        self.env_data = OrderedDict()
        self.eth_sw_err_age_msg_data = OrderedDict()
        self.eth_sw_stat_maclrnerr_data = OrderedDict()
        self.eth_sw_tbl_summ_data = OrderedDict()
        self.stp_stats_data = OrderedDict()
        self.arp = OrderedDict()
        self.krt_q = OrderedDict()
        self.krt_st = OrderedDict()
        self.buff_data = OrderedDict()
        self.task_io_data = OrderedDict()
        self.sys_cores_data = OrderedDict()
        self.sys_license_data = OrderedDict()
        self.sys_stats_data = OrderedDict()
        self.sys_stor_data = OrderedDict()
        self.sys_vm_swap = OrderedDict()
        self.ukern_trace_mem_comp_data = OrderedDict()
        self.ch_fab_sum_data = OrderedDict()
        self.mpc_jnh_summ_data = OrderedDict()
        self.nhdb_zones = OrderedDict()
        self.pfe_heap_mem = OrderedDict()
        self.ps_data = OrderedDict()
        self.pfe_st_err = OrderedDict()
        self.pfe_st_notif_data = OrderedDict()
        self.pfe_tr_data = OrderedDict()
        self.proc_mem_data = OrderedDict()
        self.pwr_data = OrderedDict()
        self.re_data = OrderedDict()
        self.rt_sum_data = OrderedDict()
        self.sec_alg_st_data = OrderedDict()
        self.sec_nat_intf_nat_prts_data = OrderedDict()
        self.sec_utm_aspam_stats_data = OrderedDict()
        self.sec_utm_av_st_data = OrderedDict()
        self.sec_utm_av_stats_data = OrderedDict()
        self.sec_utm_st_data = OrderedDict()
        self.sec_utm_web_st_data = OrderedDict()
        self.sec_utm_web_stat_data = OrderedDict()
        self.sh_mem_frag_data = OrderedDict()
        self.task_mem_data = OrderedDict()
        self.ch_fab_map_data = OrderedDict()
        # Versioning Metdata
        self.host_name_versioning = ""
        self.model_versioning = ""
        # Metadata variables
        self.model = ""
        self.servicenow_device_id = ""
        self.node = ""
        self.login_mail_id = ""
        self.old_account_name = ""
        self.perceived_secondary_id = ""
        self.old_account_id = ""
        self.space_device_id = ""
        self.host_name = ""
        self.serial_number = ""
        self.base_product_name = ""
        self.phd_collected_time = ""
        self.account_id = ""
        self.servicenow_version = ""
        self.platform = ""
        self.received_time = ""
        self.base_software_release = ""
        self.account_name = ""
        self.group_name = ""
        self.disable_time = ""
        self.perceived_account_name = ""
        self.device_timezone = ""
        self.status = ""
        self.product = ""
        self.servicenow_timezone = ""
        self.perceived_account_id = ""
        self.additional_device_info = ""
        self.group_id = ""
        self.enabled_time = ""
        self.space_version = ""
        self.software_release = ""
        self.aiscript_version = ""
        self.phdct_utc = ""
        self.phdrt_utc = ""
        self.common_query = ""
        self.command_query = ""
        self.output = ""

    def command_report1(self, C, command_report):
        command_report.append("Does not exists in Hadoop")
        command_report.append(C.common_query+C.command_query)
        command_report.append(C.common_query)
        command_report.append(C.command_query)
        command_report.append(str(result_set))
        command_report.append(str(C.output))
        command_report.append("Command exists in file")
        command_report.append("Common fields does not exists")
        command_report.append(str())
        return command_report

    def command_report2(self, C, command_report, result_set):
        command_report.append("Does not exists in Hadoop")
        command_report.append(C.common_query+C.command_query)
        command_report.append(C.common_query)
        command_report.append(C.command_query)
        command_report.append(str(result_set[0]))
        command_report.append(str(C.output))
        command_report.append("Command exists in file")
        command_report.append("Common fields exists")
        command_report.append(str(result_set))
        return command_report

    def command_report3(self, C, command_report, result_set):
        command_report.append("Exists in Hadoop")
        command_report.append(C.common_query+C.command_query)
        command_report.append(C.common_query)
        command_report.append(C.command_query)
        command_report.append(str(result_set))
        command_report.append(str(C.output))
        command_report.append("Command exists in file")
        command_report.append("")
        command_report.append("")
        return command_report

    def command_report4(self, command_report):
        command_report.append("")
        command_report.append("")
        command_report.append("")
        command_report.append("")
        command_report.append("")
        command_report.append("")
        command_report.append("Does not exists in file")
        command_report.append("")
        command_report.append("")
        return command_report

    def report_writer(self, writer, command_report):
        print "\t\t\t\t\t\tWritten to report\t"+str(command_report[2])+"\t"+str(command_report[9])
        writer.writerow(command_report)
        #print command_report
        command_report = []
        return command_report

if __name__ == "__main__":
    # E = Extractor("mx-480-sn2_phdc_jmb_ais_health_201508*.txt") # environment
    dbconnection = impala.dbapi.connect(host="172.22.147.240", port="27003", database="parseattachments")
    dbconnection.close()
    cur = dbconnection.cursor()
    count = 0
    summary = []
    print_query = 1
    print_data = 0
    print_output = 0

    arp_data = 0
    buff_data = 1
    ch_alarm_data = 1
    ch_fab_map_data = 1
    ch_fab_sum_data = 1
    ch_fpc_pic_data = 0
    ch_hard_data = 1
    env_data = 1
    eth_sw_err_age_msg_data = 0
    eth_sw_stat_maclrnerr_data = 0
    eth_sw_tbl_summ_data = 0
    fan_data = 1
    fpc_data = 1
    ipsec_stats_data = 0
    jtree_mem = 1
    krt_q = 1
    krt_st = 1
    mpc_jnh_summ_data = 1
    nhdb_zones = 1
    pfe_err_ichip = 0
    pfe_err_ichip_mx = 0
    pfe_err_lchip = 0
    pfe_heap_mem = 1
    pfe_st_err = 0
    pfe_st_notif_data = 0
    pfe_tr_data = 1
    proc_mem_data = 1
    ps_data = 1
    pwr_data = 1
    re_data = 1
    rt_sum_data = 1
    sec_alg_st_data = 0
    sec_nat_intf_nat_prts_data = 0
    sec_utm_aspam_stats_data = 0
    sec_utm_av_st_data = 0
    sec_utm_av_stats_data = 0
    sec_utm_st_data = 0
    sec_utm_web_st_data = 0
    sec_utm_web_stat_data = 0
    sh_mem_frag_data = 1
    stp_stats_data = 0
    sys_cores_data = 1
    sys_license_data = 0
    sys_stats_data = 1
    sys_stor_data = 1
    sys_ver_data = 1
    sys_vm_swap = 1
    task_io_data = 1
    task_mem_data = 1
    ukern_trace_mem_comp_data = 1
    up_data = 1
    vc_prtcl_adj_data = 0
    vc_prtcl_stat_data = 0
    vc_stat_data = 0
    vc_vcp_stat_data = 0
    chassis_cluster_statistics_data = 0

    report = []
    file_report = []

    reports_dir = "C:\\tmp\\PHCreports\\mx1\\"
    phcs_home_dir = "C:\\Users\\asifj\\Desktop\\sandbox\\ImpalaTesting\\PHCFiles\\mx\\"

    file = "*20150907*.txt"
    #file = "sn-space-mx320-sys_phdc_jmb_ais_health_20150810_071932.txt"
    phcs = sorted(glob.glob(phcs_home_dir+file))

    for phc in phcs:
        try:
            C = CommandProcessor(phc)
            process = 0
            C.getMetdata()
            C.phdct_utc = C.epochToUTC(C.phd_collected_time)
            C.phdrt_utc = C.epochToUTC(C.received_time)
            tmp = phc.replace(phcs_home_dir, "").replace(".txt","")+"_PHC_"+str(C.phdct_utc).replace(":", "-")
            size = 0
            try:
                size = os.path.getsize(reports_dir+str(tmp)+".csv") / 1000
            except Exception:
                size = 0
            #  os.path.isfile(reports_dir+str(tmp)+".csv") and
            if size < 2:
            #if True:
                print "\n\n\n\n\n" + C.hashs() + "  START  " + C.hashs()
                print "\nFilename: " + str(phc)

                C.phdct_utc = C.epochToUTC(C.phd_collected_time)
                C.phdrt_utc = C.epochToUTC(C.received_time)

                fo = open(reports_dir+str(tmp)+".csv", "wb")
                writer = csv.writer(fo)
                row = ['FileName','Command','TableName','HadoopExist','FullQuery','CommonQuery','CommandQuery','HadoopOutput','CommandOutput','CommandExistsInFile','CommonFieldExists','']
                writer.writerow(row)

                command_report = []
                file_report = []

                # buff_data
                if buff_data==1:
                    C.get_buff_data()
                    cur.execute("refresh buff_data")
                    how_many = 0
                    if bool(C.buff_data[0])==False:
                        how_many = 0
                    else:
                        how_many = len(C.buff_data)
                    for i in range (0, how_many):
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show system buffers | display xml")
                        command_report.append("buff_data")
                        status = []
                        status.append("buff_data")
                        status.append(C.phdct_utc)
                        C.build_common_query("buff_data")
                        C.build_buff_data_query(C.buff_data[i])
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No buff_data Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                print "Collected time: "+str(C.phdct_utc)
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************buff_data Match Found*********************"
                            # C.tabulate_print(result_set)
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("buff_data Match Found")
                        if print_query == 1:
                            print query
                        if print_data == 1:
                            print json.dumps(C.buff_data[i], indent=4)
                        if print_output == 1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)
                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show system buffers | display xml")
                        command_report.append("buff_data")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # ch_alarm_data
                if ch_alarm_data==1:
                    C.get_ch_alarm_data()
                    cur.execute("refresh ch_alarm_data")
                    #print json.dumps(C.ch_alarm_data, indent=4)
                    how_many = len(C.ch_alarm_data)
                    for i in range(0, how_many):
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show chassis alarm")
                        command_report.append("ch_alarn_data")
                        status = []
                        status.append("ch_alarn_data")
                        status.append(C.phdct_utc)
                        C.build_common_query("ch_alarm_data")
                        C.build_ch_alarm_query(C.ch_alarm_data[i])
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No ch_alarm_data Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                print "Collected time: "+str(C.phdct_utc)
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************ch_alarm_data Match Found*********************"
                            # C.tabulate_print(result_set)
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("ch_alarm_data Match Found")
                        if print_query == 1:
                            print query
                        if print_data == 1:
                            print json.dumps(C.ch_alarm_data[i], indent=4)
                        if print_output == 1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)
                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show chassis alarm")
                        command_report.append("ch_alarm_data")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # ch_fab_map_data
                if ch_fab_map_data==1:
                    C.get_ch_fab_map_data()
                    cur.execute("refresh ch_fab_map_data")
                    how_many = len(C.ch_fab_map_data)
                    for i in range(0, how_many):
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show chassis fabric map")
                        command_report.append("ch_fab_map_data")
                        status = []
                        status.append("ch_fab_map_data")
                        status.append(C.phdct_utc)
                        C.build_common_query("ch_fab_map_data")
                        C.build_fab_map_data_query(C.ch_fab_map_data[i])
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No ch_fab_map_data Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                print "Collected time: "+str(C.phdct_utc)
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************ch_fab_map_data Match Found*********************"
                            # C.tabulate_print(result_set)
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("ch_fab_map_data Match Found")
                        if print_query == 1:
                            print query
                        if print_data == 1:
                            print json.dumps(C.ch_alarm_data[i], indent=4)
                        if print_output == 1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)
                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show chassis fabric map")
                        command_report.append("ch_fab_map_data")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)


                # ch_fab_sum_data
                if ch_fab_sum_data==1:
                    # ex-8200-sn1_phdc_jmb_ais_health_20150811_161933.txt
                    C.get_ch_fab_sum_data()
                    cur.execute("refresh ch_fab_sum_data")
                    how_many = len(C.ch_fab_sum_data)
                    for i in range(0, how_many):
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show chassis fabric summary")
                        command_report.append("ch_fab_sum_data")
                        status = []
                        status.append("ch_fab_sum_data")
                        status.append(C.phdct_utc)
                        C.build_common_query("ch_fab_sum_data")
                        C.build_ch_fab_sum_data_query(C.ch_fab_sum_data[i])
                        #print json.dumps(C.ch_fab_sum_data, indent=4)
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No ch_fab_sum_data Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************ch_fab_sum_data Match Found*********************"
                            # C.tabulate_print(result_set)
                            #print result_set
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("ch_fab_sum_data Match Found")
                        if print_query == 1:
                            print query
                        if print_data == 1:
                            print json.dumps(C.ch_fab_sum_data[i], indent=4)
                        if print_output == 1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)
                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show chassis fabric summary")
                        command_report.append("ch_fab_sum_data")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)


                # ch_hard_data
                if ch_hard_data==1:
                    C.get_ch_hard_data()
                    cur.execute("refresh ch_hard_data")
                    how_many = len(C.ch_hard_data)
                    for k,v in C.ch_hard_data.iteritems():
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show chassis hardware no-forwarding")
                        command_report.append("ch_hard_data")
                        status = []
                        status.append("ch_hard_data")
                        status.append(C.phdct_utc)
                        C.build_common_query("ch_hard_data")
                        C.build_ch_hard_data_query(k)
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        #print query
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No ch_hard_data Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************ch_hard_data Match Found*********************"
                            # C.tabulate_print(result_set)
                            #print result_set
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("Match Found")
                        if print_query == 1:
                            print query
                        if print_data == 1:
                            print json.dumps(C.ch_hard_data, indent=4)
                        if print_output == 1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show chassis hardware no-forwarding")
                        command_report.append("ch_hard_data")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)


                # env_data
                if env_data==1:
                    C.get_env_data()
                    cur.execute("refresh env_data")
                    how_many = len(C.env_data.get('Temp',""))
                    for i in range (0, how_many):
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show chassis environment-Temp")
                        command_report.append("env_data")
                        status = []
                        status.append("env_data")
                        status.append(C.phdct_utc)
                        C.build_common_query("env_data")
                        tempc = 0
                        m = re.match(r"([0-9]+).*", C.env_data['Temp'][i]['measurement'].strip(), re.I | re.M)
                        if m:
                            tempc = m.groups(0)[0]
                        if int(tempc) > 55:
                            command_report.append(str(phc.replace(phcs_home_dir,"")))
                            command_report.append("show chassis environment no-forwarding-Temp")
                            command_report.append("env_data")
                            status = []
                            status.append("env_data")
                            status.append(C.phdct_utc)

                            C.build_env_data_query(C.env_data['Temp'][i])
                            query = C.common_query + C.command_query
                            cur.execute(query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                print "\n\t\t\t\t\t\t******************No env_data-Temp Match Found*********************"
                                status.append("NA")
                                print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                                cur.execute(C.common_query)
                                result_set = cur.fetchall()
                                if len(result_set) < 1:
                                    command_report = C.command_report1(C, command_report)
                                else:
                                    command_report = C.command_report2(C, command_report, result_set)
                                status.append("env_data No Match Found")
                            else:
                                print "\n\t\t\t\t\t\t******************env_data-Temp Match Found*********************"
                                # C.tabulate_print(result_set)
                                #print result_set
                                status.append(result_set[0][2])
                                command_report = C.command_report3(C, command_report, result_set)
                                status.append("env_data Match Found")
                            if print_query == 1:
                                print query
                            if print_data == 1:
                                print json.dumps(C.env_data['Temp'][i], indent=4)
                            if print_output == 1:
                                print C.output
                            status.append(phc)
                            summary.append(status)
                            file_report.append(command_report)
                            command_report = C.report_writer(writer, command_report)
                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show chassis environment no-forwarding-Temp")
                        command_report.append("env_data")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # fan_data
                if fan_data==1:
                    C.get_fan_data()
                    cur.execute("refresh fan_data")
                    how_many = len(C.fan_data)
                    for i in range(0, how_many):
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show chassis environment no-forwarding-Fan")
                        command_report.append("fan_data")
                        status = []
                        status.append("fan_data")
                        status.append(C.phdct_utc)
                        C.build_common_query("fan_data")
                        C.build_fan_data_query(C.fan_data[i])
                        #print json.dumps(C.fan_data, indent=4)
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No fan_data Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("fan_data No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************fan_data Match Found*********************"
                            # C.tabulate_print(result_set)
                            #print result_set
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("fan_data Match Found")
                        if print_query == 1:
                            print query
                        if print_data == 1:
                            print json.dumps(C.fan_data[i], indent=4)
                        if print_output == 1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show chassis environment no-forwarding-Fan")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # fpc_data
                if fpc_data==1:
                    C.get_fpc_data()
                    cur.execute("refresh fpc_data")
                    how_many = len(C.fpc_data)
                    for i in range(0, how_many):
                        if not C.fpc_data[i]['state'].strip()=="Empty":
                            command_report.append(str(phc.replace(phcs_home_dir,"")))
                            command_report.append("show chassis fpc | display xml")
                            command_report.append("fpc_data")
                            status = []
                            status.append("FPC")
                            status.append(C.phdct_utc)
                            C.build_common_query("fpc_data")
                            C.build_fpc_data_query(C.fpc_data[i])
                            #print json.dumps(C.fpc_data, indent=4)
                            query = C.common_query + C.command_query
                            cur.execute(query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                print "\n\t\t\t\t\t\t******************No FPC Match Found*********************"
                                status.append("NA")
                                print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                                cur.execute(C.common_query)
                                result_set = cur.fetchall()
                                if len(result_set) < 1:
                                    command_report = C.command_report1(C, command_report)
                                else:
                                    command_report = C.command_report2(C, command_report, result_set)
                                status.append("fpc_data No Match Found")
                            else:
                                print "\n\t\t\t\t\t\t******************FPC Match Found*********************"
                                # C.tabulate_print(result_set)
                                #print result_set
                                status.append(result_set[0][2])
                                command_report = C.command_report3(C, command_report, result_set)
                                status.append("Match Found")
                            if print_query == 1:
                                print query
                            if print_data == 1:
                                print json.dumps(C.fpc_data[i], indent=4)
                            if print_output == 1:
                                print C.output
                            status.append(phc)
                            summary.append(status)
                            file_report.append(command_report)
                            command_report = C.report_writer(writer, command_report)

                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show chassis fpc | display xml")
                        command_report.append("fpc_data")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)


                # jtree_mem
                if jtree_mem==1:
                    C.get_jtree_mem()
                    cur.execute("refresh jtree_mem")
                    how_many = 0
                    if bool(C.jtree_mem[0])==False:
                        how_many = 0
                    else:
                        how_many = len(C.jtree_mem)
                    if how_many:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append('request pfe execute command "show jtree 0 memory extensive" target fpc(NUMBER)')
                        command_report.append("jtree_mem")
                        status = []
                        status.append("jtree_mem")
                        status.append(C.phdct_utc)
                        C.build_common_query("jtree_mem")
                        C.build_jtree_mem_query(C.jtree_mem)
                        #print json.dumps(C.jtree_mem, indent=4)
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No jtree_mem Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                print "Collected time: "+str(C.phdct_utc)
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("jtree_mem No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************jtree_mem Match Found*********************"
                            # C.tabulate_print(result_set)
                            #print result_set
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("jtree_mem Match Found")
                        if print_query==1:
                            print query
                        if print_data == 1:
                            print json.dumps(C.jtree_mem, indent=4)
                        if print_output == 1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)
                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append('request pfe execute command "show jtree 0 memory extensive" target fpc(NUMBER)')
                        command_report.append("jtree_mem")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # krt_q
                if krt_q==1:
                    C.get_krt_q()
                    cur.execute("refresh krt_q")
                    how_many = len(C.krt_q)
                    if how_many:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show krt queue")
                        command_report.append("krt_q")
                        status = []
                        status.append("krt_q")
                        status.append(C.phdct_utc)
                        C.build_common_query("krt_q")
                        C.build_krt_q_query(C.krt_q)
                        #print json.dumps(C.krt_q, indent=4)
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No krt_q Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("krt_q No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************krt_q Match Found*********************"
                            # C.tabulate_print(result_set)
                            #print result_set
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("krt_q Match Found")
                        if print_query==1:
                            print query
                        if print_data == 1:
                            print json.dumps(C.krt_q, indent=4)
                        if print_output == 1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)
                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show krt queue")
                        command_report.append("krt_q")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # krt_st
                if krt_st==1:
                    C.get_krt_st()
                    cur.execute("refresh krt_st")
                    how_many = len(C.krt_st)
                    if how_many:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show krt state")
                        command_report.append("krt_st")
                        status = []
                        status.append("krt_st")
                        status.append(C.phdct_utc)
                        C.build_common_query("krt_st")
                        C.build_krt_st_query(C.krt_st)
                        #print json.dumps(C.krt_st, indent=4)
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No krt_st Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("krt_q No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************krt_st Match Found*********************"
                            # C.tabulate_print(result_set)
                            #print result_set
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("krt_st Match Found")
                        if print_query == 1:
                            print query
                        if print_data == 1:
                            print json.dumps(C.krt_st, indent=4)
                        if print_output == 1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show krt state")
                        command_report.append("krt_st")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # mpc_jnh_summ_data
                if mpc_jnh_summ_data==1:
                    # Command error on MX series
                    C.get_mpc_jnh_summ_data()
                    cur.execute("refresh mpc_jnh_summ_data")
                    how_many = len(C.mpc_jnh_summ_data)
                    #print json.dumps(C.mpc_jnh_summ_data, indent=4)
                    for i in range (0,how_many):
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append('request pfe execute command "show jnh pool summary" target fpc(NUMBER)')
                        command_report.append("mpc_jnh_summ_data")
                        status = []
                        status.append("mpc_jnh_summ_data")
                        status.append(C.phdct_utc)
                        C.build_common_query("mpc_jnh_summ_data")
                        C.build_mpc_jnh_summ_data_query(C.mpc_jnh_summ_data[i])
                        #print json.dumps(C.mpc_jnh_summ_data, indent=4)
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No mpc_jnh_summ_data Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("mpc_jnh_summ_data No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************mpc_jnh_summ_data Match Found*********************"
                            # C.tabulate_print(result_set)
                            #print result_set
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("mpc_jnh_summ_data Match Found")
                        if print_query==1:
                            print query
                        if print_data==1:
                            print json.dumps(C.fpc_data[i], indent=4)
                        if print_output==1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)
                    #print C.mpc_jnh_summ_data
                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append('request pfe execute command "show jnh pool summary" target fpc(NUMBER)')
                        command_report.append("mpc_jnh_summ_data")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # nhdb_zones
                if nhdb_zones==1:
                    # Command error on MX series
                    C.get_nhdb_zones()
                    cur.execute("refresh nhdb_zones")
                    how_many = len(C.nhdb_zones)
                    #print json.dumps(C.nhdb_zones, indent=4)
                    for i in range (0,how_many):
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append('request pfe execute command "show nhdb zones" target fpc(NUMBER)')
                        command_report.append("nhdb_zones")
                        status = []
                        status.append("nhdb_zones")
                        status.append(C.phdct_utc)
                        C.build_common_query("nhdb_zones")
                        C.build_nhdb_zones_query(C.nhdb_zones[i])
                        #print json.dumps(C.nhdb_zones, indent=4)
                        query = C.common_query + C.command_query
                        print query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No nhdb_zones Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("nhdb_zones No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************nhdb_zones Match Found*********************"
                            # C.tabulate_print(result_set)
                            #print result_set
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("nhdb_zones Match Found")
                        if print_query==1:
                            print query
                        if print_data==1:
                            print json.dumps(C.fpc_data[i], indent=4)
                        if print_output==1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)
                    #print C.nhdb_zones
                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append('request pfe execute command "show nhdb zones" target fpc(NUMBER)')
                        command_report.append("nhdb_zones")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)


                # pfe_heap_mem
                if pfe_heap_mem==1:
                    # Command error on MX series
                    C.get_pfe_heap_mem()
                    cur.execute("refresh pfe_heap_mem")
                    how_many = len(C.pfe_heap_mem)
                    #print json.dumps(C.pfe_heap_mem, indent=4)
                    for i in range (0,how_many):
                        if C.pfe_heap_mem[i]['type']=="total":
                            command_report.append(str(phc.replace(phcs_home_dir,"")))
                            command_report.append('request pfe execute command "show heap 0" target cfeb0')
                            command_report.append("pfe_heap_mem")
                            status = []
                            status.append("pfe_heap_mem")
                            status.append(C.phdct_utc)
                            C.build_common_query("pfe_heap_mem")
                            C.build_pfe_heap_mem_query(C.pfe_heap_mem[i])
                            #print json.dumps(C.pfe_heap_mem, indent=4)
                            query = C.common_query + C.command_query
                            cur.execute(query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                print "\n\t\t\t\t\t\t******************No pfe_heap_mem Match Found*********************"
                                status.append("NA")
                                print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                                cur.execute(C.common_query)
                                result_set = cur.fetchall()
                                if len(result_set) < 1:
                                    command_report = C.command_report1(C, command_report)
                                else:
                                    command_report = C.command_report2(C, command_report, result_set)
                                status.append("pfe_heap_mem No Match Found")
                            else:
                                print "\n\t\t\t\t\t\t******************pfe_heap_mem Match Found*********************"
                                # C.tabulate_print(result_set)
                                #print result_set
                                status.append(result_set[0][2])
                                command_report = C.command_report3(C, command_report, result_set)
                                status.append("pfe_heap_mem Match Found")
                            if print_query==1:
                                print query
                            if print_data==1:
                                print json.dumps(C.fpc_data[i], indent=4)
                            if print_output==1:
                                print C.output
                            status.append(phc)
                            summary.append(status)
                            file_report.append(command_report)
                            command_report = C.report_writer(writer, command_report)
                    #print C.pfe_heap_mem
                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append('request pfe execute command "show heap 0" target cfeb0')
                        command_report.append("pfe_heap_mem")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # pfe_tr_data
                if pfe_tr_data==1:
                    C.get_pfe_tr_data()
                    cur.execute("refresh pfe_tr_data")
                    how_many = 0
                    if bool(C.pfe_tr_data[0])==False:
                        how_many = 0
                    else:
                        how_many = len(C.pfe_tr_data)
                    for i in range (0,how_many):
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show pfe statistics traffic")
                        command_report.append("pfe_tr_data")
                        status = []
                        status.append("pfe_tr_data")
                        status.append(C.phdct_utc)
                        C.build_common_query("pfe_tr_data")
                        #print json.dumps(C.pfe_tr_data, indent=4)
                        C.build_pfe_tr_data_query(C.pfe_tr_data[i])
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No pfe_tr_data Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("pfe_tr_data No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************pfe_tr_data Match Found*********************"
                            # C.tabulate_print(result_set)
                            #print result_set
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("pfe_tr_data Match Found")
                        if print_query==1:
                            print query
                        if print_data==1:
                            print json.dumps(C.pfe_tr_data[i], indent=4)
                        if print_output==1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show pfe statistics traffic")
                        command_report.append("pfe_tr_data")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # proc_mem_data
                if proc_mem_data==1:
                    C.get_proc_mem_data()
                    cur.execute("refresh proc_mem_data")
                    how_many = len(C.proc_mem_data)
                    for i in range (0,how_many):
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show system processes extensive no-forwarding-proc_mem_data")
                        command_report.append("proc_mem_data")
                        status = []
                        status.append("proc_mem_data")
                        status.append(C.phdct_utc)
                        C.build_common_query("proc_mem_data")
                        C.build_proc_mem_data_query(C.proc_mem_data[i])
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No proc_mem_data Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("proc_mem_data No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************proc_mem_data Match Found*********************"
                            # C.tabulate_print(result_set)
                            #print result_set
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("proc_mem_data Match Found")
                        if print_query==1:
                            print query
                        if print_data==1:
                            print json.dumps(C.proc_mem_data[i], indent=4)
                        if print_output==1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show system processes extensive no-forwarding-proc_mem_data")
                        command_report.append("proc_mem_data")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)


                # ps_data
                if ps_data==1:
                    C.get_ps_data()
                    cur.execute("refresh ps_data")
                    how_many = len(C.ps_data)
                    for i in range (0,how_many):
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show system processes extensive no-forwarding-ps_data")
                        command_report.append("ps_data")
                        status = []
                        status.append("ps_data")
                        status.append(C.phdct_utc)
                        C.build_common_query("ps_data")
                        C.build_ps_data_query(C.ps_data[i])
                        query = C.common_query + C.command_query
                        result_set = ""
                        if not C.command_query=='':
                            cur.execute(query)
                            result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No ps_data Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("ps_data No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************ps_data Match Found*********************"
                            # C.tabulate_print(result_set)
                            #print result_set
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("ps_data Match Found")
                        if print_query==1:
                            print query
                        if print_data==1:
                            print json.dumps(C.ps_data[i], indent=4)
                        if print_output==1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)
                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show system processes extensive no-forwarding-ps_data")
                        command_report.append("ps_data")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # pwr_data
                if pwr_data==1:
                    C.get_pwr_data()
                    cur.execute("refresh pwr_data")
                    how_many = len(C.pwr_data)
                    for i in range (0,how_many):
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show chassis environment no-forwarding-pwr_data")
                        command_report.append("pwr_data")
                        status = []
                        status.append("pwr_data")
                        status.append(C.phdct_utc)
                        C.build_common_query("pwr_data")
                        C.build_pwr_data_query(C.pwr_data[i])
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No pwr_data Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("pwr_data No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************pwr_data Match Found*********************"
                            # C.tabulate_print(result_set)
                            #print result_set
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("pwr_data Match Found")
                        if print_query==1:
                            print query
                        if print_data==1:
                            print json.dumps(C.ps_data[i], indent=4)
                        if print_output==1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)
                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show chassis environment no-forwarding-pwr_data")
                        command_report.append("pwr_data")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # re_data
                if re_data==1:
                    C.get_routing_engine_data()
                    cur.execute("refresh re_data")
                    how_many = len(C.re_data)
                    for i in range(0, how_many):
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show chassis routing-engine | display xml")
                        command_report.append("re_data")
                        status = []
                        status.append("RE")
                        status.append(C.phdct_utc)
                        C.build_common_query("re_data")
                        C.build_re_data_query(C.re_data[i])
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No RE Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("re_data No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************RE Match Found*********************"
                            #C.tabulate_print(result_set)
                            #print result_set
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("Match Found")
                        if print_query==1:
                            print query
                        if print_data==1:
                            print json.dumps(C.re_data[i], indent=4)
                        if print_output==1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)
                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show chassis routing-engine | display xml")
                        command_report.append("re_data")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # rt_sum_data
                if rt_sum_data==1:
                    C.get_rt_sum_data()
                    cur.execute("refresh rt_sum_data")
                    how_many = len(C.rt_sum_data)
                    if how_many:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show route summary")
                        command_report.append("rt_sum_data")
                        status = []
                        status.append("rt_sum_data")
                        status.append(C.phdct_utc)
                        C.build_common_query("rt_sum_data")
                        C.build_rt_sum_data_query(C.rt_sum_data)
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No rt_sum_data Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("rt_sum_data No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************rt_sum_data Match Found*********************"
                            # C.tabulate_print(result_set)
                            #print result_set
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("rt_sum_data Match Found")
                        if print_query==1:
                            print query
                        if print_data==1:
                            print json.dumps(C.rt_sum_data, indent=4)
                        if print_output==1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show route summary")
                        command_report.append("rt_sum_data")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # sh_mem_frag_data
                if sh_mem_frag_data==1:
                    C.get_sh_mem_frag_data()
                    cur.execute("refresh sh_mem_frag_data")
                    how_many = len(C.sh_mem_frag_data)
                    for i in range (0,how_many):
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show task memory fragmentation")
                        command_report.append("sh_mem_frag_data")
                        status = []
                        status.append("sh_mem_frag_data")
                        status.append(C.phdct_utc)
                        C.build_common_query("sh_mem_frag_data")
                        C.build_sh_mem_frag_data_query(C.sh_mem_frag_data[i])
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No sh_mem_frag_data Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("sh_mem_frag_data No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************sh_mem_frag_data Match Found*********************"
                            # C.tabulate_print(result_set)
                            #print result_set
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("sh_mem_frag_data Match Found")
                        if print_query == 1:
                            print query
                        if print_data == 1:
                            print json.dumps(C.sh_mem_frag_data[i], indent=4)
                        if print_output == 1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show task memory fragmentation")
                        command_report.append("sh_mem_frag_data")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # sys_cores_data
                if sys_cores_data==1:
                    C.get_sys_cores_data()
                    cur.execute("refresh sys_cores_data")
                    how_many = len(C.sys_cores_data)
                    for i in range (0,how_many):
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show system core-dumps no-forwarding")
                        command_report.append("sys_cores_data")
                        status = []
                        status.append("sys_cores_data")
                        status.append(C.phdct_utc)
                        C.build_common_query("sys_cores_data")
                        C.build_sys_cores_data_query(C.sys_cores_data[i])
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No sys_cores_data Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("sys_cores_data No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************sys_cores_data Match Found*********************"
                            # C.tabulate_print(result_set)
                            #print result_set
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("sys_cores_data Match Found")
                        if print_query == 1:
                            print query
                        if print_data == 1:
                            print json.dumps(C.sys_cores_data[i], indent=4)
                        if print_output == 1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)
                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show system core-dumps no-forwarding")
                        command_report.append("sys_cores_data")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # sys_stats_data
                if sys_stats_data==1:
                    C.get_sys_stats_data()
                    cur.execute("refresh sys_stats_data")
                    how_many = len(C.sys_stats_data)
                    if how_many:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show system statistics")
                        command_report.append("sys_stats_data")
                        status = ["sys_stats_data", C.phdct_utc]
                        C.build_common_query("sys_stats_data")
                        #print json.dumps(C.sys_stats_data, indent=4)
                        C.build_sys_stats_data_query(C.sys_stats_data)
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No sys_stats_data Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                print "Collected time: "+str(C.phdct_utc)
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************sys_stats_data Match Found*********************"
                            # C.tabulate_print(result_set)
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("sys_stats_data Match Found")
                        if print_query == 1:
                            print query
                        if print_data == 1:
                            print json.dumps(C.sys_stats_data[i], indent=4)
                        if print_output == 1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)
                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show system statistics")
                        command_report.append("sys_stats_data")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # sys_stor_data
                if sys_stor_data==1:
                    C.get_sys_stor_data()
                    cur.execute("refresh sys_stor_data")
                    how_many = len(C.sys_stor_data)
                    for i in range (0,how_many):
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show system storage")
                        command_report.append("sys_stor_data")
                        status = []
                        status.append("sys_stor_data")
                        status.append(C.phdct_utc)
                        C.build_common_query("sys_stor_data")
                        C.build_sys_stor_data_query(C.sys_stor_data[i])
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No sys_stor_data Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("sys_stor_data No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************sys_stor_data Match Found*********************"
                            #print result_set
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("sys_stor_data Match Found")
                        if print_query == 1:
                            print query
                        if print_data == 1:
                            print json.dumps(C.sys_stor_data[i], indent=4)
                        if print_output == 1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show system storage")
                        command_report.append("sys_stor_data")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # sys_ver_data_query
                if sys_ver_data==1:
                    C.get_sys_ver_data()
                    cur.execute("refresh sys_ver_data")
                    how_many = len(C.sys_ver_data)
                    if how_many:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show version no-forwarding")
                        command_report.append("sys_ver_data")
                        status = []
                        status.append("sys_ver_data")
                        status.append(C.phdct_utc)
                        C.build_common_query("sys_ver_data")
                        C.build_sys_ver_data_query(C.sys_ver_data)
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No sys_ver_data Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("sys_ver_data No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************sys_ver_data Match Found*********************"
                            # C.tabulate_print(result_set)
                            #print result_set
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("Match Found")
                        if print_query == 1:
                            print query
                        if print_data == 1:
                            print json.dumps(C.sys_ver_data, indent=4)
                        if print_output == 1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)
                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show version no-forwarding")
                        command_report.append("sys_ver_data")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # sys_vm_swap
                if sys_vm_swap==1:
                    C.get_sys_vm_swap()
                    cur.execute("refresh sys_vm_swap")
                    how_many = len(C.sys_vm_swap)
                    #print C.sys_vm_swap
                    if how_many:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show system virtual-memory")
                        command_report.append("sys_vm_swap")
                        status = []
                        status.append("sys_vm_swap")
                        status.append(C.phdct_utc)
                        C.build_common_query("sys_vm_swap")
                        C.build_sys_vm_swap_query(C.sys_vm_swap)
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No sys_vm_swap Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("sys_vm_swap No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************sys_vm_swap Match Found*********************"
                            # C.tabulate_print(result_set)
                            #print result_set
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("Match Found")
                        if print_query == 1:
                            print query
                        if print_data == 1:
                            print json.dumps(C.sys_vm_swap, indent=4)
                        if print_output == 1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show system virtual-memory")
                        command_report.append("sys_vm_swap")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # task_io_data
                if task_io_data==1:
                    C.get_task_io_data()
                    cur.execute("refresh task_io_data")
                    how_many = len(C.task_io_data)
                    for i in range(0, how_many):
                        if int(C.task_io_data[i]['dropped'])>0:
                            command_report.append(str(phc.replace(phcs_home_dir,"")))
                            command_report.append("show task io data")
                            command_report.append("task_io_data")
                            status = []
                            status.append("task_io_data")
                            status.append(C.phdct_utc)
                            C.build_common_query("task_io_data")
                            C.build_task_io_data_query(C.task_io_data[i])
                            query = C.common_query + C.command_query
                            cur.execute(query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                print "\n\t\t\t\t\t\t******************No task_io_data Match Found*********************"
                                status.append("NA")
                                print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                                cur.execute(C.common_query)
                                result_set = cur.fetchall()
                                if len(result_set) < 1:
                                    print "Collected time: "+str(C.phdct_utc)
                                    command_report = C.command_report1(C, command_report)
                                else:
                                    command_report = C.command_report2(C, command_report, result_set)
                                status.append("No Match Found")
                            else:
                                print "\n\t\t\t\t\t\t******************task_io_data Match Found*********************"
                                # C.tabulate_print(result_set)
                                status.append(result_set[0][2])
                                command_report = C.command_report3(C, command_report, result_set)
                                status.append("task_io_data Match Found")
                            if print_query == 1:
                                print query
                            if print_data == 1:
                                print json.dumps(C.task_io_data[i], indent=4)
                            if print_output == 1:
                                print C.output
                            status.append(phc)
                            summary.append(status)
                            file_report.append(command_report)
                            command_report = C.report_writer(writer, command_report)
                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show task io data")
                        command_report.append("task_io_data")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # task_mem_data
                if task_mem_data==1:
                    C.get_task_mem_data()
                    cur.execute("refresh task_mem_data")
                    how_many = len(C.task_mem_data)
                    if how_many:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show task memory fragmentation")
                        command_report.append("task_mem_data")
                        status = []
                        status.append("task_mem_data")
                        status.append(C.phdct_utc)
                        C.build_common_query("task_mem_data")
                        C.build_task_mem_data_query(C.task_mem_data)
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No task_mem_data Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("No Match Found")
                            status.append("task_mem_data No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************task_mem_data Match Found*********************"
                            # C.tabulate_print(result_set)
                            #print result_set
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("task_mem_data Match Found")
                        if print_query == 1:
                            print query
                        if print_data == 1:
                            print json.dumps(C.task_mem_data, indent=4)
                        if print_output == 1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show task memory fragmentation")
                        command_report.append("task_mem_data")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # ukern_trace_mem_comp_data
                if ukern_trace_mem_comp_data==1:
                    C.get_ukern_trace_mem_comp_data()
                    cur.execute("refresh ukern_trace_mem_comp_data")
                    how_many = len(C.ukern_trace_mem_comp_data)
                    for i in range (0, how_many):
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("request pfe execute command \"show ukern_trace memory-composition\" target fpc(NUMBER)")
                        command_report.append("ukern_trace_mem_comp_data")
                        status = []
                        status.append("ukern_trace_mem_comp_data")
                        status.append(C.phdct_utc)
                        C.build_common_query("ukern_trace_mem_comp_data")
                        C.build_ukern_trace_mem_comp_data_query(C.ukern_trace_mem_comp_data[i])
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No ukern_trace_mem_comp_data Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("No Match Found")
                            status.append("ukern_trace_mem_comp_data No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************ukern_trace_mem_comp_data Match Found*********************"
                            # C.tabulate_print(result_set)
                            #print result_set
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("ukern_trace_mem_comp_data Match Found")
                        if print_query == 1:
                            print query
                        if print_data == 1:
                            print json.dumps(C.ukern_trace_mem_comp_data[i], indent=4)
                        if print_output == 1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)
                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("request pfe execute command \"show ukern_trace memory-composition\" target fpc(NUMBER)")
                        command_report.append("ukern_trace_mem_comp_data")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                # up_data
                if up_data==1:
                    C.get_up_data()
                    cur.execute("refresh up_data")
                    how_many = len(C.up_data)
                    if how_many:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show system uptime no-forwarding")
                        command_report.append("up_data")
                        status = []
                        status.append("UP DATA")
                        status.append(C.phdct_utc)
                        C.build_common_query("up_data")
                        C.build_up_data_query(C.up_data)
                        query = C.common_query + C.command_query
                        cur.execute(query)
                        result_set = cur.fetchall()
                        if len(result_set) < 1:
                            print "\n\t\t\t\t\t\t******************No up_data Match Found*********************"
                            status.append("NA")
                            print "\t\t\t\t\t\t\t\t"+C.phdct_utc
                            cur.execute(C.common_query)
                            result_set = cur.fetchall()
                            if len(result_set) < 1:
                                command_report = C.command_report1(C, command_report)
                            else:
                                command_report = C.command_report2(C, command_report, result_set)
                            status.append("up_data No Match Found")
                        else:
                            print "\n\t\t\t\t\t\t******************up_data Match Found*********************"
                            # C.tabulate_print(result_set)
                            #print result_set
                            status.append(result_set[0][2])
                            command_report = C.command_report3(C, command_report, result_set)
                            status.append("Match Found")
                        if print_query == 1:
                            print query
                        if print_data == 1:
                            print json.dumps(C.up_data, indent=4)
                        if print_output == 1:
                            print C.output
                        status.append(phc)
                        summary.append(status)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)
                    if len(C.output)==1:
                        command_report.append(str(phc.replace(phcs_home_dir,"")))
                        command_report.append("show system uptime no-forwarding")
                        command_report = C.command_report4(command_report)
                        file_report.append(command_report)
                        command_report = C.report_writer(writer, command_report)

                print "\nCollected Time: " + str(C.phdct_utc) + "\n"
                print C.hashs() + "  END  " + C.hashs()
                #report.append(file_report)
                fo.close()
                file_report = []

        except Exception, err:
            #print "Problem. %s" % str(e)
            print(traceback.format_exc())
            print "hihello"
            exit()
            #or
            #print(sys.exc_info()[0])
            '''cur = C.get_db_connection()
            if not cur:
                print "Unable to connect Impala."
                print "Retrying in 10 seconds..."
                time.sleep(10)
            '''
    print "\n\n"

    print str(C.hashs()) + "\tSUMMARY\t" + str(C.hashs())
    #C.tabulate_summary(summary)
    for s in summary:
        print s
    print str(C.hashs()) + "\tSUMMARY\t" + str(C.hashs())