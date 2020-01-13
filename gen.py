#!/usr/bin/env python

import json
import os

from django.template import Template, Context
from django.conf import settings
#settings.configure() # We have to do this to use django templates standalone - see
# http://stackoverflow.com/questions/98135/how-do-i-use-django-templates-without-the-rest-of-django

settings.configure(
    TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates'}],
)

script_dir = os.path.dirname(os.path.realpath(__file__))

# Cognitive capabilities
cogs_path = os.path.join(script_dir,'cogs.json')
with open(cogs_path) as cogs_file:
    cogs = json.load(cogs_file)

# Projects
projects_dir = os.path.join(script_dir,'projects')
projects = []
for root, dirs, files in os.walk(projects_dir):
    for filename in files:
        file_path = os.path.join(projects_dir,filename)
        with open(file_path) as proj_file:
            projects.append(json.load(proj_file, 'iso-8859-1'))

# cog_pubs
cog_map={}
for cog in cogs:
    cog_map[cog['id']]=cog
    cog['pubs']=[]
for proj in projects:
    for pub in proj['publications']:
        pub['project']=proj['id']
        for cog_id in pub['cogs']:
            cog_map[cog_id]['pubs'].append(pub)

with open('template.html', 'r') as in_file:
    t = Template(in_file.read())
    c = Context({'cogs': cogs,
                 'projects': projects})
    ##
    with open("index.html", "w") as text_file:
        text_file.write(t.render(c).encode('utf8'))

