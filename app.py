from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client.dbattack


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/post', methods=['POST'])
def save_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    idx = soup.select_one('meta[property="og:idx"]')['content']
    title = soup.select_one('meta[property="og:title"]')['content']
    content = soup.select_one('meta[property="og:content"]')['content']
    reg_data = soup.select_one('meta[property="og:reg_data"]')['content']

    doc = {
        'idx': idx,
        'title': title,
        'content': content,
        'reg_data': reg_data

    }

    db.articles.insert_one(doc)

    return {"result": "success"}


@app.route('/post', methods=['GET'])
def get_post():
    articles = list(db.articles.find({}, {'_id': False}))
    return {"result": "success"}


@app.route('/post', methods=['DELETE'])
def delete_post():
    def delete_star():
        name_receive = request.form['name_give']
        db.mystar.delete_one({'name': name_receive})
        
    return {"result": "success"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)