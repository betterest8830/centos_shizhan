#!/bin/bash

#source ~/.bashrc

date_time=`date +%Y%m%d-%H%M`
log_name=${date_time}_shida.log
python spider_shida.py >log/${log_name} 2>&1
flag=`grep -c 'FAIL\|ERR' log/${log_name}`
if [ ${flag} -ne '0' ]
then
    /root/anaconda3/bin/python /home/xcl/centos_shizhan/tool/bin/send_email.py '北邮十大抓取失败' '/home/xcl/centos_shizhan/spider/beiyouluntan'
    echo 'fail'
else
    echo 'succ'
fi



