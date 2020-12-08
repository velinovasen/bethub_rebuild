# Generated by Django 3.1.3 on 2020-12-08 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('home_team', models.CharField(max_length=40)),
                ('away_team', models.CharField(max_length=40)),
                ('home_prob', models.IntegerField()),
                ('draw_prob', models.IntegerField()),
                ('away_prob', models.IntegerField()),
                ('bet_sign', models.CharField(max_length=1)),
                ('score_predict', models.CharField(max_length=10)),
                ('avg_goals', models.FloatField()),
                ('odds_for_prediction', models.FloatField()),
                ('home_odd', models.FloatField()),
                ('draw_odd', models.FloatField()),
                ('away_odd', models.FloatField()),
                ('temp', models.CharField(max_length=5)),
            ],
        ),
    ]
