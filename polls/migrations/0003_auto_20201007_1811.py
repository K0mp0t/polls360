# Generated by Django 3.1.2 on 2020-10-07 13:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0002_auto_20201007_1643'),
    ]

    operations = [
        migrations.CreateModel(
            name='PollResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionAnswerPair',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=255)),
                ('poll_result', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='polls.pollresult')),
            ],
        ),
        migrations.DeleteModel(
            name='ListField',
        ),
        migrations.RemoveField(
            model_name='question',
            name='question_id',
        ),
        migrations.AddField(
            model_name='poll',
            name='name',
            field=models.CharField(default='default_poll_name', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='poll',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='polls.poll'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionanswerpair',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='polls.question'),
        ),
    ]
