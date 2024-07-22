#!/bin/bash
#

# 启动 nginx
nginx -g "daemon on;"

# 启动项目
BINDIR=/usr/local/services/lb_chore-1.0
cd $BINDIR && make run

/usr/bin/crond

while true; do sleep infinity; done
