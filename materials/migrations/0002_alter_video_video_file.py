from django.db import migrations, models
import materials.models


class Migration(migrations.Migration):
    dependencies = [("materials", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="video_file",
            field=models.FileField(blank=True, upload_to=materials.models.safe_upload_path, validators=[materials.models.validate_video_upload]),
        ),
    ]
