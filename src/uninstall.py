# -*- coding: UTF-8 -*-

import os, sys
from config import get_config


def get_root():
	path = os.path.normpath(os.path.join(os.getcwd(), sys.argv[0]))
	return os.path.sep.join(path.split(os.path.sep)[:-2])


def get_modules_on(config):
	return [item['name'] for item in config['modules'] if item['on'] is True]


def uninstall_module(module):
	print(u'正在卸载模块【%s】...' % module)
	os.chdir('module/%s' % module)
	os.system('/bin/sh ./uninstall.sh')
	os.chdir('../..')


if __name__=='__main__':
	# change working directory
	root = get_root()
	os.chdir(root)

	# uninstall modules
	config = get_config()
	modules_on = get_modules_on(config)
	for module in modules_on:
		uninstall_module(module)