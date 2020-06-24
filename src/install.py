# -*- coding: UTF-8 -*-

import os, sys, json
from config import get_config


def get_root():
	path = os.path.normpath(os.path.join(os.getcwd(), sys.argv[0]))
	return os.path.sep.join(path.split(os.path.sep)[:-2])


def read_file(path):
	with open(path) as f:
		return f.read()
	return None


def write_file(path, data):
	with open(path, 'w') as f:
		f.write(data)


def generate_plist(config):
	plist = read_file('src/template/io.github.gallenshao.dailytask.plist.template')
	item = read_file('src/template/plist_item.template')

	array_list = ''
	for hour in range(config['startTime'], 24, config['startInterval']):
		array_list += item.replace('{HOUR}', str(hour))

	plist = plist.replace('{LIST}', array_list)
	plist = plist.replace('{DIR}', os.getcwd())

	write_file('bin/io.github.gallenshao.dailytask.plist', plist)


def get_modules_on(config):
	return [item['name'] for item in config['modules'] if item['on']]


def install_module(module):
	print(u'正在初始化模块【%s】...' % module['name'])
	os.chdir('module/%s' % module['name'])

	if module.has_key('config'):
		print(u'正在生成模块配置文件...')
		os.system('[ -d conf ] || mkdir conf')
		write_file('conf/config.json', json.dumps(module['config']))
	
	os.system('/bin/sh ./install.sh')
	os.chdir('../..')


def generate_runfile(config, modules):
	runfile = read_file('src/template/run.sh.template')
	item = read_file('src/template/run_item.template')

	array_list = ''
	for mod in modules:
		array_list += item.replace('{MOD}', mod)

	runfile = runfile.replace('{LIST}', array_list)
	runfile = runfile.replace('{LIMIT}', str(config['logLimits']))
	runfile = runfile.replace('{MAX}', str(int(1.5 * config['logLimits'])))

	write_file('bin/run.sh', runfile)
	os.system('chmod +x bin/run.sh')


if __name__=='__main__':
	# change working directory
	root = get_root()
	os.chdir(root)

	# generate files
	config = get_config()
	generate_plist(config)

	# install modules
	for module in config['modules']:
		if module['on']:
			install_module(module)

	modules_on = get_modules_on(config)
	generate_runfile(config, modules_on)
