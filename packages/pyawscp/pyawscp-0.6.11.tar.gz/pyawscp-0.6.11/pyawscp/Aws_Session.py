import datetime, os, re
import boto3
from botocore.exceptions import ClientError
from pathlib import Path
from pyawscp.Config import Config
from pyawscp.PrettyTable import PrettyTable
from pyawscp.Emoticons import Emoticons
from pyawscp.TableArgs import TableArgs
from pyawscp.Utils import Utils, Style
from pyawscp.messages import Messages
from pyawscp.Functions import Functions

class AwsSession:

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
    
    def botoSession(self, profile):
        if not profile:
           return boto3.Session()
        return boto3.Session(profile_name=profile)

    def getAccountOwner(self, profile=None):
        sts = self.botoSession(profile).client("sts")
        return sts.get_caller_identity()
    
    def getMFADevices(self, profile=None):
        iam = self.botoSession(profile).client("iam")
        return iam.list_mfa_devices()
    
    def session_info(self):
        sizeSeparator    = 28
        sizeLabelProfile = 18

        try:
            sts = self.getAccountOwner(self.config.awsProfile)
        except ClientError as e:
            if e.response['Error']['Code'] == "ExpiredToken":
                msg = e.response['Error']['Message']
                Messages.showError("Expired Token!")
                return ""
        
        output      = "\n\n"
        assume_role = self.config.assumeRole if self.config.assumeRole and self.config.assumeRole != "" else "---"
        mfa_device  = self.config.mfaSerial if self.config.mfaSerial and self.config.mfaSerial != "" else "---"

        cookie = self.config.loadCookieTempCredentials()
        if not cookie:
            output    += f"{Style.GREEN}" + "=".ljust(sizeSeparator,"=") + "\n"
            output    += (f"    {Style.IYELLOW}{Emoticons.pin()} AWS SESSION") + "\n"
            output    += f"{Style.GREEN}" + "=".ljust(sizeSeparator,"=") + f"\n{Style.GREEN}"
        else:
            sizeSeparator = 44
            expiration    = cookie.timeToExpire()
            access_key    = cookie.accessKey
            output       += f"{Style.GREEN}" + "=".ljust(sizeSeparator,"=") + "\n"
            output       += (f"    {Style.IYELLOW}{Emoticons.pin()} TEMPORARY AWS SESSION (TOKEN)") + "\n"
            output       += f"{Style.GREEN}" + "=".ljust(sizeSeparator,"=") + f"\n{Style.GREEN}"

            if expiration == -1:
                expiration = f"{Style.IRED}TIME OUT {Style.GREEN}Expired!"
        
        output += f"  Profile............:{Style.IBLUE} {self.config.awsProfile} {Style.GREEN}\n"
        if cookie:
            output += f"  Access Key.........:{Style.IBLUE} {access_key}{Style.GREEN}\n"
        output += f"  Account............:{Style.IBLUE} {sts['Account']} {Style.GREEN}\n"
        output += f"  Region.............:{Style.IBLUE} {self.config.awsRegion} {Style.GREEN}\n"
        output += f"  Assume Role........:{Style.IBLUE} {assume_role} {Style.GREEN}\n"
        output += f"  MFA Device.........:{Style.IBLUE} {mfa_device} {Style.GREEN}\n"
        if cookie:
            output += f"  Remaining Time.....:{Style.IBLUE} {expiration}{Style.RESET}\n"

        return output