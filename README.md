# Solr_Browser (WikiWar)

✅ A small UI + tools for browsing and evaluating a Solr collection of historical battles.

This repository contains a small frontend (HTML/CSS/JS), helper servers (Flask and Node proxy), Solr schemas and scripts to populate a Solr collection and run retrieval/evaluation experiments (TREC-style).

---

## Features
- Static front-end interface for searching battle data (`index.html`, `result.js`, `style.css`).
- Flask-based API endpoints to query Solr and serve a battle-detail page (`query.py`).
- NodeJS proxy to forward requests to Solr when needed (`proxy-server.js`).
- Scripts and tools for dataset preparation (e.g., `main.py`) and query/evaluation helpers under `solr/scripts/`.
- Docker-based startup scripts to create Solr containers and apply different schema configurations (`solr/startup_*.sh`).

## Quick start (development)
These steps will get a minimal setup running. They assume you have Docker, Python 3.x, and Node.js installed.

1) Prepare Python environment

```powershell
# (Windows) create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pandas matplotlib wikipedia-api requests beautifulsoup4 flask flask-cors
```

2) Start Solr with dataset
- The repo includes startup scripts under `solr/` to create a Solr collection and push `solr/output.json` into it. Each startup script configures the collection differently:

- For a simple schema:
```bash
cd solr
./startup_simple.sh
```
- For a boosted (weighting) schema:
```bash
cd solr
./startup_boosted.sh
```
- For no schema (dynamic fields):
```bash
cd solr
./startup_no_schema.sh
```

Note: these scripts are shell scripts — on Windows use Git Bash, WSL, or convert them into PowerShell commands. Alternatively run Docker manually (they map port 8983 by default):

```powershell
docker run -p 8983:8983 --name wikiwar_solr -v "$(pwd):/data" -d solr:9 solr-precreate wikiwar
curl -X POST -H "Content-type:application/json" --data-binary "@schema_simple.json" http://localhost:8983/solr/wikiwar/schema
docker exec wikiwar_solr bin/solr post -c wikiwar /data/output.json
```

3) Start the Flask query server (handles queries & battle details)

```powershell
python query.py
```

By default it runs on `127.0.0.1:5000` and exposes two endpoints:
- POST /query-solr — accepts JSON of the shape `{ uri, collection, params }` and forwards requests to Solr
- GET /battle-detail/<battle_id> — HTML detail view rendered with `templates/battle_detail.html`

4) Optional: Run NodeJS proxy server
- If you need to proxy requests to `http://localhost:8983/solr` (e.g., the front-end needs same-origin access to Solr), start the Node proxy server:

```powershell
npm install
node proxy-server.js
```

By default it runs on port `5000` and proxies `/solr` to `http://localhost:8983/solr`.

Note: both the Flask server and the Node server are configured to listen on port `5000` by default — they conflict if started simultaneously. Run them on separate ports or disable the Node proxy if you're using Flask for the front-end backend.

5) Open the front-end
- You can open `index.html` directly in a browser, or serve it with a local HTTP server to avoid file:// CORS issues:

```powershell
# from repository root
python -m http.server 8000
# then open http://localhost:8000/index.html
```

---

## Data preparation & enrichment
- `main.py` — enriches `final.csv` with descriptions by fetching Wikipedia (and 10000battles) data. It uses BeautifulSoup, requests, and wikipedia-api to fill missing or short descriptions.

Run it like this (after installing dependencies):

```powershell
python main.py
```

It reads `final.csv` and outputs `final_test.csv`.

---

## Scripts & evaluation
- `solr/scripts/` contains helpful scripts for performing queries, converting results, and producing plots:
	- `query_solr.py` — CLI to run queries against Solr
	- `solr2trec.py` — convert Solr results into TREC-style format
	- `qrels2trec.py` — convert QRELs to TREC-style format
	- `plot_pr.py` — plot precision/recall graphs
	- Others include helpers to generate stopwords/synonyms and embeddings

- The `test.sh` file demonstrates a complete evaluation flow for several query configurations (simple/boosted/no-schema). You can adapt and run the commands for automated benchmarking.

---

## Directory overview
- `index.html` — main front-end search UI
- `result.js`, `style.css` — front-end behavior and styling
- `query.py` — Flask server (query backend & details page)
- `proxy-server.js` — Express proxy server for `http://localhost:8983/solr`
- `solr/` — schema files, data, startup helpers, and evaluation scripts
- `main.py` — dataset enrichment (wikipedia & 10000battles)

---

## Notes & tips 💡
- On Windows, the `solr/startup_*.sh` are bash scripts; use WSL, Git Bash, or convert to PowerShell commands for Docker.
- If you only want to use the Flask backend, you can skip the Node proxy. The front-end `result.js` requests `http://127.0.0.1:5000/query-solr` by default (this is served by `query.py`).
- Ensure your Solr instance is accessible at `http://localhost:8983/solr` if you use the default configuration.

---

## Contributing
Contributions are welcome. Please open an issue for feature requests or bug reports — small improvements to scripts, documentation, or UI are appreciated.

---

## License
This repository does not currently include a license file — please add a LICENSE if you plan to open-source this project.
