import lightgbm
import pandas as pd
import numpy as np
from scipy.sparse import load_npz
from scipy.sparse import csr_matrix, csr_array

class ModelGBM:
    def __init__(self, 
                 path_to_model: str, 
                 dataset: pd.DataFrame,
                 csr_path: str = './files/video_csr_matrix.npz') -> None:
        with open(path_to_model, 'r') as file:
            data = file.read()

        self.model = lightgbm.Booster(model_str=data)
        self.dataset = dataset
        self.csr_path = csr_path
        self.csr = self.load_csr()

    def load_csr(self):
        return load_npz(self.csr_path)
    
    def candidate_selection(self, rating_vec: np.ndarray, user_features: np.ndarray):
        """
        rating_vec - вектор рейтингов для каждого видео
        user_features - вектор признаков юзера (region, city)
        """
        current_time = pd.Timestamp.now()



        top_views = 'v_week_views' # много просмотров
        avg_wt = 'v_avg_watchtime_7_day' # дольше всего смотрели
        f_avg_wt = 'v_frac_avg_watchtime_30_day_duration' # лучшая досматриваемость
        # long_views = 'v_long_views_30_days' # кол-во длинных просмотров
        cat_pop = 'v_category_popularity_percent_30_days' # популярность категории
        # cr_clk = 'v_cr_click_long_view_7_days' # привлекает длинные клики

        top_views_df = self.dataset.sort_values(top_views, ascending=False)['video_id'].head(100)
        avg_wt_df = self.dataset.sort_values(avg_wt, ascending=False)['video_id'].head(100)
        f_avg_wt_df = self.dataset.sort_values(f_avg_wt, ascending=False)['video_id'].head(100)
        # long_views_df = self.dataset.sort_values(long_views, ascending=False)['video_id'].head(100)
        cat_pop_df = self.dataset.sort_values(cat_pop, ascending=False)['video_id'].head(100)
        # cr_clk_df = self.dataset.sort_values(cr_clk, ascending=False)['video_id'].head(100)

        # csr_rating = csr_array(rating_vec)
        # top_similar = load_npz(self.csr_path).dot(csr_rating).toarray().argsort()[-100:][::-1]


        res = top_views_df.append(avg_wt_df).append(f_avg_wt_df).append(cat_pop_df).to_list()
        
        not_interacted = rating_vec.columns[(rating_vec == 0).iloc[0]]

        return res[res.isin(not_interacted)]

        

    def pred(self, rating_vec: np.ndarray = None, user_features: np.ndarray = None):
        """
        rating_vec - вектор рейтингов для каждого видео
        user_features - вектор признаков юзера (region, city)
        """
        candidates = self.candidate_selection(rating_vec, user_features)
        candidates_df = self.dataset[self.dataset['video_id'].isin(candidates)]

        print(candidates_df.drop(columns=['video_id']).columns)
        res = self.model.predict(candidates_df.drop(columns=['video_id']))
        
        res_ids = candidates_df[['video_id']].assign(rating=res).sort_values('rating', ascending=False).head(10)['video_id'].values
        return res_ids


if __name__ == '__main__':
    m = ModelGBM('./files/lgbr_v1.txt', pd.DataFrame())
    csr = m.load_csr()
    print(type(csr))
    print(csr)