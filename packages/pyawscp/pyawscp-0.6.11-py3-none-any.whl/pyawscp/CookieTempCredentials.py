import datetime
from pyawscp.Emoticons import Emoticons
from pyawscp.Utils import Utils, Style

class CookieTempCredentials:

    def __init__(self):
        self.accessKey       = None
        self.secretAccessKey = None
        self.sessionToken    = None
        self.expirationDate  = None
    
    def isExpired(self):
        return self.expirationDate < datetime.datetime.now()

    def humanReadFormatExpirationDate(self):
        return self.expirationDate.strftime("%d-%m-%Y %H:%M:%S")

    def timeToExpire(self):
        if self.expirationDate:
           if self.isExpired():
              return -1
           diff = (self.expirationDate - datetime.datetime.now())
           if diff.seconds > 60:
               min  = int(diff.seconds / 60)
               secs = int(((diff.seconds / 60) - min) * 60)
               return f"{Style.IYELLOW}00:{Style.IYELLOW}{min:02d}{Style.IBLUE}:{Style.IYELLOW}{secs:02d} {Style.IBLUE}minutes"
           else:   
              return f"{Style.IYELLOW}00{Style.IBLUE}:{Style.IYELLOW}00{Style.IBLUE}:{Style.IYELLOW}{diff.seconds:02d} {Style.IBLUE}seconds"
        return 0

    def dateToString(self, dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def stringToDate(self, strDate):
        return datetime.datetime.strptime(strDate, "%Y-%m-%d %H:%M:%S")


    @staticmethod
    def headerCookieSTS():
        output  = "\n\n" + Style.RESET
        output += f"{Style.GREEN}====================================="
        output += "\n"
        output += f"  {Emoticons.pin()}{Style.IYELLOW}AWS TEMPORARY SESSION (TOKEN)"
        output += "\n" + Style.RESET
        output += f"{Style.GREEN}====================================="
        output += "\n"
        return output

   
    @staticmethod
    def invalidCookie():
        output  = CookieTempCredentials.headerCookieSTS()
        output += Style.IRED + "Not found!"
        output += "\n"
        output += Style.GREEN + "There's no active/valid Temporary Session Role"
        output += "\n"
        output += "\n"
        return output

    @staticmethod
    def printCookie(isValid, role, serial, expiration ):
        output = CookieTempCredentials.headerCookieSTS()
        if isValid:
           output += Style.GREEN + "Role.............: " +  Style.IBLUE + role + Style.RESET
           output += "\n"
           output += Style.GREEN + "MFA Serial.......: " +  Style.IBLUE + serial + Style.RESET
           output += "\n"
           output += Style.GREEN + "Time Remaining...: " + Style.IBLUE + str(expiration) + Style.RESET
           output += "\n" 
        else:
           output += Style.IRED + "Not found!"
           output += "\n"
           output += Style.GREEN + "There's no active/valid Temporary Session Role"
           output += "\n"
           output += "\n"
        return output
    
