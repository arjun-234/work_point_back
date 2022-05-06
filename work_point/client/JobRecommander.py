import pandas as pd
from sklearn.metrics.pairwise import sigmoid_kernel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel
import MySQLdb
import MySQLdb.cursors

class JobRecommander:
    
    def __init__(self):
        database = MySQLdb.connect(host = "work-point.cckrazp59xhr.ap-south-1.rds.amazonaws.com", user = "work_admin", passwd = "YpFyCwcdpKAswevhXMjy", db = "work_point", cursorclass=MySQLdb.cursors.DictCursor)
        cursor = database.cursor()


        cursor.execute("SELECT * FROM client_job")
        job_list = cursor.fetchall()
        job_list = list(job_list)


        cursor.execute("SELECT * FROM client_skill")
        skill_list = cursor.fetchall()
        skill_list = list(skill_list)


        cursor.execute("SELECT * FROM client_skill_job")
        job_skill_list = cursor.fetchall()
        job_skill_list = list(job_skill_list)


        job_df = pd.DataFrame.from_dict(job_list)
        skill_df =  pd.DataFrame.from_dict(skill_list)
        skill_df = skill_df.rename(columns={'id':'skill_id'})
        skill_df = skill_df.rename(columns={'name':'skill_name'})
        job_skill_df = pd.DataFrame.from_dict(job_skill_list)
        job_skill_df = job_skill_df.drop(['id'],axis='columns')
        job_df = job_df.rename(columns={'id':'job_id'})


        job_skill_combined = pd.merge(job_df, job_skill_df, on='job_id')


        self.combine_df = pd.merge(job_skill_combined,skill_df, on='skill_id')


        self.combine_df.drop(['is_completed','client_id','price','posted_date','skill_id'],axis='columns',inplace=True)

    def give_job_recommandation(self,username=None,skill_list=None):
        new_row = pd.DataFrame.from_dict({'title':username, 'skill_name':skill_list})
        combine_df = pd.concat([self.combine_df, new_row])


        combined_skill_list=[]
        for i in combine_df['title']:
            temp = list(combine_df[combine_df['title']==i]['skill_name'])
            combined_skill_list.append(temp)


        combine_df['skill_list'] = combined_skill_list


        combine_df.drop(['skill_name'],axis='columns',inplace=True)


        combine_df.drop_duplicates(subset=['title'],keep="first",inplace=True)


        def create_soup(x):
            return ' '.join(x['skill_list'])


        combine_df['soup'] = combine_df.apply(create_soup, axis=1)


        count = CountVectorizer(stop_words='english')
        count_matrix = count.fit_transform(combine_df['soup'])


        combine_df = combine_df.reset_index()


        indices = pd.Series(combine_df.index, index=combine_df['title'])


        sig = sigmoid_kernel(count_matrix, count_matrix)


        def give_rec(title, sig=sig):
            idx = indices[title]
            sig_scores = list(enumerate(sig[idx]))
            sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)
            sig_scores = sig_scores[:10]
            job_indices = [i[0] for i in sig_scores]
            return combine_df['job_id'].iloc[job_indices].drop(combine_df[combine_df['title'] == username].index[0]).astype(int)


        return list(give_rec(username))




