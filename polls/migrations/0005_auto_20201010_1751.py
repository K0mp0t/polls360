# Generated by Django 3.1.2 on 2020-10-10 12:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0004_auto_20201007_1933'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'Question', 'verbose_name_plural': 'Questions'},
        ),
        migrations.AddField(
            model_name='poll',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='Polls', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pollresult',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='pollresult',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='PollsResults', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Questions', to='polls.poll'),
        ),
        migrations.AlterField(
            model_name='questionanswerpair',
            name='poll_result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='QuestionAnswerPairs', to='polls.pollresult'),
        ),
        migrations.AlterField(
            model_name='questionanswerpair',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.question'),
        ),
    ]
