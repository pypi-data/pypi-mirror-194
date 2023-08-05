import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, accuracy_score, roc_curve, auc

class DSTools:
    def __init__(self):
        pass

    @staticmethod
    def roc_optimal_cutoff(y_pred_prob, y_true):
        """
        A function to find the optimal cutoff value for binary classification using Receiver Operating Characteristic (ROC) curve.

        Parameters:
        -----------
        y_pred_prob (array-like): Predicted probabilities for the positive class.

        y_true (array-like): True binary labels.

        Returns:
        -----------
        float: Optimal cutoff value for binary classification.

        Example:
        -----------
        >>> import numpy as np
        >>> from sklearn.metrics import roc_auc_score
        >>> y_pred_prob = np.array([0.2, 0.4, 0.6, 0.8])
        >>> y_true = np.array([0, 0, 1, 1])
        >>> roc_optimal_cutoff(y_pred_prob, y_true)
        0.6
        """
        fpr, tpr, thresholds = roc_curve(y_true=y_true, y_score=y_pred_prob)
        # thresholds are for predicting true (Above which will be predicted as true)
        roc_auc = auc(fpr, tpr)
        optimal_idx = np.argmax(tpr - fpr)
        optimalTrueCutoff = thresholds[optimal_idx]
        sns.lineplot(x=fpr, y=tpr)
        sns.lineplot(x=[0, 1], y=[0, 1], linestyle='dashed')
        sns.scatterplot(x=[fpr[optimal_idx]], y=[tpr[optimal_idx]], s=80, color='green')
        # linestyle takes following input: 'solid', 'dashed', 'dashdot' and 'dotted'
        plt.text(0.5, 0.2, 'AUC: {:.2f}%'.format(roc_auc * 100), fontsize=20)
        plt.text(fpr[optimal_idx] + 0.02, tpr[optimal_idx] - 0.05, 'Optimal Cutoff', fontsize=10)
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title('ROC Curve', fontsize=20)
        plt.show()
        return optimalTrueCutoff

    @staticmethod
    def compareRegressors(X, y, regressorList, numOfRun=10, testSize=0.2, regressorNames=None):
        """
        Compares the R2 score of different regressors on a given dataset.

        Parameters:
        -----------
        X : numpy.ndarray or pandas.DataFrame
            The feature matrix of shape (n_samples, n_features).

        y : numpy.ndarray or pandas.Series
            The target vector of shape (n_samples,).

        regressorList : list of regressor objects
            A list of regressors to compare. Each regressor should implement the `fit` and `predict` methods.

        numOfRun : int, optional (default=10)
            The number of times to repeat the train/test split and regression.

        testSize : float, optional (default=0.2)
            The fraction of the data to use as the test set in each run.

        regressorNames : list of strings, optional (default=None)
            A list of names for the regressors. If provided, the names will be used in the plot.

        Returns:
        --------
        None

        Examples:
        ---------
        >>> from sklearn.linear_model import LinearRegression, Ridge, Lasso
        >>> from sklearn.datasets import load_boston
        >>> X, y = load_boston(return_X_y=True)
        >>> regressorList = [LinearRegression(), Ridge(), Lasso(alpha=0.1)]
        >>> compareRegressors(X, y, regressorList, numOfRun=5, testSize=0.3, regressorNames=['LR', 'Ridge', 'Lasso'])
        """
        performanceDataframe = pd.DataFrame()
        modelNumber = 1
        for regressor in regressorList:
            performanceList = []
            n = 1
            while n <= numOfRun:
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=testSize, random_state=None)
                regressor.fit(X_train, y_train)
                prediction = regressor.predict(X_test)
                r2 = r2_score(y_test, prediction)
                performanceList.append(r2)
                n = n + 1
            modelName = ''
            if regressorNames is not None:
                modelName = regressorNames[modelNumber - 1]
            else:
                modelName = 'Model ' + str(modelNumber)
            performanceDataframe[modelName] = performanceList
            modelNumber = modelNumber + 1
        sns.boxplot(data=performanceDataframe)
        plt.title('Model Performance (R2)', fontsize=15)
        plt.show()

    @staticmethod
    def compareClassifiers(X, y, classifierList, numOfRun=10, testSize=0.2, classifierNames=None):
        """
        Compares the Accuracy score of different classifiers on a given dataset.

        Parameters:
        -----------
        X : numpy.ndarray or pandas.DataFrame
            The feature matrix of shape (n_samples, n_features).
        y : numpy.ndarray or pandas.Series
            The target vector of shape (n_samples,).
        classifierList : list
            A list of scikit-learn classifier objects to evaluate.
        numOfRun : int, optional (default=10)
            The number of times to perform the k-fold cross-validation.
        testSize : float, optional (default=0.2)
            The proportion of the data to include in the test split.
        classifierNames : list, optional (default=None)
            A list of string names for each classifier in classifierList.

        Returns:
        --------
        None

        Examples:
        ---------
        >>> from sklearn.datasets import load_iris
        >>> from sklearn.linear_model import LogisticRegression
        >>> from sklearn.tree import DecisionTreeClassifier
        >>> X, y = load_iris(return_X_y=True)
        >>> classifierList = [LogisticRegression(), DecisionTreeClassifier()]
        >>> compareClassifiers(X, y, classifierList, numOfRun=5, testSize=0.3, regressorNames=['LR', 'DecisionTree'])
        """

        performanceDataframe = pd.DataFrame()
        modelNumber = 1
        for classifier in classifierList:
            performanceList = []
            n = 1
            while n <= numOfRun:
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=testSize, random_state=None)
                classifier.fit(X_train, y_train)
                prediction = classifier.predict(X_test)
                accuracy = accuracy_score(y_test, prediction)
                performanceList.append(accuracy)
                n = n + 1
            modelName = ''
            if classifierNames is not None:
                modelName = classifierNames[modelNumber - 1]
            else:
                modelName = 'Model ' + str(modelNumber)
            performanceDataframe[modelName] = performanceList
            modelNumber = modelNumber + 1
        sns.boxplot(data=performanceDataframe)
        plt.title('Model Performance (Accuracy)', fontsize=15)
        plt.show()














