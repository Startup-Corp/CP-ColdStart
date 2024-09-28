from flask import Flask, request, jsonify
from model import ModelGBM
import pandas as pd
from dataset import Dataset
import numpy as np

data = Dataset('./files/mvp_movie.parquet')
df = data.get_data_for_pred()

model = ModelGBM('./files/lgbr_v1.txt', df)
app = Flask(__name__)

user = np.zeros((1, df.shape[0]))# кол-во фильмов

@app.route('/video', methods=['GET']) # передать доп данные для отображения
def react():
    data = request.get_json()
    
    video_id = data.get('id')
    if not video_id:
        return jsonify({'status': 'no video_id'})
    
    user[video_id] += 1 # = 1

    return jsonify({'status': 'ok'}) 
# title, description, category, likes, dislikes

@app.route('/react', methods=['POST'])
def react():
    data = request.get_json()
    
    video_id = data.get('id')
    if not video_id:
        return jsonify({'status': 'no video_id'})

    rating = data.get('rating', 0) # 0 - dis, 1 - like
    
    user[video_id] += rating

    return jsonify({'status': 'ok'})

@app.route('/comment', methods=['POST'])
def comment():
    data = request.get_json()
    
    video_id = data.get('id')
    if not video_id:
        return jsonify({'status': 'no video_id'})

    comment = data.get('comment', 0) # 0 - dis, 1 - like
    
    # user[video_id] += rating

    return jsonify({'status': 'ok'})

@app.route('/predict', methods=['GET'])
def predict():
    ids = model.pred()
    print(ids)

    response = {
        'predictions': data.get_data_by_ids(ids)
    }

    return jsonify(response)

if __name__ == '__main__':
    data.dataset_prepare()
    app.run(debug=True, port=5005)
