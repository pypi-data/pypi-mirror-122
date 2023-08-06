import sys,os
import time

'''
日志引擎
'''
class Logger:

    @property
    def Null(self):
        return Logger(isNull= False)

    def info(self, v):
        if not self.__isNull:
            v = '\n[I] {}: {}'.format(time.strftime('%H:%M:%S', time.localtime()), v)
            print(f'\033[1;32m {v}\033[0m',end=' ')
            self.__writer.write(v)

    def warn(self, v):
        if not self.__isNull:
            v = '\n[W] {}: {}'.format(time.strftime('%H:%M:%S', time.localtime()), v)
            print(f'\033[1:33m {v} \033[0m',end=' ')
            self.__writer.write(v)

    def error(self, v):
        if not self.__isNull:
            v = '\n[E] {}: {}'.format(time.strftime('%H:%M:%S', time.localtime()), v)
            print(f'\033[1:33m {v} \033[0m',end=' ')
            self.__writer.write(v)

    def fatal(self, v):
        if not self.__isNull:
            v = '\n[F] {}: {}'.format(time.strftime('%H:%M:%S', time.localtime()), v)
            print(f'\033[1;31m {v}\033[0m',end=' ')
            self.__writer.write(v)
            self.__release()
        sys.exit(-1)

    def __release(self):
        self.__writer.flush()
        self.__writer.close()

    def __init__(self,folder = '', isNull = False):
        if len(folder) <= 0:
            folder = 'logs'
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.__isNull = isNull
        self.__currentFile = '{}/{}.log'.format(folder,time.strftime('%Y%m%d', time.localtime()))
        self.__writer = open(self.__currentFile, 'a', encoding='UTF-8')

        print('''
$$\  $$\  $$\  $$$$$$\   $$$$$$\  $$$$$$$\  $$$$$$\   $$$$$$\  $$$$$$$\  
$$ | $$ | $$ |$$  __$$\ $$  __$$\$$  _____|$$  __$$\ $$  __$$\ $$  __$$\ 
$$ | $$ | $$ |$$ /  $$ |$$ |  \__\$$$$$$\  $$ /  $$ |$$ /  $$ |$$ |  $$ |
$$ | $$ | $$ |$$ |  $$ |$$ |      \____$$\ $$ |  $$ |$$ |  $$ |$$ |  $$ |
\$$$$$\$$$$  |\$$$$$$  |$$ |     $$$$$$$  |\$$$$$$  |\$$$$$$  |$$ |  $$ |
 \_____\____/  \______/ \__|     \_______/  \______/  \______/ \__|  \__|''',end=' ')

'''
扩展
'''
class Convert:
    @classmethod
    def toBase64(self, str, encoding='utf-8'):
        pass
