
class Inventory(object):
  def __init__(self, filename):
     self.filename = filename
     self.hosts = {
        "groups" : {},
        "hosts" : {}
     }
     self.groupname = False
     self.hostname = False
     self.parse_config()

  def clean(self, line):
     return line.replace("\n", "")

  def parse_config(self):
     with open(self.filename, 'r') as inventory:
        for line in inventory:
           if ":children" in line:
              self.add_group(line)
           elif "[" in line:
              self.add_host(line)
           elif len(line) < 2:
              self.groupname = False
              self.hostname = False
           elif self.groupname:
              self.add_host_to_group(line)
           elif self.hostname:
              self.add_host_config(line)

  def add_group(self, line):
     line = self.clean(line)
     self.hostname = False
     self.groupname = line.split(":children")[0].replace("[", "")
     self.hosts["groups"][self.groupname] = []

  def add_host_to_group(self, line):
     self.line = self.clean(line)
     self.hosts["groups"][self.groupname].append(self.line)

  def add_host(self, line):
     line = self.clean(line)
     self.groupname = False
     self.hostname = line.split("]")[0].replace("[","")

  def add_host_config(self, line):
     line = line.replace("\n", "")
     self.hosts["hosts"][self.hostname] = line

  def add_host_by_name(self, name, config):
     self.hosts["hosts"][name] = config 

  def add_group_by_name(self, groups, host):
     for group in groups:
        if self.hosts["groups"].get(group, False):
           self.hosts["groups"][group].append(host)
        else:
           self.hosts["groups"][group] = [ host ]

  def write_config(self):
     print "writing {}".format(self.filename)
     with open(self.filename, "w") as inventory:
        for host in self.hosts["hosts"]:
           inventory.write("[" + host + "]\n")
           inventory.write(self.hosts["hosts"][host] + "\n")
           inventory.write("\n")
        for group in self.hosts["groups"]:
           inventory.write("[" + group + ":children]\n")
           for host in self.hosts["groups"][group]:
              print host
              inventory.write(host + "\n")
           inventory.write("\n")
