"""
Data Modelling Module
"""

import os
import joblib
import pandas as pd
import openpyxl as op
from openpyxl.styles.borders import Border, Side, BORDER_THIN
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn import model_selection
from sklearn.model_selection import train_test_split,GridSearchCV
from  sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score,recall_score,precision_score,f1_score,confusion_matrix,roc_auc_score,classification_report

class modelData:
    """Class to build, evaluate and predict model"""

    def modelbuild(self,data,cols,target,split_size):
        """
        Build the model on the data

        Parameters
        ----------
        data : dataframe
                Input dataframe.
        cols: List of str
                List of input columns
        target : str
                Target column name
        split_size : float
                Split size value of data

        Returns
        -------
        fit_model : self
                    Fitted model estimator.
        """
        print("\nModel Generation starts...")

        print("\nSplitting the data into train and test...")
        X = data[cols]
        Y = data[target]
        X_train, X_test, y_train, y_test = train_test_split(X, Y, train_size=split_size, random_state=42)
        print("Size of the X-train dataset: ",X_train.shape)
        print("Size of the X-test dataset: ",X_test.shape)

        print("\nBuilding the model...")

        dfs = []
        models = [('LogReg', LogisticRegression(solver='lbfgs', max_iter=1000)),('RF', RandomForestClassifier()),('XGB', XGBClassifier())]
        results = []
        names = []
        scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
        target_names = ['0', '1']
        for name, model in models:
                kfold = model_selection.KFold(n_splits=5, shuffle=True, random_state=42)
                cv_results = model_selection.cross_validate(model, X_train, y_train, cv=kfold, scoring=scoring)
                clf = model.fit(X_train, y_train)
                y_pred = clf.predict(X_test)
                print(name)
                print(classification_report(y_test, y_pred, target_names=target_names))
                results.append(cv_results)
                names.append(name)
                this_df = pd.DataFrame(cv_results)
                this_df['model'] = name
                this_df['test_confusion_matrix'] = str(confusion_matrix(y_test, y_pred))
                this_df['params'] = str(model.get_params())
                # save the model to disk
                newpath = r'model_results'
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                filename = newpath+ '/' + name.lower() + '_model.pkl'
                this_df['pickle'] = filename
                joblib.dump(model, filename)
                dfs.append(this_df)
        final = pd.concat(dfs, ignore_index=True)
        final['split'] = final.index%5 + 1
        final = final [['split','model','params','test_accuracy','test_precision','test_recall','test_f1', 'test_confusion_matrix','test_roc_auc','pickle']]

        print("\nWriting Model Evaluation Results to excel...")
        with pd.ExcelWriter("documentation_final.xlsx",mode="a",engine="openpyxl",if_sheet_exists="overlay") as writer:
            final.to_excel(writer, sheet_name='6. Overview of Model Eval',startrow=2,startcol=0,index=False,header=False)
        xfile = op.load_workbook('documentation_final.xlsx')
        sheet = xfile['6. Overview of Model Eval']
        thin_border = Border(
                                left=Side(border_style=BORDER_THIN, color='00000000'),
                                right=Side(border_style=BORDER_THIN, color='00000000'),
                                top=Side(border_style=BORDER_THIN, color='00000000'),
                                bottom=Side(border_style=BORDER_THIN, color='00000000'))
        for r in range(3,final.shape[0]+3):
                for c in range(1,12):
                        sheet.cell(row=r, column=c).border = thin_border
        xfile.save('documentation_final.xlsx')

        return X_train, X_test, y_train, y_test, final



    def modeltuning(self,model,X,y):
        """
        Tuning the model hyperparameters

        Parameters
        ----------
        model : model object
            Model object built
        X: dataframe
            Input dataframe
        y : dataframe
            Target dataframe

        Returns
        -------
        gs_result : self
                    Fitted model estimator.
        """
        print("\nModel Tuning starts...")
        parameters = [{'penalty':['l1','l2']},
                    {'C':[0.001, 0.01, 0.1, 1, 10, 100, 1000]}]
        grid_search = GridSearchCV(estimator = model,
                                param_grid = parameters,
                                scoring = 'accuracy',
                                cv = 5,
                                verbose=0)
        gs_result = grid_search.fit(X, y)
        print("\nBest Score: %s" % gs_result.best_score_)
        print("\nBest Hyperparameters: %s" % gs_result.best_params_)
        print("\nModel Tuning ends...")

        return gs_result

    def modeleval(self,model,X,y,metrics_data,data_type='train'):
        """
        Model Evaluation

        Parameters
        ----------
        model : model object
            Model object built
        X: dataframe
            Input dataframe
        y : dataframe
            Target dataframe
        metrics_data : dataframe
            Evaluation Metrics dataframe
        data_type : str
            Type of data, train, test or validation

        Returns
        -------
        y_pred : array-like
            Predicted values array
        """
        print("\nModel Evaluation starts...")

        y_pred = model.predict(X)

        # Model Evaluation metrics
        print("\nType of Data : " + data_type)
        print("\nAlgroithm : " + str(model))
        print("\nParamters Used : " + str(model.get_params()))
        print("\nAccuracy Score : " + str(accuracy_score(y,y_pred)))
        print("\nPrecision Score : " + str(precision_score(y,y_pred)))
        print("\nRecall Score : " + str(recall_score(y,y_pred)))
        print("\nF1 Score : " + str(f1_score(y,y_pred)))
        print("\nConfusion Matrix :", confusion_matrix(y, y_pred))
        print("\nArea Under the ROC Curve :", roc_auc_score(y, y_pred))

        row_to_append = pd.DataFrame([{'Type of Data':data_type,'Algorithm':str(model),'Parameters':str(model.get_params()),'Accuracy Score':str(accuracy_score(y,y_pred)),'Precision Score':str(precision_score(y,y_pred)),'Recall Score':str(recall_score(y,y_pred)),'F1 Score':str(f1_score(y,y_pred)),'Confusion Matrix':confusion_matrix(y, y_pred),'Area under the ROC':roc_auc_score(y, y_pred)}])
        metrics_data = pd.concat([metrics_data,row_to_append])

        return y_pred,metrics_data
