from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
import random
from web.models import Name
from rest_framework import viewsets
from rest_framework import permissions
from web.serializers import \
    NameSerializer, UserSerializer
from web.models import Name
from rest_framework import generics
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics 

def index(request):
    names_with_a = Name.objects.order_by('text')[:5]
    output = ', '.join([n.text for n in names_with_a])
    return HttpResponse("""
        Hello BRIDGERS! The names are: 
        <b> {0} </b>       
       """.format(output))

class NameList(generics.ListAPIView):
    serializer_class = NameSerializer
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        name = self.kwargs['name'].upper()
        queryset = Name.objects.filter(text = name)
        if not queryset:
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
            y_pred = clf.predict(X_test)

            def predict_name(name):
                cols = X.columns.to_list()
                lst = [0] * len(cols)
                #name = "MARIO ANTONIO JESUS"
                last = name[-1:]
                last_str = "L_" + last
                first = name[:1]
                first_str = "F_" + last    
                last_idx = cols.index(last_str)
                if last_idx >= 0:
                    lst[last_idx] = 1
                first_idx = cols.index(first_str)
                if first_idx >= 0:
                    lst[first_idx] = 1
                lword = is_vowel(last)
                fword = is_vowel(first)
                num_words = count_words(name)
                num_chars = count_chars(name)
                lst[0] = lword
                lst[1] = fword
                lst[2] = num_words
                lst[3] = num_chars           
                d = np.array(lst).reshape(1, -1)
            #    e = pd.DataFrame(data = d, columns = cols)
                p = clf.predict(d)
            #    p = clf.predict(e)
                print(p)
                if p[0] == 1:
                    return "FEMALE"
                else:
                    return "MALE"
            
            g = predict_name(name)
            print(g)
#        N = Name(
#            text,
#            prob_f,
#            prob_m,
#            gender,
#            pub_date = datetime.now())
#        N.save()
        #if username is not None:
        #    queryset = queryset.filter(purchaser__username=username)
        return queryset


#class NameViewSet(viewsets.ModelViewSet):
#    """
#    API endpoint that allows groups to be viewed or edited.
#    """
#    queryset = Name.objects.all()
#    serializer_class = NameSerializer
#    lookup_field = 'text'
#    permission_classes = [permissions.IsAuthenticated]  

#class UserViewSet(viewsets.ModelViewSet):
#    """
#    API endpoint that allows groups to be viewed or edited.
#    """
#    queryset = User.objects.all()
#    serializer_class = UserSerializer
#    permission_classes = [permissions.IsAuthenticated]  
