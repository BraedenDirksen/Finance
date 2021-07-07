# https://developers.coinbase.com/api/v2
from coinbase.wallet.client import Client
from coinbase.wallet import error
from coinbase.wallet.model import Transaction
class coinbaseMethods:
    def __init__(self):
        self._keysFile = None
        self._key = None
        self._secretKey = None
        self._client = None
        self._accounts = None
        self._transactions = None
        self._trades = None
        self._sells = None
        self._buys = None
        self._sends = None
        self._prices = None

    def openKeysFile(self,filename = "keys.txt"):
        # opens the files with the keys given by the user or defualts to keys.txt
        # returns 1 if success and 0 if not
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
        # gets the key and secret key from the file
        # returns 1 if success and 0 if not
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
        # connects to the coinbase api using users key and secret key
        # returns 1 if successful 0 if not
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
        # gets the accounts data from the coinbase api
        # returns 1 if success and 0 if not
        try:
            self._accounts = self._client.get_accounts()
            return 1
        except Exception:
            print("Error:", Exception)
            return 0
            
    def getBalances(self):
        # gets the amount held in the account currently of each different wallet
        # returns a list of each of strings of each wallets current balance
        output = []
        total = 0
        self._accounts.refresh
        for wallet in self._accounts.data:
            output.append( str(wallet['name']) + ' ' +   str(wallet['native_balance']) )
            value = str( wallet['native_balance']).replace('CAD','')
            total += float(value)
        output.append( 'Total Balance: ' + 'CAD ' + str(total) )
        return output
    
    def getTransactions(self):
        # gets raw transactions data from api and groups by each wallet
        # returns a dictionary of the different wallets transactions data
        transactions = {}
        for account in self._accounts.data:
            transactions[account['name']] = self._client.get_transactions(account['id'])
        if not self._transactions or self._transactions != transactions:
            self._transactions = transactions
        return transactions
    
    def getPrices(self):
        # gets current prices of all currecies that have transactions associated with them
        prices =[]
        for currency in list(self._transactions.keys()):
            currency = currency.strip(" Wallet") + "-CAD"
            prices.append(self._client.get_buy_price(currency_pair = currency))
            try: 
                prices[-1]["base"]
                pass
            except:
                prices[-1]["base"] = currency.strip("-CAD")

        self._prices = prices

    def getTradesProfits(self):
        trades = []
        trade_ids = []
        for currency in list(self._transactions.keys()):
            for transaction in self._transactions[currency]['data']:
                if transaction["type"] == "trade":
                    trade_id = transaction["trade"]["id"]
                    if trade_id not in trade_ids: # if the transaction has already been processed skip it
                        trade_ids.append(trade_id) # if not add to processed transactions and process
                        
                        # finding associated transaction
                        for currency2 in list(self._transactions.keys()):
                            for transaction2 in self._transactions[currency2]['data']:
                                if transaction2["type"] == "trade":
                                    if transaction2["trade"]["id"] == trade_id:
                                        break

                        # gets payment amount and recieved amount
                        if float(transaction["amount"]["amount"]) >= 0:
                            recieved = (float(transaction["amount"]["amount"]), transaction["amount"]["currency"])
                            payment = (float(transaction2["amount"]["amount"]), transaction2["amount"]["currency"])
                        else:
                            recieved = (float(transaction2["amount"]["amount"]), transaction2["amount"]["currency"])
                            payment = (float(transaction["amount"]["amount"]), transaction["amount"]["currency"])
                        
                        for currency in self._prices:
                            if payment[1] == currency["base"]:
                                paymentValueCurrent = float(currency["amount"]) * payment[0]
                            if recieved[1] == currency["base"]:
                                recievedValueCurrent = float(currency["amount"]) * recieved[0]
                        
                        profit = paymentValueCurrent + recievedValueCurrent
                        trades.append(profit)
                        print(payment[0] * -1,payment[1],"to", recieved[0], recieved[1], "profit:", round(profit,3))
        print("value added by trades:", sum(trades) / len(trades))

    def getLedgerAmount(self):
        ledgerHoldings = []
        for currency in list(self._transactions.keys()):
            for transaction in self._transactions[currency]['data']:
                if transaction['type'] == "send":

                    
                    if "to" in list(transaction.keys()):
                        if "address" in list(transaction["to"].keys()):
                            # ledger DOGE account
                            if transaction["to"]["address"] == "DM4G6KPXeUTb2jQcxw5H91rz1QngsHSq1y":
                                amount = float(transaction["amount"]["amount"])
                                for currency in self._prices:
                                    if currency["base"] == "DOGE":
                                        value = float(currency["amount"]) * amount
                                        break
                                ledgerHoldings.append((amount * -1, "DOGE", value * -1))
                            
                            # ledger BTC account
                            if transaction["to"]["address"] == "bc1qa7z8zpk5s00ln0u3q997pkmy5hjsw8pstqdw50":
                                amount = float(transaction["amount"]["amount"])
                                for currency in self._prices:
                                    if currency["base"] == "BTC":
                                        value = float(currency["amount"]) * amount
                                        break
                                ledgerHoldings.append((amount * -1, "BTC", value * -1))
                            
                            # ledger ETH account
                            if transaction["to"]["address"] == "0x5E95d930A3e7329CC0594Ba9E8372Fa36A1D4FC3":
                                amount = float(transaction["amount"]["amount"])
                                for currency in self._prices:
                                    if currency["base"] == "ETH":
                                        value = float(currency["amount"]) * amount
                                        break
                                ledgerHoldings.append((amount * -1, "ETH", value * -1))

                            # ledger LTC account
                            if transaction["to"]["address"] == "ltc1qrrag0qgyrcm9k6g9mmauvrs4ta54jhalkghn5x":
                                amount = float(transaction["amount"]["amount"])
                                for currency in self._prices:
                                    if currency["base"] == "LTC":
                                        value = float(currency["amount"]) * amount
                                        break
                                ledgerHoldings.append((amount * -1, "LTC", value * -1))


        total = 0
        for wallet in ledgerHoldings:
            print(round(wallet[0], 3), wallet[1], "worth $" + str(round(wallet[2], 3)), "CAD")
            total += wallet[2]
        print("total holdings: $" + str(round(total,3)), "CAD")

    def getMiningAmount(self):
        for currency in list(self._transactions.keys()):
            for transaction in self._transactions[currency]['data']:
                if transaction['type'] == "send":
                    pass



if __name__ == "__main__":
    test = coinbaseMethods()
    print("Opening Keys File...")
    if test.openKeysFile() == 1:
        print("keys file success")
        print("Retrieving Keys...")
        if test.getKeys() == 1:
            print("get keys success")
            print("Creating Client...")
            if test.getClient() == 1:
                print("client success")
                print("Getting Accounts...")
                if test.getAccounts() == 1:
                    print("get accounts success")
                    print("Getting Transactions...")
                    transactions = test.getTransactions()
                    print("get transactions success")
                    print("Getting Coin Prices...")
                    test.getPrices()
                    print("get prices success")
                    #f = open('transactions.txt', 'w')
                    #f.write(str(transactions))
                    #f.close()
                    balances = test.getBalances()
                    print("\nCoinbase holdings:")
                    for balance in balances:
                        print(balance)

                    print("\nTransactions:")
                    test.getTradesProfits()

                    print("\nLedger Holdings:")
                    test.getLedgerAmount()