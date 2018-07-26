from __future__ import print_function
import yaml 
import os
import paramiko
import time
import logging
import sys
import commands
from prometheus_client import Gauge
from datetime import datetime
from n15xxcommands import n15xxcommands


cfg_login ={}
cfg_task ={}
yamlFile = sys.argv[1:].__str__().strip("[']")

for key, value in yaml.load(open(yamlFile))['sw_login'].iteritems():
    cfg_login[key]=value
#print (cfg_login.get("user"))

for key, value in yaml.load(open(yamlFile))['sw_task'].iteritems():
    cfg_task[key]=value
#print (cfg_task)

#if (cfg.get(''))

if (cfg_task.get('function') in'tftp_backup'):
    sw = n15xxcommands(cfg_login.get("user"), cfg_login.get("key"), cfg_login.get("ip"),cfg_login.get("port"))
    sw.tftp_backup(cfg_task.get('path'),cfg_task.get('filename'))