import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
import numpy as np


class Dataset:
    def __init__(self, path_video: str):
        self.df_video = pd.read_parquet(path_video, engine='pyarrow')
        self.predict_data = None
        print(self.df_video)


    # def create_rank(self, row):
    #     w = row['watchtime'] / row['v_duration']
    #     if w == 0:
    #         return 4
    #     elif 0 <= w <= 0.25:
    #         return 3
    #     elif 0.25 <= w <= 0.5:
    #         return 2
    #     elif 0.5 <= w <= 0.75:
    #         return 1
    #     return 0


    def dataset_prepare(self,
                      region='43d88b4b-0c70-4f47-bb59-a1e331f215bb', 
                      city='65762d4f-c467-4c84-bfd7-9f2bd6b18cd9'):
        all_data = self.df_video.copy()
        all_data['region'] = region
        all_data['city'] = city

        oe = OrdinalEncoder(dtype=np.uint64)
        all_data = all_data.drop(columns=['title', 'description'])
        for col in ['region', 'city', 'category_id', 'author_id']:
            all_data[col] = oe.fit_transform(all_data[[col]])
        all_data['v_pub_datetime'] = all_data['v_pub_datetime'].astype(int)
        # all_data['rank'] = all_data[['v_duration']].apply(lambda row: self.create_rank(row), axis=1)
        # all_data = all_data.drop(columns=['watchtime', 'event_timestamp'])
        self.predict_data = all_data


    def get_data_for_pred(self):
        if self.predict_data is None:
            self.dataset_prepare()
        return self.predict_data
    
    def get_data_to_view(self, id):
        video = self.df_video[self.df_video['video_id'] == id].iloc[0]
        return video[
            ['video_id', 'title', 'description', 'category_id', 'v_likes', 'v_dislikes']
        ].to_dict()


    def get_data_by_ids(self, ids: list):
        top_10 = self.df_video[self.df_video['video_id'].isin(ids)]
        print(len(top_10))
        res = []
        for i in range(len(top_10)):
            v = top_10.iloc[i, :]
            res.append({
                'id': int(v['video_id']),
                'title': v['title'],
                'desc': v['description'],
                'category': v['category_id'],
                'views': int(v['v_year_views']),
                'pub_datetime': v['v_pub_datetime'],
            })
        return res

