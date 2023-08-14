from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Bundle, Doc, Department
from django.contrib import messages
import os
from django.db.models import Q
from os.path import exists
from django.conf import settings
import inspect
import sys
import time
from datetime import datetime, timedelta
import fitz
from django.contrib.auth.decorators import permission_required, user_passes_test
from django.http import JsonResponse
from .forms import UploadFileForm, DeletePdfFile, SearchQRCodeForm
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt

# from django_user_agents.utils import get_user_agent

def getmenu():
    return Department.objects.all()

def getdata(method, parquery):
    query = ""
    if method == "GET":
        query = parquery

    isfirst = True
    boxlist = []
    #get caller function name
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    link = "alihmedia_inactive_" + calframe[1][3]
    d = Department.objects.get(link=link)
    if query == None or query == '':
        docs = Doc.objects.filter(bundle__department_id__exact=d.id)
    else:
        docs = Doc.objects.filter(Q(bundle__department_id__exact=d.id) & (Q(description__icontains=query)  | Q(bundle__title__icontains=query) | Q(bundle__year__contains=query)))
    isfirst = True
    curbox_number = ""
    curbundle_number = ""
    # mlink = d.link.replace(__package__.split('.')[1] + "_", "")    
    for ke, doc in enumerate(docs):
        
        path = os.path.join(settings.PDF_LOCATION, __package__.split('.')[1], d.folder, str(doc.bundle.box_number), str(doc.doc_number) + ".pdf")
        pdffound = False
        filesize = 0
        pagecount = 0
        coverfilename = ""
        if exists(path):
            pdffound = True
            coverfilename = "{}_{}_{}_{}.png".format(__package__.split('.')[1], d.folder, doc.bundle.box_number, doc.doc_number)
        filetmppath = os.path.join(settings.MEDIA_ROOT, "tmpfiles", f"{__package__.split('.')[1]}-{doc.id}.pdf")
        pdftmpfound = False
        if exists(filetmppath):
            pdftmpfound = True

        if isfirst:
            isfirst = False

            curbox_number = doc.bundle.box_number
            boxlist.append({
                "box_number": doc.bundle.box_number,
                "bundle_number": doc.bundle.bundle_number,
                "doc_number": doc.doc_number,
                "bundle_code": doc.bundle.code,
                "bundle_title": doc.bundle.title,
                "bundle_year": doc.bundle.year,
                "doc_description": doc.description,
                "doc_count": doc.doc_count,
                "bundle_orinot": doc.bundle.orinot,
                "row_number": ke + 1,
                "pdffound": pdffound,
                "doc_id": doc.id,
                "coverfilepath": os.path.join(settings.COVER_URL, coverfilename),
                "filesize": doc.filesize,
                "pagecount": doc.page_count,
                "doc_uuid_id": doc.uuid_id,
                "pdftmpfound": pdftmpfound,
            })
            continue
        if curbox_number == doc.bundle.box_number:
            box_number = ""
        else:
            box_number = doc.bundle.box_number
            curbox_number = doc.bundle.box_number
        
        if curbundle_number == doc.bundle.bundle_number:
            bundle_number = ""
            bundle_code = ""
            bundle_title = ""
            bundle_year = ""
            bundle_orinot = ""
        else:
            bundle_number = doc.bundle.bundle_number
            curbundle_number = doc.bundle.bundle_number
            bundle_code = doc.bundle.code
            bundle_title = doc.bundle.title
            bundle_year = doc.bundle.year
            bundle_orinot = doc.bundle.orinot
        
        doc_number = doc.doc_number
        doc_description = doc.description
        doc_count = doc.doc_count
        boxlist.append({
            "box_number": box_number,
            "bundle_number": bundle_number,
            "doc_number": doc_number,
            "bundle_code": bundle_code,
            "bundle_title": bundle_title,
            "bundle_year": bundle_year,
            "doc_description": doc_description,
            "doc_count": doc_count,
            "bundle_orinot": bundle_orinot,
            "row_number": ke + 1,
            "pdffound": pdffound,
            "doc_id": doc.id,
            "coverfilepath": os.path.join(settings.COVER_URL, coverfilename),
            "filesize": doc.filesize,
            "pagecount": doc.page_count,
            "doc_uuid_id": doc.uuid_id,
            "pdftmpfound": pdftmpfound,
        })
        
    isfirst = True
    rowbox = 0
    rowbundle = 0
    boxspan = 1
    bundlespan = 1      
    for ke, box in enumerate(boxlist):
        if isfirst:
            isfirst = False
            rowbox = ke
            rowbundle = ke
            boxspan = 1
            bundlespan = 1      
            continue
        if box['box_number'] == "":
            boxspan += 1
        else:
            boxlist[rowbox]['boxspan'] = boxspan
            boxspan = 1
            rowbox = ke

        if box['bundle_number'] == "":
            bundlespan += 1
        else:
            boxlist[rowbundle]['bundlespan'] = bundlespan
            bundlespan = 1
            rowbundle = ke

    # for last record
    if docs.count() != 0:
        boxlist[rowbox]['boxspan'] = boxspan
        boxlist[rowbundle]['bundlespan'] = bundlespan

    return boxlist

def summarydata(data):
    sumscan = 0
    listyear = []
    for d in data:
        if d['bundle_year'] is not None and d['bundle_year'].strip() != '':
            listyear.append(d['bundle_year'])
        if d['pdffound'] == True:
            sumscan += 1
    unyears = list(set(listyear))
    # tes = unyears.sort()
    unyears.sort()
    unyearstr = ", ".join(unyears)
    sumnotscan = len(data) - sumscan
    try:
        percent = sumscan / len(data) * 100
    except:
        percent = 0

    return (len(data), sumscan, sumnotscan, percent, unyearstr )

# @permission_required('apps_alihmedia_inactive.irigasi')
def irigasi(request):
    # user_agent = get_user_agent(request)
    if not request.user.is_authenticated:
        return redirect('login')
    funcname = __package__.split('.')[1] + "_" + sys._getframe().f_code.co_name
    data = getdata(method=request.method, parquery=request.GET.get("search"))
    summary = summarydata(data)
    context = {
        "data": data,
        "link": funcname,
        "totscan": summary[1],
        "totnotscan": summary[2],
        "totdata": summary[0],
        "percent": f"{summary[3]:.3f}",
        "years": summary[4],
        "menu": getmenu(),
        "appname":__package__.split('.')[1],
    }
    return render(request=request, template_name='alihmedia_inactive/irigasi2.html', context=context)
    # if user_agent.is_mobile:
    #     return render(request=request, template_name='alihmedia_inactive/irigasi.html', context=context)
    # else:
    #     return render(request=request, template_name='alihmedia_inactive/irigasi.html', context=context)

def air_baku(request):
    if not request.user.is_authenticated:
        return redirect('login')
    funcname = __package__.split('.')[1] + "_" + sys._getframe().f_code.co_name
    data = getdata(method=request.method, parquery=request.GET.get("search"))
    summary = summarydata(data)
    context = {
        "data": data,
        "link": funcname,
        "totscan": summary[1],
        "totnotscan": summary[2],
        "totdata": summary[0],
        "percent": f"{summary[3]:.3f}",
        "years": summary[4],
        "menu": getmenu(),
        "appname":__package__.split('.')[1],
    }
    return render(request=request, template_name='alihmedia_inactive/irigasi2.html', context=context)

def sungai(request):
    if not request.user.is_authenticated:
        return redirect('login')
    funcname = __package__.split('.')[1] + "_" + sys._getframe().f_code.co_name
    data = getdata(method=request.method, parquery=request.GET.get("search"))
    summary = summarydata(data)
    context = {
        "data": data,
        "link": funcname,
        "totscan": summary[1],
        "totnotscan": summary[2],
        "totdata": summary[0],
        "percent": f"{summary[3]:.3f}",
        "years": summary[4],
        "menu": getmenu(),
        "appname":__package__.split('.')[1],
    }
    return render(request=request, template_name='alihmedia_inactive/irigasi2.html', context=context)

def pantai(request):
    if not request.user.is_authenticated:
        return redirect('login')

    funcname = __package__.split('.')[1] + "_" + sys._getframe().f_code.co_name
    data = getdata(method=request.method, parquery=request.GET.get("search"))
    summary = summarydata(data)
    context = {
        "data": data,
        "link": funcname,
        "totscan": summary[1],
        "totnotscan": summary[2],
        "totdata": summary[0],
        "percent": f"{summary[3]:.3f}",
        "years": summary[4],
        "menu": getmenu(),
        "appname":__package__.split('.')[1],
    }
    return render(request=request, template_name='alihmedia_inactive/irigasi2.html', context=context)

def keuangan(request):
    if not request.user.is_authenticated:
        return redirect('login')

    funcname = __package__.split('.')[1] + "_" + sys._getframe().f_code.co_name
    data = getdata(method=request.method, parquery=request.GET.get("search"))
    summary = summarydata(data)
    context = {
        "data": data,
        "link": funcname,
        "totscan": summary[1],
        "totnotscan": summary[2],
        "totdata": summary[0],
        "percent": f"{summary[3]:.3f}",
        "years": summary[4],
        "menu": getmenu(),
        "appname":__package__.split('.')[1],
    }
    return render(request=request, template_name='alihmedia_inactive/irigasi2.html', context=context)

def pdfdownload(request, uuid_id):
    if not request.user.is_authenticated:
        return redirect('login')

    doc = Doc.objects.get(uuid_id=uuid_id)
    folder = doc.bundle.department.folder
    box_number = doc.bundle.box_number
    doc_number = doc.doc_number
    # link = link.replace(__package__.split('.')[1] + "_", "")
    
    path = os.path.join(settings.PDF_LOCATION, __package__.split('.')[1], folder, str(box_number), str(doc_number) + ".pdf")
    if exists(path):
        filename = f"{__package__.split('.')[1]}_{folder}_{box_number}_{doc_number}.pdf"
        with open(path, 'rb') as pdf:
            response = HttpResponse(pdf.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline;filename={filename}'
            return response
    raise Http404

def statistics(request):
    if not request.user.is_authenticated:
        return redirect('login')

    deps = Department.objects.all()
    depnamelist = []
    depvaluelist = []
    colorlist = []
    foundall = 0
    notfoundall = 0
    for d in deps:
        folder = d.folder
        foundlist = [os.path.join(root, file) for root, dirs, files in os.walk(os.path.join(settings.PDF_LOCATION, __package__.split('.')[1], folder)) for file in files if file.endswith(".pdf")]
        found = len(foundlist)
        foundall += found
        docs = Doc.objects.filter(bundle__department_id__exact=d.id)
        notfound = len(docs) - found
        notfoundall += notfound
        depnamelist.append(" | ".join([d.name, "Sudah"]))
        depnamelist.append(" | ".join([d.name, "Belum"]))
        depvaluelist.append(found)
        depvaluelist.append(notfound)
        colorlist.append("rgba(112, 185, 239, 1)")
        colorlist.append("rgba(244, 204, 204, 1)")
        total = foundall + notfoundall
        procfound = foundall / total * 100
        procnotfound = notfoundall / total * 100
    
    fileinfolist = []
    allfilelist = [os.path.join(root, file) for root, dirs, files in os.walk(os.path.join(settings.PDF_LOCATION, __package__.split('.')[1])) for file in files if file.endswith(".pdf")]
    for filepath in allfilelist:
        # infotime = os.path.getmtime(filepath)
        infotime = os.stat(filepath).st_mtime
        infodate = datetime.fromtimestamp(infotime).strftime('%d-%m-%Y')
        mdict = {
            "file": filepath,
            "date": infodate,
            "pages": fitz.open(filepath).page_count
        }
        fileinfolist.append(mdict)

    num_of_dates = 30
    start = datetime.today()
    date_list = [start.date() - timedelta(days=x) for x in range(num_of_dates)]
    date_list.sort()
    docscan = []
    doccolor = []
    docdate = []
    # print(date_list)
    for d in date_list:
        pages = 0
        for fl in fileinfolist:
            if fl['date'] == d.strftime('%d-%m-%Y'):
                pages += fl['pages']
        docdate.append(d.strftime('%d-%m-%Y'))
        docscan.append(pages)
        doccolor.append("rgba(112, 185, 239, 1)")
    context = {
        "menu": getmenu(),
        "depnamelist": depnamelist,
        "depvaluelist": depvaluelist,
        "colorlist": colorlist,
        "foundall": str(foundall),
        "notfoundall": str(notfoundall),
        "procfound":f"{procfound:.3f}",
        "procnotfound":f"{procnotfound:.3f}",
        "docdate": docdate,
        "docscan": docscan,
        "doccolor": doccolor,
    }
    return render(request=request, template_name='alihmedia_inactive/statistics.html', context=context)
@csrf_exempt
# def boxsearch(request, link, box_number):
def boxsearch(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        qrcode = request.POST.get("qrcode")
        strlist = qrcode.strip().split('/')
        try:
            folder = strlist[3]
            box_number = strlist[4]
        except:
            return HttpResponse("QRcode Error")
        # return HttpResponse(folder + box)
        d = Department.objects.get(folder=folder)
        depname = d.name
        docs = Doc.objects.filter(bundle__department_id__exact=d.id, bundle__box_number__exact=box_number)
        boxdata = []
        for ke, doc in enumerate(docs):
            path = os.path.join(settings.PDF_LOCATION, __package__.split('.')[1], folder, str(doc.bundle.box_number), str(doc.doc_number) + ".pdf")
            pdffound = False
            coverfilename = ""
            if exists(path):
                pdffound = True
                coverfilename = "{}_{}_{}_{}.png".format(__package__.split('.')[1], folder, doc.bundle.box_number, doc.doc_number)
            boxdata.append({
                "box_number": doc.bundle.box_number,
                "bundle_number": doc.bundle.bundle_number,
                "doc_number": doc.doc_number,
                "bundle_code": doc.bundle.code,
                "bundle_title": doc.bundle.title,
                "bundle_year": doc.bundle.year,
                "doc_description": doc.description,
                "doc_count": doc.doc_count,
                "bundle_orinot": doc.bundle.orinot,
                "row_number": ke + 1,
                "pdffound": pdffound,
                "doc_id": doc.id,
                "coverfilepath": os.path.join(settings.COVER_URL, coverfilename),
                "filesize": doc.filesize,
                "pagecount": doc.page_count,
                "doc_uuid_id": doc.uuid_id,
            })

        # return HttpResponse(docs[2].bundle.title)
        # context['form'] = SearchQRCodeForm()
        context = {'data':boxdata, 'depname':depname, 'box_number': box_number, "folder": folder, 'form': SearchQRCodeForm()}
        return render(request=request, template_name='alihmedia_inactive/boxsearch2.html', context=context)
        # pass
    context = {}
    context['form'] = SearchQRCodeForm()
    # context['url'] = url
    return render(request, 'alihmedia_inactive/boxsearch2.html', context=context)

def pdfupload(request, uuid_id):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST' and request.FILES['filepath']:
        upload = request.FILES['filepath']
        fss = FileSystemStorage()
        doc = Doc.objects.get(uuid_id=uuid_id)
        folder = doc.bundle.department.folder
        doc_id = doc.id
        box_number = doc.bundle.box_number
        # doc_number = doc.doc_number
        
        filepath = os.path.join(settings.MEDIA_ROOT, "tmpfiles", f"{__package__.split('.')[1]}-{doc_id}.pdf")
        if exists(filepath):
            os.remove(filepath)
        fss.save(filepath, upload)
        return redirect(f"/{__package__.split('.')[1]}/{folder}#{box_number}")

    context = {}
    context['form'] = UploadFileForm(initial={'uuid_id': uuid_id})
    # context['url'] = url
    return render(request,'alihmedia_inactive/pdfupload.html', context=context)

def deletePdfFile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = DeletePdfFile(request.POST or None)
        if form.is_valid():
            depname = form.cleaned_data['listdepartment']
            box_number = form.cleaned_data['box_number']
            doc_number = form.cleaned_data['doc_number']
            doc = Doc.objects.filter(bundle__box_number__exact=box_number, doc_number__exact=doc_number, bundle__department__name__exact=depname).first()
            if doc is not None:
                folder = doc.bundle.department.folder
                path = os.path.join(settings.PDF_LOCATION, __package__.split('.')[1], folder, str(box_number), str(doc_number) + ".pdf")
                if exists(path):
                    coverfilename = "{}_{}_{}_{}.png".format(__package__.split('.')[1], folder, box_number, doc_number)
                    os.remove(path)
                    if exists(os.path.join(settings.COVER_URL, coverfilename)):
                        os.remove(os.path.join(settings.COVER_URL, coverfilename))
                    return redirect(f"/{__package__.split('.')[1]}/{folder}")
                
            return HttpResponse("File not found")
                    

    context = {}
    context['form'] = DeletePdfFile()
    return render(request,'alihmedia_inactive/delete_pdf.html', context=context)    
