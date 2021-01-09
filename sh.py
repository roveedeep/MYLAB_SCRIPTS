import mysql.connector
from tabulate import tabulate
from sys import argv


mydb=mysql.connector.connect(host="41.21.8.15", user="ntombi", passwd="CIS467t$", database="admindb")

mycursor =mydb.cursor()

action1 = 'ENTER SOLUTION ID TO SEARCH'


print(tabulate([[action1]], tablefmt = 'rst'))

print ('\n')


sol_id_in =str(input('SOLUTION ID: '))
vvv=sol_id_in,

sql_select = """SELECT SITE.SOLUTION_ID,CUSTOMER_NAME, SITE_NAME,CIRCUIT_ID,LINK_TYPE,VLAN,
                DEVICE.DEVICE_ID,DEVICE_MODEL,DEVICE_SN, POP, PACKET_LOSS, ADDRESS
                  FROM SITE JOIN DEVICE
                    ON SITE.SOLUTION_ID=DEVICE.SOLUTION_ID AND SITE.SOLUTION_ID=%s
                    JOIN RECHABILITY R
                       ON DEVICE.DEVICE_ID = R.DEVICE_ID
                 """



q=mycursor.execute(sql_select,vvv)
record = mycursor.fetchall()
print ('\n')

print(tabulate(record, headers=['SOLUTION ID','CUSTOMER NAME','SITE NAME','CIRCUIT ID','LINK TYPE','VLAN',
                                'DEVICE ID','DEVICE MODEL','S/N','POP','PACKET LOSS','ADDRESS'], tablefmt = 'github'))

mydb.commit()
