#
# Conteudo do arquivo `wsgi.py`
#
import sys

#activator = '/home/grader/nd_project/catalog-site/venv/bin/activate_this.py'  # Looted from virtualenv; should not require modification, since it's defined relatively
#with open(activator) as f:
#    exec(f.read(), {'__file__': activator})

#activate_this = '/home/grader/nd_project/catalog-site/venv/bin/activate_this.py'
#execfile(activate_this, dict(__file__=activate_this))

sys.path.insert(0, "/home/grader/nd_project/catalog-site")

from catalog_project import app as application
