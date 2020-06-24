#!/bin/sh

which python &>/dev/null || { echo "未检测到Python" && exit; }

CUR_PATH=$(cd "$(dirname "$0")";pwd)
cd $CUR_PATH

[ -d log ] || mkdir log
[ -d bin ] || mkdir bin

[ -e conf/config.json ] || cp conf/config.json.template conf/config.json

echo "正在初始化..."
python src/install.py

echo "正在创建定时任务..."
mv bin/io.github.gallenshao.dailytask.plist ~/Library/LaunchAgents/io.github.gallenshao.dailytask.plist
launchctl load -w ~/Library/LaunchAgents/io.github.gallenshao.dailytask.plist
launchctl start ~/Library/LaunchAgents/io.github.gallenshao.dailytask.plist
echo "定时任务启动成功"

echo "正在尝试第一次启动，请在权限弹窗中选择允许"
./bin/run.sh