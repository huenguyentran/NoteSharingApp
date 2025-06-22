import django.db.models.deletion
import uuid
from django.db import migrations, models

def generate_tokens(apps, schema_editor):
    Note = apps.get_model('notes', 'Note')
    for note in Note.objects.all():
        note.share_token = uuid.uuid4()
        note.save()

class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0004_comment_parentcomment_alter_comment_note'),
    ]

    operations = [
        # 1. Thêm field tạm thời, không unique, cho phép null
        migrations.AddField(
            model_name='note',
            name='share_token',
            field=models.UUIDField(null=True, editable=False),
        ),
        # 2. Gán dữ liệu unique bằng tay
        migrations.RunPython(generate_tokens),
        # 3. Đổi lại field thành unique, không null
        migrations.AlterField(
            model_name='note',
            name='share_token',
            field=models.UUIDField(unique=True, null=False, editable=False),
        ),
        # Các field khác
        migrations.AddField(
            model_name='note',
            name='is_shared_via_link',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='note',
            name='link_permission',
            field=models.CharField(
                choices=[('view', 'View'), ('edit', 'Edit')],
                default='view',
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name='noteshare',
            name='note',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='shares',
                to='notes.note',
            ),
        ),
    ]
