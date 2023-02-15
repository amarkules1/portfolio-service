import json

import cachetools
from flask import Flask
import pandas as pd
import sqlalchemy
from sqlalchemy import sql
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS


app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["300 per hour", "30 per minute"],
    storage_uri="memory://",
)
CORS(app)

secret_sauce = json.load(open('secret_sauce.json',))


@app.route("/projects", methods=['GET'])
def projects():
    return get_response()


@cachetools.cached(cache=cachetools.TTLCache(maxsize=1024, ttl=30))
def get_response():
    conn = sqlalchemy.create_engine(secret_sauce['db_conn_string']).connect()
    data = pd.read_sql(sql.text("select * from portfolio_projects"), conn)
    data['row_number'] = data.reset_index().index
    conn.commit()
    data = data.sort_values(['priority', 'created_at'], ascending=[True, False])[['id', 'url', 'title', 'description',
                                                                                  'row_number']]
    return data.to_json(orient="records")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
