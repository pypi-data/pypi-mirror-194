"""
牧德原始数据的查找整理。
原始牧德文件包含Project、Defect和VerifyResult三个文件夹，每个文件由project、layer、date组成，此.py用于查找三个文件夹的交集并记录成.ini
load_verify_result：重新排版VerifyResult文件，按照project-date-layer的顺序
load_projects：筛选同时具有project, defect和verify result的projects，保存在projects.ini
load_dates：根据筛选出来的projects，筛选可以读取数据的(project, layer, date)
"""
import os
import mudeConstant as mc
import shutil

WIDTH = mc.WIDTH
HEIGHT = mc.HEIGHT
RESOLUTION = mc.RESOLUTION
DIGIT = mc.DIGIT
digit = mc.digit

PATH = mc.PATH
Defect_Path = mc.Defect_Path
Project_Path = mc.Project_Path
VerifyResult_path = mc.VerifyResult_path
NewVerifyResult_path = mc.NewVerifyResult_path


def load_verify_results(reload=False):
    """
    重新排版Verify Resuls文件
    """
    elements = []
    if not os.path.exists(NewVerifyResult_path) or reload:
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
            path = os.path.join(NewVerifyResult_path, t[-3], t[-1], t[-2])
            if not os.path.exists(path):
                os.makedirs(path)
            for file in os.listdir(element):
                if file.find('Desktop') >= 0:
                    continue
                shutil.copy(os.path.join(element, file), path)


def load_projects(reload=False):
    """
    遍历所有projects的名字，找出其交集
    :param reload: 是否重新查找projects
    :return: projects交集
    """
    if os.path.exists(r'E:\Data\PCB\Mude\projects.ini') and not reload:
        f = open(r'E:\Data\PCB\Mude\projects.ini', 'r')
        h = f.readlines()
        projects = [i.strip() for i in h]
        f.close()
        return projects
    else:
        projects = set(os.listdir(Defect_Path))
        projects = projects & set(os.listdir(Project_Path))
        projects = projects & set(os.listdir(NewVerifyResult_path))

        f = open(r'E:\Data\PCB\Mude\projects.ini', 'w')
        for project in projects:
            f.write(project + '\n')
        f.close()
        return projects


def load_dates(reload=False):
    """
    根据筛选出来的projects，筛选可以读取数据的(project, layer, date)
    :param reload: 是否重新查找可读取得数据
    :return: 可读取得(project, layer, date)列表
    """
    projects = load_projects(reload=False)

    if os.path.exists(r'E:\Data\PCB\Mude\dates.ini') and not reload:
        f = open(r'E:\Data\PCB\Mude\dates.ini', 'r')
        h = f.readlines()
        f.close()
        projects, layers, dates = tuple(zip(*[i.strip().split('\t') for i in h]))
        return projects, layers, dates
    else:
        f = open(r'E:\Data\PCB\Mude\dates.ini', 'w')
        for project in projects:
            def_layer = set(os.listdir(os.path.join(Defect_Path, project)))
            for layer in def_layer:
                if not os.path.exists(os.path.join(Project_Path, project, '0_101', project + '_' + layer + '_' + '101.mvi')):
                    continue
                def_date = set(os.listdir(os.path.join(Defect_Path, project, layer, '0')))
                for date in def_date:
                    if not os.path.exists(os.path.join(NewVerifyResult_path, project, date, project + '_' + layer + '_0')):
                        continue
                    f.write(project + '\t' + layer + '\t' + date + '\n')
                    f.flush()
        f.close()
        f = open(r'E:\Data\PCB\Mude\dates.ini', 'r')
        h = f.readlines()
        f.close()
        projects, layers, dates = tuple(zip(*[i.strip().split('\t') for i in h]))
        return projects, layers, dates


if __name__ == '__main__':
    projects = load_projects(reload=True)
    print(len(projects))
    projects, layers, dates = load_dates(reload=True)
