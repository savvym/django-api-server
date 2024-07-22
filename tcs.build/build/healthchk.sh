#!/bin/bash
# health check shell
# return 0 if healthy, none zero for unhealthy
process_name=(LB_CHORE LB_CHORE-slave)
check_nginx_process=(nginx)

#process check
check_process()
{
    processes=$1
    for process in ${processes[@]}
    do
        processNum=`ps -ef | grep "$process" | grep -v 'grep' | wc -l`
        if [ "$processNum" = "0" ];then
            exit 1
        fi
    done
}

check_process "${process_name[*]}"
check_process "${check_nginx_process[*]}"

exit 0