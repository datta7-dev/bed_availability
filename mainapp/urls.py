from django.urls import path
from mainapp import views
urlpatterns = [
    path("", views.Index.as_view(), name="home"),
    path("gethospital", views.HospitalData.as_view(), name="gethospital"),
    path("hospitalfacilitydata", views.HospitalFacility.as_view(), name="hospital"),
    path("hospitalregistration",
         views.HospitalRegistration.as_view(), name="hospitalregistration"),
    path("hospitallogin",
         views.HospitalLogin.as_view(), name="hospitallogin"),
    path("retrievehospital/<email>",
         views.RetrieveHospitalData.as_view(), name="retrievehospital"),
    path("hospitalfacility",
         views.HospitalFacility.as_view(), name="hospitalfacility"),
]
