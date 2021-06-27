from CBConnect import coinbaseMethods
from time import sleep
from os import system

def main():
    import coinbase
    from coinbase.wallet.client import Client
    CB = coinbaseMethods()
    initCoinbase(CB)

    try:
        while True:
            print("use ctrl + c at anytime to stop program")
            balances = CB.getBalances()
            for balance in balances:
                print(balance)
            sleep(2)
            system('cls')
    except KeyboardInterrupt:
        pass
def initCoinbase(CB):
    if CB.openKeysFile() == 1:
        print("keys file success")
        if CB.getKeys() == 1:
            print("get keys success")
            if CB.getClient() == 1:
                print("client success")
                if CB.getAccounts() == 1:
                    print("get accounts success")

main()
