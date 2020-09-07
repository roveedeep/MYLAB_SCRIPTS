from netmiko import Netmiko
from sys import argv
from netmiko.ssh_exception import NetmikoTimeoutException
from netmiko.ssh_exception import AuthenticationException
from netmiko.ssh_exception import SSHException
import datetime
import os
from pathlib import Path


#Creating a folder and File Fuctions:

def folder(b,c):

    for r in range(0,1):
        try:
            os.makedirs(c)
        except:
            continue

    d =Path(c)
    e = d/str(b)
    return open(e, 'w')

def count(a):
    b= a+1
    return b

#Command to Excecute

def conf_send(a,b):
    c = a.send_command(b)
    return c

#Telnet Fuction
def TelnetConnection(a,b,c):

    con_tel = {
                'device_type' : 'cisco_ios_telnet',
                'host' : a,
                'username' : b,
                'password' : c
              }

    return con_tel

#SSH Fuction
def SSHConnection(a,b,c):

    con_ssh = {
                'device_type' : 'cisco_ios',
                'host' : a,
                'username' : b,
                'password' : c
        }

    return con_ssh

# cisco XR Connection
def SSH_ios_xr(a,b,c):

    con_ssh_xr = {
                'device_type' : 'cisco_xr',
                'host' : a,
                'username' : b,
                'password' : c
        }

    return con_ssh_xr


#Variables
string, host_ip, user_name, pass_word = argv

#Backup_log file name
host_dev = open(host_ip)
script_date = datetime.datetime.now()
current_time = script_date.strftime("[%d-%b-%Y %H:%M:%S]")
backup_path ='/home/osboxes/rancid/'

dest_file = 's_back_fail_log'
commands =  'sh run'
commands2 = 'sh int trunk'
commands3 = 'sh vlan br'

with open(host_ip) as f:
    dev_host = f.read().splitlines()


fail_count = 0
pass_count = 0
fail_list = []

#Create the log file
for i in dev_host:

    status_pass ='BACKUP SUCCESSFUL !!  , DEVICE :  ' +  i
    status_fail ='BACKUP UNSUCCESSFUL !!  , DEVICE :  ' +  i

    #Calling the functions
    con_tel =  TelnetConnection(i,user_name,pass_word)
    con_ssh =  SSHConnection(i,user_name,pass_word)
    con_ssh_xr =  SSH_ios_xr(i,user_name,pass_word)


    if i == 'h2':
        d_connect = Netmiko(**con_ssh_xr)
        print(status_pass)
        output2 = d_connect.send_command('sh ip int br')
        print(output2)
    else:
        try:

            d_connect = Netmiko(**con_ssh)

        except (NetmikoTimeoutException):
#Telnet try
            for k in range (0,1):
                try:
                    d_connect = Netmiko(**con_tel)

                except (AuthenticationException):
                    print(status_fail)
                    fail_list.append(i + '      :   Auth Fail')
                    fail_count = count(fail_count)
                    continue

                except Exception as unknown_error:
                    print(status_fail)
                    fail_list.append(i + '      :   TimeOut')
                    fail_count= count(fail_count)
                    continue

                backup_file = folder(i,backup_path)
                print(status_pass)
                output2 = conf_send(d_connect,commands)
                output3 = conf_send(d_connect,commands3)
                output = conf_send(d_connect,commands2)
                backup_file.truncate()
                backup_file.writelines('\n\n\n' + current_time + '\n\n\n\n\n')
                backup_file.write(output2 + output + '\n' + output3 +"\n")
                backup_file.close()
                pass_count =count(pass_count)
            continue

        except (AuthenticationException):
            print('Auth Failure ' + host_ip)
            fail_count = count(fail_count)
            fail_list.append(i + '      :   Auth Fail')
            print(status_fail)
            continue

        except (EOFError):
            print('Empty_Space_on_the_file')
            continue


        except (SSHException):
            print('tring the device via Telnet')

#Telnet try
            for k in range (0,1):
                try:
                    d_connect = Netmiko(**con_tel)

                except (AuthenticationException):
                    print(status_fail)
                    fail_list.append(i + '      :   Auth Fail')
                    fail_count = count(fail_count)
                    continue

                backup_file = folder(i,backup_path)
                print(status_pass)
                output2 = conf_send(d_connect,commands)
                output = conf_send(d_connect,commands2)
                output3 = conf_send(d_connect,commands3)
                backup_file.truncate()
                backup_file.writelines('\n\n\n' + current_time + '\n\n\n\n\n')
                backup_file.write(output2 + output + '\n' +  output3 +"\n")
                backup_file.close()
                pass_count = count(pass_count)
                fail_list.append(i)
                print(output)

            continue

        except Exception as unknown_error:
            print(status_fail)
            fail_count = count(fail_count)
            fail_list.append(i + '      :   '+unknown_error)
            continue

        backup_file = folder(i,backup_path)
        print(status_pass)
        output2 = conf_send(d_connect,commands)
        output3 = conf_send(d_connect,commands3)
        output = conf_send(d_connect,commands2)
        backup_file.truncate()
        backup_file.writelines('\n\n\n' + current_time + '\n\n\n\n\n')
        backup_file.write(output2 + output + "\n" + output3 +"\n")
        backup_file.close()
        pass_count = count(pass_count)

log = folder(dest_file,backup_path)
log.truncate()  # erase the file contente before writing
log.write("\n\n" +current_time + "\n\n")
log.write('\n--Successful :   {0}\n'.format(pass_count))
log.write('--UnSuccessful : {0}\n--------------------------\n'.format(fail_count))
for fail_list_dev in fail_list:
    log.write('---{0}\n'.format(fail_list_dev))
log.close()
