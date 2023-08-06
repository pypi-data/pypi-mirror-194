"""
Shapley Values Module
"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import openpyxl as op

from datetime import *
import time
import random
seed = 42
import shap
import os

# import warnings

# warnings.filterwarnings("ignore")


class shapPlots:
    
    def __init__(self, model, x_data):
        """
        model - Model object - Only tree based models
        x_data - The independent featreus used to train the model
        """
        
        shap.initjs()
        
        self.model = model
        self.x_data = x_data
        self.explainer = shap.TreeExplainer(self.model)
        self.shap_values = self.explainer.shap_values(self.x_data)
        
        
    def summaryPlot(self, data=None, save_plot=None):
        if isinstance(data, pd.DataFrame):
            shap.summary_plot(self.shap_values, data, show=False)
            if isinstance(save_plot, str):
                if not os.path.exists(save_plot):
                    os.makedirs(save_plot)
                    plt.savefig(save_plot+"/summary_plot.png", dpi=600, bbox_inches='tight')
                else:
                    plt.savefig(save_plot+"/summary_plot.png", dpi=600, bbox_inches='tight')
        else:
            shap.summary_plot(self.shap_values, self.x_data, show=False)
            if isinstance(save_plot, str):
                if not os.path.exists(save_plot):
                    os.makedirs(save_plot)
                    plt.savefig(save_plot+"/summary_plot.png", dpi=600, bbox_inches='tight')
                else:
                    plt.savefig(save_plot+"/summary_plot.png", dpi=600, bbox_inches='tight')
            
    def abs_shap(self, save_plot=None):
        
        print("8")
        # Make a copy of the input data
        shap_values_df = pd.DataFrame(self.shap_values)
        feature_list = self.x_data.columns
        shap_values_df.columns = feature_list
        df_v = self.x_data.copy().reset_index().drop('index', axis=1)

        # Determine the correlation in order to plot with different colors
        corr_list = list()
        for i in feature_list:
            b = np.corrcoef(shap_values_df[i], df_v[i])[1][0]
            corr_list.append(b)
        corr_df = pd.concat([pd.Series(feature_list), pd.Series(corr_list)], axis=1).fillna(0)

        # Make a data frame. Column 1 is the feature, and Column 2 is the correlation coefficient
        corr_df.columns  = ['Variable','Corr']
        corr_df['Sign'] = np.where(corr_df['Corr']>0, 'red', 'blue')

        # Plot it
        shap_abs = np.abs(shap_values_df)
        k = pd.DataFrame(shap_abs.mean()).reset_index()
        k.columns = ['Variable','SHAP_abs']
        k2 = k.merge(corr_df, left_on = 'Variable', right_on='Variable', how='inner')
        k2 = k2.sort_values(by='SHAP_abs', ascending = True)
        colorlist = k2['Sign']
        ax = k2.plot.barh(x='Variable', y='SHAP_abs', color = colorlist, figsize=(12, 8), legend=False)
        ax.set_xlabel("SHAP Value (Red = Positive Impact)")
        if isinstance(save_plot, str):
            if not os.path.exists(save_plot):
                os.makedirs(save_plot)
                plt.savefig(save_plot+"/abs_shap.png", dpi=600, bbox_inches='tight')
            else:
                plt.savefig(save_plot+"/abs_shap.png", dpi=600, bbox_inches='tight')