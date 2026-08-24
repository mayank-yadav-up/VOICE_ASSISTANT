from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# In-memory shopping list database for demo purposes
shopping_list = []

# Category mapping helper
CATEGORIES = {
    "dairy": ["milk", "cheese", "butter", "yogurt", "cream", "almond milk"],
    "produce": ["apple", "apples", "banana", "bananas", "orange", "oranges", "tomato", "spinach"],
    "bakery": ["bread", "bagel", "muffin", "croissant"],
    "beverages": ["water", "juice", "soda", "coffee", "tea"],
    "household": ["toothpaste", "soap", "detergent", "shampoo"]
}

def categorize_item(item_name):
    item_lower = item_name.lower()
    for category, items in CATEGORIES.items():
        if any(i in item_lower for i in items):
            return category.capitalize()
    return "General"

@app.route('/api/command', methods=['POST'])
def handle_command():
    global shopping_list  # Declared at the top of the function
    
    data = request.json
    command = data.get('command', '').lower().strip()
    
    # 1. ADD / BUY COMMAND
    if any(word in command for word in ['add', 'buy', 'i need', 'want to buy']):
        # Extract quantity (default to 1 if not specified)
        qty_match = re.search(r'\b(\d+)\b', command)
        quantity = int(qty_match.group(1)) if qty_match else 1
        
        # Clean up item name by removing action words and numbers
        item_name = command
        for word in ['add', 'to my list', 'to the list', 'i need to buy', 'i need', 'want to buy', 'please', 'buy']:
            item_name = item_name.replace(word, '')
        if qty_match:
            item_name = item_name.replace(qty_match.group(1), '')
        item_name = item_name.strip()
        
        if not item_name:
            return jsonify({"success": False, "message": "Could not identify item name."}), 400
            
        category = categorize_item(item_name)
        
        # Check for substitutes or smart suggestions logic
        suggestion = None
        if "milk" in item_name and "almond" not in item_name:
            suggestion = "Tip: Consider almond milk as a dairy-free alternative."
        elif "bread" in item_name:
            suggestion = "Smart Suggestion: You might also need butter or eggs!"

        newItem = {
            "id": len(shopping_list) + 1,
            "name": item_name,
            "quantity": quantity,
            "category": category,
            "completed": False
        }
        shopping_list.append(newItem)
        
        return jsonify({
            "success": True,
            "action": "add",
            "item": newItem,
            "suggestion": suggestion,
            "list": shopping_list
        })

    # 2. REMOVE COMMAND
    elif any(word in command for word in ['remove', 'delete', 'take off']):
        item_name = command
        for word in ['remove', 'delete', 'from my list', 'from the list', 'take off']:
            item_name = item_name.replace(word, '')
        item_name = item_name.strip()
        
        initial_len = len(shopping_list)
        shopping_list = [item for item in shopping_list if item['name'] not in item_name]
        
        removed = len(shopping_list) < initial_len
        return jsonify({
            "success": True,
            "action": "remove",
            "message": f"Removed {item_name}" if removed else "Item not found in list.",
            "list": shopping_list
        })

    # 3. GET LIST COMMAND
    elif 'show' in command or 'list' in command:
        return jsonify({"success": True, "action": "show", "list": shopping_list})

    return jsonify({"success": False, "message": "Command not recognized. Try 'Add 2 apples'."}), 400

@app.route('/api/list', methods=['GET'])
def get_list():
    return jsonify({"success": True, "list": shopping_list})

import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)