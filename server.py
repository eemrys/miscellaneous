from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

imitationDB = [
    ('admin', 'nY3j001Asq', 'elradfmw'),
    ('editor', 'qwerty9876', 'elramw'),
    ('creator', '45t67r8', 'elrmw'),
    ('nobody', '123', 'el')
]

'''
Разрешения на чтение:
«e» = изменить каталог (команды CWD, CDUP)
"l" = список файлов (команды LIST, NLST, STAT, MLSD, MLST, SIZE)
"r" = получить файл с сервера (команда RETR)

Разрешения на запись:
«a» = добавить данные в существующий файл (команда APPE)
"d" = удалить файл или каталог (команды DELE, RMD)
"f" = переименовать файл или каталог (команды RNFR, RNTO)
"m" = создать каталог (команда MKD)
"w" = сохранить файл на сервере (команды STOR, STOU)
'''

authorizer = DummyAuthorizer()
for user in imitationDB:
    authorizer.add_user(user[0], user[1], "./sticker", perm=user[2])
authorizer.add_anonymous("./sticker", perm="elr")

handler = FTPHandler
handler.authorizer = authorizer
server = FTPServer(("127.0.0.1", 8080), handler)
server.serve_forever()

