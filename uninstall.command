#!/bin/sh

which python &>/dev/null || { echo "未检测到Python" && exit; }

CUR_PATH=$(cd "$(dirname "$0")";pwd)
cd $CUR_PATH

[ -e conf/config.json ] || cp conf/config.json.template conf/config.json

echo "正在取消定时任务..."
launchctl stop ~/Library/LaunchAgents/io.github.gallenshao.dailytask.plist &>/dev/null
launchctl unload -w ~/Library/LaunchAgents/io.github.gallenshao.dailytask.plist &>/dev/null

echo "正在删除临时文件..."
rm ~/Library/LaunchAgents/io.github.gallenshao.dailytask.plist &>/dev/null
rm bin/run.sh &>/dev/null

echo "正在卸载..."
python src/uninstall.py

echo "卸载成功"