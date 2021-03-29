from ftplib import FTP
import sys, argparse
from pynput import keyboard



helps = ''' h = help
a - abort, прерывает передачу
c - close, закрывает соединение
z - изменить директорию
d  - удалить файл
l - получить список файлов
m - создать каталог
f - скачать файл
w - загрузить файл на сервер
v - добавить данные в файл
r - удалить каталог
n - переименовать файл
'''
    
def main(log, passw):
    ftp = FTP('')
    ftp.connect('localhost',8080)
    print(log, passw)
    if log and passw:
        ftp.login(str(log), str(passw))
        print(f'You login as {str(log)}')
    else:
        ftp.login()
        print('You login as anonym')

    def on_key_release(key):
        key = str(key)[1:-1]
        if key=='h': 
            print(helps)

        if key=='a': 
            print('Abort file transport!')
            ftp.abort()

        if key=='c':  
            print('Close!')
            ftp.close()
            return False

        if key=='z':  
            path = input('Введите путь: ')
            ftp.cwd(path)

        if key=='l':  
            path = input('Введите путь: ')
            ftp.dir(path)

        if key=='d':  
            try:
                path = input('Введите путь: ')
                ftp.delete(path)
            except:
                print('У вас нет прав на эту команду')  

        if key=='m':  
            try:
                path = input('Введите название каталога: ')
                ftp.mkd(path)
            except:
                print('У вас нет прав на эту команду')  

        if key=='f':  
            try:
                filename = input('Введите имя файла: ')
                localfile = open(filename, 'wb')
                ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
                localfile.close()
            except:
                print('У вас нет прав на эту команду')  

        if key=='w':  
            try:
                filename = input('Введите имя файла: ')
                localfile = open('clientDir/'+filename, 'rb')
                ftp.storbinary('STOR '+filename, localfile)
                localfile.close()
            except:
                print('У вас нет прав на эту команду')  

        if key=='v':  
            try:  
                filewrite = input('Введите имя файла для загрузки: ')
                fin = open ('clientDir/'+filewrite, 'r')
                filename = input('Введите имя файла: ')
                ftp.storbinary ('APPE ' + filename, fin, 1024)
                fin.close()
            except:
                print('У вас нет прав на эту команду')  

        if key=='r':  
            try:
                path = input('Введите название каталога: ')
                ftp.rmd(path)
            except:
                print('У вас нет прав на эту команду')  

        if key=='n':  
            try:
                name = input('Введите старое имя файла: ')
                rename = input('Введите новое имя файла: ')
                ftp.sendcmd('RNFR ' + name)
                ftp.voidcmd('RNTO ' + rename)
            except:
                print('У вас нет прав на эту команду')        

    with keyboard.Listener(on_release = on_key_release) as listener:
        listener.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-l','--login', help='Username for connection to server')
    parser.add_argument('-p','--password', help='Passowrd for connection to server')
    args = parser.parse_args()
    main(args.login, args.password)