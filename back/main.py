from flask import Flask, request, jsonify
from model import ModelGBM
import pandas as pd
from dataset import Dataset
import numpy as np
from flask_cors import CORS
# from collections import defaultdict

data = Dataset('./files/mvp_movie.parquet')
df = data.get_data_for_pred()

model = ModelGBM('./files/lgbr_v1.txt', df)
app = Flask(__name__)
CORS(app)

# user = pd.DataFrame(0, index=df.index, columns=df.columns)
user = pd.DataFrame(0, columns=df['video_id'], index=[0])
recomended: list = []
rec_id: int | None = None

reaction_rating_table = {
    'like': lambda x : x + 1,
    'dislike': lambda x : x - 8,
    'comment': lambda x : x + 8,
    'share': lambda x : x + 4,
    'view': lambda x : x + 0.5
}

@app.route('/video', methods=['GET']) # передать доп данные для отображения
def video():
    video_id = int(request.args.get('id'))

    if not video_id:
        return jsonify({'status': 'no video_id'})
    
    # global recomended
    global rec_id
    rec_id = video_id
    # recomended = None

    user[video_id] = reaction_rating_table['view'](user[video_id])

    return data.get_data_to_view(video_id)
# title, description, category, likes, dislikes

@app.route('/react', methods=['GET'])
def react():
    video_id = int(request.args.get('id'))
    type_reaction = request.args.get('rating', 'view')
    if not video_id:
        return jsonify({'status': 'no video_id'})

    user[video_id] = reaction_rating_table[type_reaction](user[video_id])

    return jsonify({'status': 'ok'})


@app.route('/predict', methods=['GET'])
def predict():
    global recomended
    for i in recomended:
        user[i] -= 0.5
    if rec_id is not None:
        user[rec_id] += 0.5

    ids = model.pred(user)
    print('pred', ids)
    recomended = ids['video_id']
    # print(ids)

    response = {
        'predictions': data.get_data_by_ids(ids)
    }

    return jsonify(response)

if __name__ == '__main__':
    data.dataset_prepare()
    app.run(debug=True, port=5005, host='0.0.0.0')
