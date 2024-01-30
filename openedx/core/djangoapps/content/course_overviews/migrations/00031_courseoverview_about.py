

from django.conf import settings
from django.db import migrations, models



class Migration(migrations.Migration):

    dependencies = [

          ('course_overviews', '0030_courseoverview_custom_lab'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseOverviewAbout',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=255)),
                ('overview', models.TextField(default='')),
                ('target' , models.TextField(default='')),
                ('participant', models.TextField(default='')),
                ('input_required', models.TextField(default='')),

            ],
        )
    ]








