import os
print(f"File: {__file__}")
print(f"Dirname: {os.path.dirname(__file__)}")
print(f"Abspath Dirname: {os.path.abspath(os.path.dirname(__file__))}")
path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
print(f"Path: {path}")
uri = 'sqlite:///' + path
print(f"URI: {uri}")
