from django.shortcuts import render, redirect, HttpResponse
from .models import Doc, Variety
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
import os
from os.path import exists
from .forms import SearchDoc, InserPdfDoc
import json

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.GET.get("folder"):
        pass
    context = {}
    context['form'] = InserPdfDoc()
    return render(request,'alihmedia_vital/index.html', context=context)

def sertifikat(request):
    pass

def bpkb_mobil_dan_motor(request):
    pass
def searchdoc(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.GET.get("folder"):
        query = request.GET.get("search")
        folder = request.GET.get("folder")
        d = Variety.objects.get(folder=folder)
        if query == None or query == '':
            docs = Doc.objects.filter(variety_id__exact=d.id)
        else:
            docs = Doc.objects.filter(Q(variety_id__exact=d.id) & (Q(name__icontains=query)  | Q(work_unit__icontains=query) | Q(period__exact=query ) | Q(save_location__icontains=query)))
        if not docs:
            messages.info(request, "Data tidak ditemukan")
        docdata = []
        for ke, doc in enumerate(docs):
            path = os.path.join(settings.PDF_LOCATION, __package__.split('.')[1], doc.variety.folder, str(doc.doc_number) + ".pdf")
            pdffound = False
            coverfilename = ""
            if exists(path):
                pdffound = True
                coverfilename = "{}_{}_{}_{}.png".format(__package__.split('.')[1], doc.variety.folder, doc.doc_number)

            docdata.append({
                "variety": doc.variety.name,
                "doc_number": doc.doc_number,
                "name": doc.name,
                "work_unit": doc.work_unit,
                "period": doc.period,
                "media": doc.media,
                "countstr": doc.countstr,
                "save_life": doc.save_life,
                "uuid_id": doc.uuid_id,
                "save_location": doc.save_location,
                "protect_method": doc.protect_method,
                "description": doc.description,
                "pdffound": pdffound,
                "coverfilepath": os.path.join(settings.COVER_URL, coverfilename),

            })
        # return HttpResponse(docdata) 
        context = {'data':docdata, 'form': SearchDoc(), 'folder':folder, 'query':query}
        return render(request,'alihmedia_vital/searchdoc.html', context=context)

    context = {}
    context['form'] = SearchDoc()
    return render(request,'alihmedia_vital/searchdoc.html', context=context)
