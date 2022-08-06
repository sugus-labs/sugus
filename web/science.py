from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics 
import joblib

def generate_model():
    # MAKE THE MODEL HERE
    name_basics_df = pd.read_csv(
        "/home/gustavo_martin/sugus/data/names_master.csv", sep = ",")
    name_basics_w_df = name_basics_df
    name_basics_w_df = name_basics_w_df.reset_index()
    name_basics_w_df["lword"] = name_basics_w_df["name"].str[-1:]
    name_basics_w_df["fword"] = name_basics_w_df["name"].str[:1]
    name_basics_w_df = name_basics_w_df[
        name_basics_w_df["lword"].notnull()
    ]
    name_basics_w_df = name_basics_w_df[
        name_basics_w_df["fword"].notnull()
    ]
    def is_vowel(word):
        if word.lower() in "aeiou":
            return 1
        return 0

    name_basics_w_df["lvowel"] = name_basics_w_df["lword"].apply(is_vowel)
    name_basics_w_df["fvowel"] = name_basics_w_df["fword"].apply(is_vowel)
    def count_words(name):
        l = len(name.split(" "))   
        return l

    name_basics_w_df["num_words"] = \
        name_basics_w_df["name"].apply(count_words)
    def count_chars(name):
        l = len(name)   
        return l

    name_basics_w_df["num_chars"] = \
        name_basics_w_df["name"].apply(count_chars)
    name_basics_w_df = name_basics_w_df.drop(
        columns = ["prob_f", "prob_m"], 
        axis = 1
    )
    enc = OneHotEncoder(
        categories = 'auto',  # Categories per feature
        drop = None, # Whether to drop one of the features
        sparse = True, # Will return sparse matrix if set True
        handle_unknown = 'error' # Whether to raise an error 
    )      
    lword_tr = enc.fit_transform(name_basics_w_df[['lword']])
    name_basics_w_df["L_" + enc.categories_[0]] = lword_tr.toarray()
    fword_tr = enc.fit_transform(name_basics_w_df[['fword']])
    name_basics_w_df["F_" + enc.categories_[0]] = fword_tr.toarray()
    name_basics_w_df["gender"] = np.where(
        name_basics_w_df["gender"] == 'F', 1, 0)
    name_basics_w_df = name_basics_w_df.drop(columns = \
        ["lword", "fword", "name"], axis = 1)
    X = name_basics_w_df.drop(columns = ["gender"])
    y = name_basics_w_df[["gender"]]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size = 0.2, random_state = 42)
    clf = DecisionTreeClassifier(random_state = 42)
    clf = clf.fit(X_train,y_train)

    filename = "decission_tree.sav"
    joblib.dump(clf, filename)
 