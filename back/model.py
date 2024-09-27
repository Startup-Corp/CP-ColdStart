import lightgbm
import pandas as pd

class ModelGBM:
    def __init__(self, path_to_model, dataset: pd.DataFrame ) -> None:
        self.model = lightgbm.Booster(model_file=path_to_model)
        self.dataset = dataset

    def pred(self):
        print(self.dataset.drop(columns=['video_id']).columns)
        res = self.model.predict(self.dataset.drop(columns=['video_id']))

        res_df = self.dataset[['video_id']].copy()
        res_df['rating'] = res
        res_df = res_df.sort_values('rating', ascending=False)
        
        res_ids = res_df.head(10)['video_id'].values
        return res_ids
