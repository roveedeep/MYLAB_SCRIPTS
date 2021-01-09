import mysql.connector
from netmiko import Netmiko
import time


def con(host):
    con_tel = {
                'device_type' : 'cisco_ios_telnet',
                'host' : host,
                'username' : 'cisco',
                'password' : 'cisco'
        }
    return con_tel


mydb=mysql.connector.connect(host="41.21.8.15", user="bilab", passwd="CIS467t$", database="admindb")

mycursor =mydb.cursor()


sql_select = """SELECT MGNT_IP FROM RECHABILITY
                 """
sql_insert= """UPDATE RECHABILITY SET UP_TIME = %s
                    WHERE MGNT_IP=%s
                        """


#while True:
q=mycursor.execute(sql_select)
record = mycursor.fetchall()

for hosts in record:
    try:
#            print(hosts[0])
        con_tel2 = con(hosts[0])
        c = Netmiko(**con_tel2)
    except Exception as unknown_error:
        continue

#        print('accessing : %s' , format(hosts[0]))
    output = c.send_command('sh ver | i min')
    ins_1 = (output[13:], hosts[0])
    mycursor.execute(sql_insert, ins_1)
#        print(ins_1)

    mydb.commit()

#    time.sleep(3600)
