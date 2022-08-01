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

def index(request):
#    r = random.randint(0, 10)
    names_with_a = Name.objects.order_by('text')[:5]
    output = ', '.join([n.text for n in names_with_a])
    return HttpResponse("""
        Hello BRIDGERS! The names are: 
        <b> {0} </b>       
       """.format(output))

#def xxxx(request):
#    return HttpResponse("Bye BRIDGERS!")

class NameList(generics.ListAPIView):
#    queryset = Name.objects.all()
    serializer_class = NameSerializer
#    lookup_field = 'text'
#    permission_classes = [permissions.IsAuthenticated] 
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
#        name = self.request.query_params.get('name', False)
        name = self.kwargs['name']



#        print(name)
#        print(self.request.query_params)
        queryset = Name.objects.filter(text=name)
        if not queryset:
            # MAKE THE MODEL HERE
            pass
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
