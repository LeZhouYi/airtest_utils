import json
import os
import shutil
import requests
from pathlib import Path

def cleanReports():
    '''
    清空所有报告
    '''
    report_folder = str.format('{}/reports', os.getcwd())
    img_folder = str.format('{}/reports/screenshots', os.getcwd())
    log_folder = str.format('{}/reports/logs', os.getcwd())
    if Path(report_folder).exists():
        shutil.rmtree(report_folder)
    os.mkdir(report_folder)
    os.mkdir(img_folder)
    os.mkdir(log_folder)

def checkWdaStatus():
    '''
    检查WDA的运行状态
    '''
    response = requests.get('http://localhost:8200/status')
    assert response.status_code == 200, "EROOR:WDA NOT RUNNING!!!"
    content = json.loads(response.content)
    assert content["value"]["state"]=="success", "ERROR: WDA NOT CONNECT CORRECTLY, STATE NOT SUCCESS"
    return True