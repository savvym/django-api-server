#!/bin/bash
CELERY_PATH=/data/home/zhhdzhang/venv/bin/celery

# 读取当前角色
if [ -f current_role ]; then
    CURRENT_ROLE=$(cat current_role)
else
    CURRENT_ROLE=master
fi

# 设置下一个角色
if [ "$CURRENT_ROLE" == "master" ]; then
    NEXT_ROLE=slave
else
    NEXT_ROLE=master
fi

# 启动新的Celery进程
# nohup ${CELERY_PATH} -A project worker -n ${NEXT_ROLE} --pidfile=${NEXT_ROLE}.pid -l INFO &
${CELERY_PATH} multi start ${NEXT_ROLE} -A project -P gevent -c 100 \
                --pidfile=${NEXT_ROLE}.pid \
                -l INFO

# 检查并杀掉旧的Celery进程
if [ -f ${CURRENT_ROLE}.pid ]; then
    PID=$(cat ${CURRENT_ROLE}.pid)
    if ps -p ${PID} > /dev/null; then
        kill ${PID}
    fi
fi

# 更新当前角色
echo ${NEXT_ROLE} > current_role