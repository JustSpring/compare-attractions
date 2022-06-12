import sys
sys.path.insert(0, '/home/public')

activate_this='/home/private/.local/share/virtualenvs/public-bnM8vzgC/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file.read(), dict(__file__=activate_this))


from website import app as application
