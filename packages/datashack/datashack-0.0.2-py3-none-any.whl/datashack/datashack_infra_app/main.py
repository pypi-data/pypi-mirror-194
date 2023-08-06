#!/usr/bin/env python

import os, sys
sys.path.append(os.path.dirname(__file__))
# sys.path.append(os.path.dirname(__file__) + '/../datashack_infra_app')

import json
import os
import subprocess
import sys
from typing import Dict, List
from cdktf import App
from additional_plugins.datashack_glue import GlueTableConf
from additional_plugins import DatashackStack, DatashackStackConf
import json 
import re
import tempfile
import shutil


def create_app_with_resource(env_data: Dict):
    app = App()
    
    resources = env_data["resources"]

    stack_conf = DatashackStackConf(
        env=env_data['env_id'],
        resources=resources)

    DatashackStack(app, stack_conf)
    app.synth()


def _move_to_this_dir():
    # move to this folder as we need to be in cdktf context now
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)


if __name__ == '__main__':
    # env_data = json.loads(sys.argv[1])
    env_data = {"env_id": "dev", "resources": [{"resource_type": "DatabaseConf", "resource_json": {"database_name": "db1", "s3_bucket": "tables-bucket"}}, {"resource_type": "StreamingTableConf", "resource_json": {"table_name": "users_events", "database_name": "db1", "columns": {"c1": {"col_type": "string", "partition": False, "required": True}, "c2": {"col_type": "int", "partition": False, "required": True}, "c3": {"col_type": "string", "partition": True, "required": True}, "c4": {"col_type": "string", "partition": False, "required": True}, "c5": {"col_type": "double", "partition": True, "required": True}}, "no_shards": 1}}, {"resource_type": "StreamingTableConf", "resource_json": {"table_name": "users", "database_name": "db1", "columns": {"id": {"col_type": "string", "partition": False, "required": True}, "age": {"col_type": "int", "partition": False, "required": True}, "name": {"col_type": "string", "partition": False, "required": True}}, "no_shards": 1}}]}
    create_app_with_resource(env_data)
