import datetime, os, re
from pathlib import Path
from pyawscp.Config import Config
from pyawscp.PrettyTable import PrettyTable
from pyawscp.Emoticons import Emoticons
from pyawscp.TableArgs import TableArgs
from pyawscp.Utils import Utils, Style
from pyawscp.Functions import Functions

class Credentials:

    def __init__(self, config):
        self.credentials = {}
        self.config      = config
        self.parse_credentials()
    
    def parse_credentials(self):
        file_credentials = os.path.expanduser("~") + "/.aws/credentials"

        if not Path(file_credentials).is_file:
            return
        

        profiles = {}
        with open(file_credentials,'r') as file:
            for line in file:
                if len(line.strip()) > 0:
                    profile = re.search("(\[.*\])", line) 
                    if profile:
                        profile_name = profile.group(1).replace("[","").replace("]","")
                        profiles[profile_name] = {}
    
                    attribute = re.search("(.*=.*)", line) 
                    if attribute:
                        attribute_pair  = attribute.group(1).split("=")
                        attribute_key   = attribute_pair[0].strip()
                        attribute_value = attribute_pair[1].strip()
                        profiles[profile_name][attribute_key] = attribute_value
        
        self.credentials["profiles"] = profiles
    
    def list_credentials_formatted(self):
        tableArgs  = TableArgs()
        tableArgs.setArguments(self.config.commandArguments) 

        jsonResult = ""
        if self.config.printResults or tableArgs.verbose or tableArgs.saveToFile: 
           jsonResult = Utils.dictToJson(self.credentials)

        header = ["#","Profile", "Access Key", "Source Profile", "Role ARN", "MFA Serial"]
        prettyTable = PrettyTable(header)

        idx_lin    = 0
        for profile in self.credentials["profiles"]:
            idx_lin += 1
            
            aws_access_key = "---"
            source_profile = "---"
            role_arn       = "---"
            mfa_serial     = "---"
            if "aws_access_key_id" in self.credentials["profiles"][profile]:
                aws_access_key = self.credentials["profiles"][profile]["aws_access_key_id"]
            if "source_profile" in self.credentials["profiles"][profile]:
                source_profile = self.credentials["profiles"][profile]["source_profile"]
            if "role_arn" in self.credentials["profiles"][profile]:
                role_arn = self.credentials["profiles"][profile]["role_arn"]
            if "mfa_serial" in self.credentials["profiles"][profile]:
                mfa_serial = self.credentials["profiles"][profile]["mfa_serial"]

            columns = [ str(idx_lin), profile, aws_access_key, source_profile, role_arn, mfa_serial ]
            prettyTable.addRow(columns)
        
        resultTxt = ""
        resultTxt = " Credentials, total..: " + Style.GREEN + format(idx_lin,",") + Style.RESET
        
        if (int(tableArgs.sortCol) - 1) > len(columns):
            tableArgs.sortCol = "1"
            prettyTable.sortByColumn(int(tableArgs.sortCol) - 1)

        
        tableArgs.setArguments(f"| {self.config.awsProfile}")

        prettyTable.sortByColumn(0)   
        prettyTable.numberSeparator = True
        prettyTable.ascendingOrder(not tableArgs.desc)
        result = resultTxt + "\n\n" + prettyTable.printMe("listBucketsS3",self.config.tableLineSeparator, tableArgs)
        return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_CREDENTIALS]["name"], result, self.config, jsonResult, True, tableArgs)

