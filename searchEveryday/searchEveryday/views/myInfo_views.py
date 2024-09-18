import requests
import jwt, json

from ..common.confirm import login_yn
from ..config import URI, KAKAO_CONFIG, DB_PATH, DatabaseConnection
from django.shortcuts import render, redirect
import pandas as pd
from ..sql.select import getSeCustInfo_WithCi, getSeCustInfo_WithCust_id


def myInfo_details(request):
    #if login_yn(request):
    cust_id = request.POST.get('cust_id')
    if cust_id:
        df = getCustInfo(cust_id)
        cust_info = df.iloc[0]
        request.session['cust_id'] = cust_info["cust_id"]
        request.session['cust_nm'] = cust_info["cust_nm"]
        request.session['sign_up_way'] = cust_info["sign_up_way"]
        request.session['cust_hp'] = cust_info["cust_hp"]
        request.session['cust_email'] = cust_info["cust_email"]
        request.session.modified = True
        return render(request,URI['MYINFO_DETAILS'])
    else:
        return redirect(URI['DEFAULT'])


def getCustInfo(cust_id):
    with DatabaseConnection(DB_PATH) as conn:
        df_SeCustInfo = getSeCustInfo_WithCust_id(
            cust_id, conn
        )
        if len(df_SeCustInfo) == 0:
            print(f'Error: cust_id is wrong: [{cust_id}]')
        return df_SeCustInfo
