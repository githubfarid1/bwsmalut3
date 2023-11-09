from django.db import models
import uuid
from taggit.managers import TaggableManager
from django.core.validators import MinLengthValidator

class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    link = models.CharField(max_length=50, unique=True)
    folder = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Subfolder(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    # link = models.CharField(max_length=50, unique=True)
    year = models.CharField(max_length=4, validators=[MinLengthValidator(4)], default='2023')
    folder = models.CharField(max_length=50, unique=True)
    
    department = models.ForeignKey(
        Department,
        db_column='department_id',
        on_delete=models.CASCADE, 
        # related_name='pjpsa_departments',
        default=None
    )        


    def __str__(self) -> str:
        return self.name

class File(models.Model):
    id = models.AutoField(primary_key=True)
    uuid_id = models.UUIDField(default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=100)
    tags = TaggableManager(related_name="pjsa_taggit")
    description = models.TextField(null=True, blank=True)

    subfolder = models.ForeignKey(
        Subfolder,
        db_column='subfolder_id',
        on_delete=models.CASCADE, 
        # related_name='pjsa_files'
    )        
    def __str__(self):
        return self.filename