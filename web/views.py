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
import numpy as np
import joblib

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

            filename = "decission_tree.sav"
            clf = joblib.load(filename)

            def is_vowel(word):
                if word.lower() in "aeiou":
                    return 1
                return 0

            def count_words(name):
                l = len(name.split(" "))   
                return l

            def count_chars(name):
                l = len(name)   
                return l

            def predict_name(name):
                cols = clf.feature_names_in_.tolist()
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
                p = clf.predict(d)
                if p[0] == 1:
                    return "FEMALE", 1, 0
                else:
                    return "MALE", 0, 1
            
            gender, prob_f, prob_m = predict_name(name)
            N = Name(
                text = name,
                prob_f = prob_f,
                prob_m = prob_m,
                gender = gender,
                pub_date = datetime.now())
            N.save()
            queryset = Name.objects.filter(text = name)
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
