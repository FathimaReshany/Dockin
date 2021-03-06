# Generated by Django 2.0.9 on 2021-10-25 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='block_request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'block_request',
            },
        ),
        migrations.CreateModel(
            name='chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat', models.CharField(max_length=500)),
                ('chat_date', models.CharField(max_length=50)),
                ('chat_type', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'chat',
            },
        ),
        migrations.CreateModel(
            name='company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=50)),
                ('year', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('pin', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('image', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'company',
            },
        ),
        migrations.CreateModel(
            name='complaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complaint', models.CharField(max_length=200)),
                ('complaint_date', models.CharField(max_length=50)),
                ('complaint_type', models.CharField(max_length=50)),
                ('reply', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'complaint',
            },
        ),
        migrations.CreateModel(
            name='feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback', models.CharField(max_length=100)),
                ('feedback_date', models.CharField(max_length=100)),
                ('feedback_type', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'feedback',
            },
        ),
        migrations.CreateModel(
            name='login',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('logintype', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'login',
            },
        ),
        migrations.CreateModel(
            name='payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.CharField(max_length=50)),
                ('payment_date', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'payment',
            },
        ),
        migrations.CreateModel(
            name='skills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'skills',
            },
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=50)),
                ('dob', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('house_name', models.CharField(max_length=50)),
                ('pin', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('image', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50)),
                ('LOGIN', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.login')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='vaccancy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('date', models.CharField(max_length=50)),
                ('COMPANY', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.company')),
            ],
            options={
                'db_table': 'vaccancy',
            },
        ),
        migrations.CreateModel(
            name='vaccancy_request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vaccancy_request_date', models.CharField(max_length=50)),
                ('status', models.CharField(default='1', max_length=50)),
                ('VACCANCY', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.vaccancy')),
            ],
            options={
                'db_table': 'vaccancy_request',
            },
        ),
        migrations.CreateModel(
            name='vaccancy_skills',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SKILLS', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.skills')),
                ('VACCANCY', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='newapp.vaccancy')),
            ],
            options={
                'db_table': 'vaccancy_skills',
            },
        ),
        migrations.CreateModel(
            name='work_request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_request_date', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=100)),
                ('USER', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.user')),
            ],
            options={
                'db_table': 'work_request',
            },
        ),
        migrations.CreateModel(
            name='worker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=50)),
                ('dob', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('house_name', models.CharField(max_length=50)),
                ('pin', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('image', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('LOGIN', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.login')),
            ],
            options={
                'db_table': 'worker',
            },
        ),
        migrations.CreateModel(
            name='worker_resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=50)),
                ('resume_path', models.CharField(max_length=100)),
                ('WORKER', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.worker')),
            ],
            options={
                'db_table': 'worker_resume',
            },
        ),
        migrations.CreateModel(
            name='worker_skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SKILL', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.skills')),
                ('WORKER', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.worker')),
            ],
            options={
                'db_table': 'worker_skill',
            },
        ),
        migrations.CreateModel(
            name='works',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('works_image', models.CharField(max_length=500)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('amount', models.CharField(max_length=50)),
                ('WORKER_SKILL', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='newapp.worker_skill')),
            ],
            options={
                'db_table': 'works',
            },
        ),
        migrations.AddField(
            model_name='work_request',
            name='WORKS',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.works'),
        ),
        migrations.AddField(
            model_name='vaccancy_request',
            name='WORKER',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.worker'),
        ),
        migrations.AddField(
            model_name='payment',
            name='USER',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.user'),
        ),
        migrations.AddField(
            model_name='payment',
            name='WORKER',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.worker'),
        ),
        migrations.AddField(
            model_name='payment',
            name='WORK_REQUEST',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.work_request'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='FROM_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loginA', to='newapp.login'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='TO_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loginB', to='newapp.login'),
        ),
        migrations.AddField(
            model_name='complaint',
            name='LOGIN',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.login'),
        ),
        migrations.AddField(
            model_name='company',
            name='LOGIN',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.login'),
        ),
        migrations.AddField(
            model_name='chat',
            name='USER',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.user'),
        ),
        migrations.AddField(
            model_name='chat',
            name='WORKER',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.worker'),
        ),
        migrations.AddField(
            model_name='block_request',
            name='USER',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='newapp.user'),
        ),
        migrations.AddField(
            model_name='block_request',
            name='WORKER',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newapp.worker'),
        ),
    ]
