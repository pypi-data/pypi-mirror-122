# coding=utf-8

import sys
import json
import os, re
import random
import configparser
from os.path import expanduser

from botocore.credentials import Credentials
from pyawscp.Functions import Functions
from pyawscp.PyAwsShell import PREFERENCES
from pyawscp.Utils import Utils, Style
from pyawscp.Emoticons import Emoticons
from pyawscp.Config import Config
from pyawscp.TableArgs import TableArgs
from pygments import highlight, lexers, formatters
from pyawscp.PyEc2Cp import PyEc2CP
from pyawscp.PyEc2NetSecCp import PyEc2NetSecCP
from pyawscp.PyElbCp import PyElbCP
from pyawscp.PyS3Cp import PyS3CP
from pyawscp.PyR53Cp import PyR53CP
from tinydb import Query, where
from datetime import datetime
from arnparse import arnparse

from pyawscp.Aws_Session import AwsSession as AwsSession
from pyawscp.messages import Messages
from pyawscp.repository import credentials_service, mfa_service
from pyawscp.repository import role_service
from repository.repository_manager import RoleRepository
from repository.credentials_service import CredentialsService
from repository.role_service import RoleService
from repository.mfa_service import MfaService

class Test:
    def __init__(self):
        self.my_function(a=12, _vpcid=123456)

    def my_function(self, **args):
        print(args["_vpcid"])

def loadTmpSession():
    tempConfigFile = os.path.expanduser("~") + "/.pyawscp/tmp.bin"
    if not os.path.exists(tempConfigFile):
       print("")
       print("=".ljust(80,"="))
       print("File {} not found".format(tempConfigFile))
       print("""
       FILE NAME: \033[32mmyTempSession.tmp\033[0m
       EXPECTED FIELDS:\033[32m
       assume-role=NaNaNaNa
       mfa-serial=NaNaNaNa
       region=NaNaNaNa
       profile=NaNaNaNa\033[0m
       """)
       print("=".ljust(80,"="))
       print("")
       sys.exit()
    
    config = Config()
    with open(tempConfigFile, "r") as fp:
        for idx, line in enumerate(fp):
            if not line.startswith("#"):
                if "assume-role=" in line:
                    config.assumeRole = line.replace("assume-role=","").rstrip().lstrip()
                elif "mfa-serial=" in line:
                    config.mfaSerial = line.replace("mfa-serial=","").rstrip().lstrip() 
                elif "region=" in line:
                    config.awsRegion = line.replace("region=","").rstrip().lstrip() 
    config.printResults = False
    config.tableLineSeparator = False

    if len(sys.argv) > 1:
       config.mfaPassCode=sys.argv[1]
    
    print("=".ljust(80,"="))
    print(" All set!")
    print("=".ljust(80,"="))
    return config

def loadSavedConfig():
    preferences = Config()
    configFileIni = configparser.ConfigParser()
    configFileIni.read(expanduser("~") + "/.pyawscp/pyawscp.ini")
    preferences.awsProfile               = configFileIni[PREFERENCES]["aws-profile"]
    preferences.awsRegion                = configFileIni[PREFERENCES]["aws-region"]
    preferences.assumeRole               = configFileIni[PREFERENCES]["assume-role"]
    preferences.mfaSerial                = configFileIni[PREFERENCES]["mfa-serial"]
    return preferences

def test2():
    config = loadTmpSession()
    pyEc2CP = PyEc2CP(config)
    connBt, data, report, content = pyEc2CP.listEc2()
    print(report)

def testListVpc():
    config = loadTmpSession()
    config.commandArguments = "verbose"
    pyEc2Cp = PyEc2CP(config)
    report = pyEc2Cp.listVpc()
    print(report)

def testListEc2():
    config = loadTmpSession()
    pyEc2Cp = PyEc2CP(config)
    connBt, data, report, content = pyEc2Cp.listEc2()
    print(report)

def testFindRoute():
    config = loadTmpSession()
    #config.commandArguments = "i-0b5d342791d7ed2c4,i-0c54d18dc352d71e6,excel"
    #config.commandArguments = "i-0b5d342791d7ed2c4,i-0c54d18dc352d71e6,save,verbose"
    #config.commandArguments = "i-0b5d342791d7ed2c4,i-0c54d18dc352d71e6,target-group"
    #config.commandArguments = "i-0b5d342791d7ed2c4,i-0c54d18dc352d71e6"
    #config.commandArguments = "i-06f4a5c3bb81fec46,i-0d9a673532481f016,i-09117ce6865a30ab7,i-04a483aed2cf4a8c7"
    config.commandArguments = "i-06f4a5c3bb81fec46,i-0d9a673532481f016,i-09117ce6865a30ab7"

    #config.commandArguments = "i-0d9a673532481f016,i-09117ce6865a30ab7,label-name,target-group"
    #config.commandArguments = "i-0d9a673532481f016,i-09117ce6865a30ab7,target-group"
    #config.commandArguments = "i-0d9a673532481f016,i-09117ce6865a30ab7,label-name"
    config.tableLineSeparator = False

    Utils.clearScreen()
    py = PyR53CP(config)
    data, report = py.findRouteEc2s()
    print(Utils.formatPrettyJson(data))
    #print(report)

    # Utils.saveToFile("TestData.json",data)
    # Load previous data (saved before) to save time on testing only Result Format
    # with open("results/TestData.json", 'r') as f:
    #     jsonSaved = f.read()
    # data = json.loads(jsonSaved)    

    result = py.findRouteEc2sPrintResult(data, config.commandArguments)
    print(result)

def test_list_profiles():
    config = loadTmpSession()
    credentials_service = CredentialsService(config)   
    print(credentials_service.list_profiles_view())

def test_list_roles():
    config = loadTmpSession()
    role_service = RoleService(config)
    print(role_service.list_roles_view())

def test_feature_sync_repository_credentials():
    config = loadTmpSession()

    print("")
    Messages.showStartExecution("Wait, synchronizing AWS credentials...      ")
    credentials_service = CredentialsService(config)
    credentials_service.loadAndSyncProfiles()
    Messages.showStartExecution("Synchronization done!                        ")
    print("")

def test_feature_list_repository_credentials():
    config = loadTmpSession()
    print("")
    credentials_service = CredentialsService(config)
    print(credentials_service.list_profiles_view())

def test_feature_add_role():
    config = loadTmpSession()
    role_service = RoleService(config)
    role_service.add_role()

def test_remove_role():
    config = loadTmpSession()
    role_service = RoleService(config)
    role_service.remove_role()

def test_list_mfas():
    config = loadTmpSession()
    mfa_service = MfaService(config)
    print(mfa_service.list_mfas_view())

def test_add_mfa():
    config = loadTmpSession()
    mfa_service = MfaService(config)
    mfa_service.add_mfa()

def test_remove_mfa():
    config = loadTmpSession()
    mfa_service = MfaService(config)
    mfa_service.remove_mfa()

def rollback_import_from_awsee():
    from_date = "2021-10-06_13-06-55"
    #from_date = "2021-10-0610-11-13"
    correct_format = re.match("\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}",from_date)
    if not correct_format:
        Messages.showError(f"{Style.GREEN}Wrong format!\n    Expected format: {Style.CYAN}YYYY-MM-DD_HH-MM-SS\n{Style.GREEN}    Example........: {Style.CYAN}2021-10-06_10-11-13")
        return
    
    pyawscp_folder = os.path.join(expanduser("~"),".pyawscp")

    # Restore Credentials
    pyawscp_credentials_file        = os.path.join(pyawscp_folder,"credentials")
    pyawscp_credentials_file_backup = os.path.join(pyawscp_folder,f"bkp-credentials-{from_date}")
    if not os.path.exists(pyawscp_credentials_file_backup):
        Messages.showError(f"The file bkp-credentials-{from_date} was not found!")
        return
    with open(pyawscp_credentials_file_backup, 'r') as f:
        content = f.read()
    with open(pyawscp_credentials_file,'w') as f:
        f.write(content)
    
    # Restore Roles
    pyawscp_roles_file        = os.path.join(pyawscp_folder,"role")
    pyawscp_roles_file_backup = os.path.join(pyawscp_folder,f"bkp-role-{from_date}")
    if not os.path.exists(pyawscp_roles_file_backup):
        Messages.showError(f"The file bkp-role-{from_date} was not found!")
        return
    with open(pyawscp_roles_file_backup, 'r') as f:
        content = f.read()
    with open(pyawscp_roles_file,'w') as f:
        f.write(content)
    
    # Restore MFAs
    pyawscp_mfas_file        = os.path.join(pyawscp_folder,"mfa")
    pyawscp_mfas_file_backup = os.path.join(pyawscp_folder,f"bkp-mfa-{from_date}")
    if not os.path.exists(pyawscp_mfas_file_backup):
        Messages.showError(f"The file bkp-mfa-{from_date} was not found!")
        return
    with open(pyawscp_mfas_file_backup, 'r') as f:
        content = f.read()
    with open(pyawscp_mfas_file,'w') as f:
        f.write(content)

    Messages.showMessage(f" Backup from {Style.CYAN}{from_date}{Style.GREEN} restored!")

def import_from_awsee():
    awsee_folder   = os.path.join(expanduser("~"),".awsee")
    pyawscp_folder = os.path.join(expanduser("~"),".pyawscp")

    if not os.path.exists(awsee_folder):
        Messages.showError(f"{Style.GREEN}AwsSee home folder was not found!\n    Are you sure you have it installed?\n    {Style.CYAN}https://ualter.github.io/awsee-site/")
        return
    
    snapshot_date = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"

    # CREDENTIALS
    awsee_credentials_file = os.path.join(awsee_folder,"cred")
    if os.path.exists(awsee_credentials_file):
        with open(awsee_credentials_file, 'r') as f:
            awsee_credentials_file_content = f.read() 

        # Backup PyAwsCp Credentials File
        pyawscp_credentials_file        = os.path.join(pyawscp_folder,"credentials")
        pyawscp_credentials_file_backup = os.path.join(pyawscp_folder,f"bkp-credentials-{snapshot_date}")
        if os.path.exists(pyawscp_credentials_file):
            with open(pyawscp_credentials_file, 'r') as f:
                pyawscp_credentials_file_content = f.read()
            with open(pyawscp_credentials_file_backup,'w') as f:
                f.write(pyawscp_credentials_file_content)
        # Import Credentials from AwsSee to PyAwsCp        
        with open(pyawscp_credentials_file,'w') as f:
            f.write(awsee_credentials_file_content)
    
    # ROLES
    awsee_roles_file = os.path.join(awsee_folder,"role")
    if os.path.exists(awsee_roles_file):
        with open(awsee_roles_file, 'r') as f:
            awsee_roles_file_content = f.read() 

        # Backup PyAwsCp Role File
        pyawscp_role_file        = os.path.join(pyawscp_folder,"role")
        pyawscp_role_file_backup = os.path.join(pyawscp_folder,f"bkp-role-{snapshot_date}")
        if os.path.exists(pyawscp_role_file):
            with open(pyawscp_role_file, 'r') as f:
                pyawscp_role_file_content = f.read()
            with open(pyawscp_role_file_backup,'w') as f:
                f.write(pyawscp_role_file_content)
        # Import Role from AwsSee to PyAwsCp        
        with open(pyawscp_role_file,'w') as f:
            f.write(awsee_roles_file_content)
    
    # MFA
    awsee_mfas_file = os.path.join(awsee_folder,"mfa")
    if os.path.exists(awsee_mfas_file):
        with open(awsee_mfas_file, 'r') as f:
            awsee_mfas_file_content = f.read() 

        # Backup PyAwsCp MFA File
        pyawscp_mfa_file        = os.path.join(pyawscp_folder,"mfa")
        pyawscp_mfa_file_backup = os.path.join(pyawscp_folder,f"bkp-mfa-{snapshot_date}")
        if os.path.exists(pyawscp_mfa_file):
            with open(pyawscp_mfa_file, 'r') as f:
                pyawscp_mfa_file_content = f.read()
            with open(pyawscp_mfa_file_backup,'w') as f:
                f.write(pyawscp_mfa_file_content)
        # Import MFA from AwsSee to PyAwsCp        
        with open(pyawscp_mfa_file,'w') as f:
            f.write(awsee_mfas_file_content)
    
    Messages.showMessage(f"Imported susccesfully!\n Backup created with label date {Style.CYAN}{snapshot_date}{Style.GREEN}")
           

## Troubleshoot
## in WSL (Bash), in case the Enter is resulting a ^M   use this command "stty sane" before call Python
def test1():
    pass
    # val = input("Enter your value: ") 
    # print(val) 
    # AWS_CREDENTIALS_DIR = "~/.aws/"
    # print("") 
    # print("")
    # print("\033[31m ---> Ops!\033[33m AWS CREDENTIALS NOT FOUND!")
    # print("") 
    # print("") 
    # print("\033[34m ---> \033[33mPlease, configure your AWS Credentials:")
    # print("\033[34m      \033[33m1. Create the folder \033[35m{}\033[0m".format(AWS_CREDENTIALS_DIR))
    # print("\033[34m      \033[33m2. Create the file \033[35m{}credentials\033[33m with the  content:".format(AWS_CREDENTIALS_DIR))
    # print("\033[34m      \033[94m   [default]")
    # print("\033[34m      \033[94m   aws_access_key_id = YOUR_ACCESS_KEY")
    # print("\033[34m      \033[94m   aws_secret_access_key = YOUR_SECRET_KEY")
    # print("\033[34m      \033[33m3. Optionally, create the file \033[35m{}config\033[33m with your default region:".format(AWS_CREDENTIALS_DIR))
    # print("\033[34m      \033[94m   [default]")
    # print("\033[34m      \033[94m   region=us-east-1")
    # print("")
    # print("")

def session_info():
    preferences = loadSavedConfig()
    aws_session = AwsSession(preferences)
    print(aws_session.session_info())

def main():
    #test_feature_add_role()
    #test_list_profiles()
    #test_list_roles()
    #test_remove_role()
    #test_list_mfas()
    #test_add_mfa()
    #test_remove_mfa()
    #import_from_awsee()
    #rollback_import_from_awsee()
    session_info()
    

if __name__ == '__main__':
    main()
        