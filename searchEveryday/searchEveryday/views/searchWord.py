import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from ..config import URI, DB_PATH, DatabaseConnection
from ..sql.insert import insertCustKeyword
from ..sql.select import getSeCustKeyword_WithCust_id
from ..common.confirm import login_yn


def addSearchWord(request):
    print("Called addSearchWord")
    try:
        data = json.loads(request.body)
        cust_id = data.get('cust_id')
        df = getCustKeyword(cust_id)
        response_data = {'success': False, 'redirect_url': URI['DEFAULT']}
        if not df.empty:
            print("2")
            cust_info = df.iloc[0]
            response_data['cust_id'] = cust_info["cust_id"]
            response_data['reg_date'] = cust_info["reg_date"]
            response_data['reg_time'] = cust_info["reg_time"]
            print("3")
            # keyword가 None일 경우에 대한 처리 추가
            keyword_list = cust_info["keyword"].split("|") if cust_info.get("keyword") else []
            if len(keyword_list) > 0:
                response_data['keyword1'] = keyword_list[0]
            if len(keyword_list) > 1:
                response_data['keyword2'] = keyword_list[1]
            if len(keyword_list) > 2:
                response_data['keyword3'] = keyword_list[2]
            print("4")
        else:
            response_data['cust_id'] = cust_id
        response_data['redirect_url'] = '/addSearchWordView/'
        response_data['success'] = True
        return JsonResponse(response_data)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:  # 추가적인 예외 처리
        return JsonResponse({'error': str(e)}, status=500)

def addSearchWordView(request):
    if login_yn(request):
        return render(request, URI['ADDSEARCHWORDVIEW'])
    else:
        return redirect(URI['DEFAULT'])

def getCustKeyword(cust_id):
    with DatabaseConnection(DB_PATH) as conn:
        df_SeCustKeyword = getSeCustKeyword_WithCust_id(
            cust_id, conn
        )
        if len(df_SeCustKeyword) == 0:
            print(f'Registered Keyword is null: [{cust_id}]')
        return df_SeCustKeyword


def saveCustKeyword(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # JSON 데이터 파싱
            cust_id = data.get('cust_id')
            keyword1 = data.get('keyword1')
            keyword2 = data.get('keyword2')
            keyword3 = data.get('keyword3')
            if not keyword1 and not keyword2 and not keyword3:
                print("Nothing to Register")
            else:
                with DatabaseConnection(DB_PATH) as conn:
                    df_SeCustKeyword = insertCustKeyword(cust_id, keyword1, keyword2, keyword3, conn)
                    # if len(df_SeCustKeyword) == 0:
                    #     print(f'Save Cust Keyword: [{cust_id}] - [{keyword1}, {keyword2}, {keyword3}]')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return redirect(URI['DEFAULT'])