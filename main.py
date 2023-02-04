import json

from flask import Flask, jsonify, make_response
import requests
import os
import pandas as pd
import sqlalchemy
from sqlalchemy import sql


app = Flask(__name__)


secret_sauce = json.load(open('secret_sauce.json',))
conn = sqlalchemy.create_engine(secret_sauce['db_conn_string']).connect()


@app.route("/projects", methods=['GET'])
def projects():
    data = pd.read_sql(sql.text("select * from portfolio_projects"), conn)
    data = data.sort_values(['priority', 'created_at'], ascending=[True, False])[['id', 'url', 'title', 'description']]
    return data.to_json(orient="records")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
