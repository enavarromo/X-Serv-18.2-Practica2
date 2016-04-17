#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script de comprobación de entrega de ejercicio

Para ejecutarlo, desde la shell:
 $ python check.py login_github

"""

import os
import random
import sys

ejercicio = 'X-Serv-15.8-CmsUsersPut'

student_projname = 'myproject'
student_appname = 'cms_users_put'

student_files = [
    'manage.py',
    'db.sqlite3',
    student_projname + '/__init__.py',
    student_projname + '/settings.py',
    student_projname + '/urls.py',
    student_projname + '/wsgi.py',
    student_appname + '/__init__.py',
    student_appname + '/admin.py',
    student_appname + '/models.py',
    student_appname + '/tests.py',
    student_appname + '/views.py',
    student_appname + '/migrations/__init__.py'
    ]

repo_files = [
    'README.md',
    '.gitignore',
    'LICENSE'
    ]

files = student_files + repo_files

if len(sys.argv) != 2:
    print
    sys.exit("Usage: $ python check.py login_github")

repo_git = "http://github.com/" + sys.argv[1] + "/" + ejercicio


aleatorio = str(int(random.random() * 1000000))

error = 0

print
print "Clonando el repositorio " + repo_git + "\n"
os.system('git clone ' + repo_git + ' /tmp/' + aleatorio + ' > /dev/null 2>&1')

github_files = []

for root, dirs, files in os.walk('/tmp/' + aleatorio):
    for name in files:
        filename = os.path.join(root, name).replace('/tmp/' + aleatorio + '/', '')
        if filename in student_files or filename in repo_files:
            github_files.append(filename)

if len(github_files) != len(student_files) + len(repo_files):
    error = 1
    print "Error: número de ficheros en el repositorio incorrecto"

    for filename in student_files:
        if filename not in github_files:
            print "\tError: " + filename + " no encontrado en el repositorio."

    for filename in repo_files:
        if filename not in github_files:
            print "\tError: " + filename + " no encontrado en el repositorio."


if not error:
    print "Parece que la entrega se ha realizado bien."

print
print "La salida de pep8 es: (si todo va bien, no ha de mostrar nada)"
print
filename = student_appname + '/views.py'
if filename in github_files:
    os.system('pep8 --repeat --show-source --statistics /tmp/'
              + aleatorio + '/' + filename)
else:
    print "Fichero " + filename + " no encontrado en el repositorio."
print
