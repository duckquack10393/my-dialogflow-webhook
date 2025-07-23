from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load sample product data
df = pd.read_csv("products.csv")  # Make sure products.csv is in same folder

@app.route("/searchProducts", methods=["POST"])
def search_products():
    data = request.get_json()

    # Extract parameters from Dialogflow CX
    params = data.get("sessionInfo", {}).get("parameters", {})
    category = params.get("category")
    price_limit = params.get("price_limit")

    # Filter products
    filtered = df.copy()
    if category:
        filtered = filtered[filtered["category"].str.contains(category, case=False)]
    if price_limit:
        filtered = filtered[filtered["price"] <= int(price_limit)]

    # Prepare response
    top_items = filtered.head(3)
    response_text = "\n".join(f"{row['name']} - ${row['price']}" for _, row in top_items.iterrows())

    return jsonify({
        "fulfillment_response": {
            "messages": [
                {"text": {"text": [response_text or "No products found."]}}
            ]
        }
    })

@app.route("/", methods=["GET"])
def home():
    return "Webhook is up!"

if __name__ == "__main__":
    app.run(debug=True)
