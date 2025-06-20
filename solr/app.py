from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

SOLR_URL = "http://localhost:8983/solr"
COLLECTION_NAME = "wikiwar"

@app.route("/query", methods=["POST"])
def execute_query():
    data = request.json
    params = {
        "q": data.get("query", ""),
        "rows": data.get("rows", 10),
        "start": data.get("start", 0),
        "defType": "edismax",
        "q.op": "AND"
    }
    # Add query fields (qf) specific to the boosted schema
    params["qf"] = "Description^5 Participants^4 Country^3 Name_War^2 Winner"
    response = requests.get(f"{SOLR_URL}/{COLLECTION_NAME}/select", params=params)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
