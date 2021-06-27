# https://github.com/MarkGalloway/wealthsimple-trade
# https://github.com/seansullivan44/Wealthsimple-Trade-Python
import wealthsimple

class wealthSimpleMethods:
    def __init__(self):
        self._user = None
        self._password = None
        self._TFA = None
        self._client = None
        self._accounts = None

    def getLoginCred(self, filename = "WSCreds.txt"):
        try:
            creds = open(filename)
        except FileNotFoundError:
            print("Error: keys.txt does not exist")
            return 0
        except PermissionError:
            print("Error: unable to open file")
            return 0
        except Exception:
            print("Error:", Exception)
            return 0
        self._user = creds.readline().strip()
        self._password = creds.readline().strip()
        return 1
    

    def getClient(self):
        try:
            self.cleint = wealthsimple.WSTrade(self._user, self._password, two_factor_callback=getTFA)
        except Exception as e:
            print(e)
            return 0
        return 1

    def getAccounts(self):
        self._accounts = self.cleint.get_accounts()
        print(self._accounts)

    
if __name__ == "__main__":
        
    def getTFA():
        return input("Enter TFA code: ")
    wsm = wealthSimpleMethods()
    if wsm.getLoginCred() == 1:
        print("get login cred success")
    if wsm.getClient() == 1:
       print("get client success")
    wsm.getAccounts()