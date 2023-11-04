from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Department, Subfolder, File
import sys
from django.template.defaultfilters import slugify
from .forms import FileForm
from taggit.models import Tag

def atab(request, year):
    link = __package__.split('.')[1] + "_" + sys._getframe().f_code.co_name
    print(link)
    dep = Department.objects.filter(link=link).first()
    subfolders = dep.subfolder_set.filter(year=year)
    context = {
        'data':subfolders,
        'depname':dep.name,
    }
    return render(request=request, template_name='fm_pjpa/subdepartment.html', context=context)

def irwa_1(request, year):
    link = __package__.split('.')[1] + "_" + sys._getframe().f_code.co_name
    dep = Department.objects.filter(link=link).first()
    # dep = Department.objects.first()
    subfolders = dep.subfolder_set.filter(year=year)

    context = {
        'data':subfolders,
        'depname':dep.name,
    }
    return render(request=request, template_name='fm_pjpa/subdepartment.html', context=context)
    

def subfolder(request, id):
    subfolder = Subfolder.objects.get(id=id)
    files = subfolder.file_set.all()
    common_tags = File.tags.most_common()[:10]
    if request.method == 'POST' and request.FILES['filename']:
        form = FileForm(request.POST)
        upload = request.FILES['filename']
        print(upload)
        if form.is_valid():
            # breakpoint()
            newsubfolder = form.save(commit=False)
            newsubfolder.slug = slugify(newsubfolder.filename)
            newsubfolder.subfolder_id = id
            newsubfolder.save()
            # Without this next line the tags won't be saved.
            form.save_m2m()
    form = FileForm()
    context = {
    'data':files,
    'depname':subfolder.department.name,
    'subfoldername': subfolder.name,
    'year': subfolder.year,
    'common_tags':common_tags,
    'form':form,        
    }

    return render(request=request, template_name='fm_pjpa/subfolder.html', context=context)


def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name  
    files = File.objects.filter(tags=tag)
    context = {
        'tag':tag,
        'data':files,
    }
    return render(request, 'fm_pjpa/subfolder.html', context)