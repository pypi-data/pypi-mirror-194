import seaborn as sns  # enhanced data viz
import matplotlib.pyplot as plt                      # data visualization
from sklearn.metrics import confusion_matrix         # confusion matrix
import numpy as np

class MBAN:

    def __init__(self):
        self.temp = 0

    def import_data_explore(self):
        print("""
        # importing libraries
        import pandas as pd                   # data science essentials
        import matplotlib.pyplot as plt       # essential graphical output
        import seaborn as sns                 # enhanced graphical output
        import numpy as np                    # mathematical essentials

        # setting pandas print options
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)

        # specifying file name
        file = './file.xlsx'

        # reading the file into Python
        housing = pd.read_excel(io = file)

        # outputting the first ten rows of the dataset
        housing.head(n=10)
        """) 
        
    def import_linear_regression(self):
        print("""
        # importing libraries
        import pandas as pd # data science essentials
        import matplotlib.pyplot as plt # data visualization
        import seaborn as sns # enhanced data visualization
        import statsmodels.formula.api as smf # regression modeling
        from sklearn.model_selection import train_test_split # train/test split
        import sklearn.linear_model # linear modeling in scikit-learn

        # setting pandas print options
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)

        # specifying the path and file name
        file = './__datasets/housing_feature_rich.xlsx'

        # reading the file into Python
        housing = pd.read_excel(file)

        # checking the file
        housing.head(n = 5)
        """)
        
    def import_CART_ensemble(self):
        print("""
        # importing critical libraries
        import pandas            as pd                 # data science essentials
        import matplotlib.pyplot as plt                # data visualization
        import seaborn           as sns                # enhanced data viz
        import statsmodels.formula.api as smf # regression modeling

        # importing machine learning models
        from sklearn.tree     import DecisionTreeRegressor     # regression trees
        from sklearn.ensemble import RandomForestRegressor     # random forest
        from sklearn.ensemble import GradientBoostingRegressor # gbm

        # importing machine learning tools
        from sklearn.model_selection import train_test_split # train-test split
        from sklearn.tree import plot_tree                   # tree plots

        # loading data
        housing = pd.read_excel('./__datasets/housing_feature_rich.xlsx')

        # setting pandas print options
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_colwidth', 100)

        # displaying the head of the dataset
        housing.head(n = 5)
        """)

    def import_hyperparam_tune(self):
        print("""
        ########################################
        # importing packages
        ########################################
        import matplotlib.pyplot as plt                      # data visualization
        import pandas as pd                                  # data science essentials
        from sklearn.model_selection import train_test_split # train-test split
        from sklearn.tree import DecisionTreeRegressor       # regression trees
        from sklearn.ensemble import RandomForestRegressor   # random forest
        from sklearn.tree import plot_tree                   # tree plots
        from sklearn.model_selection import RandomizedSearchCV # hyperparameter tuning

        ########################################
        # loading data and setting display options
        ########################################
        housing = pd.read_excel('./file.xlsx')

        # setting pandas print options
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_colwidth', 100)

        ########################################
        # x-variable sets
        ########################################
        x_variables = ['x1', 'x2', 'x3']

        full_x = ['x1', 'x2', 'x3', 'x4']

        reduced_x = ['x1', 'x2']

        ########################################
        # checking results
        ########################################
        housing.head(n = 5)""")

    def import_classification(self):
        print("""
        # importing libraries
        import pandas            as pd                       # data science essentials
        import matplotlib.pyplot as plt                      # data visualization
        import seaborn           as sns                      # enhanced data viz
        from sklearn.model_selection import train_test_split # train-test split
        from sklearn.linear_model import LogisticRegression  # logistic regression
        import statsmodels.formula.api as smf                # logistic regression
        from sklearn.metrics import confusion_matrix         # confusion matrix
        from sklearn.metrics import roc_auc_score            # auc score
        from sklearn.neighbors import KNeighborsClassifier   # KNN for classification
        from sklearn.neighbors import KNeighborsRegressor    # KNN for regression
        from sklearn.preprocessing import StandardScaler     # standard scaler
        from sklearn.tree import DecisionTreeClassifier      # classification trees
        from sklearn.tree import plot_tree                   # tree plots

        # loading data
        data = pd.read_excel("./file.xlsx")

        # setting pandas print options
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_colwidth', 100)

        # displaying the head of the dataset
        data.head(n = 5)""")

    def import_prediction_threshold(self):
        print("""
        # importing libraries
        import pandas            as pd                       # data science essentials
        import matplotlib.pyplot as plt                      # data visualization
        import seaborn           as sns                      # enhanced data viz
        from sklearn.model_selection import train_test_split # train-test split
        from sklearn.linear_model import LogisticRegression  # logistic regression
        import statsmodels.formula.api as smf                # logistic regression
        from sklearn.metrics import confusion_matrix         # confusion matrix
        from sklearn.metrics import roc_auc_score            # auc score
        from sklearn.neighbors import KNeighborsClassifier   # KNN for classification
        from sklearn.neighbors import KNeighborsRegressor    # KNN for regression
        from sklearn.preprocessing import StandardScaler     # standard scaler
        from sklearn.tree import DecisionTreeClassifier      # classification trees
        from sklearn.tree import plot_tree                   # tree plots

        # loading data
        data = pd.read_excel('./file.xlsx')

        # setting pandas print options
        pd.set_option('display.max_rows', 500)
        pd.set_option('display.max_columns', 500)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_colwidth', 100)

        # displaying the head of the dataset
        data.head(n = 5)
        """)

    def data_size(self):
        print(
        "# formatting and printing the dimensions of the dataset"
        "print(f"""""
        "Size of Original Dataset"
        "------------------------"
        
        "Observations: {data.shape[0]}"
        "Features:     {data.shape[1]}"
        """")")

    def histplot(self):
        print("""
        # developing a histogram using HISTPLOT
        sns.histplot(data   = data,
                    x      = 'Price',
                    kde    = True)

        # title and axis labels
        plt.title(label   = "Original Distribution of data Prices")
        plt.xlabel(xlabel = "Price") # avoiding using dataset labels
        plt.ylabel(ylabel = "Count")

        # displaying the histogram
        plt.show()
                """)

    def corr_base_model(self):
        print("""
        # creating a list of continuous features (including Sale_Price)
        continuous_data = ['Var_1', 'Var_2', 'Var_3']

        # developing a correlation matrix based on continuous features
        chef_corr = data[continuous_data].corr(method = 'pearson')

        # filtering the results to only show correlations with Sale_Price
        chef_corr.loc[ : , 'Price'].round(decimals = 2).sort_values(ascending = False)
                """)
        
    def corr_new_features(self):
        print("""
        # developing a small correlation matrix
        zeroes_corr = housing.corr()    # .round(decimals = 2)

        # checking the correlations of the newly-created variables with Price
        zeroes_corr.loc['Price',                   # Y-variable
                       ['has_Second_Flr', 'has_Garage', # X-variables
                        'has_Mas_Vnr', 'has_Porch']] \
                        .sort_values(ascending = False)
        """)

    def scatterplot(self):
        print("""
        # scatterplot - orig ovr_qual and price
        sns.scatterplot(x    = 'Overall_Qual',
                        y    = 'Sale_Price',
                        data = housing)

        # titles and axis labels
        plt.title(label   = 'Scatterplot with Interval Data')
        plt.xlabel(xlabel = 'Overall Quality')
        plt.ylabel(ylabel = 'Sale Price')

        # displaying the plot
        plt.show()
        """)

    def scatterplot_by_subplots(self):
        print("""
        # setting figure size
        fig, ax = plt.subplots(figsize = (9, 6))
        # to adjust the gap between subplots
        #fig.subplots_adjust(hspace=0.325, wspace=0.225)

        # (row, col, index)
        plt.subplot(3, 2, 6)
        sns.boxplot(x = chef['WEEKLY_PLAN'],
                        y = chef['REVENUE'],
                        color = 'green')
        # adding labels but not adding title
        # rotate populated xtickers
        plt.xticks(rotation=60)
        plt.xlabel(xlabel = 'Weekly Plan')
        plt.ylabel(ylabel = 'Revenue')

        # SHOWing the results
        plt.show()""")

    def plot_feature_imprt(self):
        print("""
        # plotting feature importance
        plot_feature_importances(tree_pruned,
                                train = x_train,
                                export = False)
        """)

    def ols_model_statsmodel(self,data, delete_col):
        temp_string = ""
        for val in data:
            if val != delete_col:
                temp_string += (f" {val} + \n")
            else:
                pass
        print("# Step 1: INSTANTIATE a model object\n"
        f'lm_best = smf.ols(formula = """{delete_col} ~ {temp_string}"""\n'
        f"                               data = {data})\n\n"
        "# Step 2: FIT the data into the model object\n"
        "results = lm_best.fit()\n\n"
        "# Step 3: analyze the SUMMARY output\n"
        "print(results.summary())")

    def logistic_regression_statsmodels(self,data,delete_col):
        temp_string = ""
        for val in data:
            if val != delete_col:
                temp_string += (f" {val} + \n")
            else:
                pass
        print(\
            '# Step 1: INSTANTIATE logistic regression model object\n'
            f'logistic_full = smf.logit(formula = """ {delete_col} ~ {temp_string} """,\n'
            f'                          data    = {data})\n\n'
            "# Step 2: FIT the data into the model object\n"
            'results_full = logistic_full.fit()\n\n'
            "# Step 3: analyze the SUMMARY output\n"
            'results_full.summary2()'
            )
    def logistic_regression_scikit(self):
        print("""
        # train/test split with the full model
        titanic_data   =  titanic.loc[ : , candidate_dict[_____]]
        titanic_target =  titanic.loc[ : , _____]

        # This is the exact code we were using before
        _____, _____, _____, _____ = _____(
                    _____,
                    _____,
                    test_size    = 0.25,
                    random_state = 219,
                    stratify     = _____)

        # INSTANTIATING a logistic regression model
        logreg = LogisticRegression(solver = 'lbfgs',
                                    C = 1,
                                    random_state = 219)

        # FITTING the training data
        logreg_fit = logreg.fit(_____, _____)

        # PREDICTING based on the testing set
        logreg_pred = logreg_fit.predict(_____)

        # SCORING the results
        print('Training ACCURACY:', logreg_fit.score(_____, _____).round(4))
        print('Testing  ACCURACY:', logreg_fit.score(_____, _____).round(4))

        # saving scoring data for future use
        logreg_train_score = logreg_fit.score(_____, _____).round(4) # accuracy
        logreg_test_score  = logreg_fit.score(_____, _____).round(4) # accuracy""")

    def confusion_matrix(self):
        print("""
        # creating a confusion matrix
        print(confusion_matrix(y_true = y_test,
                            y_pred = logreg_pred))

        # unpacking the confusion matrix
        logreg_tn, \
        logreg_fp, \
        logreg_fn, \
        logreg_tp = confusion_matrix(y_true = y_test, y_pred = logreg_pred).ravel()

        # printing each result one-by-one
        print(
        "True Negatives : {logreg_tn}\n"
        "False Positives: {logreg_fp}\n"
        "False Negatives: {logreg_fn}\n"
        "True Positives : {logreg_tp}\n")

        # calling the visual_cm function
        visual_cm(true_y = y_test,
                pred_y = logreg_pred,
                labels = ['Life Boat', 'Not In Life Boat'])
            """)
    def auc(self):
        print("""
        # area under the roc curve (auc)
        print(roc_auc_score(y_true  = y_test,
                            y_score = logreg_pred).round(decimals = 4))

        # saving AUC score for future use
        logreg_auc_score = roc_auc_score(y_true  = y_test,
                                        y_score = logreg_pred).round(decimals = 4)""")
    
    def auc_coeff(self):
        print("""
        # zipping each feature name to its coefficient
        logreg_model_values = zip(titanic[candidate_dict['logit_sig_2']].columns,
                                logreg_fit.coef_.ravel().round(decimals = 2))

        # setting up a placeholder list to store model features
        logreg_model_lst = [('intercept', logreg_fit.intercept_[0].round(decimals = 2))]

        # printing out each feature-coefficient pair one by one
        for val in logreg_model_values:
            logreg_model_lst.append(val)

        # checking the results
        for pair in logreg_model_lst:
            print(pair)""")
        
    def auc_decision_tree(self):
        print("""
        # INSTANTIATING a classification tree object
        full_tree = DecisionTreeClassifier()

        # FITTING the training data
        full_tree_fit = full_tree.fit(x_train, y_train)

        # PREDICTING on new data
        full_tree_pred = full_tree_fit.predict(x_test)

        # SCORING the model
        print('Full Tree Training ACCURACY:', full_tree_fit.score(x_train,
                                                            y_train).round(4))
        print('Full Tree Testing ACCURACY :', full_tree_fit.score(x_test,
                                                            y_test).round(4))
        print('Full Tree AUC Score:', roc_auc_score(y_true  = y_test,
                                                    y_score = full_tree_pred).round(4))

        # saving scoring data for future use
        full_tree_train_score = full_tree_fit.score(x_train, y_train).round(4) # accuracy
        full_tree_test_score  = full_tree_fit.score(x_test, y_test).round(4)   # accuracy

        # saving AUC
        full_tree_auc_score   = roc_auc_score(y_true  = y_test,
                                            y_score = full_tree_pred).round(4) # auc
        """)

    def auc_compare_result(self):
        print("""
        # comparing results
        print(
        "Model         AUC Score      TN, FP, FN, TP\n"
        "-----         ---------      --------------\n"
        f"Logistic      {logreg_auc_score}         {logreg_tn, logreg_fp, logreg_fn, logreg_tp}\n"
        f"Full Tree     {full_tree_auc_score}           {full_tree_tn, full_tree_fp, full_tree_fn, full_tree_tp}\n"
        f"Pruned Tree   {pruned_tree_auc_score}         {pruned_tree_tn, pruned_tree_fp, pruned_tree_fn, pruned_tree_tp}\n")

        # creating a dictionary for model results
        model_performance = {
            
            'Model Name'    : ['Logistic', 'Full Tree', 'Pruned Tree'],
                
            'AUC Score' : [logreg_auc_score, full_tree_auc_score, pruned_tree_auc_score],
            
            'Training Accuracy' : [logreg_train_score, full_tree_train_score,
                                pruned_tree_train_score],
                
            'Testing Accuracy'  : [logreg_test_score, full_tree_test_score,
                                pruned_tree_test_score],

            'Confusion Matrix'  : [(logreg_tn, logreg_fp, logreg_fn, logreg_tp),
                                (full_tree_tn, full_tree_fp, full_tree_fn, full_tree_tp),
                                (pruned_tree_tn, pruned_tree_fp, pruned_tree_fn, pruned_tree_tp)]}

        # converting model_performance into a DataFrame
        model_performance = pd.DataFrame(model_performance)

        # sending model results to Excel
        model_performance.to_excel('./__results/classification_model_performance.xlsx',
                                index = False)
        """)

    def visual_tree_output(self):
        print("""
        # setting figure size
        plt.figure(figsize=(150,50))

        # developing a plotted tree
        plot_tree(decision_tree = full_tree_fit, 
                feature_names = titanic.columns,
                filled        = True, 
                rounded       = True, 
                fontsize      = 14)

        # rendering the plot
        plt.show()
        """)

    def loop_check_missing(self):
        print("""
        # looping to detect features with missing values
        for col in housing:

        # creating columns with 1s if missing and 0 if not
        if housing[col].isnull().astype(int).sum() > 0:
        housing['m_'+col] = housing[col].isnull().astype(int)


        # summing the missing value flags to check the results of the loop above
        housing[    ['m_Mas_Vnr_Area', 'm_Total_Bsmt_SF',
                    'm_Garage_Cars', 'm_Garage_Area']    ].sum(axis = 0)
        """)

    def log_transform(self):
        print("""
        # log transforming Lot_Area and saving it to the dataset
        housing['log_Lot_Area'] = np.log(housing['Lot_Area'])

        # log transforming Mas_Vnr_Area and saving it to the dataset
        housing['log_Mas_Vnr_Area'] = np.log(housing['Mas_Vnr_Area'] + 0.001)
        """)
    
    def log_transform_auto(self):
        print("""
        ############################## TREAT SKEWNESS ##################################
        # define continuous data
        continuous = [x1, x2, x3]

        # check skewness of continuous data before logarithmic transformation
        print("========== BEFORE LOG TRANSFORM ==========")
        print(data[continuous].skew())
        print("\n\n")

        # Log transformation all continuous data
        # treat any continuous values which is above 1 or under -1
        # also append the new log varialbes into continuous data list
        for item in data[continuous]:
            if data[continuous][item].skew() > 1 or data[continuous][item].skew() < -1:
                data[f'log_{item}'] = np.log(data[continuous][item])
                continuous.append(f'log_{item}')

        # check the skewness again to check if the skewness are improved
        print("========== AFTER LOG TRANSFORM ==========")
        print(data[continuous].skew())
        """)

    def subplots(self):
        print("""
        ########################
        # Visual EDA (Scatterplots)
        ########################
        # setting figure size
        fig, ax = plt.subplots(figsize = (10, 8))
        # developing a scatterplot
        plt.subplot(2, 2, 1)
        sns.scatterplot(x = housing['Lot_Area'],
                        y = housing['Sale_Price'],
                        color = 'g')

        # adding labels but not adding title
        plt.xlabel(xlabel = 'Lot Area')
        plt.ylabel(ylabel = 'Sale Price')
        ########################
        # developing a scatterplot
        plt.subplot(2, 2, 2)
        sns.scatterplot(x = housing['Total_Bsmt_SF'],
                        y = housing['Sale_Price'],
                        color = 'g')

        # adding labels but not adding title
        plt.xlabel(xlabel = 'Total Basement Square Footage')
        plt.ylabel(ylabel = 'Sale Price')
        ########################
        # developing a scatterplot
        plt.subplot(2, 2, 3)
        sns.scatterplot(x = housing['First_Flr_SF'],
                        y = housing['Sale_Price'],
                        color = 'orange')

        # adding labels but not adding title
        plt.xlabel(xlabel = 'First Floor Square Footage')
        plt.ylabel(ylabel = 'Sale Price')
        ########################
        # developing a scatterplot
        plt.subplot(2, 2, 4)
        sns.scatterplot(x = housing['Second_Flr_SF'],
                        y = housing['Sale_Price'],
                        color = 'r')

        # adding labels but not adding title
        plt.xlabel(xlabel = 'Second Floor Square Footage')
        plt.ylabel(ylabel = 'Sale Price')

        # cleaning up the layout, saving the figures, and displaying the results
        plt.tight_layout()
        plt.savefig('./__analysis_images/Housing Scatterplots 1 of 2.png')
        plt.show()
        """)

    def count_zeros(self):
        print("\n"
        "# counting the number of zeroes"
        "bsmt_zeroes   = len(housing['Total_Bsmt_SF'][housing['Total_Bsmt_SF'] == 0])\n"
        "sf_zeroes     = len(housing['Second_Flr_SF'][housing['Second_Flr_SF'] == 0])\n"
        "garage_zeroes = len(housing['Garage_Area'][housing['Garage_Area'] == 0])\n"
        "pool_zeroes   = len(housing['Pool_Area'][housing['Pool_Area'] == 0])\n"
        "mas_zeroes    = len(housing['Mas_Vnr_Area'][housing['Mas_Vnr_Area'] == 0])\n"
        "porch_zeroes  = len(housing['Porch_Area'][housing['Porch_Area'] == 0])\n\n"

        "# printing a table of the results\n"
        'print(f"                 No\t\tYes\n'
               "                 ---------------------\n"
               "Basement       | {bsmt_zeroes}\t\t{len(housing) - bsmt_zeroes}\n"
               "Second Floor   | {sf_zeroes}\t\t{len(housing) - sf_zeroes}\n"
               "Garage         | {garage_zeroes}\t\t{len(housing) - garage_zeroes}\n"
               "Pool           | {pool_zeroes}\t\t{len(housing) - pool_zeroes}\n"
               "Masonic Veneer | {mas_zeroes}\t\t{len(housing) - mas_zeroes}\n"
               "Porch          | {porch_zeroes}\t\t{len(housing) - porch_zeroes}\n")
        
    def conditional_iterrows(self):
        print("""
        # placeholder variables
        housing['has_Second_Flr'] = 0
        housing['has_Garage']     = 0
        housing['has_Mas_Vnr']    = 0
        housing['has_Porch']      = 0

        for index, value in housing.iterrows():

            # Second_Flr_SF
            if housing.loc[index, 'Second_Flr_SF'] > 0:
                housing.loc[index, 'has_Second_Flr'] = 1
                
            # Garage_Area
            if housing.loc[index, 'Garage_Area'] > 0:
                housing.loc[index, 'has_Garage'] = 1
                
            # Mas_Vnr_Area
            if housing.loc[index, 'Mas_Vnr_Area'] > 0:
                housing.loc[index, 'has_Mas_Vnr'] = 1
                
            # Porch_Area
            if housing.loc[index, 'Porch_Area'] > 0:
                housing.loc[index, 'has_Porch'] = 1
        """)

    #########################
    # mv_flagger
    #########################
    def mv_flagger(df):
        """
        Flags all columns that have missing values with 'm-COLUMN_NAME'.

        PARAMETERS
        ----------
        df : DataFrame to flag missing values

        RETURNS
        -------
        DataFrame with missing value flags."""

        for col in df:

            if df[col].isnull().astype(int).sum() > 0:
                df['m_'+col] = df[col].isnull().astype(int)
                
        return df
    
    #########################
    # text_split_feature
    #########################
    def text_split_feature(col, df, sep=' ', new_col_name='number_of_names'):
        """
        Splits values in a string Series (as part of a DataFrame) and sums the number
        of resulting items. Automatically appends summed column to original DataFrame.

        PARAMETERS
        ----------
        col          : column to split
        df           : DataFrame where column is located
        sep          : string sequence to split by, default ' '
        new_col_name : name of new column after summing split, default
                    'number_of_names'
        """
        
        df[new_col_name] = 0
        
        
        for index, val in df.iterrows():
            df.loc[index, new_col_name] = len(df.loc[index, col].split(sep = ' '))

    ########################################
    # visual_cm
    ########################################
    def visual_cm(true_y, pred_y, labels = None):
        """
        Creates a visualization of a confusion matrix.

        PARAMETERS
        ----------
        true_y : true values for the response variable
        pred_y : predicted values for the response variable
        labels : , default None
        """
        # visualizing the confusion matrix

        # setting labels
        lbls = labels

        # declaring a confusion matrix object
        cm = confusion_matrix(y_true = true_y,
                            y_pred = pred_y)

        # heatmap
        sns.heatmap(cm,
                    annot       = True,
                    xticklabels = lbls,
                    yticklabels = lbls,
                    cmap        = 'Blues',
                    fmt         = 'g')

        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.title('Confusion Matrix of the Classifier')
        plt.show()

    ########################################
    # plot_feature_importances
    ########################################
    def plot_feature_importances(model,x_train, train, export = False):
        """
        Plots the importance of features from a CART model.
        
        PARAMETERS
        ----------
        model  : CART model
        train  : explanatory variable training data
        export : whether or not to export as a .png image, default False
        """
        
        # declaring the number
        n_features = x_train.shape[1]
        
        # setting plot window
        fig, ax = plt.subplots(figsize=(12,9))
        
        plt.barh(range(n_features), model.feature_importances_, align='center')
        plt.yticks(np.arange(n_features), train.columns)
        plt.xlabel("Feature importance")
        plt.ylabel("Feature")
        
        if export == True:
            plt.savefig('Tree_Leaf_50_Feature_Importance.png')