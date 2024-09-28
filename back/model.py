import lightgbm
import pandas as pd
import numpy as np

class ModelGBM:
    def __init__(self, path_to_model, dataset: pd.DataFrame ) -> None:
        with open(path_to_model, 'r') as file:
            data = file.read()

        self.model = lightgbm.Booster(model_str=data)
        self.dataset = dataset
    
    def candidate_selection(self, rating_vec: np.ndarray, user_features: np.ndarray):
        """
        rating_vec - вектор рейтингов для каждого видео
        user_features - вектор признаков юзера (region, city)
        """
        current_time = pd.Timestamp.now()

        top_views = 'v_week_views'
        avg_wt = 'v_avg_watchtime_7_day'
        f_avg_wt = 'v_frac_avg_watchtime_30_day_duration'
        long_views = 'v_long_views_30_days'
        cat_pop = ''

    def pred(self, rating_vec: np.ndarray, user_features: np.ndarray):
        """
        rating_vec - вектор рейтингов для каждого видео
        user_features - вектор признаков юзера (region, city)
        """
        print(self.dataset.drop(columns=['video_id']).columns)
        res = self.model.predict(self.dataset.drop(columns=['video_id']))
        
        res_ids = self.dataset[['video_id']].assign(rating=res).sort_values('rating', ascending=False).head(10)['video_id'].values
        return res_ids
