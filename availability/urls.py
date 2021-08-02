from django.contrib import admin
from django.urls import path, include
from availability import views

urlpatterns = [
    path('', views.HospitalLogin.as_view(), name="hospitalhome"),
    path('hospitalregistration', views.HospitalRegistration.as_view(),
         name="hospitalregistration"),
    path("hospitallogin", views.HospitalLogin.as_view(), name="hospitallogin"),
    path("gethospitalfacility", views.HospitalFacility.as_view(),
         name="hospitalfacility"),
    path("addhospitalfacility", views.HospitalFacility.as_view(),
         name="addhospitalfacility"),
    path("updatefacility", views.UpdateFacility.as_view(),
         name="updatefacility"),
    path("deletefacility", views.DeleteFacility.as_view(),
         name="deletefacility"),
    # path("logout", views.HospitalLogout,name="logout"),
]
