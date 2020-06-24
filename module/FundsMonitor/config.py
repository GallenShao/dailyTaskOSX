# -*- coding: UTF-8 -*-

import json
import copy

config = None

def get_config():
	global config
	if config is None:
		with open('conf/config.json') as f:
			config = json.load(f)

	return copy.deepcopy(config)