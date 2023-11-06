from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Department, Subfolder, File
import sys
from django.template.defaultfilters import slugify
from .forms import FileForm, DepartmentForm
from taggit.models import Tag
import os
from django.conf import settings
from os.path import exists
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from sanitize_filename import sanitize

def getmenu_year(department_id):
    years = Subfolder.objects.filter(department_id=department_id).order_by("year").values("year").distinct()
    return [x['year'] for x in years if x['year'] != '']

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
    
def department(request, slug):
    dep = Department.objects.get(slug=slug)
    context = {
        # 'data':subfolders,
        "menu": getmenu_year(dep.id),
        'depname':dep.name,
        'slug': slug,
    }
    return render(request=request, template_name='fm_pjpa/department.html', context=context)
    
def department_year(request, slug, year):
    dep = Department.objects.get(slug=slug)
    subfolders = dep.subfolder_set.filter(year=year)
    context = {
        'data':subfolders,
        "menu": getmenu_year(dep.id),
        'depname':dep.name,
        'slug': slug,
        'year': year,
    }
    return render(request=request, template_name='fm_pjpa/department_year.html', context=context)


def add_department(request):
    departments = Department.objects.all()
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            newdep = form.save(commit=False)
            newdep.folder = sanitize(newdep.shortname)
            newdep.slug = slugify(newdep.shortname)
            newdep.save()
            
    form = DepartmentForm()
    context = {
    'data':departments,
    # 'depname':subfolder.department.name,
    # 'subfoldername': subfolder.name,
    # 'year': subfolder.year,
    # 'common_tags':common_tags,
    'form':form,        
    }

    return render(request=request, template_name='fm_pjpa/add_department.html', context=context)
    
def subfolder(request, id):
    subfolder = Subfolder.objects.get(id=id)
    files = subfolder.file_set.all()
    common_tags = File.tags.most_common()[:10]
    if request.method == 'POST' and request.FILES['fileupload']:
        form = FileForm(request.POST)
        upload = request.FILES['fileupload']
        folder1 = os.path.join(settings.PDF_LOCATION, __package__.split('.')[1], subfolder.year)
        folder2 = os.path.join(folder1, str(subfolder.folder))
        if not exists(folder1):
            os.mkdir(folder1)
        if not exists(folder2):
            os.mkdir(folder2)
            
        filepath = os.path.join(folder2, str(upload))
        if exists(filepath):
            messages.info(request, "File Sudah ada")
            
        # print(form.errors)
        if form.is_valid():
            # breakpoint()
            newsubfolder = form.save(commit=False)
            newsubfolder.filename = upload
            newsubfolder.slug = slugify(newsubfolder.filename)
            newsubfolder.subfolder_id = id
            newsubfolder.save()
            # Without this next line the tags won't be saved.
            form.save_m2m()
            fss = FileSystemStorage()
            fss.save(filepath, upload)
    else:
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