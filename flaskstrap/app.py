from flask import (
   Flask,
   request,
   jsonify
)
import os
from string import ascii_lowercase
from random import choice
from ansi_parser import Inventory
      
app = Flask(__name__)
inv = os.path.join(os.path.expanduser('~'), "hosts")
if not os.path.exists(inv):
   open(inv,'w').close()

@app.route('/')
def show_environ():
   inventory = Inventory(inv)
   return jsonify(inventory.hosts)

@app.route('/add', methods=["GET", "POST"])
def add_server():
   random_name = ''.join([choice(ascii_lowercase) for i in  range(6)])
   if request.method == 'POST':
      config = request.form.get('config', request.environ['REMOTE_ADDR'])
      name = request.form.get('name', random_name)
      groups = request.form.get('groups', 'common')
      groups = groups.split(",")  
   else:
      name = random_name
      config = request.environ['REMOTE_ADDR']
      groups = ['common']
   inventory = Inventory(inv)
   inventory.add_host_by_name(name, config)
   inventory.add_group_by_name(groups, name)
   inventory.write_config()
   return jsonify({
                   "name": name, 
                   "config": config, 
                   "groups": groups
                  })


def main():   
   app.run(host='0.0.0.0')
