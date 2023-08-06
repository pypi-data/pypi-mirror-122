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
from pyawscp.repository.repository_manager import MfaRepository

sizeSeparator    = 120
sizeLabelProfile = 18

class MfaService:

    def __init__(self,config):
        self.preferences         = config
        self.credentials_service = CredentialsService(config)
        self.mfa_repository     = MfaRepository()
    
    def list_mfas_by_profile(self, profile):
        return self.mfa_repository.findByProfile(profile)

    def search_mfa_by_username(self, username):
        return self.mfa_repository.searchByQuery(Query()['user-name'] == username)

    def list_mfas(self):
        return self.mfa_repository.all()

    def list_mfas_view(self):
        mfas = self.list_mfas()

        tableArgs  = TableArgs()
        tableArgs.setArguments(self.preferences.commandArguments) 
        self.preferences.awsTagsToFilter = None

        jsonResult = ""
        if self.preferences.printResults or tableArgs.verbose or tableArgs.saveToFile: 
           jsonResult = Utils.dictToJson(mfas)

        if not mfas or len(mfas) == 0:
            result = f"{Style.GREEN}No MFA Serial found" + "\n\n"
            return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_MFAS]["name"], result, self.preferences, jsonResult, True, tableArgs)

        header = ["#","MFA Device/Serial","Username","Profile","Account"]
        prettyTable = PrettyTable(header)

        idx_lin    = 0
        for m in mfas:
            idx_lin       += 1

            account = ""
            profile = self.credentials_service.get_profile(m['profile'])
            if profile:
                account = profile['account']
                
            columns = [ idx_lin, m['mfa-device'], m['user-name'], m['profile'], account]

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
        result = resultTxt + "\n\n" + prettyTable.printMe("listMfas",self.preferences.tableLineSeparator, tableArgs)
        return Utils.formatResult(Functions.FUNCTIONS[Functions.LIST_ROLES]["name"], result, self.preferences, jsonResult, True, tableArgs)

    def _choose_profile_for_mfa(self):
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
            labelMfa = "MFAs: "
            mfas     = ""
            for idx, r in enumerate(self.mfa_repository.searchByQuery(where('profile') == profile['profile'])):
                 if len(mfas) > 1:
                     mfas += "\n" + " ".ljust(len(Utils.removeCharsColors(line)) + len(labelMfa) + 1," ")
                 mfas += f"{Style.BLUE}{idx+1:02d}{Style.GREEN}-{r['mfa-device']} {Style.BLUE}({r['user-name']})"
            if len(mfas) > 1:
                mfas = f"{Style.IBLUE}{labelMfa}{Style.GREEN}{mfas}{Style.GREEN}"
            output += line + f" {mfas}\n"
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

    def add_mfa(self):
        output  = ""
        output += f"{Style.GREEN}" + "=".ljust(sizeSeparator,"=") + "\n"
        output += (f" {Style.BYELLOW}{Emoticons.pin()} ADD A MFA SERIAL")
        print(output)

        profile_chosen = self._choose_profile_for_mfa()
        if not profile_chosen:
            print("\n")
            return 
        
        mfa       = {}
        print(f"{Style.GREEN} {Emoticons.pin()} Device..............:{Style.BLUE}",end=' ')
        mfaDevice = input()
        spacesFound = re.search(" ",mfaDevice)
        if spacesFound:
            Messages.showWarning(f"Invalid Device \"{Style.IBLUE}{mfaDevice}{Style.IGREEN}\", spaces are not allowed")
            print("\n")
            return None
        try:
            mfaArnParse = arnparse(mfaDevice)
        except:
            Messages.showWarning(f"Invalid MFA Serial Device ARN \"{Style.IBLUE}{mfaDevice}{Style.IGREEN}\"")
            print("\n")
            return None
        mfa["mfa-device"] = mfaDevice

        print(f"{Style.GREEN} {Emoticons.pin()} Username............:{Style.BLUE}",end=' ')
        mfaUserName = input()
        if mfaUserName == "":
            Messages.showWarning(f"Invalid Username \"{Style.IBLUE}{mfaUserName}{Style.IGREEN}\"")
            print("\n")
            return None
        mfa["user-name"] = mfaUserName

        output  = "\n"
        output += f" {Style.IBLUE} --> {Style.GREEN}Profile............: {Style.IBLUE}{profile_chosen['profile']}{Style.RESET}\n"
        output += f" {Style.IBLUE} --> {Style.GREEN}Account............: {Style.IBLUE}{profile_chosen['account']}{Style.RESET}\n"
        output += f" {Style.IBLUE} --> {Style.GREEN}Device.............: {Style.IBLUE}{mfaDevice}{Style.RESET}\n"
        output += f" {Style.IBLUE} --> {Style.GREEN}Username...........: {Style.IBLUE}{mfaUserName}{Style.RESET}\n"
        print(output)

        print(f"{Style.GREEN} {Emoticons.pin()} Confirm [{Style.IGREEN}y/{Style.IGREEN}n{Style.RESET}]:{Style.BLUE}",end=' ')
        confirm = input()
        if confirm.lower() == "y":
            record = {
                "id": str(uuid.uuid4()),
                "profile": profile_chosen['profile'],
                "mfa-device": mfaDevice,
                "user-name": mfaUserName
            }
            self.mfa_repository.insert(record)
            output = f"{Style.GREEN} {Emoticons.ok()} Saved!{Style.RESET}"
            print(output)
    
    def remove_mfa(self):
        output  = ""
        output += f"{Style.GREEN}" + "=".ljust(sizeSeparator,"=") + "\n"
        output += (f" {Style.BYELLOW}{Emoticons.pin()} REMOVE A ROLE\n")
        output += (f" {Style.BBLUE}   Which Mfa?") + "\n"
        output += (f"{Style.GREEN}" + "=".ljust(sizeSeparator,"=")) + "\n"

        mfas = []
        index = 0
        for r in self.list_mfas():
            index += 1
            mfas.append(r)
            pn        = r['mfa-device']  + " ".rjust(sizeLabelProfile -len(r['mfa-device']), " ")
            name      = r['user-name'] + " ".rjust(20 - len(r['user-name']), " ")
            line      = f"  {Style.IBLUE}{index:02d} -->{Style.GREEN} {pn} {Style.IBLUE}{name}{Style.GREEN} (Profile:{Style.CYAN} {r['profile']}{Style.GREEN})"
            output += line + "\n"
        output += "-".ljust(sizeSeparator,"-")
        print(output)
        print(f"{Style.GREEN} {Emoticons.pin()} Choose a mfa....:{Style.BLUE}", end= ' ')
        result = input()
        if result == "":
            print("\n")
            return None
        if not Utils.isNumber(result) or (int(result) > len(mfas)) or (int(result) == 0):
            Messages.showWarning(f"Invalid choice \"{Style.IBLUE}{result}{Style.IGREEN}\"")
            print("\n")
            return None

        numberInList = int(result)
        mfaToRemove = None
        
        for idx,mfa in enumerate(mfas):
            if (idx+1) == numberInList:
                mfaToRemove = mfa
                break
        
        if not mfaToRemove:
            Messages.showWarning("Mfa not found!")
            print("\n")
            return
        else:
            output  = "\n"
            output += f" {Style.IBLUE} --> {Style.GREEN}MFA Device.........: {Style.IBLUE}{mfaToRemove['mfa-device']}{Style.RESET}\n"
            output += f" {Style.IBLUE} --> {Style.GREEN}Username...........: {Style.IBLUE}{mfaToRemove['user-name']}{Style.RESET}\n"
            output += f" {Style.IBLUE} --> {Style.GREEN}Profile............: {Style.IBLUE}{mfaToRemove['profile']}{Style.RESET}\n"
            print(output)
            print(f"{Style.GREEN} {Emoticons.pin()} Remove [{Style.IGREEN}y/{Style.IGREEN}n{Style.RESET}]:{Style.BLUE}",end=' ')
            confirm = input()
            if confirm.lower() == "y":
                self.mfa_repository.remove(Query().id == mfaToRemove['id'])
                output  = "\n"
                output += f"{Style.GREEN} {Emoticons.ok()} Removed!{Style.RESET}"
                print(output)

