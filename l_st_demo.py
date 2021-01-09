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

def add_time(a):
    if a ==  '':
        a=  datetime.time(0,0,0) + datetime.time(0,2)
    else:
        a = datetime.time(a) + datetime.datetime(0,2)
    return a

mydb=mysql.connector.connect(host="41.21.8.15", user="ntombi", passwd="CIS467t$", database="admindb")

mycursor =mydb.cursor()


sql_select = """SELECT MGNT_IP FROM RECHABILITY
                 """

sql_select_2 = """SELECT LINK_UP_TIME FROM RECHABILITY
                """

sql_insert= """UPDATE RECHABILITY SET PACKET_LOSS = %s, LINK_STATUS =%s, DELAY_AVG = %s, TIME=%s, LINK_UP_TIME = %s
                    WHERE MGNT_IP=%s
                        """

link_up_time = datetime.time(0,0,0)


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
            mycursor.execute(sql_select_2)
            g = mycursor.fetchall()
            print(record)
            for dev_ip in record:
                out_p = my_device.ping(dev_ip[0])
                jk = out_p['success']
                pk = jk['packet_loss']
                dl=jk['rtt_avg']
                pk_per = str(calc(pk)) + '%'
                if pk  >= 5:
                    l_st = 'DOWN'
                    for lut in g:
                        print(lut[0])
                        lut = add_time(int(lut[0]))
                        ins_2 = (pk_per, l_st,dl, ct,lut[0],  dev_ip[0])
                        mycursor.execute(sql_insert,ins_2)


                if pk < 5:
                    l_st = 'UP'
                    for lut in g:
                        print(lut)
                        lut = add_time(lut[0])
                        ins_2 = (pk_per, l_st,dl, ct,lut[0],  dev_ip[0])
                        mycursor.execute(sql_insert,ins_2)

                mydb.commit()

        except Exception as unknown_error:
            print(unknown_error)
            break
#        time.sleep(120)
