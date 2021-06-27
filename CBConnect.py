# https://developers.coinbase.com/api/v2
from coinbase.wallet.client import Client
from coinbase.wallet import error
class coinbaseMethods:
    def __init__(self):
        self._keysFile = None
        self._key = None
        self._secretKey = None
        self._client = None
        self._accounts = None

    def openKeysFile(self,filename = "keys.txt"):
        try:
            self._keysFile = open(filename)
            return 1
        except FileNotFoundError:
            print("Error: keys.txt does not exist")
            return 0
        except PermissionError:
            print("Error: unable to open file")
            return 0
        except Exception:
            print("Error:", Exception)
            return 0
        
    def getKeys(self):
        self._key = self._keysFile.readline().strip()
        if len(self._key) != 16:
            print("Error: invalid Key")
            return 0
        self._secretKey = self._keysFile.readline().strip()
        if len(self._secretKey) != 32:
            print("Error: invalid Secret Key")
            return 0
        return 1

    def getClient(self):
        try:
            self._client = Client(self._key, self._secretKey)
            self._keysFile = None
            self._key = None
            self._secretKey = None
            return 1
        except error.AuthenticationError:
            print("Error: invalid key, or secret key,", coinbase.wallet.error.AuthenticationError )
            return 0
        except Exception:
            print("Error:", Exception)
            return 0

    def getAccounts(self):
        try:
            self._accounts = self._client.get_accounts()
            return 1
        except Exception:
            print("Error:", Exception)
            return 0
            
    def getBalances(self):
        output = []
        total = 0
        self._accounts.refresh
        for wallet in self._accounts.data:
            if str(wallet['name']) == 'BTC':
                print("pls")
            output.append( str(wallet['name']) + ' ' +   str(wallet['native_balance']) )
            value = str( wallet['native_balance']).replace('CAD','')
            total += float(value)
        output.append( 'Total Balance: ' + 'CAD ' + str(total) )
        return output

if __name__ == "__main__":
    test = coinbaseMethods()
    if test.openKeysFile() == 1:
        print("keys file success")
        if test.getKeys() == 1:
            print("get keys success")
            if test.getClient() == 1:
                print("client success")
                if test.getAccounts() == 1:
                    print("get accounts success")
                    balances = test.getBalances()
                    for balance in balances:
                        print(balance)
