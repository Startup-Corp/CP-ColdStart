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
recomended: list | None = None

@app.route('/video', methods=['GET']) # передать доп данные для отображения
def video():
    video_id = int(request.args.get('id'))

    if not video_id:
        return jsonify({'status': 'no video_id'})
    
    global recomended
    recomended = None

    user[video_id] += 1


    return data.get_data_to_view(video_id)
# title, description, category, likes, dislikes

@app.route('/react', methods=['GET'])
def react():
    video_id = int(request.args.get('id'))
    rating = int(request.args.get('rating', 0))
    if not video_id:
        return jsonify({'status': 'no video_id'})

    # rating = inp_data.get('rating', 0) # 0 - dis, 1 - like
    
    if rating == 1:
        user[video_id] += 2
    else:
        user[video_id] = -2

    return jsonify({'status': 'ok'})

@app.route('/comment', methods=['GET'])
def comment():
    video_id = int(request.args.get('id'))
    comment = int(request.args.get('comment', 0))

    if not video_id:
        return jsonify({'status': 'no video_id'})

    return jsonify({'status': 'ok'})


@app.route('/predict', methods=['GET'])
def predict():
    global recomended
    if recomended is not None:
        for i in recomended:
            user[i] -= 0.5

    ids = model.pred(user)
    
    recomended = ids
    # print(ids)

    response = {
        'predictions': data.get_data_by_ids(ids)
    }

    return jsonify(response)

if __name__ == '__main__':
    data.dataset_prepare()
    app.run(debug=True, port=5005, host='0.0.0.0')
