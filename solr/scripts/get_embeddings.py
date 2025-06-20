import sys
import json
from sentence_transformers import SentenceTransformer

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    # The model.encode() method already returns a list of floats
    return model.encode(text, convert_to_tensor=False).tolist()

if __name__ == "__main__":
    with open("solr/output.json", "r") as f:
        data = json.load(f)

    # Update each document in the JSON data
    for document in data:
        # Extract fields if they exist, otherwise default to empty strings
        name = document.get("Name", "")
        descriptions = document.get("Descriptions", "")

        combined_text = name + " " + descriptions
        document["vector"] = get_embedding(combined_text)

    with open("solr/output1.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
