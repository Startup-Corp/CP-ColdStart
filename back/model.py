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

        top_views_df = self.dataset.sort_values(top_views, ascending=False)['video_id'].head(20)
        avg_wt_df = self.dataset.sort_values(avg_wt, ascending=False)['video_id'].head(20)
        f_avg_wt_df = self.dataset.sort_values(f_avg_wt, ascending=False)['video_id'].head(20)
        # long_views_df = self.dataset.sort_values(long_views, ascending=False)['video_id'].head(100)
        cat_pop_df = self.dataset.sort_values(cat_pop, ascending=False)['video_id'].head(20)
        # cr_clk_df = self.dataset.sort_values(cr_clk, ascending=False)['video_id'].head(100)

        print(top_views_df.shape)
        print(avg_wt_df.shape)
        print(f_avg_wt_df.shape)
        print(cat_pop_df.shape)
        res = csr_array(rating_vec.values).dot(self.csr).toarray().flatten()
        top_similar = pd.Series(res.argsort()[-100:][::-1])

        not_interacted = rating_vec.columns[(rating_vec == 0).iloc[0]]



        return (top_similar[top_similar.isin(not_interacted)],
               top_views_df[top_views_df.isin(not_interacted)],
               avg_wt_df[avg_wt_df.isin(not_interacted)],
               f_avg_wt_df[f_avg_wt_df.isin(not_interacted)],
               cat_pop_df[cat_pop_df.isin(not_interacted)])


        res = pd.concat([top_similar, top_views_df, avg_wt_df, f_avg_wt_df, cat_pop_df])
        # res = top_views_df.append(avg_wt_df).append(f_avg_wt_df).append(cat_pop_df)
        
        not_interacted = rating_vec.columns[(rating_vec == 0).iloc[0]]

        return res[res.isin(not_interacted)].unique()

    def pred(self, rating_vec: np.ndarray = None, user_features: np.ndarray = None):
        """
        rating_vec - вектор рейтингов для каждого видео
        user_features - вектор признаков юзера (region, city)
        """
        candidates = self.candidate_selection(rating_vec, user_features)
        candidates_res = np.array([])
        for cand in candidates:
            candidates_df = self.dataset[self.dataset['video_id'].isin(cand)]
            # print(candidates_df.drop(columns=['video_id']).columns)
            res = self.model.predict(candidates_df.drop(columns=['video_id']))
        
            res_ids = candidates_df[['video_id']].assign(rating=res).sort_values('rating', ascending=False).head(2)['video_id'].values
            candidates_res = np.concatenate([candidates_res, res_ids])

        return candidates_res


if __name__ == '__main__':
    m = ModelGBM('./files/lgbr_v1.txt', pd.DataFrame())
    csr = m.load_csr()
    print(type(csr))
    print(csr)