import os, sys, re, uuid
from arnparse import arnparse
from os.path import expanduser
from tinydb import Query, where
from pyawscp.messages import Messages
from pyawscp.Utils import Utils, Style
from pyawscp.Emoticons import Emoticons
from pyawscp.Config import Config
from pyawscp.Functions import Functions
from pyawscp.PrettyTable import PrettyTable
from pyawscp.TableArgs import TableArgs
from pyawscp.Aws_Session import AwsSession
from pyawscp.repository.credentials_service import CredentialsService
from pyawscp.repository.repository_manager import RoleRepository

sizeSeparator    = 120
sizeLabelProfile = 18

class RoleService:

    def __init__(self,config):
        self.preferences         = config
        self.credentials_service = CredentialsService(config)
        self.role_repository     = RoleRepository()
    
    def search_role_by_name(self, name):
        return self.role_repository.searchByQuery(Query()['role-name'] == name)

    def list_roles_by_profile(self, profile):
        return self.role_repository.findByProfile(profile)

    def list_roles(self):
        return self.role_repository.all()

    def list_roles_view(self):
        roles = self.list_roles()

        if not roles or len(roles) == 0:
            result = f"{Style.GREEN}No Roles found" + "\n\n"
            return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_ROLES]["name"], result, self.preferences, "", True, None)

        tableArgs  = TableArgs()
        tableArgs.setArguments(self.preferences.commandArguments) 
        self.preferences.awsTagsToFilter = None

        jsonResult = ""
        if self.preferences.printResults or tableArgs.verbose or tableArgs.saveToFile: 
           jsonResult = Utils.dictToJson(roles)

        header = ["#","Role Name","ARN","Profile","Account"]
        prettyTable = PrettyTable(header)

        idx_lin    = 0
        for r in roles:
            idx_lin       += 1

            account = ""
            profile = self.credentials_service.get_profile(r['profile'])
            if profile:
                account = profile['account']
                
            columns = [ idx_lin, r['role-name'], r['role-arn'], r['profile'], account]

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
        result = resultTxt + "\n\n" + prettyTable.printMe("listRoles",self.preferences.tableLineSeparator, tableArgs)
        return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_ROLES]["name"], result, self.preferences, jsonResult, True, tableArgs)

    def _choose_profile_for_role(self):
        output           = ""
        index            = 0
        profiles         = []

        output += (f" {Style.BBLUE}   Which AWS Profile Credentials?") + "\n"
        output += (f"{Style.GREEN}" + "=".ljust(sizeSeparator,"=")) + "\n"
        
        for profile in self.credentials_service.list_profiles():
            index += 1
            profiles.append(profile)
            pn        = profile['profile'] + " ".rjust(sizeLabelProfile -len(profile['profile']), " ")
            account   = profile['account']
            line      = f"  {Style.IBLUE}{index:02d} -->{Style.GREEN} {pn} {Style.IBLUE}Account..:{Style.GREEN} {account}"
            labelRole = "Roles..: "
            roles     = ""
            for idx, r in enumerate(self.role_repository.searchByQuery(where('profile') == profile['profile'])):
                 if len(roles) > 1:
                     roles += "\n" + " ".ljust(len(Utils.removeCharsColors(line)) + len(labelRole) + 1," ")
                 roles += f"{Style.BLUE}{idx+1:02d}{Style.GREEN}-{r['role-arn']} {Style.BLUE}({r['role-name']})"
            if len(roles) > 1:
                roles = f"{Style.IBLUE}{labelRole}{Style.GREEN}{roles}{Style.GREEN}"
            output += line + f" {roles}\n"
        output += "-".ljust(sizeSeparator,"-")
        print(output)
        print(f"{Style.GREEN} {Emoticons.pin()} Choose a profile....:{Style.BLUE}", end= ' ')
        result = input()
        if result == "":
            return None
            
        if not Utils.isNumber(result):
            Messages.showWarning(f"Invalid choice \"{Style.IBLUE}{result}{Style.IGREEN}\"")
            return None
        if int(result) > index:
            Messages.showWarning(f"Profile \"{Style.IBLUE}{result}{Style.IGREEN}\" not valid!")
            return None
        
        return profiles[int(result) - 1]

    def add_role(self):
        output  = ""
        output += f"{Style.GREEN}" + "=".ljust(sizeSeparator,"=") + "\n"
        output += (f" {Style.BYELLOW}{Emoticons.pin()} ADD A ROLE")
        print(output)

        profile_chosen = self._choose_profile_for_role()
        if not profile_chosen:
            print("\n")
            return 
        
        role       = {}
        print(f"{Style.GREEN} {Emoticons.pin()} Role Name...........:{Style.BLUE}",end=' ')
        roleName = input()
        spacesFound = re.search(" ",roleName)
        if spacesFound:
            Messages.showWarning(f"Invalid Role Name \"{Style.IBLUE}{roleName}{Style.IGREEN}\", spaces are not allowed")
            print("\n")
            return None
        role["name"] = roleName

        print(f"{Style.GREEN} {Emoticons.pin()} Role ARN............:{Style.BLUE}",end=' ')
        roleArn = input()
        try:
            roleArnParse = arnparse(roleArn)
        except:
            Messages.showWarning(f"Invalid Role ARN \"{Style.IBLUE}{roleArn}{Style.IGREEN}\"")
            print("\n")
            return None
        role["arn"] = roleArn

        output  = "\n"
        output += f" {Style.IBLUE} --> {Style.GREEN}Profile............: {Style.IBLUE}{profile_chosen['profile']}{Style.RESET}\n"
        output += f" {Style.IBLUE} --> {Style.GREEN}Account............: {Style.IBLUE}{profile_chosen['account']}{Style.RESET}\n"
        output += f" {Style.IBLUE} --> {Style.GREEN}Role Name..........: {Style.IBLUE}{roleName}{Style.RESET}\n"
        output += f" {Style.IBLUE} --> {Style.GREEN}Role ARN...........: {Style.IBLUE}{roleArn}{Style.RESET}\n"
        print(output)

        print(f"{Style.GREEN} {Emoticons.pin()} Confirm [{Style.IGREEN}y/{Style.IGREEN}n{Style.RESET}]:{Style.BLUE}",end=' ')
        confirm = input()
        if confirm.lower() == "y":
            record = {
                "id": str(uuid.uuid4()),
                "profile": profile_chosen['profile'],
                "role-name": roleName,
                "role-arn": roleArn
            }
            self.role_repository.insert(record)
            output = f"{Style.GREEN} {Emoticons.ok()} Saved!{Style.RESET}"
            print(output)
    
    def remove_role(self):
        output  = ""
        output += f"{Style.GREEN}" + "=".ljust(sizeSeparator,"=") + "\n"
        output += (f" {Style.BYELLOW}{Emoticons.pin()} REMOVE A ROLE\n")
        output += (f" {Style.BBLUE}   Which Role?") + "\n"
        output += (f"{Style.GREEN}" + "=".ljust(sizeSeparator,"=")) + "\n"
        print(output)
        roles = []
        index = 0
        for r in self.list_roles():
            index += 1
            roles.append(r)
            pn        = r['role-arn']  + " ".rjust(sizeLabelProfile -len(r['role-arn']), " ")
            name      = r['role-name'] + " ".rjust(20 - len(r['role-name']), " ")
            line      = f"  {Style.IBLUE}{index:02d} -->{Style.GREEN} {pn} {Style.IBLUE}{name}{Style.GREEN} (Profile:{Style.CYAN} {r['profile']}{Style.GREEN})"
            output += line + "\n"
        output += "-".ljust(sizeSeparator,"-")
        print(output)
        print(f"{Style.GREEN} {Emoticons.pin()} Choose a role....:{Style.BLUE}", end= ' ')
        result = input()
        if result == "":
            print("\n")
            return None
        if not Utils.isNumber(result) or (int(result) > len(roles)) or (int(result) == 0):
            Messages.showWarning(f"Invalid choice \"{Style.IBLUE}{result}{Style.IGREEN}\"")
            print("\n")
            return None

        numberInList = int(result)
        roleToRemove = None
        
        for idx,role in enumerate(roles):
            if (idx+1) == numberInList:
                roleToRemove = role
                break
        
        if not roleToRemove:
            Messages.showWarning("Role not found!")
            print("\n")
            return
        else:
            output  = "\n"
            output += f" {Style.IBLUE} --> {Style.GREEN}Role ARN...........: {Style.IBLUE}{roleToRemove['role-arn']}{Style.RESET}\n"
            output += f" {Style.IBLUE} --> {Style.GREEN}Role Name..........: {Style.IBLUE}{roleToRemove['role-name']}{Style.RESET}\n"
            output += f" {Style.IBLUE} --> {Style.GREEN}Profile............: {Style.IBLUE}{roleToRemove['profile']}{Style.RESET}\n"
            print(output)
            print(f"{Style.GREEN} {Emoticons.pin()} Remove [{Style.IGREEN}y/{Style.IGREEN}n{Style.RESET}]:{Style.BLUE}",end=' ')
            confirm = input()
            if confirm.lower() == "y":
                self.role_repository.remove(Query().id == roleToRemove['id'])
                output  = "\n"
                output += f"{Style.GREEN} {Emoticons.ok()} Removed!{Style.RESET}"
                print(output)

