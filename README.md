# VOICE_ASSISTANT
# 🛒 Smart Shopping List API

A simple Flask-based REST API for managing a smart shopping list using natural-language commands.

The application allows users to add, remove, and view shopping-list items through simple commands such as:

- `Add 2 apples`
- `Buy 1 milk`
- `Remove apples`
- `Show my list`

## 🚀 Features

- Add shopping items using natural-language commands
- Specify item quantities
- Automatically categorize shopping items
- Remove items from the shopping list
- Display the current shopping list
- Provide basic smart suggestions
- REST API using Flask
- CORS enabled for frontend integration
- In-memory data storage
- Supports deployment using the `PORT` environment variable

## 🛠️ Tech Stack

- Python
- Flask
- Flask-CORS
- Regular Expressions (`re`)
- JSON

## 📂 Project Structure

```text
project/
│
├── app.py
└── README.md
