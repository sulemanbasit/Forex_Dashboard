# pip install MetaTrader5

import MetaTrader5 as mt5
mt5.initialize()

import pandas as pd
from datetime import datetime, timezone
import time
# Read the CSV file into a DataFrame
df_credentials = pd.read_csv('../../api_credentials.csv') # fetch in root folder of nextcloud

#test
# Print the DataFrame
# for i in range(df.shape[0]):
#     print(df.iloc[i]["Login"])
print(df_credentials)

def fetch_account_info():
    login_list = []
    alias_list = []
    location_list = []
    balance_list = []
    equity_list = []
    margin_list = []
    margin_free_list = []
    pnl_list = []
    type_list = []

    for i in range(df_credentials.shape[0]): # access all rows
        mt5.login(int(df_credentials.iloc[i]["Login"]), df_credentials.iloc[i]["Password"], df_credentials.iloc[i]["Server"]) # login has to be integer otherwise it won't work

        accountInfo = mt5.account_info()
        
        print(accountInfo)

        print("Account: " + str(accountInfo.login))
        print("Balance: " + str(accountInfo.balance))
        print("Equity: " + str(accountInfo.equity))
        print("Profit: " + str(accountInfo.profit))
        print("Free Margin: " + str(accountInfo.margin_free))


        # This is needed to extract server time
        # Define the symbol to fetch the last tick time
        symbol = "BTCUSD_"  # Change this to the symbol you are interested in

        # Request the last tick for the symbol
        last_tick = mt5.symbol_info_tick(symbol)

        # Check if the last tick retrieval was successful
        if last_tick:
            # Retrieve the time of the last tick
            last_tick_time = last_tick.time

            # Convert last tick time from seconds to a datetime object
            last_tick_time_datetime = datetime.fromtimestamp(last_tick_time, timezone.utc)
            print("Server time:", last_tick_time_datetime)
        else:
            print("Failed to retrieve last tick information")
        print("")

        login_list.append(accountInfo.login)
        alias_list.append(df_credentials.iloc[i]["Alias"])
        location_list.append(df_credentials.iloc[i]["Location"])
        balance_list.append(accountInfo.balance)
        equity_list.append(accountInfo.equity)
        margin_list.append(accountInfo.margin)
        margin_free_list.append(accountInfo.margin_free)
        pnl_list.append(accountInfo.equity - accountInfo.balance)
        type_list.append(df_credentials.iloc[i]["Type"])
    columns = ["ID", "Name", "Location", "Balance", "Equity", "Margin", "Free Margin", "Floating PnL", "Type"]

    df_data = pd.DataFrame(columns=columns)
    # print(type_list)

    df_data["ID"] = login_list
    df_data["Name"] = alias_list
    df_data["Location"] = location_list
    df_data["Balance"] = balance_list
    df_data["Equity"] = equity_list
    df_data["Margin"] = margin_list
    df_data["Free Margin"] = margin_free_list
    df_data["Floating PnL"] = pnl_list
    df_data["Type"] = type_list

    df_data.to_csv('api_web.csv', index=False, mode='w')


    df_data

# Loop to fetch information every 10 seconds
count = 0
try:
    while True:
        fetch_account_info()
        count += 1
        print()
        print("INFORMATION FETCHED " + str(count) + " TIMES")
        time.sleep(10)
except KeyboardInterrupt:
    print("Stopped by user")
finally:
    mt5.shutdown()