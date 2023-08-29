from django.shortcuts import render, redirect, HttpResponse
from .models import Doc, Variety
from django.contrib import messages
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from os.path import exists
from .forms import SearchDoc, InserPdfDoc, UploadFileForm
import sys

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.GET.get("folder"):
        folder = request.GET.get("folder")
        return redirect(f"/{__package__.split('.')[1]}/{folder}")
    context = {}
    context['form'] = InserPdfDoc()
    return render(request,'alihmedia_vital/index.html', context=context)

def getdata(folder):
    d = Variety.objects.get(folder=folder)
    docs = Doc.objects.filter(variety_id__exact=d.id)
    docdata = []
    for ke, doc in enumerate(docs):
        path = os.path.join(settings.PDF_LOCATION, __package__.split('.')[1], doc.variety.folder, str(doc.doc_number) + ".pdf")
        pdffound = False
        coverfilename = ""
        if exists(path):
            pdffound = True
            coverfilename = "{}_{}_{}_{}.png".format(__package__.split('.')[1], doc.variety.folder, doc.doc_number)
        filetmppath = os.path.join(settings.MEDIA_ROOT, "tmpfiles", f"{__package__.split('.')[1]}-{doc.id}.pdf")
        pdftmpfound = False
        if exists(filetmppath):
            pdftmpfound = True

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
            "filesize": doc.filesize,
            "pagecount": doc.page_count,
            "pdftmpfound": pdftmpfound,


        })
    return docdata
def sertifikat(request):
    if not request.user.is_authenticated:
        return redirect('login')
    folder = sys._getframe().f_code.co_name
    d = Variety.objects.get(folder=folder)
    docdata = getdata(folder)
    context = {'data':docdata, "title": d.name}
    return render(request,'alihmedia_vital/datalist.html', context=context)

def bpkb_mobil_dan_motor(request):
    if not request.user.is_authenticated:
        return redirect('login')
    folder = sys._getframe().f_code.co_name
    d = Variety.objects.get(folder=folder)
    docdata = getdata(folder)
    context = {'data':docdata, "title": d.name}
    return render(request,'alihmedia_vital/datalist.html', context=context)

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

def pdfupload(request, uuid_id):
    if not request.user.is_authenticated:
        return redirect('login')
    doc = Doc.objects.get(uuid_id=uuid_id)
    folder = doc.variety.folder
    doc_id = doc.id
    pdfpath = os.path.join(settings.PDF_LOCATION, __package__.split('.')[1], str(doc.doc_number) + ".pdf")
    tmppath = os.path.join(settings.MEDIA_ROOT, "tmpfiles", f"{__package__.split('.')[1]}-{doc_id}.pdf")
    if exists(pdfpath):
        messages.info(request, "File sudah ada")
        return redirect(f"/{__package__.split('.')[1]}/{folder}")


    if request.method == 'POST' and request.FILES['filepath'] and not exists(pdfpath):
        upload = request.FILES['filepath']
        fss = FileSystemStorage()
        if exists(tmppath):
            os.remove(tmppath)
        fss.save(tmppath, upload)
        messages.info(request, "File berhasil diupload, akan segera diproses")
        # time.sleep(2)
        return redirect(f"/{__package__.split('.')[1]}/{folder}")

    context = {}
    context['form'] = UploadFileForm(initial={'uuid_id': uuid_id})
    context['isexist'] = exists(tmppath)
    context['data'] = doc

    # context['url'] = url
    return render(request,'alihmedia_vital/pdfupload.html', context=context)
