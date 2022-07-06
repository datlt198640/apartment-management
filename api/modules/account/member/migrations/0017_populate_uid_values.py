from django.db import migrations
import uuid

def gen_uid(apps, schema_editor):
    MyModel = apps.get_model('member', 'Member')
    for row in MyModel.objects.all():
        row.uid = uuid.uuid4()
        row.save(update_fields=['uid'])

class Migration(migrations.Migration):

    dependencies = [
        ('member', '0016_member_uid'),
    ]

    operations = [
        # omit reverse_code=... if you don't want the migration to be reversible.
        migrations.RunPython(gen_uid, reverse_code=migrations.RunPython.noop),
    ]