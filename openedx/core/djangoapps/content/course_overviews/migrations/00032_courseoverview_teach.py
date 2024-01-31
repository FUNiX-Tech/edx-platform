

from django.conf import settings
from django.db import migrations, models



class Migration(migrations.Migration):

    dependencies = [

          ('course_overviews', '00031_courseoverview_about'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseOverviewAboutTeacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=255)),
                ('workplace', models.CharField(max_length=255)),
                ('img', models.ImageField(max_length=255)),
                ('sex' , models.CharField(max_length=50)),
                ('is_teacher_start' , models.BooleanField(default=False)),
                ('is_design'  , models.BooleanField(default=False)),
                ('is_expert' , models.BooleanField(default=False)),
                
            ],
        )
    ]








