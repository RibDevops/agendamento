from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0002_conexaoagenda_ativo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WhatsAppEnvio',
        ),
        migrations.CreateModel(
            name='WhatsAppEnvio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash_evento', models.CharField(max_length=64)),
                ('enviado_em', models.DateTimeField(auto_now_add=True)),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agenda.turma')),
            ],
            options={
                'unique_together': {('turma', 'hash_evento')},
            },
        ),
    ]
