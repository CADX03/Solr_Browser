#!/usr/bin/env python3

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import logging
from urllib.parse import unquote

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
CORS(app)

@app.route("/query-solr", methods=["POST"])
def query_solr():
    app.logger.info(f"Request received: {request.json}")
    try:
        data = request.json
        solr_uri = data.get("uri", "http://localhost:8983/solr")
        collection = data.get("collection", "wikiwar")
        params = data.get("params")

        uri = f"{solr_uri}/{collection}/select"

        min_year = params.get("minYear")
        max_year = params.get("maxYear")

        payload = {
            "q": params.get("q"),
            "q.op": params.get("q_op", "AND"),
            "start": params.get("start", 0),
            "rows": params.get("rows", 10),
            "defType": params.get("defType", "edismax"),
            "qf": params.get("qf", "Description^5 Participants^4 Country^3 Name_War^2 Winner")
        }

        if min_year is not None and max_year is not None:
            payload["fq"] = f"Year:[{min_year} TO {max_year}]"

        app.logger.debug(f"Payload: {payload}")

        response = requests.get(uri, params=payload) 
        app.logger.debug(f"Response: {response.text}")

        response.raise_for_status()  

        return jsonify(response.json())

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Erro na requisição ao Solr: {e}")
        return jsonify({"error": "Erro na requisição ao Solr", "message": str(e)}), 500
    except Exception as e:
        app.logger.error(f"Erro desconhecido: {e}")
        return jsonify({"error": "Erro desconhecido", "message": str(e)}), 500


@app.route("/battle-detail/<battle_id>")
def battle_detail(battle_id):
    try:
        decoded_battle_id = unquote(battle_id)
        print("ENCODED", decoded_battle_id)
        solr_query = f'ID:"{decoded_battle_id}"'

        uri = "http://localhost:8983/solr/wikiwar/select"
        params = {
            "q": solr_query,  
            "rows": 1,
        }

        response = requests.get(uri, params=params)
        data = response.json()
        print("CONSULTA", data)
        if data['response']['numFound'] == 0:
            return "Battle not found", 404

        battle = data['response']['docs'][0]
        
        def flatten_list(nested_list):
            """Helper function to flatten a list of lists into a single list."""
            flattened = []
            for item in nested_list:
                if isinstance(item, list):
                    flattened.extend(flatten_list(item))  
                else:
                    flattened.append(item)
            return flattened
        
        if isinstance(battle.get('Participants'), list):
            battle['Participants'] = ', '.join(flatten_list(battle['Participants']))
        if isinstance(battle.get('Winner'), list):
            battle['Winner'] = ', '.join(flatten_list(battle['Winner']))
        if isinstance(battle.get('Loser'), list):
            battle['Loser'] = ', '.join(flatten_list(battle['Loser']))
        if isinstance(battle.get('Name_War'), list):
            battle['Name_War'] = ', '.join(flatten_list(battle['Name_War']))

        return render_template('battle_detail.html', battle=battle)
    
    except requests.exceptions.RequestException as e:
        return f"Error fetching battle details: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)