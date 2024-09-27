from flask import Flask, request, jsonify
from model import ModelGBM
import pandas as pd
from dataset import Dataset

data = Dataset('./files/mvp_movie.parquet')
df = data.get_data_for_pred()

model = ModelGBM('./files/lgbr_v1.txt', df)
app = Flask(__name__)


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
