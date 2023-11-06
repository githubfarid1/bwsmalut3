from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.http import HttpResponse, Http404
from .models import Department, Subfolder, File
import sys
from django.template.defaultfilters import slugify
from .forms import FileForm, DepartmentForm, SubfolderForm
from taggit.models import Tag
import os
from django.conf import settings
from os.path import exists
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from sanitize_filename import sanitize
from django.contrib.auth.models import Group
from urllib.parse import unquote, urlparse
from django.contrib.auth.decorators import user_passes_test
import datetime

def check_permission(request, depslug):
    if request.user.is_superuser:
        return True
    if depslug == '':
        groupname = __package__.split('.')[1]
    else: 
        groupname = __package__.split('.')[1] + "_" + depslug
    
    test_group1 = Group.objects.get(name=__package__.split('.')[1])
    test_group2 = Group.objects.get(name=groupname)
    user_group = request.user.groups.all()
    status1 = test_group1 in user_group
    status2 = test_group2 in user_group
    if status1:
        return status1
    else:
        return status2

def getmenu_year(department_id):
    years = Subfolder.objects.filter(department_id=department_id).order_by("year").values("year").distinct()
    yearlist = [int(x['year']) for x in years if x['year'] != '']
    today = datetime.date.today()
    if not today.year in yearlist:
        yearlist.append(today.year)
    yearlist.append(today.year+1)
    return yearlist        


def department(request, slug):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if not check_permission(request, slug):
        return render(request=request, template_name='fm_pjpa/page_404.html', context={})
        
    dep = Department.objects.get(slug=slug)
    if not dep:
        return render(request=request, template_name='fm_pjpa/page_404.html', context={})
    
    context = {
        # 'data':subfolders,
        "menu": getmenu_year(dep.id),
        'depname':dep.name,
        'slug': slug,
    }
    return render(request=request, template_name='fm_pjpa/department.html', context=context)

def department_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not check_permission(request, ''):
        return render(request=request, template_name='fm_pjpa/page_404.html', context={})
    departments = Department.objects.all()
    context = {
        'data':departments,
    }

    return render(request=request, template_name='fm_pjpa/department_list.html', context=context)
        
    
def department_year(request, slug, year):
    if not request.user.is_authenticated:
        return redirect('login')
    if not check_permission(request, slug):
        return render(request=request, template_name='fm_pjpa/page_404.html', context={})
    dep = Department.objects.get(slug=slug)
    subfolders = dep.subfolder_set.filter(year=year)
    if request.method == 'POST':
        form = SubfolderForm(request.POST)
        if form.is_valid():
            newfloder = form.save(commit=False)
            newfloder.folder = sanitize(newfloder.name)
            newfloder.year = year
            newfloder.department_id = dep.id
            newfloder.save()
    
    form = SubfolderForm()
    context = {
        'data':subfolders,
        "menu": getmenu_year(dep.id),
        'depname':dep.name,
        'slug': slug,
        'year': year,
        'form': form,
    }
    return render(request=request, template_name='fm_pjpa/department_year.html', context=context)


def add_department(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not check_permission(request, ''):
        return render(request=request, template_name='fm_pjpa/page_404.html', context={})
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
    
def add_subfolder(request, depslug):
    pass

def subfolder(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    subfolder = Subfolder.objects.get(id=id)
    depslug = subfolder.department.slug
    if not check_permission(request, depslug):
        return render(request=request, template_name='fm_pjpa/page_404.html', context={})
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

def page_404(request):
    print('sss')
    return render(request, 'fm_pjpa/page_404.html', {})
