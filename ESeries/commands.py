__author__ = 'asifj'

import re
from bs4 import BeautifulSoup
import math
import json


class Commands:

    def __init__(self):
        pass

    def get_arp_data(self):
        # hi#
        if self.product.startswith("MX"):
            output = ""
            with open(self.file_name, "rb") as fopen:
                for line in fopen:
                    if not re.match(".*@.*>\\s+show\\s+system\\s+statistics\\s+arp.*", line, re.M | re.I) == None:
                        break
                for line in fopen:
                    if not re.match(".*@.*>\\sshow.*", line, re.M | re.I) == None:
                        break
                    if line.strip():
                        output = output + line
            #print output
            output = output.split("\n")
            self.arp_data = {}
            for line in output:
                if line.strip() and not line.strip().startswith("arp_data:"):
                    m = re.match(r'\s+(\d+)\s([\w|\s]+).*', line, re.M|re.I)
                    if m:
                        self.arp_data[m.groups(0)[1]] = m.groups(0)[0]
        elif self.product.startswith("EX"):
            output = ""
            with open(self.file_name, "rb") as fopen:
                for line in fopen:
                    if not re.match(".*@.*>\\s+show\\s+arp.*", line, re.M | re.I) == None:
                        break
                for line in fopen:
                    if not re.match(".*@.*>\\sshow.*", line, re.M | re.I) == None:
                        break
                    if line.strip():
                        output = output + line
            output = output.split("\n")
            #print output
            self.arp_data = {}
            for line in output:
                if line.strip().startswith("Total entries:"):
                    m = re.match(r'Total entries:\s(\d+).*', line, re.M|re.I)
                    if m:
                        self.arp_data["total_entries"] = m.groups(0)[0]

    def get_buff_data(self):
        # hi#
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+system\\s+buffers.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\sshow.*", line, re.M | re.I) == None:
                    break
                output = output + line
        #print output
        output = output.split("\n")
        self.output = output
        record_count = 0
        self.buff_data[record_count] = {}

        for line in output:
            m = re.match(r'((\S+\d+:).*)', line.strip(), re.M|re.I)
            if m:
                self.buff_data[record_count]['chassisname']=m.groups(0)[0]
            m = re.match(r'(.*)\/(.*)\/(.*)\s+mbufs\s+in\s+use\s+\(current\/cache\/total\)', line.strip(), re.M|re.I)
            if m:
                self.buff_data[record_count]['mbufs in use (current/cache/total)']=m.groups(0)
                continue
            m = re.match(r'(.*)\/(.*)\/(.*)\/(.*) mbuf clusters in use \(current\/cache\/total\/max\)', line.strip(), re.M|re.I)
            if m:
                self.buff_data[record_count]['mbuf clusters in use (current/cache/total/max)']=m.groups(0)
                continue
            m = re.match(r'(.*)\/(.*) mbuf\+clusters out of packet secondary zone in use \(current\/cache\)', line.strip(), re.M|re.I)
            if m:
                self.buff_data[record_count]['mbuf+clusters out of packet secondary zone in use (current/cache)']=m.groups(0)
                continue
            m = re.match(r'([0-9]+)\/([0-9]+)\/([0-9]+)[ \t]+requests[\s]+for[\s]mbufs[\s]denied.*\)', line.strip(), re.M|re.I)
            if m:
                self.buff_data[record_count]['requests for mbufs denied (mbufs/clusters/mbuf+clusters)']=m.groups(0)
                continue
            m = re.match(r'(.*)\s+cluster\s+requests\s+delayed', line.strip(), re.M|re.I)
            if m:
                self.buff_data[record_count]['cluster requests delayed']=m.groups(0)
                continue
            m = re.match(r'(.*)\s+mbuf\s+requests\s+delayed', line.strip(), re.M|re.I)
            if m:
                self.buff_data[record_count]['mbuf requests delayed']=m.groups(0)
                continue
            m = re.match(r'(.*)\s+cluster\s+requests\s+delayed', line.strip(), re.M|re.I)
            if m:
                self.buff_data[record_count]['cluster requests delayed']=m.groups(0)
                continue

        #print json.dumps(self.buff_data, indent=4)

    def get_ch_alarm_data(self):
        # hi#
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+chassis\\s+alarm\s*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                output += line
        #print output
        self.output = output
        output = output.split("\n")
        record_count = 0
        chassisname = ""

        for line in output:
           if line.strip():
                m = re.match(r'(sfc[0-9]+.*:|lcc[0-9]+.*:)', line, re.M|re.I)
                if m:
                    chassisname = m.groups(0)[0]
                m = re.match(r'(?P<alarm_time>\d+\-\d+\-\d+\s\d+:\d+:\d+\s[A-Z]+)\s+(?P<alarm_class>\S+)\s+(?P<alarm_description>.*)', line, re.M|re.I)
                if m:
                    self.ch_alarm_data[record_count] = m.groupdict(0)
                    self.ch_alarm_data[record_count]['chassisname'] = chassisname
                    record_count += 1

    def get_ch_fab_map_data(self):
        # root@sn-space-ex6200-sys> show chassis fabric map
        #
        # FPC4PFE0->CB0port10    Up
        # FPC4PFE0->CB1port24    Up
        # FPC4PFE0->CB2port40    Up
        # DPC1PFE3->CB0F0_00_3    Down
        # DPC1PFE0->CB0F0_01_0    Down
        # DPC1PFE1->CB0F0_01_1    Down
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+chassis\\s+fabric\\s+map.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        chassisname = ""
        output = output.split("\n")
        self.output = output
        record_count = 0
        for line in output:
            if line.strip():
                m = re.match(r'(sfc[0-9]+.*:|lcc[0-9]+.*:)', line, re.M|re.I)
                if m:
                    chassisname = m.groups(0)[0]
                m = re.match(r"(\S+\->\S+)\s+([a-z]+)", line.strip(), re.M|re.I)
                if m:
                    self.ch_fab_map_data[record_count] = {}
                    self.ch_fab_map_data[record_count]['fabricmap'] = m.groups(0)[0]
                    self.ch_fab_map_data[record_count]['mapstatus'] = m.groups(0)[1]
                    self.ch_fab_map_data[record_count]['chassisname'] = chassisname
                    record_count += 1
                    #self.ch_fab_map_data[record_count] = {}
                    #self.ch_fab_map_data[record_count]['fabricmap'] = m.groups(0)[2]
                    #self.ch_fab_map_data[record_count]['mapstatus'] = m.groups(0)[3]

        #print json.dumps(self.ch_fab_map_data, indent=4)


    def get_ch_fab_sum_data(self):
        #    root@ex-8200-sn1> show chassis fabric summary

        #    Plane   State    Uptime
        #     0      Online   127 days, 7 hours, 42 minutes, 20 seconds
        #     1      Online   127 days, 7 hours, 42 minutes, 8 seconds
        #     2      Online   127 days, 7 hours, 42 minutes, 8 seconds
        #     3      Online   127 days, 7 hours, 41 minutes, 53 seconds
        #     4      Spare    127 days, 7 hours, 41 minutes, 36 seconds
        #     5      Spare    127 days, 7 hours, 41 minutes, 31 seconds
        #     6      Spare    127 days, 7 hours, 41 minutes, 31 seconds
        #     7      Spare    127 days, 7 hours, 41 minutes, 28 seconds

        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+chassis\\s+fabric\\s+summary.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        chassisname = ""
        output = output.split("\n")
        self.output = output
        record_count = 0
        for line in output:
            if line.strip():
                m = re.match(r'(sfc[0-9]+.*:|lcc[0-9]+.*:)', line, re.M|re.I)
                if m:
                    chassisname = m.groups(0)[0]
                m = re.match(r'(?P<plane>\d+)\s+(?P<state>\S+)\s+(?P<uptime>[\S|\s]+)$', line.strip(), re.M|re.I)
                if m:
                    self.ch_fab_sum_data[record_count] = m.groupdict()
                    record_count = record_count + 1

    # For SRX display xml
    def get_ch_fpc_pic_data(self):
        # hi#
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s*show\\s*chassis\\s*fpc\\s*pic\-status\\s*.\\s*display\\s*xml", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                output += line
        #print output
        self.output = output
        chassisname = ""
        i = 0
        soup = BeautifulSoup(output, "lxml")
        output = output.split("\n")
        for line in output:
            if line.strip():
                m = re.match(r'<re-name>(.*)<\/re-name>', line, re.M|re.I)
                if m:
                    chassisname = m.groups(0)[0]
        for record in soup.findAll("fpc"):
            children = record.findChildren()
            self.ch_fpc_pic_data[i] = {}
            for child in children:
                self.ch_fpc_pic_data[i][child.name.strip().replace("-", "_")] = child.text.strip()
                self.ch_fpc_pic_data[i]["chassiname"] = chassisname
            i += 1
        #print json.dumps(self.ch_fpc_pic_data, indent=4)

    #Not for EX
    def get_ch_hard_data(self):
        # ch_hard_data
        output = ""
        output_type = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+chassis\\s+hardware\\sno\-forwarding$", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        if not output.strip():
            with open(self.file_name, "rb") as fopen:
                for line in fopen:
                    if not re.match(".*@.*>\\s+show\\s+chassis\\s+hardware\\s+.\\s+display.*", line, re.M | re.I) == None:
                        output_type = "xml"
                        break
                for line in fopen:
                    if not line.strip() == "":
                        if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                            break
                        output += line
        self.output = output
        #print output
        record_count = 0
        chassisname = ""
        if output_type == "xml":
            print "hi"
            soup = BeautifulSoup(output, "lxml")
            i = 0
            for record in soup.findAll("chassis"):
                children = record.findChildren()
                self.ch_hard_data[i] = {}
                for child in children:
                    self.ch_hard_data[i][child.name.strip().replace("-", "_")] = child.text.strip()
                i += 1
            for record in soup.findAll("chassis-module"):
                children = record.findChildren()
                self.ch_hard_data[i] = {}
                for child in children:
                    self.ch_hard_data[i][child.name.strip().replace("-", "_")] = child.text.strip()
                i += 1
            for record in soup.findAll("chassis-sub-module"):
                children = record.findChildren()
                self.ch_hard_data[i] = {}
                for child in children:
                    self.ch_hard_data[i][child.name.strip().replace("-", "_")] = child.text.strip()
                i += 1
        else:
            output = output.split("\n")
            for line in output:
                if line.strip() and not line.strip()=="hardware_data inventory:" and not line.strip()=="Item             Version  Part number  Serial number     Description":
                    m = ""
                    if len(line.strip().split(" "))<=2:
                        line = line + "                                                                              "
                        m = re.match(r'(?P<item>[\S|\s|\d]{4,18})\s(?P<version>[REV|\s\d|\s]+)\s+(?P<part_number>[\d{3,3}\-\d{6,6}|\s|BUILTIN|\s]{10,13})\s+(?P<serial_number>[A-Z0-9|\s]{10,18})\s(?P<description>.*)$', line, re.M|re.I)
                    else:
                        m = re.match(r'(?P<item>[\S|\s|\d]{4,18})\s(?P<version>[REV|\s\d|\s]{6,8})\s(?P<part_number>[\d{3,3}\-\d{6,6}|\s|BUILTIN|\s]{10,13})\s(?P<serial_number>[A-Z0-9|\s]{10,18})\s(?P<description>.*)$', line, re.M)
                    if m:
                        self.ch_hard_data[str(record_count)]=m.groupdict()
                        record_count = record_count + 1
        #print json.dumps(self.ch_hard_data, indent=4)

    def get_env_data(self):
        # env_data
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+chassis\\s+environment.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        #print output
        output = output.split("\n")
        self.output = output
        self.env_data = {}
        Class = ""
        chassisname = ""
        for line in output:
            if line.strip() and not line.strip().startswith("Class"):
                m = ""
                m = re.match(r'(sfc[0-9]+.*:|lcc[0-9]+.*:)', line, re.M|re.I)
                if m:
                    chassisname = m.groups(0)[0]
                if not line.startswith("    "):
                    Class = line[0:5].strip()
                if line.startswith("Temp"):
                    m = re.match(r'Temp\s+(?P<item>[\S|\s|\d]{5,31})\s(?P<status>OK|Absent)\s+(?P<measurement>.*)$', line, re.M|re.I)
                elif line.startswith("Fans"):
                    m = re.match(r'Fans\s+(?P<item>[\S|\s|\d]{5,31})\s(?P<status>OK|Absent)\s+(?P<measurement>.*)$', line, re.M|re.I)
                else:
                    m = re.match(r'\s+(?P<item>[\S|\s|\d]{5,31})\s(?P<status>OK|Absent)\s+(?P<measurement>.*)$', line, re.M|re.I)
                if m:
                    count = 0
                    if Class in self.env_data:
                        count = len(self.env_data[Class])
                    else:
                        self.env_data[Class] = {}
                    self.env_data[Class][count] = m.groupdict()
                    self.env_data[Class][count]["chassisname"] = chassisname
                #else:
                #    print "\n\t\t\t"+self.questions()+"env_data data not found!"+self.questions()
        #self.env_data = self.removeWhiteSpaceFromDict(self.env_data)
        #print json.dumps(self.env_data, indent=4)

    def get_eth_sw_err_age_msg_data(self):
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+ethernet\-switching\\s+statistics\\s+aging.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        output = output.split("\n")
        self.output = output
        record_count = 0
        #print output
        for line in output:
            if line.strip():
                m = re.match(r'Error\s+age\s+messages:\s+(?P<erroragemessages>\d+)', line.strip(), re.M|re.I)
                if m:
                    self.eth_sw_err_age_msg_data[record_count] = m.groupdict()
                    record_count = record_count + 1
        #print json.dumps(self.eth_sw_err_age_msg_data, indent=4)

    def get_eth_sw_stat_maclrnerr_data(self):
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+ethernet\-switching\\s+statistics\\s+mac\-learning.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        output = output.split("\n")
        self.output = output
        record_count = 0
        #print output
        for line in output:
            if line.strip():
                m = re.match(r'Learning stats: \d+\s+.*,\s+(?P<learnerrors>\d+).*,.*', line.strip(), re.M|re.I)
                if m:
                    self.eth_sw_stat_maclrnerr_data[record_count] = m.groupdict()
                    record_count = record_count + 1
        #print json.dumps(self.eth_sw_err_age_msg_data, indent=4)

    def get_eth_sw_tbl_summ_data(self):
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+ethernet\-switching\\s+table\\s+summar.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        output = output.split("\n")
        self.output = output
        record_count = 0
        #print output
        for line in output:
            if line.strip():
                m = re.match(r'Total\s+:\s?(?P<totalentries>\d+)', line.strip(), re.M|re.I)
                if m:
                    self.eth_sw_tbl_summ_data[record_count] = m.groupdict()
                    record_count = record_count + 1
        #print json.dumps(self.eth_sw_tbl_summ_data, indent=4)

    def get_stp_stats_data(self):
        output = ""
        print "hi"
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+spanning\-tree\\s+bridge\\s+brief.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        if output.startswith("Spanning-tree is not enabled at global level."):
            output=['']
        #output = output.split("\n")
        self.output = output
        record_count = 0
        print output
        for line in output.split("\n"):
            if line.strip():
                m = re.match(r'Number\s+of\s+topology\s+changes\s+:\s+(?P<numberoftopologychanges>\d+)', line.strip(), re.M|re.I)
                if m:
                    self.stp_stats_data[record_count] = m.groupdict()
                m = re.match(r'Time\s+since\s+last\s+topology\s+change\s+:\s+(?P<timesincelasttopologychange>\d+)', line.strip(), re.M|re.I)
                if m:
                    self.stp_stats_data[record_count] = m.groupdict()
                record_count = record_count + 1
        print json.dumps(self.stp_stats_data, indent=4)

    def get_fan_data(self):
        # env_data
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+chassis\\s+environment.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        self.output = output
        #print output
        output = output.split("\n")
        self.fan_data = {}
        record_count = 0
        chassisname = ""
        for line in output:
            if line.strip() and not line.strip().startswith("Class"):
                m = re.match(r'(sfc[0-9]+.*:|lcc[0-9]+.*:)', line, re.M|re.I)
                if m:
                    chassisname = m.groups(0)[0]
                if line.startswith("Fans"):
                    m = re.match(r'Fans\s+(?P<fanloc>[\S|\s|\d]{5,31})\s(?P<fanstatus>OK|Absent)\s+Spinning\sat\s(?P<fanspeed>high)\sspeed$', line.strip(), re.M|re.I)
                    if m:
                        self.fan_data[record_count] = m.groupdict()
                        self.fan_data[record_count]["chassiname"] = chassisname
                        record_count += 1
                if line.strip().startswith("Fan"):
                    m = re.match(r'(?P<fanloc>[\S|\s|\d]{5,31})\s(?P<fanstatus>OK|Absent)\s+Spinning\sat\s(?P<fanspeed>high)\sspeed$', line.strip(), re.M|re.I)
                    if m:
                        self.fan_data[record_count] = m.groupdict()
                        self.fan_data[record_count]["chassiname"] = chassisname
                        record_count += 1
        #print json.dumps(self.fan_data, indent=4)

    # For EX only
    def get_fpc_data(self):
        # hi#
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+chassis\\s+fpc\\s+.\\s+display.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                output += line
        #print output
        self.output = output
        soup = BeautifulSoup(output, "lxml")
        i = 0
        for record in soup.findAll("fpc"):
            children = record.findChildren()
            self.fpc_data[i] = {}
            for child in children:
                self.fpc_data[i][child.name.strip().replace("-", "_")] = child.text.strip()
            i += 1

   # For SRX display xml
    def get_ipsec_stats_data(self):
        # hi#
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+security\\s+ipsec\\sstatistics\\s.\\sdisplay\\sxml", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                output += line
        print output
        self.output = output
        chassisname = ""
        soup = BeautifulSoup(output, "lxml")
        output = output.split("\n")
        for line in output:
            if line.strip():
                m = re.match(r'<re-name>(.*)<\/re-name>', line, re.M|re.I)
                if m:
                    chassisname = m.groups(0)[0]
        i = 0
        for record in soup.findAll("usp-ipsec-total-statistics-information"):
            children = record.findChildren()
            self.ipsec_stats_data[i] = {}
            for child in children:
                self.ipsec_stats_data[i][child.name.strip().replace("-", "_")] = child.text.strip()
                self.ipsec_stats_data[i]["chassiname"] = chassisname
            i += 1
        print json.dumps(self.ipsec_stats_data, indent=4)

    def get_krt_q(self):
        # hi#
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+krt\\s+queue.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\sshow.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        self.output = output
        #print output
        output = output.split("\n")
        for line in output:
            if line.strip():
                m = re.match(r'([\w|\s|\-|\/]+):\s(\d+)\squeued.*', line, re.M|re.I)
                if m:
                    self.krt_q[m.groups(0)[0]] = m.groups(0)[1]

    def get_krt_st(self):
        # krt_st
        output = ""
        installJob = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+krt\\s+state.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\sshow.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        #print output
        self.output = output
        output = output.split("\n")

        for line in output:
            if line.strip() and not line.startswith("General state"):
                #print line
                m = re.match(r'Install\s+job\s+is\s+(.*)', line.strip(), re.M|re.I)
                if m:
                    self.krt_st['Install Job is']=m.groups(0)[0]
                    continue
                m = re.match(r'Number\s+of\s+operations\s+queued:\s+([0-9]+)', line.strip(), re.M|re.I)
                if m:
                    self.krt_st['Number of operations queued']=m.groups(0)[0]
                    continue
                m = re.match(r'Routing\s+table\s+adds:\s+([0-9]+)', line.strip(), re.M|re.I)
                if m:
                    self.krt_st['Routing table adds']=m.groups(0)[0]
                    continue
                m = re.match(r'Interface\s+routes:\s+([0-9]+)', line.strip(), re.M|re.I)
                if m:
                    self.krt_st['Interface routes']=m.groups(0)[0]
                    continue
                m = re.match(r'High\s+pri\s+multicast\s+Adds/Changes:\s+([0-9]+)', line.strip(), re.M|re.I)
                if m:
                    self.krt_st['High pri multicast Adds/Changes']=m.groups(0)[0]
                    continue
                m = re.match(r'Indirect\s+Next\s+Hop\s+Adds\/Changes:\s+([0-9]+)\s+Deletes:\s+([0-9]+)', line.strip(), re.M|re.I)
                if m:
                    self.krt_st['Indirect Next Hop Adds/Changes']=m.groups(0)
                    continue
                m = re.match(r'MPLS\s+Adds:\s+([0-9]+)\s+Changes:\s+([0-9]+)', line.strip(), re.M|re.I)
                if m:
                    self.krt_st['MPLS Adds']=m.groups(0)
                    continue
                m = re.match(r'High\s+pri\s+Adds:\s+([0-9]+)\s+Changes:\s+([0-9]+)\s+Deletes:\s+([0-9]+)', line.strip(), re.M|re.I)
                if m:
                    self.krt_st['High pri Adds']=m.groups(0)
                    continue
                m = re.match(r'Normal\s+pri\s+Indirects:\s+([0-9]+)', line.strip(), re.M|re.I)
                if m:
                    self.krt_st['Normal pri Indirects']=m.groups(0)[0]
                    continue
                m = re.match(r'Normal\s+pri\s+Adds:\s+([0-9]+)\s+Changes:\s+([0-9]+)\s+Deletes:\s+([0-9]+)', line.strip(), re.M|re.I)
                if m:
                    self.krt_st['Normal pri Adds']=m.groups(0)
                    continue
                m = re.match(r'Routing\s+Table\s+deletes:\s+([0-9]+)', line.strip(), re.M|re.I)
                if m:
                    self.krt_st['Routing Table deletes']=m.groups(0)[0]
                    continue
                m = re.match(r'Number\s+of\s+operations\s+deferred:\s+([0-9]+)', line.strip(), re.M|re.I)
                if m:
                    self.krt_st['Number of operations deferred']=m.groups(0)[0]
                    continue
                m = re.match(r'Number\s+of\s+operations\s+canceled:\s+([0-9]+)', line.strip(), re.M|re.I)
                if m:
                    self.krt_st['Number of operations canceled']=m.groups(0)[0]
                    continue
                m = re.match(r'Time\s+until\s+next\s+queue\s+run:\s+([0-9]+)', line.strip(), re.M|re.I)
                if m:
                    self.krt_st['Time until next queue run']=m.groups(0)[0]
                    continue
                m = re.match(r'Routes\s+learned\s+from\s+kernel:\s+([0-9]+)', line.strip(), re.M|re.I)
                if m:
                    self.krt_st['Routes learned from kernel']=m.groups(0)[0]
                    continue
                m = re.match(r'Time\s+until\s+next\s+scan:\s+([0-9]+)', line.strip(), re.M|re.I)
                if m:
                    self.krt_st['Time until next scan']=m.groups(0)[0]
                    continue

    def get_mpc_jnh_summ_data(self):
        #    root@ex-8200-sn1> show chassis fabric summary

        #    Plane   State    Uptime
        #     0      Online   127 days, 7 hours, 42 minutes, 20 seconds
        #     1      Online   127 days, 7 hours, 42 minutes, 8 seconds
        #     2      Online   127 days, 7 hours, 42 minutes, 8 seconds
        #     3      Online   127 days, 7 hours, 41 minutes, 53 seconds
        #     4      Spare    127 days, 7 hours, 41 minutes, 36 seconds
        #     5      Spare    127 days, 7 hours, 41 minutes, 31 seconds
        #     6      Spare    127 days, 7 hours, 41 minutes, 31 seconds
        #     7      Spare    127 days, 7 hours, 41 minutes, 28 seconds
        # Note: Regex 2699 perl 2-24

        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+request\\s+pfe\\s+execute\\s+command\\s+\"show\\s+jnh\\s+pool.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        #print output
        chassisname = ""
        output = output.split("\n")
        record_count = 0
        for line in output:
            if line.strip():
                m = re.match(r'(sfc[0-9]+.*:|lcc[0-9]+.*:)', line, re.M|re.I)
                if m:
                    chassisname = m.groups(0)[0]
                m = re.match(r'(?P<plane>\d+)\s+(?P<state>\S+)\s+(?P<uptime>[\S|\s]+)$', line.strip(), re.M|re.I)
                if m:
                    #print m.groupdict(0)
                    self.mpc_jnh_summ_data[record_count] = m.groupdict()
                    record_count = record_count + 1

    def get_nhdb_zones(self):
        #   root@sn-space-mx320-sys> request pfe execute command "show nhdb zones" target fpc0

        #   SENT: Ukern command: show nhdb zones
        #   GOT:
        #   GOT: Chip  Start   Size   Rsvd   Used/Hi Water/Total  Size  Name
        #   GOT: ----  -----  -----  -----  --------------------  ----  ----
        #   GOT:    0  200000  200000  00000           0/0/2097024     1  Multicast Lists
        #   GOT:    0  400000  400000  00200         14/14/4194176     2  L2 Descriptors
        #   GOT:    0  250000  00200  00000                3/3/64     8  L2 Programs
        #   GOT:    1  200000  200000  00000           0/0/2097024     1  Multicast Lists
        #   GOT:    1  400000  400000  00200           0/0/4194176     2  L2 Descriptors
        #   GOT:    1  250000  00200  00000                1/1/64     8  L2 Programs
        #   LOCAL: End of file
        #if self.product.startswith(""):
        output = ""
        device = ""
        devicenum = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\s+request\s+pfe\s+execute\s+command\s+\"show\s+nhdb\s+zones.*", line, re.M | re.I) == None:
                    output = output + line
                    break
            for line in fopen:
                if not re.match(".*@.*>\s+show\s.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        #print output
        chassisname = ""
        output = output.split("\n")
        self.output = output
        record_count = 0
        for line in output:
            if line.strip():
                m = re.match(r'(sfc[0-9]+.*:|lcc[0-9]+.*:)', line, re.M|re.I)
                if m:
                    chassisname = m.groups(0)[0]
                m = re.match(".*@.*>\\s+request\\s+pfe\\s+execute\\s+command\\s+\"show\\s+nhdb\\s+zones.*target\\s+([a-z]+)(\d+)$", line, re.M | re.I)
                if m:
                    device = m.groups(0)[0]
                    devicenum = m.groups(0)[1]
                m = re.match(r'\S+:\s+(?P<nhdbchip>\d+)\s+(?P<nhdbstart>\d+)\s+(?P<nhdbsize1>\d+)\s+(?P<nhdbrsvd>\d+)\s+(?P<nhdbused>\d+)/(?P<nhdbhiwater>\d+)/(?P<nhdbtotal>\d+)\s+(?P<nhdbsize2>\d+)\s+(?P<nhdbname>.*)$', line.strip(), re.M|re.I)
                if m:
                    self.nhdb_zones[record_count] = m.groupdict()
                    self.nhdb_zones[record_count]["device"] = device
                    self.nhdb_zones[record_count]["devicenum"] = devicenum
                    self.nhdb_zones[record_count]["chassisname"] = chassisname
                    record_count += 1

    def get_pfe_st_notif_data(self):
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+pfe\\s+statistics\\s+notification.*", line, re.M | re.I) == None:
                    output = output + line
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        #print output
        output = output.split("\n")
        record_count = 0
        self.pfe_st_notif_data[record_count] = {}
        for line in output:
           if line.strip():
                m = re.match(r'(?P<illegal>[0-9]+)\s+illegal', line.strip(), re.M|re.I)
                if m:
                    self.pfe_st_notif_data[record_count]["illegal"] = m.groupdict(0)["illegal"]
                m = re.match(r'(?P<dma_failure>[0-9]+)\s+DMA\s+failure', line.strip(), re.M|re.I)
                if m:
                    self.pfe_st_notif_data[record_count]["dma_failure"] = m.groupdict(0)["dma_failure"]
                m = re.match(r'Illegal\s+[0-9]+\s+[0-9]+\s+(?P<illegal_failed>[0-9]+)\s+[0-9]+', line.strip(), re.M|re.I)
                if m:
                    self.pfe_st_notif_data[record_count]["illegal_failed"] = m.groupdict(0)["illegal_failed"]
                m = re.match(r'Unclass\s+[0-9]+\s+[0-9]+\s+(?P<unclass_failed>[0-9]+)\s+[0-9]+', line.strip(), re.M|re.I)
                if m:
                    self.pfe_st_notif_data[record_count]["unclass_failed"] = m.groupdict(0)["unclass_failed"]
                m = re.match(r'Option\s+[0-9]+\s+[0-9]+\s+(?P<option_failed>[0-9]+)\s+[0-9]+', line.strip(), re.M|re.I)
                if m:
                    self.pfe_st_notif_data[record_count]["option_failed"] = m.groupdict(0)["option_failed"]
                m = re.match(r'Next-Hop\s+[0-9]+\s+[0-9]+\s+(?P<nexthop_failed>[0-9]+)\s+[0-9]+', line.strip(), re.M|re.I)
                if m:
                    self.pfe_st_notif_data[record_count]["nexthop_failed"] = m.groupdict(0)["nexthop_failed"]
                m = re.match(r'Discard\s+[0-9]+\s+[0-9]+\s+(?P<discard_failed>[0-9]+)\s+[0-9]+', line.strip(), re.M|re.I)
                if m:
                    self.pfe_st_notif_data[record_count]["discard_failed"] = m.groupdict(0)["discard_failed"]
                m = re.match(r'Sample\s+[0-9]+\s+[0-9]+\s+(?P<sample_failed>[0-9]+)\s+[0-9]+', line.strip(), re.M|re.I)
                if m:
                    self.pfe_st_notif_data[record_count]["sample_failed"] = m.groupdict(0)["sample_failed"]
                m = re.match(r'Redirect\s+[0-9]+\s+[0-9]+\s+(?P<redirect_failed>[0-9]+)\s+[0-9]+', line.strip(), re.M|re.I)
                if m:
                    self.pfe_st_notif_data[record_count]["redirect_failed"] = m.groupdict(0)["redirect_failed"]
                m = re.match(r'DontFrag\s+[0-9]+\s+[0-9]+\s+(?P<dontfrag_failed>[0-9]+)\s+[0-9]+', line.strip(), re.M|re.I)
                if m:
                    self.pfe_st_notif_data[record_count]["dontfrag_failed"] = m.groupdict(0)["dontfrag_failed"]
                m = re.match(r'cfDF\s+[0-9]+\s+[0-9]+\s+(?P<cfdf_failed>[0-9]+)\s+[0-9]+', line.strip(), re.M|re.I)
                if m:
                    self.pfe_st_notif_data[record_count]["cfdf_failed"] = m.groupdict(0)["cfdf_failed"]
                m = re.match(r'Poison\s+[0-9]+\s+[0-9]+\s+(?P<poison_failed>[0-9]+)\s+[0-9]+', line.strip(), re.M|re.I)
                if m:
                    self.pfe_st_notif_data[record_count]["poison_failed"] = m.groupdict(0)["poison_failed"]
                m = re.match(r'MemPkt\s+[0-9]+\s+[0-9]+\s+(?P<mempkt_failed>[0-9]+)\s+[0-9]+', line.strip(), re.M|re.I)
                if m:
                    self.pfe_st_notif_data[record_count]["mempkt_failed"] = m.groupdict(0)["mempkt_failed"]
                m = re.match(r'Autoconf\s+[0-9]+\s+[0-9]+\s+(?P<autoconf_failed>[0-9]+)\s+[0-9]+', line.strip(), re.M|re.I)
                if m:
                    self.pfe_st_notif_data[record_count]["autoconf_failed"] = m.groupdict(0)["autoconf_failed"]
                m = re.match(r'Reject\s+[0-9]+\s+[0-9]+\s+(?P<reject_failed>[0-9]+)\s+[0-9]+', line.strip(), re.M|re.I)
                if m:
                    self.pfe_st_notif_data[record_count]["reject_failed"] = m.groupdict(0)["reject_failed"]
        #print json.dumps(self.pfe_st_notif_data, indent=4)


    def get_pfe_tr_data(self):
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+pfe\\s+statistics\\s+traffic", line, re.M | re.I) == None:
                    output = output + line
                    break
                if line.startswith("[----BEGIN"):
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        #print output
        self.output = output
        chassisname = ""
        record_count = 0
        output = output.split("\n")
        self.pfe_tr_data[record_count] = {}
        for line in output:
           if line.strip():
                m = re.match(r'(sfc[0-9]+.*:|lcc[0-9]+.*:)', line, re.M|re.I)
                if m:
                    chassisname = m.groups(0)[0]
                m = re.match(r'([\S|\s]+):\s+(\d+)\s+(\d+)\spps', line.strip(), re.M|re.I)
                if m:
                    self.pfe_tr_data[record_count][m.groups(0)[0].strip()] = m.groups(0)[1].strip()
                    self.pfe_tr_data[record_count][m.groups(0)[0].strip()+" PPS"] = m.groups(0)[2].strip()
                m = re.match(r'([\S|\s]+):\s+(\d+)$', line.strip(), re.M|re.I)
                if m:
                    self.pfe_tr_data[record_count][m.groups()[0].strip()] = m.groups(0)[1].strip()
        #print json.dumps(self.pfe_tr_data, indent=4, sort_keys=True)

    def get_proc_mem_data(self):
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+system\\s+processes\\s+extensive.*", line, re.M | re.I) == None:
                    output = output + line
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        #print output
        self.output = output
        chassisname = ""
        record_count = -1
        output = output.split("\n")
        for line in output:
           if line.strip():
                m = re.match(r'(sfc[0-9]+.*:|lcc[0-9]+.*:)', line, re.M|re.I)
                if m:
                    chassisname = m.groups(0)[0]
                m = re.match(r'Mem:\s+(?P<activemem>\d+)M\s+\S+\s(?P<inactmem>\d+)M\s+\S+\s(?P<wiredmem>\d+)M\s\S+\s(?P<cachemem>\d+)M\s\S+\s(?P<bufmem>\d+)M\s+\S+\s(?P<freemem>\d+)M.*', line.strip(), re.M|re.I)
                if m:
                    record_count = record_count + 1
                    self.proc_mem_data[record_count] = {}
                    self.proc_mem_data[record_count]["activemem"] = int(m.groupdict(0)["activemem"]) * 1000 * 1000
                    self.proc_mem_data[record_count]["inactmem"] = int(m.groupdict(0)["inactmem"]) * 1000 * 1000
                    self.proc_mem_data[record_count]["wiredmem"] = int(m.groupdict(0)["wiredmem"]) * 1000 * 1000
                    self.proc_mem_data[record_count]["cachemem"] = int(m.groupdict(0)["cachemem"]) * 1000 * 1000
                    self.proc_mem_data[record_count]["bufmem"] = int(m.groupdict(0)["bufmem"]) * 1000 * 1000
                    self.proc_mem_data[record_count]["freemem"] = int(m.groupdict(0)["freemem"]) * 1000 * 1000
                    self.proc_mem_data[record_count]["totalmem"] = (int(m.groupdict(0)["activemem"] )+int( m.groupdict(0)["inactmem"] )+int( m.groupdict(0)["wiredmem"] )+int( m.groupdict(0)["cachemem"] )+int( m.groupdict(0)["freemem"])) * 1000 * 1000
                    self.proc_mem_data[record_count]["usedmem"] = (int(m.groupdict(0)["activemem"] )+int( m.groupdict(0)["inactmem"] )+int( m.groupdict(0)["wiredmem"] )) * 1000 * 1000
                    #self.proc_mem_data[record_count]["usedmempercentage"] = int(self.proc_mem_data[record_count]["usedmem"]) * 100 / int(self.proc_mem_data[record_count]["totalmem"])
                    self.proc_mem_data[record_count]["usedmempercentage"] = int(math.floor((float(self.proc_mem_data[record_count]["usedmem"]) * 100) / float(self.proc_mem_data[record_count]["totalmem"])))
                    self.proc_mem_data[record_count]["chassisname"] = chassisname
                    #print math.floor(float(self.proc_mem_data[record_count]["usedmem"]) * 100 / (float(self.proc_mem_data[record_count]["totalmem"])))
                m = re.match(r'Swap:\s+(?P<swap_total>\d+)M\s+\S+\s(?P<swap_free>\d+)M\s+.*', line.strip(), re.M|re.I)
                if m:
                    self.proc_mem_data[record_count]["swap_total"] = int( m.groupdict(0)["swap_total"] ) * 1000 * 1000
                    self.proc_mem_data[record_count]["swap_free"] = int( m.groupdict(0)["swap_free"] ) * 1000 * 1000
        #print json.dumps(self.proc_mem_data, indent=4)

    def get_ps_data(self):
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+system\\s+processes\\s+extensive.*", line, re.M | re.I) == None:
                    output = output + line
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        #print output
        chassisname = ""
        output = output.split("\n")
        record_count = 0
        for line in output:
           if line.strip():
                m = re.match(r'(sfc[0-9]+.*:|lcc[0-9]+.*:)', line, re.M|re.I)
                if m:
                    chassisname = m.groups(0)[0]
                m = re.match(r'(?P<pid>\d+)\s+(?P<username>\S+)\s+(?P<thr>\d+)\s+(?P<pri>\d+)\s+(?P<nice>\S+)\s+(?P<size>\S+)\s+(?P<res>\S+)\s+(?P<state>\S+)\s+(?P<time>\S+)\s+(?P<wcpu>\S+)%\s+(?P<command>(chassisd)|(dfwd)|(mib2d)|(pfed)|(rpd)|(sampled)|(snmpd)|(dswd)|(dcd)|(cosd)|(mgd)|(ksyncd)|(ppmd)|(rtspd)|(l2ald))', line.strip(), re.M|re.I)
                if m:
                    self.ps_data[record_count] = m.groupdict()
                    self.ps_data[record_count]["chassisname"] = chassisname
                    record_count += 1
                    #print m.groupdict()

    def get_pwr_data(self):
        # env_data
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+chassis\\s+environment.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        #print output
        self.output = output
        output = output.split("\n")
        self.pwr_data = {}
        record_count = 0
        chassisname = ""
        for line in output:
            if line.strip() and not line.strip().startswith("Class"):
                m = ""
                m = re.match(r'(sfc[0-9]+.*:|lcc[0-9]+.*:)', line, re.M|re.I)
                if m:
                    chassisname = m.groups(0)[0]
                if line.startswith("Power"):
                    m = re.match(r'Power\s+(?P<item>[\S|\s|\d]{5,31})\s(?P<status>OK|Absent)\s*(?P<measurement>.*)$', line.strip(), re.M|re.I)
                    if m:
                        self.pwr_data[record_count] = m.groupdict()
                        self.pwr_data[record_count]["chassiname"] = chassisname
                        record_count += 1
                else:
                    m = re.match(r'(?P<item>P[\S|\s|\d]{5,31})\s(?P<status>OK|Absent)\s*(?P<measurement>.*)$', line.strip(), re.M|re.I)
                    if m:
                        self.pwr_data[record_count] = m.groupdict()
                        self.pwr_data[record_count]["chassiname"] = chassisname
                        record_count += 1
        #self.pwr_data = self.removeWhiteSpaceFromDict(self.pwr_data)
        #print json.dumps(self.pwr_data, indent=4)

    def get_routing_engine_data(self):
        # hi#
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+chassis\\s+routing-engine.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                output = output + line
        self.output = output
        rename = ""
        for line in output.split("\n"):
            m = re.match(r"<re-name>(.*)<\/re-name>", line.strip(), re.I | re.M)
            if m:
                rename = m.groups(0)[0]
        soup = BeautifulSoup(output, "lxml")
        i = 0
        for record in soup.findAll("route-engine"):
            children = record.findChildren()
            self.re_data[i] = {}
            for child in children:
                self.re_data[i][child.name.strip().replace("-", "_")] = child.text.strip()
            self.re_data[i]['rename'] = rename
            i += 1
        #print json.dumps(self.re_data, indent=4)

    def get_rt_sum_data(self):
        # hi#
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+route\\s+summary\\s+.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        #print output
        output = output.split("\n")
        chassisname = ""
        self.output = output
        for line in output:
            if line.strip():
                m = ""
                m = re.match(r'(sfc[0-9]+.*:|lcc[0-9]+.*:)', line, re.M|re.I)
                if m:
                    chassisname = m.groups(0)[0]
                if line.startswith("inet"):
                    #inet.0: 8 destinations, 8 routes (8 active, 0 holddown, 0 hidden) Limit/Threshold: 16384/16384 destinations
                    m = re.match(r'(inet\..*):\s+([0-9]+)\s+destinations,\s+([0-9]+)\s+routes\s+\(([0-9]+)\s+active,\s+([0-9]+)\s+holddown,\s+([0-9]+)\s+hidden\).*', line, re.M | re.I)
                    if m:
                        self.rt_sum_data['routetable'] = m.groups(0)[0]
                        self.rt_sum_data['destinations'] = m.groups(0)[1]
                        self.rt_sum_data['routes'] = m.groups(0)[2]
                        self.rt_sum_data['active'] = m.groups(0)[3]
                        self.rt_sum_data['holddown'] = m.groups(0)[4]
                        self.rt_sum_data['hidden'] = m.groups(0)[5]
                        self.rt_sum_data['chassisname'] = chassisname

    def get_sec_alg_st_data(self):
        # hi#
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+security\\s+alg\\sstatus\\s.\\sdisplay\\sxml", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.startswith("[----BEGIN"):
                        break
                output += line
        print output
        soup = BeautifulSoup(output, "lxml")
        self.output = output
        i = 0
        for record in soup.findAll("alg-status"):
            children = record.findChildren()
            self.sec_alg_st_data[i] = {}
            for child in children:
                self.sec_alg_st_data[i][child.name.strip().replace("-", "_")] = child.text.strip()
            i += 1
        print json.dumps(self.sec_alg_st_data, indent=4)

    def get_sec_nat_intf_nat_prts_data(self):
        # hi#
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+security\\s+nat\\sinterface\-nat\-ports.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.startswith("[----BEGIN"):
                        break
                output += line
        soup = BeautifulSoup(output, "lxml")
        self.output = output
        rename = ""
        for line in output.split("\n"):
            m = re.match(r"<re-name>(.*)<\/re-name>", line.strip(), re.I | re.M)
            if m:
                rename = m.groups(0)[0]
        i = 0
        for record in soup.findAll("interface-nat-ports-entry"):
            children = record.findChildren()
            self.sec_nat_intf_nat_prts_data[i] = {}
            for child in children:
                self.sec_nat_intf_nat_prts_data[i][child.name.strip().replace("-", "_")] = child.text.strip()
                self.sec_nat_intf_nat_prts_data[i]["rename"] = rename
            i += 1
        #print json.dumps(self.sec_nat_intf_nat_prts_data, indent=4)

    def get_sec_utm_aspam_stats_data(self):
        # hi#
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+security\\s+utm\\santi\-spam\\s+statistics\\s.\\sdisplay\\sxml", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.startswith("[----BEGIN"):
                        break
                output += line
        #print output
        soup = BeautifulSoup(output, "lxml")
        self.output = output
        i = 0
        for record in soup.findAll("anti-spam-statistics"):
            children = record.findChildren()
            self.sec_utm_aspam_stats_data[i] = {}
            for child in children:
                self.sec_utm_aspam_stats_data[i][child.name.strip().replace("-", "_")] = child.text.strip()
            i += 1
        #print json.dumps(self.sec_utm_aspam_stats_data, indent=4)

    def get_sec_utm_av_st_data(self):
        # hi#
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+security\\s+utm\\santi\-virus\\s+status\\s.\\sdisplay\\sxml", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.startswith("[----BEGIN"):
                        break
                output += line
        #print output
        soup = BeautifulSoup(output, "lxml")
        self.output = output
        i = 0
        for record in soup.findAll("anti-virus-status"):
            children = record.findChildren()
            self.sec_utm_av_st_data[i] = {}
            for child in children:
                self.sec_utm_av_st_data[i][child.name.strip().replace("-", "_")] = child.text.strip()
            i += 1
        #print json.dumps(self.sec_utm_av_st_data, indent=4)

    def get_sec_utm_av_stats_data(self):
        # hi#
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+security\\s+utm\\santi\-virus\\s+statistics\\s.\\sdisplay\\sxml", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.startswith("[----BEGIN"):
                        break
                output += line
        #print output
        soup = BeautifulSoup(output, "lxml")
        self.output = output
        i = 0
        for record in soup.findAll("anti-virus-statistics"):
            children = record.findChildren()
            self.sec_utm_av_stats_data[i] = {}
            for child in children:
                self.sec_utm_av_stats_data[i][child.name.strip().replace("-", "_")] = child.text.strip()
            i += 1
        #print json.dumps(self.sec_utm_av_stats_data, indent=4)

    def get_sec_utm_st_data(self):
        # hi#
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+security\\s+utm\\sstatus\\s.\\sdisplay\\sxml", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.startswith("[----BEGIN"):
                        break
                output += line
        #print output
        soup = BeautifulSoup(output, "lxml")
        self.output = output
        i = 0
        for record in soup.findAll("utmd-status"):
            children = record.findChildren()
            self.sec_utm_st_data[i] = {}
            for child in children:
                self.sec_utm_st_data[i][child.name.strip().replace("-", "_")] = child.text.strip()
            i += 1
        #print json.dumps(self.sec_utm_st_data, indent=4)

    def get_sec_utm_web_st_data(self):
        # hi#
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s*show\\s+security\\s+utm\\s+web\-filtering\\sstatus\\s.\\sdisplay\\sxml", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.startswith("[----BEGIN"):
                        break
                output += line
        #print output
        soup = BeautifulSoup(output, "lxml")
        self.output = output
        i = 0
        for record in soup.findAll("utmd-web-filtering-status"):
            children = record.findChildren()
            self.sec_utm_web_st_data[i] = {}
            for child in children:
                self.sec_utm_web_st_data[i][child.name.strip().replace("-", "_")] = child.text.strip()
            i += 1
        #print json.dumps(self.sec_utm_web_st_data, indent=4)

    def get_sec_utm_web_stat_data(self):
        # hi#
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s*show\\s+security\\s+utm\\s+web\-filtering\\sstatistics\\s.\\sdisplay\\sxml", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.startswith("[----BEGIN"):
                        break
                output += line
        #print output
        soup = BeautifulSoup(output, "lxml")
        self.output = output
        i = 0
        for record in soup.findAll("utmd-web-filtering-statistics"):
            children = record.findChildren()
            self.sec_utm_web_stat_data[i] = {}
            for child in children:
                self.sec_utm_web_stat_data[i][child.name.strip().replace("-", "_")] = child.text.strip()
            i += 1
        #print json.dumps(self.sec_utm_web_stat_data, indent=4)

    def get_sh_mem_frag_data(self):
        # sh_mem_frag_data
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+task\\s+memory\\s+fragmentation.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\sshow.*", line, re.M | re.I) == None:
                    break
                if line.startswith("[----BEGIN"):
                    break
                output = output + line
        #print output
        self.output = output
        output = output.split("\n")
        record_count = 0
        for line in output:
            if line.strip():
                m = re.match(r'\s?(?P<alloctype>\S+):\spages\sin\suse\s+(?P<pages_in_use>\d+)\s+pages\sneeded\s(?P<pages_needed>[\d|.]+)\s+fragmentation\s(?P<frag>[\d|.]+)%.*', line, re.M|re.I)
                if m:
                    self.sh_mem_frag_data[record_count]=m.groups(0)
                    record_count += 1

    def get_stp_stats_data(self):
        output = ""
        print "hi1"
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+spanning\-tree\\s+bridge\\s+brief.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                output = output + line
        if output.startswith("Spanning-tree is not enabled at global level."):
            output=['']
        #
        self.output = output
        record_count = 0
        #print output
        output = output.split("\n")
        #print("hi")
        self.stp_stats_data[record_count] = {}
        for line in output:
            if line.strip():
                m = re.match(r'Number\s+of\s+topology\s+changes\s+:\s+(\d+)', line.strip(), re.M|re.I)
                if m:
                    self.stp_stats_data[record_count]["numberoftopologychanges"] = m.groups(0)[0]
                m = re.match(r'Time\s+since\s+last\s+topology\s+change\s+:\s+(\d+)', line.strip(), re.M|re.I)
                if m:
                    self.stp_stats_data[record_count]["timesincelasttopologychange"] = m.groups(0)[0]
                    record_count = record_count + 1
        #print json.dumps(self.stp_stats_data, indent=4)

    def get_sys_cores_data(self):
        # hi#
        output_type = ""
        output = ""
        if self.product.startswith("MX") or self.product.startswith("EX"):
            with open(self.file_name, "rb") as fopen:
                for line in fopen:
                    if not re.match(".*@.*>\\s+show\\s+system\\s+core-dumps\\s+no-forwarding.*", line, re.M | re.I) == None:
                        break
                for line in fopen:
                    if not re.match(".*@.*>\\sshow.*", line, re.M | re.I) == None:
                        break
                    if line.startswith("[----BEGIN"):
                        break
                    output = output + line
            output = output.split("\n")
            self.output = output
            record_count = 0
            chassisname = ""
            for line in output:
                if line.strip():
                    m = re.match(r'(?P<chassisname>[sfc[0-9]+.*:|lcc[0-9]+.*:|fpc[0-9]+.*:])', line, re.M | re.I)
                    if m:
                        chassisname = m.groups(0)[0]
                    m = re.match(r".*@.*>\s+show\s+system\s+statistics\s(.+)", line, re.M | re.I)
                    #m = re.match(r'\s?(?P<alloctype>\S+):\spages\sin\suse\s+(?P<pages_in_use>\d+)\s+pages\sneeded\s(?P<pages_needed>[\d|.]+)\s+fragmentation\s(?P<frag>[\d|.]+)%.*', line, re.M|re.I)
                    m = re.match(r'.*\s(?P<user>[a-zA-Z]+)\s+[a-zA-Z]+\s+(?P<size>[0-9]+)\s+(?P<date>.*)(?P<location>[a-zA-Z0-9]*\s+\/.*)', line, re.M | re.I)
                    if m:
                        self.sys_cores_data[record_count]=m.groupdict()
                        self.sys_cores_data[record_count]['chassisname']=chassisname
                        record_count = record_count + 1

    def get_sys_license_data(self):
        # hi#
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+system\\s+license\\s.\\sdisplay\\sxml", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.startswith("[----BEGIN"):
                        break
                output += line
        #print output
        self.output = output
        soup = BeautifulSoup(output, "lxml")
        i = 0
        for record in soup.findAll("license"):
            children = record.findChildren()
            self.sys_license_data[i] = {}
            for child in children:
                self.sys_license_data[i][child.name.strip().replace("-", "_")] = child.text.strip()
            i += 1
        #print json.dumps(self.sys_license_data, indent=4)

    # Only for SRX
    def get_sys_stats_data(self):
        output_text = ""
        hit = 0
        option = ""
        output = ""
        chassisname = ""
        self.sys_stats_data = {}
        i = 0
        first = 0
        with open(self.file_name, "rb+") as fopen:
            for line in fopen:
                m = re.match(r'(?P<chassisname>[sfc[0-9]+.*:|lcc[0-9]+.*:|fpc[0-9]+.*:])', line, re.M | re.I)
                if m:
                    chassisname = m.groups(0)[0]
                m = re.match(r".*@.*>\s+show\s+system\s+statistics\s+(.+)", line, re.M | re.I)
                if m:
                    hit = 1
                    self.sys_stats_data[i] = {}
                    self.sys_stats_data[i][str(option).strip()] = {}
                    self.sys_stats_data[i][str(option).strip()] = output_text
                    option = m.groups(0)[0]
                    output_text = ""
                    output_text += line
                    i = i + 1
                else:
                    output_text = output_text + line


    def get_sys_stor_data(self):
        # hi#
        output = ""
        if self.product.startswith("MX") or self.product.startswith("EX") or True:
            with open(self.file_name, "rb") as fopen:
                for line in fopen:
                    if not re.match(".*@.*>\\s+show\\s+system\\s+storage\\s+.*", line, re.M | re.I) == None:
                        break
                for line in fopen:
                    if not re.match(".*@.*>\\sshow.*", line, re.M | re.I) == None:
                        break
                    if line.startswith("[----BEGIN"):
                        break
                    output = output + line
            output = output.split("\n")
            self.output = output
            record_count = 0
            chassisname = ""
            for line in output:
                if line.strip():
                    #m = re.match(r'\s?(?P<alloctype>\S+):\spages\sin\suse\s+(?P<pages_in_use>\d+)\s+pages\sneeded\s(?P<pages_needed>[\d|.]+)\s+fragmentation\s(?P<frag>[\d|.]+)%.*', line, re.M|re.I)
                    m = re.match(r'(?P<chassisname>[sfc[0-9]+.*:|lcc[0-9]+.*:|fpc[0-9]+.*:])', line, re.M | re.I)
                    if m:
                        chassisname = m.groups(0)[0]
                    m = re.match(r'(?P<filesystem>.*)\s+(?P<size>[0-9\.]+[BKMG])\s+(?P<used>[0-9\.]+[BKMG])\s+(?P<avail>[0-9\.]+[BKMG])\s+(?P<capacity>[0-9]+)%\s+(?P<location>.*)', line, re.M | re.I)
                    if m:
                        tmp = m.groups(0)
                        tmp = list(tmp)
                        tmp.append(chassisname)
                        self.sys_stor_data[record_count]=tuple(tmp)
                        record_count = record_count + 1

    ''' Old only for tabular
    def get_sys_ver_data(self):
        # hi#
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+\\s+version\\s+no.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not line.strip() == "":
                    if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                        break
                    output = output + line
        output = output.split("\n")
        self.output = output
        chassisname = ""
        for line in output:
            m = re.match(r'(?P<chassisname>[sfc[0-9]+.*:|lcc[0-9]+.*:|fpc[0-9]+.*:])', line, re.M | re.I)
            if m:
                chassisname = m.groups(0)[0]
            m = re.match(r'([a-z]+):(.*)', line, re.M | re.I)
            if m:
                self.sys_ver_data[m.groups(0)[0].strip()] = m.groups(0)[1].strip()
                self.sys_ver_data['chassisname'] = chassisname
            m = re.match(r'(.*)\[(.*)\]', line, re.M | re.I)
            if m:
                self.sys_ver_data[m.groups(0)[0].strip()] = m.groups(0)[1]
                self.sys_ver_data['chassisname'] = chassisname
                continue'''

    def get_sys_ver_data(self):
        # sys_ver_data
        # For xml and Tabular
        output = ""
        output_type = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+\\s+version\\s+no.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not line.strip() == "":
                    if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                        break
                    output += line
        if not output:
            with open(self.file_name, "rb") as fopen:
                for line in fopen:
                    if not re.match(".*@.*>\\s+show\\s+\\s+version\\s+.\\s+display.*", line, re.M | re.I) == None:
                        output_type = "xml"
                        break
                for line in fopen:
                    if not line.strip() == "":
                        if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                            break
                        output += line
        self.output = output
        chassisname = ""
        if output_type == "xml":
            soup = BeautifulSoup(output, "lxml")
            for record in soup.findAll("comment"):
                output = record.text.strip()
                output = output.split("\n")
                for line in output:
                    m = re.match(r'(.*) \[(.*)\]', line.strip(), re.M|re.I)
                    if m:
                        self.sys_ver_data[m.groups(0)[0]]=m.groups(0)[1]
                        continue
        else:
            output = output.split("\n")
            for line in output:
                m = re.match(r'(?P<chassisname>[sfc[0-9]+.*:|lcc[0-9]+.*:|fpc[0-9]+.*:])', line, re.M | re.I)
                if m:
                    chassisname = m.groups(0)[0]
                m = re.match(r'JUNOS Packet Forwarding Engine Support.*\[(.*)\]', line, re.M | re.I)
                if m:
                    self.sys_ver_data["JUNOS Packet Forwarding Engine Support"] = m.groups(0)[0].strip()
                m = re.match(r'([a-z]+):(.*)', line, re.M | re.I)
                if m:
                    self.sys_ver_data[m.groups(0)[0].strip()] = m.groups(0)[1].strip()
                    self.sys_ver_data['chassisname'] = chassisname
                m = re.match(r'(.*)\[(.*)\]', line, re.M | re.I)
                if m:
                    self.sys_ver_data[m.groups(0)[0].strip()] = m.groups(0)[1].strip()
                    self.sys_ver_data['chassisname'] = chassisname

    def get_sys_vm_swap(self):
        # hi#
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+system\\s+virtual.memory.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not line.strip() == "":
                    if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                        break
                    output = output + line
        chassisname = ""
        output = output.split("\n")
        self.output = output
        for line in output:
            m = re.match(r'(sfc[0-9]+.*:|lcc[0-9]+.*:)', line, re.M | re.I)
            if m:
                chassisname = m.groups(0)[0]
            m = re.match(r'\s+(\d+)\s+(swap.*)$', line, re.M | re.I)
            if m:
                self.sys_vm_swap[m.groups(0)[1].strip()] = m.groups(0)[0]
            m = re.match(r'\s+([\d])\s+(peak\s+swap\s+pages\s+used)$', line, re.M | re.I)
            if m:
                self.sys_vm_swap[m.groups(0)[1].strip()] = m.groups(0)[0]
        self.sys_vm_swap["chassisname"] = chassisname

    def get_task_io_data(self):
        # hi#
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+task\\s+io.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\sshow.*", line, re.M | re.I) == None:
                    break
                output += line
        self.output = output
        output = output.split("\n")
        record_count = 0
        for line in output:
            m = re.match(r'(?P<taskname>.+)\s+(?P<reads>[0-9]+)\s+(?P<writes>[0-9]+)\s+(?P<rcvd>[0-9]+)\s+(?P<sent>[0-9]+)\s+(?P<dropped>[0-9]+)', line.strip(), re.M | re.I)
            if m:
                self.task_io_data[record_count]=m.groupdict(0)
                #print json.dumps(m.groupdict(), indent=4)
                record_count += 1


    def get_task_mem_data(self):
        #  root@mx-480-sn2> show task memory
        #
        #  Memory                 Size (kB)  Percentage  When
        #  Currently In Use:         7897          0%  now
        #  Maximum Ever Used:        8094          0%  15/08/05 13:38:52
        #  Available:             2011070        100%  now

        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+task\\s+memory.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not line.strip() == "":
                    if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                        break
                    output = output + line
        chassisname = ""
        output = output.split("\n")
        self.output = output
        record_count = 0
        for line in output:
            m = re.match(r'(sfc[0-9]+.*:|lcc[0-9]+.*:)', line, re.M | re.I)
            if m:
                chassisname = m.groups(0)[0]
            m = re.match(r'\s+(?P<Memory>[\S|\s]+):\s+(?P<Sizekb>\d+)\s+(?P<Percentage>\d+)%\s+(?P<When>.*)$', line, re.M | re.I)
            if m:
                tmp = m.groupdict()
                tmp["chassisname"] = chassisname
                self.task_mem_data[record_count] = tmp
                record_count += 1


    def get_ukern_trace_mem_comp_data(self):
        # root@mx-480-sn2> request pfe execute command "show ukern_trace memory-composition" target fpc4

        # SENT: Ukern command: show ukern_trace memory-composition
        # GOT:
        # GOT: Name                                   Bytes        Allocs         Frees   Failures
        # GOT: ------------------------------------------------------------------------------------
        # GOT: ifd                                     2808            27             0          0
        # GOT: ifd-halp                                4032            28             0          0
        # GOT: ifl                                    22896            58             0          0
        # GOT: ifl-halp                               15872            95             2          0

        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+request\\s+pfe\\s+execute\\s+command\\s+\"show\\s+ukern.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        chassisname = ""
        output = output.split("\n")
        self.output = output
        record_count = 0
        for line in output:
            if line.strip():
                m = re.match(r'(sfc[0-9]+.*:|lcc[0-9]+.*:)', line, re.M|re.I)
                if m:
                    chassisname = m.groups(0)[0]
                m = re.match(r'\S+\s(?P<name>\w+)\s+(?P<bytes>\d+)\s+(?P<allocs>\d+)\s+(?P<frees>\d+)\s+(?P<failures>\d+)', line, re.M|re.I)
                if m:
                    self.ukern_trace_mem_comp_data[record_count] = m.groupdict()
                    record_count = record_count + 1
        #self.ukern_trace_mem_comp_data['chassisname'] = chassisname

    def get_up_data(self):
        #  root@sn-space-mx320-sys> show system uptime no-forwarding

        #  Current time: 2015-08-11 01:19:52 UTC
        #  System booted: 2015-06-05 08:34:34 UTC (9w3d 16:45 ago)
        #  Protocols started: 2015-06-05 08:35:42 UTC (9w3d 16:44 ago)
        #  Last configured: 2015-08-03 09:32:16 UTC (1w0d 15:47 ago) by root
        #  1:19AM  up 66 days, 16:45, 0 users, load averages: 0.75, 0.44, 0.26

        #  root@sn-space-mx320-sys> show system uptime

        #  Current time: 2015-08-11 01:20:42 UTC
        #  System booted: 2015-06-05 08:34:34 UTC (9w3d 16:46 ago)
        #  Protocols started: 2015-06-05 08:35:42 UTC (9w3d 16:45 ago)
        #  Last configured: 2015-08-03 09:32:16 UTC (1w0d 15:48 ago) by root
        #  1:20AM  up 66 days, 16:46, 0 users, load averages: 0.30, 0.36, 0.24

        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+system\\s+uptime.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        chassisname = ""
        output = output.split("\n")
        self.output = output
        self.up_data = {}
        for line in output:
            if line.strip():
                m = re.match(r'(sfc[0-9]+.*:|lcc[0-9]+.*:)', line, re.M|re.I)
                if m:
                    chassisname = m.groups(0)[0]
                m = re.match(r'(?P<key>\S+\s\S+):\s(?P<value>.*PDT)', line, re.M|re.I)
                if m:
                    self.up_data[m.groupdict()['key']] = m.groupdict()['value']
                m = re.match(r'System[ \t]+booted:[ \t]*([-0-9]+)[ \t]([:0-9]+)', line, re.M|re.I)
                if m:
                    self.up_data['system_booted_date'] = m.groups(0)[0]
                    self.up_data['system_booted_time'] = m.groups(0)[1]
                    multichassis = 0
                    continue
                m = re.match(r'Protocols[ \t]+started:[ \t]*([-0-9]+)[ \t]([:0-9]+)', line, re.M|re.I)
                if m:
                    self.up_data['protocols_started_date'] = m.groups(0)[0]
                    self.up_data['protocols_started_time'] = m.groups(0)[1]
                    continue
                m = re.match(r'Last[ \t]+configured:[ \t]*([-0-9]+)[ \t]([:0-9]+)', line, re.M|re.I)
                if m:
                    self.up_data['last_configured_date'] = m.groups(0)[0]
                    self.up_data['last_configured_time'] = m.groups(0)[1]
        self.up_data['chassisname'] = chassisname


    def get_vc_prtcl_adj_data(self):
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+virtual\-chassis\\s+protocol\\s+adjacency.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        if output.startswith("Spanning-tree is not enabled at global level."):
            output=['']
        self.output = output
        record_count = 0
        #print output
        #print("hi")
        member = ""
        self.vc_prtcl_adj_data[record_count] = {}
        for line in output.split("\n"):
            if line.strip():
                m = re.match(r'member|fpc(\d+):', line.strip(), re.M|re.I)
                if m:
                    member = m.groups(0)[0]
                # m = re.match(r'(?P<interface>vcp-\d*.\d+)\s+(?P<system>\d*\w*\.\d*\w*\.\d*\w*)\s+(?P<state>Up|Down|New|One-way|Initializing|Rejected)\s+(?P<hold>\d+)', line.strip(), re.M|re.I)

                m = re.match(r'(?P<interface>vcp-\d*.\d+)\s+\w+.\w+.\w+\s+(?P<state>Up|Down|New|One-way|Initializing|Rejected)', line.strip(), re.M|re.I)
                if m:
                    self.vc_prtcl_adj_data[record_count] = {}
                    self.vc_prtcl_adj_data[record_count] = m.groupdict()
                    self.vc_prtcl_adj_data[record_count]['member'] = member
                    record_count += 1
                m = re.match(r'(?P<interface>\w+-\d+\/\d+)\s+(?P<system>\d*\w*\.\d*\w*\.\d*\w*)\s+(?P<state>\w+)\s+(?P<hold>\d+)', line.strip(), re.M|re.I)
                if m:
                    self.vc_prtcl_adj_data[record_count] = {}
                    self.vc_prtcl_adj_data[record_count] = m.groupdict()
                    self.vc_prtcl_adj_data[record_count]['member'] = member
                    record_count += 1
        #print json.dumps(self.vc_prtcl_adj_data, indent=4)

    def get_vc_prtcl_stat_data(self):
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+virtual\-chassis\\s+protocol\\s+statistics.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        if output.startswith("Spanning-tree is not enabled at global level."):
            output=['']
        self.output = output

        record_count = 0
        print output
        member = ""
        isisid = ""
        self.vc_prtcl_stat_data[record_count] = {}
        for line in output.split("\n"):
            if line.strip():
                m = re.match(r'member|fpc(\d+):', line.strip(), re.M|re.I)
                if m:
                    member = m.groups(0)[0]
                m = re.match(r'IS-IS statistics for (\w+.\w+.\w+):', line.strip(), re.M|re.I)
                if m:
                    isisid = m.groups(0)[0]
                m = re.match(r'(?P<pdutype>[A-Z]+)\s+\d+\s+\d+\s+(?P<drops>\d+)\s+\d+\s+\d+', line.strip(), re.M|re.I)
                if m:
                    self.vc_prtcl_stat_data[record_count] = {}
                    self.vc_prtcl_stat_data[record_count] = m.groupdict()
                    self.vc_prtcl_stat_data[record_count]['isisid'] = isisid
                    self.vc_prtcl_stat_data[record_count]['member'] = member
                    record_count = record_count + 1

        #print json.dumps(self.vc_prtcl_stat_data, indent=4)

    def get_vc_stat_data(self):
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+virtual\-chassis\\s+status.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        if output.startswith("Spanning-tree is not enabled at global level."):
            output=['']
        self.output = output
        record_count = 0
        #print output
        member = ""
        vcid = ""
        for line in output.split("\n"):
            if line.strip():
                m = re.match(r'member|fpc(\d+):', line.strip(), re.M|re.I)
                if m:
                    member = m.groups(0)[0]
                m = re.match(r'Virtual\sChassis\sID: ([a-f0-9]{4}\.[a-f0-9]{4}\.[a-f0-9]{4})', line.strip(), re.M|re.I)
                if m:
                    vcid = m.groups(0)[0]
                m = re.match(r'(?P<memberid>[0-9]+)\s\(FPC\s(?P<fpc>[0-9]+)\)\s+(?P<status>[a-z]{5,8})\s+[a-z0-9]{11,14}\s+(?P<modelid>ex[0-8]{4}-?[0-9]?[0-9]?[ft]?)\s+(?P<priority>[0-9]{1,4})\s+(?P<role>[a-z]+).*', line.strip(), re.M|re.I)
                if m:
                    self.vc_stat_data[record_count] = {}
                    self.vc_stat_data[record_count] = m.groupdict()
                    self.vc_stat_data[record_count]['vcid'] = vcid
                    self.vc_stat_data[record_count]['type'] = "p4000"
                    record_count = record_count + 1
                m = re.match(r'.*(?P<status>Unprvsnd).*', line.strip(), re.M|re.I)
                if m:
                    self.vc_stat_data[record_count] = {}
                    self.vc_stat_data[record_count] = m.groupdict()
                    self.vc_stat_data[record_count]['vcid'] = vcid
                    self.vc_stat_data[record_count]['type'] = "u4000"
                    self.vc_stat_data[record_count]['role'] = ""
                    self.vc_stat_data[record_count]['priority'] = ""
                    record_count = record_count + 1
                m = re.match(r'(?P<memberid>[0-9]+)\s\(FPC\s(?P<fpc>[0-9]+-[0-9]+)\)\s+(?P<status>[a-z]{5,8})\s+[a-z0-9]{11,14}\s+(?P<modelid>ex[0-8]{4}-?[0-9]?[0-9]?[ft]?)\s+(?P<priority>[0-9]{1,4})\s+(?P<role>[a-z]+).*', line.strip(), re.M|re.I)
                if m:
                    self.vc_stat_data[record_count] = {}
                    self.vc_stat_data[record_count] = m.groupdict()
                    self.vc_stat_data[record_count]['vcid'] = vcid
                    self.vc_stat_data[record_count]['type'] = "p8000"
                m = re.match(r'(?P<memberid>[0-9]+)\s\(FPC\s(?P<fpc>[0-9]+-[0-9]+)\)\s+(?P<status>[a-z]{5,8})\s+[a-z0-9]{11,14}\s+(?P<modelid>ex-xre)\s+(?P<priority>[0-9]{1,4})\s+(?P<role>[a-z]+).*', line.strip(), re.M|re.I)
                if m:
                    self.vc_stat_data[record_count] = {}
                    self.vc_stat_data[record_count] = m.groupdict()
                    self.vc_stat_data[record_count]['vcid'] = vcid
                    self.vc_stat_data[record_count]['type'] = "p8000-xre"
                    record_count = record_count + 1
        #print json.dumps(self.vc_stat_data, indent=4)

    def get_vc_vcp_stat_data(self):
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".*@.*>\\s+show\\s+virtual\-chassis\\s+vc\-port.*", line, re.M | re.I) == None:
                    break
            for line in fopen:
                if not re.match(".*@.*>\\s+show.*", line, re.M | re.I) == None:
                    break
                if line.strip():
                    output = output + line
        if output.startswith("Spanning-tree is not enabled at global level."):
            output=['']
        self.output = output
        record_count = 0
        #print output
        member = ""
        for line in output.split("\n"):
            if line.strip():
                m = re.match(r'member|fpc(\d+):', line.strip(), re.M|re.I)
                if m:
                    memberid = m.groups(0)[0]
                m = re.match(r'(?P<interface>vcp-\d+\/?\d*)\s+(?P<type>[a-z]+-?[a-z]*)\s+(?P<trunk>-?\d+)\s+(?P<status>\w+)\s+(?P<speed>\d+)\s+(?P<nghbr>\d+)\s+(?P<nghbrif>.*)', line.strip(), re.M|re.I)
                if m:
                    self.vc_vcp_stat_data[record_count] = {}
                    self.vc_vcp_stat_data[record_count] = m.groupdict()
                    self.vc_vcp_stat_data[record_count]["memberid"] = memberid
                    record_count += 1
                m = re.match(r'(?P<interface>\d+\/?\d+\/?\d*)\s+(?P<type>[a-z]+-?[a-z]*)\s+(?P<trunk>-?\d+)\s+(?P<status>\w+)\s+(?P<speed>\d+)\s+(?P<nghbr>\d+)\s+(?P<nghbrif>.*)', line.strip(), re.M|re.I)
                if m:
                    self.vc_vcp_stat_data[record_count] = {}
                    self.vc_vcp_stat_data[record_count] = m.groupdict()
                    self.vc_vcp_stat_data[record_count]["memberid"] = memberid
                    record_count += 1
                m = re.match(r'(?P<interface>vcp-\d+\/?\d*)\s+(?P<type>[a-z]+-?[a-z]*)\s+(?P<trunk>-?\d+)\s+(?P<status>Down|Disabled)\s+(?P<speed>\d+)', line.strip(), re.M|re.I)
                if m:
                    self.vc_vcp_stat_data[record_count] = {}
                    self.vc_vcp_stat_data[record_count] = m.groupdict()
                    self.vc_vcp_stat_data[record_count]["memberid"] = memberid
                    self.vc_vcp_stat_data[record_count]["nghbr"] = ""
                    self.vc_vcp_stat_data[record_count]["nghbrif"] = ""
                    record_count += 1
                m = re.match(r'(?P<interface>\d+\/?\d+\/?\d*)\s+(?P<type>[a-z]+-?[a-z]*)\s+(?P<trunk>-?\d+)\s+(?P<status>Down|Disabled)\s+(?P<speed>\d+)', line.strip(), re.M|re.I)
                if m:
                    self.vc_vcp_stat_data[record_count] = {}
                    self.vc_vcp_stat_data[record_count] = m.groupdict()
                    self.vc_vcp_stat_data[record_count]["memberid"] = memberid
                    self.vc_vcp_stat_data[record_count]["nghbr"] = ""
                    self.vc_vcp_stat_data[record_count]["nghbrif"] = ""
                    record_count += 1

                m = re.match(r'(?P<interface>vcp-\d+\/?\d*)\s+(?P<type>[a-z]+-?[a-z]*)\s+(?P<status>Absent)', line.strip(), re.M|re.I)
                if m:
                    self.vc_vcp_stat_data[record_count] = {}
                    self.vc_vcp_stat_data[record_count] = m.groupdict()
                    self.vc_vcp_stat_data[record_count]["memberid"] = memberid
                    self.vc_vcp_stat_data[record_count]["nghbr"] = ""
                    self.vc_vcp_stat_data[record_count]["nghbrif"] = ""
                    self.vc_vcp_stat_data[record_count]["trunk"] = ""
                    self.vc_vcp_stat_data[record_count]["speed"] = ""
                    self.vc_vcp_stat_data[record_count]["nghbrif"] = ""
                    self.vc_vcp_stat_data[record_count]["nghbrif"] = ""
                    record_count += 1

                m = re.match(r'(?P<interface>\d+\/?\d+\/?\d*)\s+(?P<type>[a-z]+-?[a-z]*)\s+(?P<status>Absent)', line.strip(), re.M|re.I)
                if m:
                    self.vc_vcp_stat_data[record_count] = {}
                    self.vc_vcp_stat_data[record_count] = m.groupdict()
                    self.vc_vcp_stat_data[record_count]["memberid"] = memberid
                    self.vc_vcp_stat_data[record_count]["nghbr"] = ""
                    self.vc_vcp_stat_data[record_count]["nghbrif"] = ""
                    self.vc_vcp_stat_data[record_count]["trunk"] = ""
                    self.vc_vcp_stat_data[record_count]["speed"] = ""
                    self.vc_vcp_stat_data[record_count]["nghbrif"] = ""
                    self.vc_vcp_stat_data[record_count]["nghbrif"] = ""
                    record_count += 1
        #print json.dumps(self.vc_vcp_stat_data, indent=4)
