__author__ = 'asifj'

import re
import json


class metadata:

    def getMetdata(self):
        output = ""
        with open(self.file_name, "rb") as fopen:
            for line in fopen:
                if not re.match(".+Meta data by Service Now.*", line, re.M | re.I) == None:
                    output = line
                    break
        output = output.replace("[----BEGIN - Meta data by Service Now----]", "")
        output = output.replace("[----END - Meta data by Service Now----]", "")
        json_data = json.loads(output)
        self.model = json_data['product']
        self.servicenow_device_id = json_data['serviceNowVersion']
        self.node = json_data['node']
        self.login_mail_id = json_data['loginMailId']
        self.old_account_name = json_data['oldAccountName']
        self.perceived_secondary_id = json_data['perceivedSecondaryId']
        self.old_account_id = json_data['oldAccountId']
        self.space_device_id = json_data['spaceDeviceId']
        self.host_name = json_data['hostName']
        self.phd_collected_time = json_data['phdCollectedTime']
        self.account_id = json_data['accountId']
        self.servicenow_version = json_data['serviceNowVersion']
        self.platform = json_data['platform']
        self.received_time = json_data['receivedTime']
        self.base_software_release = json_data['baseSoftwareRelease']
        self.base_product_name = json_data['baseProductName']
        self.account_name = json_data['accountName']
        self.group_name = json_data['groupName']
        self.disable_time = json_data['disableTime']
        self.perceived_account_name = json_data['perceivedAccountName']
        self.device_timezone = json_data['deviceTimezone']
        self.status = json_data['status']
        self.product = json_data['product']
        self.servicenow_timezone = json_data['serviceNowTimezone']
        self.perceived_account_id = json_data['perceivedAccountId']
        self.additional_device_info = json_data['additionalDeviceInfo']
        self.group_id = json_data['groupId']
        self.enabled_time = json_data['enabledTime']
        self.serial_number = json_data['serialNumber']
        self.space_version = json_data['spaceVersion']
        self.software_release = json_data['softwareRelease']
        self.aiscript_version = json_data['aiscriptVersion']
        if self.base_product_name == None:
            # print self.base_product_name
            print "\n\t\t\t" + str(self.questions()) + "Base Product Name cannot be NULL" + str(self.questions())
            self.base_product_name = self.product
        if self.node == None:
            self.node = "NULL"