"""
牧德原始数据的查找整理。
原始牧德文件包含Project、Defect和VerifyResult三个文件夹，没问文件由project、layer、date组成，此.py用于查找三个文件夹的交集并记录成.ini
"""

import os
import shutil
import config  # 载入设置文件

WIDTH = 108
HEIGHT = 108
RESOLUTION = 12.5
DIGIT = 64
digit = 6

PATH = r'E:\Data\PCB\Mude'
Defect_Path = config.setting['NetworkSetting']['DefectPath']
Project_Path = config.setting['NetworkSetting']['ProjectPath']
VerifyResult_path = config.setting['NetworkSetting']['VRSVerifyPath']
NewVerifyResult_path = config.setting['NetworkSetting']['NewVerifyResultpath']


def load_projects(reload=False):
    """
    遍历所有projects的名字，找出其交集
    """
    if os.path.exists(r'E:\Data\PCB\Mude\projects.ini') and not reload:
        f = open(r'E:\Data\PCB\Mude\projects.ini', 'r')
        h = f.readlines()
        projects = [i.strip() for i in h]
        f.flush()
        f.close()
        return projects
    else:
        projects = set(os.listdir(Defect_Path))
        projects = projects & set(os.listdir(Project_Path))
        # projects = projects & set(os.listdir(AOIOfflineVRSVerify_Path))

        f = open(r'E:\Data\PCB\Mude\projects.ini', 'w')
        for project in projects:
            f.write(project + '\n')
        f.close()
        return projects


projects = load_projects(reload=False)


def load_verify_results(reload=False):
    """
    重新排版Verify Resuls文件
    """
    elements = []
    if not os.path.exists(r'E:\Data\PCB\Mude\NewVerifyResult') or reload:
        paths = os.listdir(VerifyResult_path)
        for path in paths:
            if path.find('.') > 0:
                continue
            files = os.listdir(os.path.join(VerifyResult_path, path))
            for file in files:
                if file.find('.') > 0:
                    continue
                layers = os.listdir(os.path.join(VerifyResult_path, path, file))
                for layer in layers:
                    if layer.find('.') > 0:
                        continue
                    dates = os.listdir(os.path.join(VerifyResult_path, path, file, layer))
                    for date in dates:
                        if date.find('.') > 0:
                            continue
                        elements.append(os.path.join(VerifyResult_path, path, file, layer, date))
        for element in elements:
            t = element.split('\\')
            path = os.path.join(r'E:\Data\PCB\Mude\NewVerifyResult', t[-3], t[-1], t[-2])
            if not os.path.exists(path):
                os.makedirs(path)
            for file in os.listdir(element):
                if file.find('Desktop') >= 0:
                    continue
                shutil.copy(os.path.join(element, file), path)


load_verify_results(reload=False)
