"""
Calculate PSI Values Module
"""

import pandas as pd
import numpy as np

class calcPSI:
    
    def __init__(self, y, y_predict_proba):
        """
        Calculates counts for PSI calculation 
        y: Targets from the train dataset
        y_predict_proba: Predicted probabilities for the train set
        """
        self.y = y
        self.y_predict_proba = y_predict_proba
        self.aggregated = pd.DataFrame({}, index=[])
        
    def psi_dev(self):
        probabilities = pd.DataFrame({}, index=[])
        probabilities["P_1"] = np.array(self.y_predict_proba)
        probabilities["Target"] = np.array(self.y)

        probabilities["Non_target"] = 1-probabilities["Target"]
        probabilities["rank"] = probabilities['P_1'].rank(method='first',ascending=False)
        probabilities["decile"] = pd.qcut(probabilities["rank"], 10, labels=False)
        grouped = probabilities.groupby("decile",sort=True)

        self.aggregated['TOTAL'] = grouped.sum()["Non_target"] + grouped.sum()["Target"]
        self.aggregated['MAX_SCORE'] = grouped.max()["P_1"]
        self.aggregated['MIN_SCORE'] = grouped.min()["P_1"]
        
        
        ## Create bins for OOTS
        self.cuts = [1.001] + self.aggregated['MIN_SCORE'].to_list()[:-1] + [0]
        self.cuts.sort()
        

        return self.aggregated
    
    def psi_test(self, y_test, y_test_predict_proba):
        """
        y_test: Targets from the test dataset
        y_test_predict_proba: Predicted probabilities for the test set
        """
        
        
        if self.aggregated.empty:
            raise RuntimeError("Run psi_dev first!")
        
        probabilities_test = pd.DataFrame({}, index=[])
        probabilities_test["Target"] = np.array(y_test)
        probabilities_test["Non_target"] = 1-probabilities_test["Target"]

        rank_df = pd.DataFrame({'tgt':y_test,'score':y_test_predict_proba}).reset_index(drop=True)
        rank_df['Rank'] = rank_df.score.rank(method='dense',ascending=False).astype(int)
        rank_df['Rank Order'] = rank_df.score.rank(method='first',ascending=False).astype(int)
        probabilities_test['decile'] = pd.qcut(rank_df['Rank Order'], 10, labels=False)
        
        
        # probabilities_test['decile'] = pd.cut(y_test_predict_proba, 
        #                                           bins=np.array(self.cuts),
        #                                           labels=[9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
        #                                           include_lowest=True, 
        #                                           right=False, 
        #                                           precision=4)
        
        grouped = probabilities_test.groupby("decile", sort=True)
        
        ## Add it to original aggregated df
        self.aggregated['TEST_COUNTS'] = grouped.sum()["Non_target"] + grouped.sum()["Target"]
        
        return self.aggregated