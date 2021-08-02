from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from mainapp.models import Facility, Hospitaldata
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from mainapp.serializers import facilitySerializer, hospitalSerializer
from rest_framework.generics import RetrieveAPIView, ListAPIView
from datetime import datetime
# Create your views here.


class Index(View):
    def get(self, request):
        data = {
            'facilities': Facility.objects.all(),
        }
        return render(request, "mainapp/index.html", data)


# to get hospital data to end user
class HospitalData(View):
    def get(self, request):
        hospital_id = request.GET.get('hospital')
        hospital = Hospitaldata.objects.get(hospital_id=hospital_id)
        data = {
            'hospital_data': hospital,
        }
        return render(request, "mainapp/hospital.html", data)


# api to register new hospital
class HospitalRegistration(APIView):

    def post(self, request):
        try:
            python_data = request.data
            # print(python_data)
            serializer_result = hospitalSerializer(data=python_data)
            # print(serializer_result)
            if serializer_result.is_valid():
                # print(serializer_result.data)
                serializer_result.save()
                response_data = {
                    'msg': True
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                # print(serializer_result.errors)
                return Response(serializer_result.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)


# api to login hospital
class HospitalLogin(APIView):

    def post(self, request):
        try:
            python_data = request.data
            # print(python_data)
            email = python_data.get('email')
            password = python_data.get('password')
            # print(email, password)
            if Hospitaldata.objects.filter(email=email, password=password).exists():
                return Response({'msg': True})
            else:
                return Response({'msg': False})
        except Exception as e:
            print(e)


# api to give hospital data to hospital user after hospital login
class RetrieveHospitalData(RetrieveAPIView):
    queryset = Hospitaldata.objects.all()
    serializer_class = hospitalSerializer
    lookup_field = 'email'


# get hospital facility data api for hospital user
class HospitalFacility(APIView):

    # to get hospital facility data
    def get(self, request):
        try:
            # print(request.data)
            if Hospitaldata.objects.filter(email=request.data.get('email_id')).exists():
                hospital = Hospitaldata.objects.get(
                    email=request.data.get('email_id'))
                # print(hospital.hospital_id)
                # print(Facility.objects.filter(
                # hospital=hospital.hospital_id))
                if Facility.objects.filter(hospital=hospital.hospital_id).exists():
                    facility_obj = Facility.objects.get(
                        hospital=hospital.hospital_id)
                    # print(facility_obj)
                    serialized_hospital_facility = facilitySerializer(
                        facility_obj)
                    # print(datetime.date(facility_obj.updated_on))
                    return Response({'data': serialized_hospital_facility.data}, status=status.HTTP_200_OK)
                else:
                    return Response({'msg': 'hospital facility data not available'})
            else:
                # print(request.data)
                return Response({'msg': 'data not found'})
        except Exception as e:
            print(e)

    # to insert hospital facility data
    def post(self, request):
        try:
            request_data = request.data
            # print(type(request_data))
            # get email from hospital and then get hospital id from hospital data and put it into the hospital key
            hospital = Hospitaldata.objects.get(
                email=request_data.get('hospital'))
            if Facility.objects.filter(hospital=hospital.hospital_id).exists():
                return_facility = self.getfacility(request, hospital)
                # print(return_facility)
                if return_facility is not False:
                    return Response({'data': return_facility}, status=status.HTTP_200_OK)
                else:
                    return Response({'msg': 'hospital facility data not available'})
            else:
                request_data['hospital'] = hospital.hospital_id
                timestamp = datetime.now()
                request_data['updated_on'] = timestamp
                # print(type(request_data))
                serializer_result = facilitySerializer(data=request_data)
                if serializer_result.is_valid():
                    serializer_result.save()
                    return_facility = self.getfacility(request, hospital)
                    if return_facility is not False:
                        return Response({'data': return_facility}, status=status.HTTP_200_OK)
                    else:
                        return Response({'msg': 'hospital facility data not available'})
                    # return Response({'msg': 'data submitted successfully'})
                else:
                    # print(serializer_result.errors)
                    return Response({'msg': 'failed to submit data'})

        except Exception as e:
            print(e)

    # to get facility data after post request, and return it to above post function
    def getfacility(self, request, hospital):
        if Facility.objects.filter(hospital=hospital.hospital_id).exists():
            facility_obj = Facility.objects.get(hospital=hospital.hospital_id)
            # print(facility_obj)
            serialized_hospital_facility = facilitySerializer(facility_obj)
            return serialized_hospital_facility.data
        else:
            return False

    # to update hospital facility data
    def patch(self, request):
        # get email from hospital and then get hospital id from hospital data and put it into the hospital key
        # print(request.data)
        hospital = Hospitaldata.objects.get(
            email=request.data.get('hospital'))
        request.data['hospital'] = hospital.hospital_id
        timestamp = datetime.now()
        request.data['updated_on'] = timestamp
        # print(request.data)
        facility_obj = Facility.objects.get(hospital=hospital.hospital_id)
        serializer_result = facilitySerializer(
            facility_obj, data=request.data, partial=True)
        if serializer_result.is_valid():
            serializer_result.save()
            return_facility = self.getfacility(request, hospital)
            if return_facility is not False:
                return Response({'data': return_facility}, status=status.HTTP_200_OK)
            else:
                return Response({'msg': 'hospital facility data not available'})
            # return Response({'msg': 'data submitted successfully'})
        else:
            # print(serializer_result.errors)
            return Response({'msg': 'failed to update data'})

    # to delete hospital facility data
    def delete(self, request):
        if Hospitaldata.objects.filter(email=request.data.get('email_id')).exists():
            hospital = Hospitaldata.objects.get(
                email=request.data.get('email_id'))
            if Facility.objects.filter(hospital=hospital.hospital_id).exists():
                facility_obj = Facility.objects.get(
                    hospital=hospital.hospital_id)
                facility_obj.delete()
                return Response({'msg': 'data deleted successfully'})
            else:
                return Response({'msg': 'facility data not found'})
        else:
            return Response({'msg': 'facility data not found'})
