import mysql.connector
from tabulate import tabulate
from sys import argv
from napalm import get_network_driver
import json

driver = get_network_driver('ios')
my_device=driver('d1','cisco','cisco')
#my_device.open()



#ping_list = ['172.21.200.1','1.1.1.1','1.1.1.2','172.21.101.1']
#j_s = int(j['uptime'])
#for pp in ping_list:

#    out_p = my_device.ping(pp)
#    jk = out_p['success']
#    print(jk['packet_loss'])

mydb=mysql.connector.connect(host="41.21.8.15", user="ntombi", passwd="CIS467t$", database="admindb")

mycursor =mydb.cursor()

action1 = 'MPLS HEALTH'


print(tabulate([[action1]], tablefmt = 'rst'))

print ('\n')


#sol_id_in =str(input('SOLUTION ID: '))
#vvv=sol_id_in,

sql_select = """SELECT DEVICE_NAME,R.MGNT_IP,SITE.SOLUTION_ID,VLAN,
                DEVICE.DEVICE_ID,POP, PACKET_LOSS,LINK_STATUS,DELAY_AVG,R.UP_TIME,TIME
                  FROM SITE JOIN DEVICE
                    ON SITE.SOLUTION_ID=DEVICE.SOLUTION_ID AND SITE.SOLUTION_ID=DEVICE.SOLUTION_ID
                    JOIN RECHABILITY R
                       ON DEVICE.DEVICE_ID = R.DEVICE_ID ORDER BY DEVICE_NAME
                 """



q=mycursor.execute(sql_select)
record = mycursor.fetchall()
#print(record)
print ('\n')

print(tabulate(record, headers=['DEVICE NAME','MGNT_IP','SOLUTION ID','VLAN',
                                'DEVICE ID','POP','PACKET LOSS','LINK STATUS','DELAY_AVG','UP-TIME','UPDATE TIME'], tablefmt = 'github'))

mydb.commit()
