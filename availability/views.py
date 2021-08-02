from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
import requests
import json
from datetime import datetime
# Create your views here.


# to register the new hospital data
class HospitalRegistration(View):

    def get(self, request):
        return render(request, "availability/hospitalRegistration.html")

    def post(self, request):
        try:
            hospital_name = request.POST.get('hospital_name')
            email = request.POST.get('email')
            state = request.POST.get('state')
            city = request.POST.get('city')
            area_code = request.POST.get('area_code')
            phone = request.POST.get('phone')
            password1 = request.POST.get('pwd1')
            password2 = request.POST.get('pwd2')
            # print(hospital_name, email, state, city,area_code, phone, password1, password2)
            post_data = {'hospital_name': hospital_name, 'email': email, 'state': state,
                         'city': city, 'area_code': area_code, 'contact': phone, 'password': password1, 'password2': password2}
            # call to validate the data
            validated_msg = self.validation(post_data)
            if validated_msg is True:
                # call to register hospital api request method
                del post_data['password2']
                # print(post_data)
                return_data = self.RequestToRegisterHospital(post_data)
                # print(return_data)
                # print(return_data.get('msg'))
                if return_data.get('msg') is True:
                    data = {
                        'msg': 'registered successfully'
                    }
                    return render(request, "availability/hospitalRegistration.html", data)
                else:
                    for msg in return_data.values():
                        msg = msg
                    data = {
                        'msg': msg[0]
                    }
                    return render(request, "availability/hospitalRegistration.html", data)
            else:
                # print(validated_msg)
                data = {
                    'msg': validated_msg
                }
                return render(request, "availability/hospitalRegistration.html", data)
        except Exception as e:
            print(e)

    # validation for post data
    def validation(self, post_data):
        try:
            msg = True
            if post_data.get('password') != post_data.get('password2'):
                msg = "password does not matched"
            elif post_data.get('password') is None or post_data.get('password2') is None:
                msg = "password should not empty"
            elif len(post_data.get('password')) < 8 or len(post_data.get('password2')) < 8:
                msg = "password length should not less than 8"
            elif post_data.get('hospital_name') is None:
                msg = "hsopital name should not empty"
            elif post_data.get('email') is None:
                msg = "email should not empty"
            elif post_data.get('email') is not None:
                if '@' not in (post_data.get('email')):
                    msg = "email should contain '@'"
            elif post_data.get('state') is None:
                msg = "state should not empty"
            elif post_data.get('city') is None:
                msg = "city should not empty"
            elif post_data.get('are_code') is None:
                msg = "area code should not empty"
            elif post_data.get('phone') is None:
                msg = "phone should not empty"
            elif len(post_data.get('phone')) > 10 or len(post_data.get('phone')) < 10:
                msg = "phone number length should be 10"
            return msg
        except Exception as e:
            print(e)

    # api requet to register new hospital
    def RequestToRegisterHospital(self, post_data):
        try:
            url = "http://127.0.0.1:8000/hospitalregistration"
            json_data = json.dumps(post_data)
            headers = {
                'content-type': 'application/json'
            }
            return_data = requests.post(
                url=url, data=json_data, headers=headers)
            # print(return_data.json())
            return return_data.json()
        except Exception as e:
            print(e)


# for hospital login
class HospitalLogin(View):

    def get(self, request):
        return render(request, "availability/hospitalLogin.html")

    def post(self, request):
        try:
            email = request.POST.get('email')
            pwd = request.POST.get('pwd')
            # print(email, pwd)
            post_data = {'email': email, 'password': pwd}
            # call to login hospital api request method
            return_data = self.RequestToLoginHospital(post_data)
            # print(return_data.get('msg'))
            if return_data.get('msg') is True:
                # call to get hospital data api request method
                return_hospital_data = self.RequestToGetHospitalData(email)
                # print(return_hospital_data)
                return render(request, "availability/hospitaldata.html", {'hospital_data': return_hospital_data})
            else:
                data = {
                    'msg': 'wrong credentials'
                }
                return render(request, "availability/hospitalLogin.html", data)
        except Exception as e:
            print(e)

    # api request to login hospital
    def RequestToLoginHospital(self, post_data):
        try:
            url = "http://127.0.0.1:8000/hospitallogin"
            json_data = json.dumps(post_data)
            headers = {
                'content-type': 'application/json'
            }
            return_data = requests.post(
                url=url, data=json_data, headers=headers)
            # print(return_data.json())
            return return_data.json()
        except Exception as e:
            print(e)

    # to get hospital data for hospital user after successful hospital login
    def RequestToGetHospitalData(self, email_id):
        try:
            url = f"http://127.0.0.1:8000/retrievehospital/{email_id}"
            """ data = {
                'email': email_id
            } """
            # json_data = json.dumps(data)
            headers = {
                'content-type': 'application/json'
            }
            return_hospital_data = requests.get(
                url=url, headers=headers)
            # print(return_hospital_data.json())
            return return_hospital_data.json()
        except Exception as e:
            print(e)


# for get/post hospital facility data
class HospitalFacility(View):

    def get(self, request):
        try:
            data = {
                'email_id': request.GET.get('email_id')
            }
            json_data = json.dumps(data)
            # print(json_data)
            headers = {
                'content-type': 'application/json'
            }
            url = "http://127.0.0.1:8000/hospitalfacility"
            return_hospital_facility = requests.get(
                url=url, data=json_data, headers=headers)
            # print(return_hospital_facility.json())
            # print(return_hospital_facility.json().get('data'))
            if return_hospital_facility.json().get('msg') is None:
                data = {
                    'facility': return_hospital_facility.json().get('data'),
                    'email_id': data.get('email_id'),
                    'hospital_name': request.GET.get('hospital'),
                }
                # print(data)
                return render(request, "availability/hospitalFacilityData.html", data)
            else:
                data = {
                    'msg': return_hospital_facility.json().get('msg'),
                    'email_id': data.get('email_id'),
                    'hospital_name': request.GET.get('hospital'),
                }
                return render(request, "availability/hospitalFacilityData.html", data)
        except Exception as e:
            print(e)

    def post(self, request):
        try:
            # instead of hospital-id we send email-id,then by email-id from hospital get hospital-id and save it in facility
            data = {
                'hospital': request.POST.get('email_id'),
                'total_oxygen_bed': request.POST.get('total_oxygen_beds'),
                'available_oxygen_bed': request.POST.get('available_oxygen_beds'),
                'total_general_bed': request.POST.get('total_general_beds'),
                'available_general_bed': request.POST.get('available_general_beds'),
                'updated_on': None,
            }
            # print(data)
            # print(request.POST.get('email_id'), request.POST.get('hospital'))
            json_data = json.dumps(data)
            headers = {
                'content-type': 'application/json'
            }
            url = "http://127.0.0.1:8000/hospitalfacility"
            return_data = requests.post(
                url=url, data=json_data, headers=headers)
            # print(return_data.json())
            if return_data.json().get('msg') is None:
                data = {
                    'facility': return_data.json().get('data'),
                    'email_id': request.POST.get('email_id'),
                    'hospital_name': request.POST.get('hospital'),
                }
                # print(data)
                return render(request, "availability/hospitalFacilityData.html", data)
            else:
                data = {
                    'msg': return_data.json().get('msg'),
                    'email_id': request.POST.get('email_id'),
                    'hospital_name': request.POST.get('hospital'),
                }
                return render(request, "availability/hospitalFacilityData.html", data)
            # return HttpResponse("ok")
        except Exception as e:
            print(e)


# to update hospital facility data
class UpdateFacility(View):
    def post(self, request):
        data = {
            'hospital': request.POST.get('email_id'),
            'total_oxygen_bed': request.POST.get('total_oxygen_beds'),
            'available_oxygen_bed': request.POST.get('available_oxygen_beds'),
            'total_general_bed': request.POST.get('total_general_beds'),
            'available_general_bed': request.POST.get('available_general_beds'),
            'updated_on': None,
        }

        json_data = json.dumps(data)

        url = "http://127.0.0.1:8000/hospitalfacility"

        headers = {
            'content-type': 'application/json'
        }
        return_data = requests.patch(url=url, data=json_data, headers=headers)
        # print(return_data.json())
        if return_data.json().get('msg') is None:
            data = {
                'facility': return_data.json().get('data'),
                'email_id': request.POST.get('email_id'),
                'hospital_name': request.POST.get('hospital'),
            }
            # print(data)
            return render(request, "availability/hospitalFacilityData.html", data)
        else:
            data = {
                'msg': return_data.json().get('msg'),
                'email_id': request.POST.get('email_id'),
                'hospital_name': request.POST.get('hospital'),
            }
            return render(request, "availability/hospitalFacilityData.html", data)
        # return HttpResponse("called update method")


# to delete hospital facility data
class DeleteFacility(View):
    def post(self, request):
        data = {
            'email_id': request.POST.get('email_id'),
        }
        json_data = json.dumps(data)
        url = "http://127.0.0.1:8000/hospitalfacility"
        headers = {
            'content-type': 'application/json'
        }
        return_data = requests.delete(url=url, data=json_data, headers=headers)
        # print(return_data.json())
        data = {
            'msg': return_data.json().get('msg'),
            'email_id': request.POST.get('email_id'),
            'hospital_name': request.POST.get('hospital'),
        }
        return render(request, "availability/hospitalFacilityData.html", data)
        # return HttpResponse("delete called")


""" # hospital user log out
def HospitalLogout(request):
    if request.method == "GET":
        return redirect("hospitallogin")
 """