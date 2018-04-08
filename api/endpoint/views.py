from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pymongo


client = pymongo.MongoClient()
db = client['hack']
collection = db.data




# Create your views here.


@csrf_exempt
def teste(request):

    if request.method == 'POST':
        aux = json.loads(request.body.decode('utf-8'))

        post_id = collection.insert_one(aux)

        return HttpResponse(status=200)

    else:
        return HttpResponse(status=410)
