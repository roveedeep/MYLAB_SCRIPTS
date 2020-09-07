import mysql.connector
from sys import argv
from napalm import get_network_driver
import time
import datetime

def calc(x):
    a = (x/5)*100
    return int(a)

def ct():
        s_d = datetime.datetime.now()
        ct = s_d.strftime("%d-%b-%Y %H:%M:%S")
        return ct

mydb=mysql.connector.connect(host="41.21.8.15", user="ntombi", passwd="CIS467t$", database="admindb")

mycursor =mydb.cursor()


sql_select = """SELECT MGNT_IP FROM RECHABILITY
                 """
sql_insert= """UPDATE RECHABILITY SET PACKET_LOSS = %s, LINK_STATUS =%s, DELAY_AVG = %s, TIME=%s
                    WHERE MGNT_IP=%s
                        """


while True:
    try:
        driver = get_network_driver('ios')
        my_device=driver('mon','cisco','cisco')
        my_device.open()

    except Exception as unknown_error:
        continue

    while True:
        q=mycursor.execute(sql_select)
        record = mycursor.fetchall()
        try:
            s_d = datetime.datetime.now()
            ct = s_d.strftime("%d-%b-%Y %H:%M:%S")
            for dev_ip in record:
                out_p = my_device.ping(dev_ip[0])
                jk = out_p['success']
                pk = jk['packet_loss']
                dl=jk['rtt_avg']
                pk_per = str(calc(pk)) + '%'
                if pk  >= 5:
                    l_st = 'DOWN'
                    ins_2 = (pk_per, l_st,dl, ct,  dev_ip[0])
                    mycursor.execute(sql_insert,ins_2)

                if pk < 5:
                    l_st = 'UP'
                    ins_2 = (pk_per, l_st,dl, ct,  dev_ip[0])
                    mycursor.execute(sql_insert,ins_2)

                mydb.commit()

        except Exception as unknown_error:
            break
        time.sleep(120)
