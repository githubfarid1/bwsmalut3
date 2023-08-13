from django.shortcuts import render, redirect
from .forms import SearchQRCodeForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage


@csrf_exempt
def qrcodesearch(request):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        url = request.POST['qrcode']
        # url = '/alihmedia_inactive/boxsearch/irigasi/2'
        return redirect(url)
    context = {}
    context['form'] = SearchQRCodeForm()
    # context['url'] = url
    return render(request,'utility/qrcodesearch.html', context=context)
def upload(request):
    if request.method == 'POST' and request.FILES['upload']:
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save("tess.pdf", upload)
        file_url = fss.url(file)
        return render(request, 'utility/upload.html', {'file_url': file_url})
    return render(request, 'utility/upload.html')