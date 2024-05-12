from flask import Flask, render_template, redirect, url_for, request
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    # Read the CSV file
    data = pd.read_csv("API_Fetch_Data/api_web.csv")

    # Group data by 'Type' column
    grouped_data = data.groupby('Type')

    # Convert the grouped data into a dictionary
    data_dict = {group: group_data.to_dict('records') for group, group_data in grouped_data}
    # print(data_dict)
    
    return render_template("index.html", data_dict=data_dict)

@app.route("/account")
def account():
    # Retrieve data from the query parameter
    account_data = request.args.get('data')

    return render_template("account.html", account_data=account_data)

if __name__ == "__main__":
    app.run(debug=True)
