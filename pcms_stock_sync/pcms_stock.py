# -*- coding: utf-8 -*-
import os
import sys
import json
import requests

from database import *

logpath = "/data/logs/ems/"

class pcms_stock:
    @classmethod
    def sync_total(cls,pcms_api):
        logfile = open(logpath + 'update_stock.txt', 'w')
        records = database.get_all_skus()

        error_list = []

        for record in records:
            total = 0
            sku = record[0]

            physical = database.count_items_by_sku(sku)
            virtual = database.count_virtual_stock_by_sku(sku)
            offline_allocation = database.count_offline_allocation_by_sku(sku)

            total += int(physical[0])

            if virtual[0] is not None:
                total += int(virtual[0])

            if offline_allocation[0] is not None:
                total -= int(offline_allocation[0])

            stock = cls.build_sku_stock_update(sku, total)
            payload = [stock]

            req = "sending sku: " + sku + ", total: " + str(total)
            logfile.write("{0}\n".format(req))
            print req

            headers = {'content-type': 'application/json'}
            response = requests.post(
                pcms_api,
                headers=headers,
                data=json.dumps(payload)
            )

            res = "{0}: {1}".format(response.json()['message'], response.json()['data'])
            logfile.write("{0}\n".format(res))
            print res

            if 'Error' in res:
                error_list.append(res)

        logfile.close()

        errfile = open(logpath + 'update_stock_error.txt', 'w')
        errfile.write('\n'.join(error_list))
        errfile.close()


    @classmethod
    def build_sku_stock_update(cls, sku, total):
        payload = {
            "sku": sku,
            "quantity": "0",
            "note": "adjust yamato stock",
            "total": str(total)
        }
        return payload


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Please specify pcms server url"
    else:
        print "Sync stock to %s" % sys.argv[1]

        host=''
        user=''
        passwd=''
        db_name=''

        if sys.argv[1] == "http://pcms.alpha.itruemart.com/api/v4/stock/increase": # FOR DIGITAL OCEAN
            host='localhost'
            user='root'
            passwd='1q2w3e4r'
            db_name='ops'
        elif sys.argv[1] == "http://pcms.itruemart-dev.com/api/v4/stock/increase": # FOR Staging
            host='myl.iems-dev.com'
            user='ems_rw'
            passwd='1q2w3e4r'
            db_name='ems_db'
        elif sys.argv[1] == "http://pcms.itruemart.com/api/v4/stock/increase": # FOR PROD
            host='myl.iems.com'
            user='ems_rw'
            passwd='EE1m4$s4'
            db_name='ems_db'
        else :
            print "Invalid URL input"
            exit(0)

        database.create_connection(
            host=host,
            user=user,
            passwd=passwd,
            db=db_name
        )

        pcms_stock.sync_total(sys.argv[1])