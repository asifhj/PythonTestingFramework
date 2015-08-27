__author__ = 'asifj'

import time
from tabulate import tabulate
import impala.dbapi
import impala.util

class Utils:

    def removeWhiteSpaceFromDict(self, d):
        return {k.strip(): self.removeWhiteSpaceFromDict(v)
        if isinstance(v, dict)
        else v.strip()
                for k, v in d.iteritems()}

    def getText(self, record, field_name):
        # Getter for tag text
        try:
            return record.find(field_name).text.strip()
        except Exception, err:
            # print(traceback.format_exc())
            # print(sys.exc_info()[0])
            # print("No data found for '%s'" % field_name)
            return None

    def display(self):
        # Display method
        print self.host_name

    def hashs(self):
        hashs = ""
        for i in range(0, 70):
            hashs = hashs + "#"
        return hashs

    def questions(self):
        questions = ""
        for i in range(0, 30):
            questions = questions + "?"
        return questions

    def epochToUTC(self, epoch):
        s, ms = divmod(epoch, 1000)
        phdct = ""
        if ms == 0:
            ms = ""
            phdct = format(time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s)))
        elif ms < 100:
            ms = "00" + str(ms)
        elif ms < 1000:
            ms = "0" + str(ms)
        # phdct = '{}.0{:d}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s)), ms)
        if phdct == "":
            phdct = '{}.{:s}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s)), ms)
        # print phdct
        #s, ms = divmod(E.received_time, 1000)
        #phdrt = '{}.0{:d}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(s)), ms)
        return phdct

    #def print_results(self, result_set):
    def tabulate_result_set(self, result_set):
        print tabulate(result_set, headers=["AccountUUID", "AccountName", "CollectorTime", "ReceivedTime", "HostName", "Model", "Product", "MastershipState"], tablefmt="fancy_grid")

    def tabulate_summary(self, summary):
        print tabulate(summary, headers=["PHC Collector Time", "Hadoop Collector Time", "Status", "Filename"], tablefmt="fancy_grid")

    def get_db_connection(self):
        dbconnection = impala.dbapi.connect(host="172.22.147.240", port="27003", database="parseattachments")
        dbconnection.close()
        cur = dbconnection.cursor()
        return cur


