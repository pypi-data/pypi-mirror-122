from django.shortcuts import render
from django.shortcuts import  HttpResponse
from .models import Pickle
from .forms import Deploy_form
import pickle
from joblib import load
from sklearn.preprocessing import StandardScaler,LabelEncoder
# Create your views here.
def home(request):
    if request.method=="POST":
        filled_form=form=Deploy_form(request.POST)
        if filled_form.is_valid():
            #retrive data  from the form
            rooms=filled_form.cleaned_data["rooms"]
            house_type = filled_form.cleaned_data["House_Type"]
            no_of_bedrooms = filled_form.cleaned_data["number_of_bedrooms"]
            bathrooms = filled_form.cleaned_data["bathrooms"]
            no_of_car_spots = filled_form.cleaned_data["number_of_car_spots"]
            landsize = filled_form.cleaned_data["landsize"]
            building_area = filled_form.cleaned_data["building_area"]

            all_data=Pickle.objects.all()[0].pickle_file.name
            file = open(all_data,"rb")
            test = pickle.load(file)
            h_types={"h":0,"u":1,'t':2}
            scaler=StandardScaler()
            price="The Price of the House is {}".format(
                "%.2f"%test.predict([[rooms,h_types[house_type],no_of_bedrooms,bathrooms,no_of_car_spots,landsize,building_area]])
                )
            form=Deploy_form()
            return render(request,"Deployment/home.html",{"cost":price,"pre_form":form})
            # return render(request, "Deployment/home.html", {"pre_form": form})

    form=Deploy_form()
    return  render(request,'Deployment/home.html',{"pre_form":form})

