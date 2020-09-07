from netmiko import Netmiko
from sys import argv
from netmiko.ssh_exception import NetmikoTimeoutException
from netmiko.ssh_exception import AuthenticationException
from netmiko.ssh_exception import SSHException
import datetime
import os
from pathlib import Path



string, host_ip, user_name, pass_word = argv

dest_file = open('back_fail_log', 'a')
host_dev = open(host_ip)
script_date = datetime.datetime.now()
current_time = script_date.strftime("_:[%d-%b-%Y %H:%M:%S]")

with open(host_ip) as f:
    dev_host = f.read().splitlines()

dest_file.write("\n\n\n###########  BACKUP FOR " + current_time + "###########\n\n\n")

for i in dev_host:



    for r in range (0,1):
        try:
            backup_f = 'backups/' +str(i)
            os.mkdir(backup_f)
        except FileExistsError:
            continue

    backup_path =  Path(backup_f)
    t = current_time
    backup_txt = backup_path / t
#    file_name = "## " + str(i) + " [ " + backup_txt
    backup_file = open(backup_txt, 'w')

    con_ssh = {
                'device_type' : 'cisco_ios',
                'host' : i,
                'username' : user_name,
                'password' : pass_word
        }


    con_tel = {
                'device_type' : 'cisco_ios_telnet',
                'host' : i,
                'username' : user_name,
                'password' : pass_word
        }


    try:

        d_connect = Netmiko(**con_ssh)

    except (NetmikoTimeoutException):
#        print('device unreachable via ssh trying Telnet : ' + host_ip)

        for k in range (0,1):
            try:
                d_connect = Netmiko(**con_tel)

            except (AuthenticationException):
#                print ('wrong Auth details')
                print('backup FAILED !!!, DEVICE :  ' +  i )
                dest_file.write("BACKUP_FAILED !!! " + i + "\n")
                continue

            except Exception as unknown_error:
                print('backup FAILED !!!, DEVICE :  ' +  i )
                dest_file.write("BACKUP_FAILED !!! " + i + "\n")
                continue

#            except (NetmikoTimeoutException):
#                print('The device is completly down')
#                continue

            print('backup in progres , DEVICE :  ' +  i )
            output2 = d_connect.send_command('sh run')
            backup_file.write(output2 + "\n")
            #print(output)

        continue

#    except Exception as unknown_error:
#         print('some other Error : ' + str(unknown_error))
#         continue

    except (AuthenticationException):
        print('Auth Failure ' + host_ip)
        continue

    except (EOFError):
        print('end of file Error')
        continue


    except (SSHException):
        print('tring the device via Telnet')

        for k in range (0,1):
            try:
                d_connect = Netmiko(**con_tel)

            except (AuthenticationException):
                print ('wrong Auth')
                continue
            print('backup in progres , DEVICE :  ' +  i )
            output = d_connect.send_command('sh ip int br')
            print(output)

        continue

    except Exception as unknown_error:
         print('backup FAILED !!!, DEVICE :  ' +  i )
         dest_file.write("BACKUP_FAILED !!! " + i + "\n")
         continue



    print('backup in progres , DEVICE :  ' +  i )
    output2 = d_connect.send_command('sh run')
    backup_file.write(output2 + "\n")
    backup_file.close()

dest_file.close()
