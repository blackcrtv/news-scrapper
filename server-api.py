from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

from src.scrappers import EuronewsScraper, MediafaxScraper 
from db.elastic import ElasticSearch

db = ElasticSearch()

app = Flask(__name__)
CORS(app) 

def convert_float32_to_float(obj):
    if isinstance(obj, dict):
        return {k: convert_float32_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_float32_to_float(i) for i in obj]
    elif isinstance(obj, np.float32):
        return float(obj)
    return obj

@app.route("/api/start-scrapping", methods=["POST"])
def process_text():
  try:
    # Get request arguments
    site_text = request.json["site_text"]
    limit = request.json["limit"]

    result_scrapping = []

    if(site_text == "euronews"):
        scrapper = EuronewsScraper(db)
        result_scrapping = scrapper.start_scrapping(limit)
    if(site_text == "mediafax"):
        scrapper = MediafaxScraper(db)
        result_scrapping = scrapper.start_scrapping(limit)

    clean_result = convert_float32_to_float(result_scrapping)
    return jsonify(clean_result)
  except (KeyError, ValueError) as e:
    # Handle errors related to missing or invalid arguments
    return jsonify({"error": f"Invalid request: {str(e)}"}), 400

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
