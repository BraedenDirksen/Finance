from CBConnect import coinbaseMethods
from WSConnect import wealthSimpleMethods
from time import sleep
from os import system




def main():
    import coinbase
    from coinbase.wallet.client import Client
    CB = coinbaseMethods()
    initCoinbase(CB)


    WS = wealthSimpleMethods()
    initWealthSimple(WS)

    try:
        while True:
            print("use ctrl + c at anytime to stop program")
            balances = CB.getBalances()
            for balance in balances:
                print(balance)
            sleep(60)
            system('cls')
    except KeyboardInterrupt:
        pass

def initCoinbase(CB):
    if CB.openKeysFile() == 1:
        print("CB keys file success")
        if CB.getKeys() == 1:
            print("CB get keys success")
            if CB.getClient() == 1:
                print("CB client success")
                if CB.getAccounts() == 1:
                    print("CB get accounts success")

def initWealthSimple(WS):
    if WS.getLoginCred() == 1:
        print("WS get login cred success")
    if WS.getClient() == 1:
        print("WS get client success")
        WS.getAccounts()

def updateTransactions():
    pass
main()
