from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
import requests
import os
import ast

# The API returns first page unless specified, and each page is limited to 1000 entries
ENDPOINT_URL = "https://the-one-api.dev/v2"
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

app = Flask(__name__)
Bootstrap5(app)

# Data from API is gotten outside the routes to minimise number of get requests used
response = requests.get(f"{ENDPOINT_URL}/book")
book_data = response.json()["docs"]

response = requests.get(f"{ENDPOINT_URL}/movie", headers=headers)
movies_data = response.json()["docs"]

response = requests.get(f"{ENDPOINT_URL}/character?sort=name:asc", headers=headers)
characters_data = response.json()["docs"]


@app.route("/")
def home():
    return render_template("index.html",
                           book_data=book_data,
                           movies_data=movies_data,
                           characters_data=characters_data)


@app.route("/book/<_id>")
def book_info(_id):
    book_name = request.args.get("book_name")

    chapter_response = requests.get(f"{ENDPOINT_URL}/book/{_id}/chapter")
    chapter_data = chapter_response.json()["docs"]
    return render_template("book_chapters.html", chapter_data=chapter_data, book_name=book_name)


@app.route("/movie/<_id>")
def movie_info(_id):
    movie_data = ast.literal_eval(request.args.get("movie_data"))
    return render_template("movie_stats.html", movie_data=movie_data)


@app.route("/character/<_id>")
def character_info(_id):
    character_data = ast.literal_eval(request.args.get("character_data"))
    quotes_response = requests.get(f"{ENDPOINT_URL}/character/{_id}/quote", headers=headers)
    character_quotes = quotes_response.json()["docs"]
    return render_template("character_info.html",
                           character_data=character_data,
                           character_quotes=character_quotes)


if __name__ == "__main__":
    app.run(debug=True)
