import pandas as pd
import numpy as np
import seaborn as sns
import LogisticRegression
import MultinomialLogisticRegression
import os
import sys

class MicrosimulationClass:
    def __init__(self,df,df_last_time,models=None,model_responses=None,model_predictors=None,model_transforms=None):
        '''
        :param df: a dataframe
        '''

        # attach attributes to the object
        self.df = df.copy()
        self.df_last_time = df_last_time.copy()

        self.dfs_projected = [self.df_last_time.copy()]

        self.models = []
        self.model_responses = []
        self.model_predictors = []
        self.model_transforms = []

        if models is not None:
            self.models = models
            if model_responses is not None:
                self.model_responses = model_responses
            else:
                raise Exception('Model is given but model responses is not')

            if model_predictors is not None:
                self.model_predictors = model_predictors
            else:
                raise Exception('Model is given but model predictors is not')

            if model_transforms is not None:
                self.model_transforms = model_transforms
            else:
                raise Exception('Model is given but model transforms is not')

    def add_model(self,model,response,predictors,transform=None):
        self.models.append(model)
        self.model_responses.append(response)
        self.model_predictors.append(predictors)
        self.model_transforms.append(transform)

    def advance(self):
        next_df = self.dfs_projected[-1]
        for model,response,predictors,transform in zip(self.models,self.model_responses,self.model_predictors,self.model_transforms):
            this_next_df = transform(next_df,predictors)
            next_df[response] = model.predict_next(model,this_next_df[predictors])

        self.dfs_projected.append(next_df.copy())



if __name__ == '__main__':
    current_dir = '/'.join(sys.path[0].split('/')[:-1])  # sys.path[0]
    data_dir = os.path.join(current_dir, 'Data', 'HR')
    hr_csv = os.path.join(data_dir, 'HR.csv')
    df = pd.read_csv(hr_csv)
    df_last_time = df[(df['Year'] == 2019) & (df['left'] != 1)].copy()

    predictors = ['satisfaction_level', 'last_evaluation', 'number_project', 'average_montly_hours',
                  'time_spend_company', 'Work_accident', 'promotion_last_5years', 'sales', 'salary']
    model_left = LogisticRegression.LogisticRegressionClass(df[predictors+['left']],'left')
    model_left.log_reg()
    predictors_after = list(model_left.X.columns)
    def transform(df,predictors):
        df_new = model_left.prepare_categories(df, model_left.response, drop=True)
        for predictor in predictors:
            if predictor not in list(df_new.columns):
                df_new[predictor] = 0
        return df_new

    def predict(model,df):
        preds = model.predict(df)
        a = []
        for p in preds:
            a.append(np.random.choice([0,1],1,p=[1-p,p]))
        return np.squeeze(a)

    model_left.result.predict_next = predict


    my_microsimulation = MicrosimulationClass(df,df_last_time)
    my_microsimulation.add_model(model_left.result,'left',predictors_after,transform=transform)
    my_microsimulation.advance()
    a=1