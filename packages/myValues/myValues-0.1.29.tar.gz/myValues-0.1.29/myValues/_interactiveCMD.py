import os as _os
def start():
    print('''Microsoft Windows [版本 10.0.19043.1237]
(c) Microsoft Corporation。保留所有权利。
''')
    while True:
        command=input(_os.getcwd()+'>')
        _os.system(command)