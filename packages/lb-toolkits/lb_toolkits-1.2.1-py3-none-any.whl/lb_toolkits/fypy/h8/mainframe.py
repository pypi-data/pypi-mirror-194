# -*- coding:utf-8 -*-
'''
@Project     : lb_toolkits

@File        : mainframe.py

@Modify Time :  2022/11/10 14:45

@Author      : Lee

@Version     : 1.0

@Description :

'''

import os
import sys
import datetime
import numpy as np

import tarfile
import glob
import re
from ahi8_l1_pro import hsd2netcdf


def extract(nowdate, tar_path, target_path):

    hsdlist = []

    try:
        tar = tarfile.open(tar_path, "r")
        file_names = tar.getnames()
        file_names.sort()

        for file_name in file_names:
            # print(file_name)
            if re.search('HS_H08_%s_%s_B\d+_FLDK_R\d+_S0[2-4]10.DAT.bz2' %(nowdate.strftime('%Y%m%d'),
                                                                           nowdate.strftime('%H%M')), file_name) :
                outname = os.path.join(target_path, file_name)
                hsdlist.append(outname)
                if os.path.isfile(outname) :
                    print('%s is exist, will continue...' %(outname))
                    continue
                else:
                    print(outname)
                    tar.extract(file_name, target_path)
        tar.close()
    except Exception as e:
        raise e

    return hsdlist



if __name__ == '__main__':

    starttime = datetime.datetime.strptime('20190626000000', '%Y%m%d%H%M%S')
    endtime   = datetime.datetime.strptime('20190626140000', '%Y%m%d%H%M%S')

    tarpath =  r'./'
    hsdpath = r'./hsd/'
    ncpath = r'./netcdf'
    dt = starttime
    while dt <= endtime :

        tarname = os.path.join(tarpath, '%s.tar' %(dt.strftime('%Y%m%d')))
        if not os.path.isfile(tarname) :
            print('%s is not exist, will continue...' %(tarname))
            continue

        pathout = os.path.join(ncpath, dt.strftime('%Y%m%d'))
        outname = os.path.join(pathout, 'HS_H08_%s_FLDK.nc' %(dt.strftime('%Y%m%d_%H%M')))
        if os.path.isfile(outname) :
            print(outname+' is exist, will continue...')
            dt += datetime.timedelta(minutes=10)
            continue

        hsdlist = extract(dt, tarname, hsdpath)

        if not os.path.isdir(pathout) :
            os.makedirs(pathout)

        hsd2netcdf(outname, dt, hsdpath)

        for hsdfile in hsdlist:
            if os.path.isfile(hsdfile) :
                os.remove(hsdfile)

        templist = glob.glob(os.path.join(pathout, 'HS_H08_%s_*10.DAT' %(dt.strftime('%Y%m%d'))))
        for tmpfile in templist:
            if os.path.isfile(tmpfile) :
                try:
                    os.remove(tmpfile)
                except BaseException as e :
                    print(e)
        dt += datetime.timedelta(minutes=10)
