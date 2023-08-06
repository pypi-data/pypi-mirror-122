import os, sys, re
from os.path import expanduser
from datetime import datetime
from tinydb import Query, where
from pyawscp.messages import Messages
from pyawscp.Utils import Utils, Style
from pyawscp.Emoticons import Emoticons
from pyawscp.Config import Config
from pyawscp.PrettyTable import PrettyTable
from pyawscp.TableArgs import TableArgs
from pyawscp.Aws_Session import AwsSession
from pyawscp.Functions import Functions
from pyawscp.repository.repository_manager import CredentialsRepository, MfaRepository, RoleRepository

sizeSeparator    = 120
sizeLabelProfile = 18

class CredentialsService:

    def __init__(self,config):
        self.preferences            = config
        self.credentials_repository = CredentialsRepository()
        self.role_repository        = RoleRepository()
        self.mfa_repository         = MfaRepository()

    def loadAndSyncProfiles(self):
        self.credentials_repository.purge()

        fileCredentials  = expanduser("~") + "/.aws/credentials"
        if not os.path.exists(fileCredentials):
            Messages.showWarning("Credentials Not Found!",f" The file {Style.IBLUE}/.aws/credentials{Style.GREEN} was not found, did you install and configure your {Style.IBLUE}awscli{Style.GREEN}?")
            sys.exit()

        currentProfileName                   = None
        accessKey                            = None
        secretKey                            = None
        credentialsProfiles                  = {}
        credentialsProfiles["credentials"]   = []
        with open(fileCredentials,'r') as fcred:
            for line in fcred.readlines():
                if line.lstrip().rstrip().startswith("["):
                   if currentProfileName:
                       # SAVE Previous
                       credentialsProfiles["credentials"].append({
                           "profile": currentProfileName,
                           "accessKey": accessKey,
                           "secretKey": secretKey
                       })
                   # Read Current    
                   currentProfileName = Utils.cleanBreakLines(line).replace("[","").replace("]","") 
                else:
                   if Utils.cleanBreakLines(line).lstrip().rstrip() != "":
                      line = Utils.cleanBreakLines(re.sub('\s',"",line))
                      kv   = line.split("=")
                      if   "aws_access_key_id" in kv[0].lower():
                         accessKey = kv[1]
                      elif "aws_secret_access_key" in kv[0].lower():
                         secretKey = kv[1]
            if currentProfileName:
                # SAVE Previous
                credentialsProfiles["credentials"].append({
                    "profile": currentProfileName,
                    "accessKey": accessKey,
                    "secretKey": secretKey
                })

        # Check if needs updates/inserts
        aws_session = AwsSession(self.preferences)
        total_loaded = 0
        for c in credentialsProfiles["credentials"]:
             dbRecordProfile = self.credentials_repository.findByProfile(c["profile"])
             # Insert the new one
             if not dbRecordProfile:
                 account   = ""
                 # Read Account and MFA Devices of the Profile at AWS
                 try:
                     account = aws_session.getAccountOwner(c["profile"])["Account"]
                     for m in aws_session.getMFADevices(c["profile"])["MFADevices"]:
                         mfaRecord = self.mfaRepository.searchByQuery(Query()['mfa-device'] == m["SerialNumber"])
                         if not mfaRecord or len(mfaRecord) < 0:
                             self.mfaRepository.insert({
                                 "profile": c["profile"],
                                 "mfa-device": m["SerialNumber"],
                                 "user-name": m["UserName"]
                             })
                 except:
                     #:XXX  Check this later
                     # LogManager().LOG.warning(f"Not able to retrieve the MFA Devices for the {c['profile']}, probably some police might be blocking by the lack of MFA Token")
                     pass
                 c["account"] = account
                 self.credentials_repository.insert(c)
                 total_loaded += 1
             else:
                 # Check if needs to update the record (credentials change)
                 if dbRecordProfile["accessKey"] != c["accessKey"]  or \
                    dbRecordProfile["secretKey"] != c["secretKey"]:
                    # UPDATEIT
                    self.credentials_repository.update(c, c["profile"])

        output  = "\n\n"
        output += f"{Style.GREEN}   {Emoticons.pointRight()} Total Credentials Loaded/Synchronized...:{Style.IBLUE} {total_loaded}\n"
        output += f"{Style.GREEN}      You can see then:{Style.IBLUE} {Functions.LIST_PROFILES}"
        output += "\n"
        return output
    
    def get_profile(self, profile):
        return self.credentials_repository.findByProfile(profile)
        
    def list_profiles(self, list_roles=False, list_mfas=False):
        profiles = self.credentials_repository.all()
        if len(profiles) == 0:
            print("")
            Messages.showWarning("No AWS Credentials loaded in PyAwsCp, yet!")
            output  = f"{Style.GREEN}    You can {Style.IYELLOW}load {Style.GREEN}and {Style.IYELLOW}synchronize{Style.GREEN} in PyAwsCp your credentials from {Style.ICYAN}~/.aws/credentials\n" 
            output += f"{Style.GREEN}    For that, start using the command: {Style.BBLUE}syncCredentials" 
            output += f"{Style.RESET}" 
            print(output)
            return None
        
        if list_roles:
            for p in profiles:
                roles = self.role_repository.searchByQuery(Query().profile == p['profile'])
                if roles and len(roles) > 0:
                    p['roles'] = []
                    for idx, role in enumerate(roles):
                        p['roles'].append({
                            "name": role['role-name'],
                            "arn": role['role-arn']
                        })
        
        if list_mfas:
            for p in profiles:
                mfas = self.mfa_repository.searchByQuery(Query().profile == p['profile'])
                if mfas and len(mfas) > 0:
                    p['mfas'] = []
                    for idx, mfa in enumerate(mfas):
                        p['mfas'].append({
                            "mfa-device": mfa['mfa-device'],
                            "user-name": mfa['user-name']
                        })
            
        return profiles
    
    def list_profiles_view(self):
        list_roles = False
        list_mfas  = False
        if "roles" in self.preferences.commandArguments:
            list_roles = True
        if "mfas" in self.preferences.commandArguments:
            list_mfas = True

        profiles_loaded = self.list_profiles(list_roles,list_mfas)
        if not profiles_loaded:
            result = f"{Style.GREEN}No Profiles found" + "\n\n"
            return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_PROFILES]["name"], result, self.preferences, "", True, None)
 
        tableArgs  = TableArgs()
        tableArgs.setArguments(self.preferences.commandArguments) 
        self.preferences.awsTagsToFilter = None

        jsonResult = ""
        if self.preferences.printResults or tableArgs.verbose or tableArgs.saveToFile: 
           jsonResult = Utils.dictToJson(profiles_loaded)

        header = ["#","Profile", "Access Key", "Account"]
        if list_roles:
            header.append("Role")
        elif list_mfas:
            header.append("MFA Device")
        prettyTable = PrettyTable(header)

        idx_lin    = 0
        for p in profiles_loaded:
            idx_lin       += 1
            profile        = p['profile']
            aws_access_key = p['accessKey']
            account        = p['account']

            if list_roles:
                if 'roles' in p:
                    for idx_role, r in enumerate(p['roles']):
                        role = f"{Style.IBLUE}{idx_role+1:02d}{Style.GREEN}-{r['arn']}{Style.IBLUE} ({r['name']}){Style.GREEN}"
                        columns = [ idx_lin, profile, aws_access_key, account, role ]
                        prettyTable.addRow(columns)
                        profile = ""
                        aws_access_key = ""
                        account = ""
                else:
                    columns = [ idx_lin, profile, aws_access_key, account, "" ]
                    prettyTable.addRow(columns)
            elif list_mfas:
                if 'mfas' in p:
                    for idx_mfa, r in enumerate(p['mfas']):
                        mfa_device = f"{Style.IBLUE}{idx_mfa+1:02d}{Style.GREEN}-{r['mfa-device']}{Style.IBLUE} ({r['user-name']}){Style.GREEN}"
                        columns = [ idx_lin, profile, aws_access_key, account, mfa_device ]
                        prettyTable.addRow(columns)
                        profile = ""
                        aws_access_key = ""
                        account = ""
                else:
                    columns = [ idx_lin, profile, aws_access_key, account, "" ]
                    prettyTable.addRow(columns)
            else:
                columns = [ idx_lin, profile, aws_access_key, account ]
                prettyTable.addRow(columns)
        
        resultTxt = ""
        resultTxt = " Total...: " + Style.GREEN + format(idx_lin,",") + Style.RESET

        if (int(tableArgs.sortCol) - 1) > len(columns):
            tableArgs.sortCol = "1"
            prettyTable.sortByColumn(int(tableArgs.sortCol) - 1)
        
        tableArgs.setArguments(f"| {self.preferences.awsProfile}")

        prettyTable.sortByColumn(0)   
        prettyTable.numberSeparator = True
        prettyTable.ascendingOrder(not tableArgs.desc)
        result = resultTxt + "\n\n" + prettyTable.printMe("listProfiles",self.preferences.tableLineSeparator, tableArgs)
        return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_PROFILES]["name"], result, self.preferences, jsonResult, True, tableArgs)
    
    def import_from_awsee(self):
        print("")
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
    
    def rollback_import_from_awsee(self):
        #from_date = "2021-10-0610-11-13"
        print("")
        if self.preferences.commandArguments == "":
            Messages.showError(f"{Style.GREEN} Date and Time not informed!\n    Expected format: {Style.CYAN}YYYY-MM-DD_HH-MM-SS\n{Style.GREEN}    Example........: {Style.CYAN}2021-10-06_10-11-13")
            return

        from_date = self.preferences.commandArguments

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