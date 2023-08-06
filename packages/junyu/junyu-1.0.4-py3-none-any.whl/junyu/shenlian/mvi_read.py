import traceback
from multiprocessing import cpu_count, Pool
import os
import pickle
from . import Mvi
import mudeConstant as mc

WIDTH = mc.WIDTH
HEIGHT = mc.HEIGHT
RESOLUTION = mc.RESOLUTION

DIGIT = mc.DIGIT
digit = mc.digit


def mvi_read(project):
    try:
        print('线程id: {}， 处理任务为: {}， 线程开始处理'.format(os.getpid(), project))
        path = os.path.join(mc.Project_Path, project, '0_101')
        # print(project)
        if os.path.exists(os.path.join(path, project + '_GTL_101.mvi')):# and not os.path.exists(os.path.join(r'E:\Data\PCB\Mude\Train', project, 'gtl.pkl')):
            gtl = Mvi.mvi(os.path.join(path, project + '_GTL_101.mvi'))
            pickle.dump(gtl, open(os.path.join(r'E:\Data\PCB\Mude\Train', project, 'gtl.pkl'), 'wb'))
        if os.path.exists(os.path.join(path, project + '_GBL_101.mvi')):# and not os.path.exists(os.path.join(r'E:\Data\PCB\Mude\Train', project, 'gbl.pkl')):
            gbl = Mvi.mvi(os.path.join(path, project + '_GBL_101.mvi'))
            pickle.dump(gbl, open(os.path.join(r'E:\Data\PCB\Mude\Train', project, 'gbl.pkl'), 'wb'))
        if os.path.exists(os.path.join(path, project + '_DRL_101.mvi')):# and not os.path.exists(os.path.join(r'E:\Data\PCB\Mude\Train', project, 'drl.pkl')):
            drl = Mvi.mvi(os.path.join(path, project + '_drl_101.mvi'))
            pickle.dump(drl, open(os.path.join(r'E:\Data\PCB\Mude\Train', project, 'drl.pkl'), 'wb'))
        print('线程id: {}， 处理任务为: {}， 线程结束处理'.format(os.getpid(), project))
    except Exception as e:
        print('Error' + str(e))
        traceback.print_exc()
        raise Exception(str(e))


if __name__ == '__main__':
    # projects, _, _ = files_find.load_dates(reload=False)
    # projects = set(projects)
    projects = os.listdir(r'E:\Data\PCB\Mude\Train')
    print('cpu count is ', cpu_count())
    print('主线程id为 ', os.getpid())
    thread_pool = Pool(48)
    thread_pool.map(mvi_read, projects)
    print('等待所有线程完成执行')
    thread_pool.close()
    thread_pool.join()
    # pass