#!/usr/bin/env python

import json
import os

from django.template import Template, Context
from django.conf import settings
settings.configure() # We have to do this to use django templates standalone - see
# http://stackoverflow.com/questions/98135/how-do-i-use-django-templates-without-the-rest-of-django

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
            projects.append(json.load(proj_file))


with open('template.html', 'r') as in_file:
    t = Template(in_file.read())
    c = Context({'cogs': cogs,
                 'projects': projects})
    ##
    with open("index.html", "w") as text_file:
        text_file.write(t.render(c))

