#! python

import os, sys, stat, platform, glob
import re
from datetime import datetime
import zipfile, json
import getpass
import time
import warnings

import symmetric_cipher as sc
import assymetric_cipher as ac

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# UI
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def clear() :
    """ Clear the terminal screen """
    os.system("cls") if platform.system() == "Windows" else os.system("clear")


def package_check() :
    """ Installs the required third-party packages """
    count, packs = 0, ""
    try :
        import pyminizip
    except ImportError:
        count += 1
        packs += " pyminizip "

    try :
        import pyfiglet
    except ImportError:
        count += 1
        packs += " pyfiglet "

    pip = "pip" if platform.system() == "Windows" else "pip3"
    if count > 0 :
        if input(f"{count} packages ({packs}) need to be installed. Install (y/N)?\t").lower() == "y" :
            os.system(f"{pip} install {packs.strip()}")
            count = 0
        else :
            return 0

    if count == 0 :
        return 1


def settings() :
    """ Opens/Creates the settings file and returns a dict """
    setting_file_name = "settings.json"

    # if the program is run for the first time and there is no settings file
    if not os.path.exists(setting_file_name) :
        setting_dic = {   
            "web-browser" : "msedge" if platform.system() == "Windows" else "firefox",
            "multiple_runs" : True,
            "figlet_styled_titles" : True,
            "password_protected_zip" : True,
            "zip_compression_level" : 5,
            "ignore_files_while_decryting": ["keys.txt", "obfuscate.bat", "lock_unlock_keys.obf.bat"], 
            "make_key_file_readOnly_by_owner" : True,

            "__comment1__" : "Below setting currently only works on Windows",
            "password_protect_the_key_file" : True,
            
            "__comment__" : "Below setting are only applicable if you are planning to work with a zip file",
            "keep_key_file_inside_zip" : False,
        }
        with open(setting_file_name, "w") as f :
            f.write(json.dumps(setting_dic))
        return setting_dic
    
    return json.load(open(setting_file_name))


def key_file(new_folder, msg, protected_keys=None, sett=None, os_name="Windows", arg=1) :

    # key file password protection
    if arg and ( sett["password_protect_the_key_file"] or protected_keys == "y" ) and os_name == "Windows":
        # read the content of the batch file
        with open("password_protection.txt") as f :
            string = f.read()
        # ask for a password
        if protected_keys is None :
            protected_keys = input("\nWant to password protect the keys file (y/N)?\t").lower()
        if  protected_keys == "y" :
            passwd = getpass.getpass("Enter password for keys file: ")
            string = string.replace("{password_here}", passwd)

            # create the batch file in the current folder only, then obfuscate the file and move it to the new_folder
            #bat_path = os.path.join(new_folder, "lock_unlock_keys.bat")
            with open("lock_unlock_keys.bat", "w") as f :
                f.write(string)
            os.system("obfuscate.bat lock_unlock_keys.bat")          
            # move the folder
            os.system(f"move /Y lock_unlock_keys.obf.bat {new_folder}")
            # delete the older batch file
            os.system("del lock_unlock_keys.bat")

            # create the locker folder
            locker_path = os.path.join(new_folder, "Locker")
            os.system(f"mkdir {locker_path}")

            # make the key file inside this locker folder
            keys_path = os.path.join(locker_path, "keys.txt")
            with open(keys_path, "w") as f :
                f.write(msg)
            
            if sett["make_key_file_readOnly_by_owner"] :
                os.chmod(keys_path, stat.S_IREAD)  # make it read-only
            
            # now lock the folder
            # first change the current directory
            os.chdir(new_folder)
            # lock the folder
            os.system('ren Locker "Control Panel.{21EC2020-3AEA-1069-A2DD-08002B30309D}"')
            os.system('attrib +h +s "Control Panel.{21EC2020-3AEA-1069-A2DD-08002B30309D}"')

            # make the file readOnly by owner
            print("Keys file protected in the Locker folder. Access it by running 'lock_unlock_keys.obf.bat' file and entering the password provided")

        else :
            keys_path = os.path.join(new_folder, "keys.txt")
            with open(keys_path, "w") as f :
                f.write(msg)
            if sett["make_key_file_readOnly_by_owner"] :
                os.chmod(keys_path, stat.S_IREAD)

    else :
        keys_path = os.path.join(new_folder, "keys.txt")
        with open(keys_path, "w") as f :
            f.write(msg)
        if sett["make_key_file_readOnly_by_owner"] :
            os.chmod(keys_path, stat.S_IREAD)


def process(sett, choose, algo, Files, key=None, ask=None, protected_keys=None):
    os_name = platform.system()

    verb = "encrypted" if choose == "e" else "decrypted"   # for displaying message

    # make a new folder with the name encryption/decryption
    dateTime = datetime.now()
    # start time and date for file name
    Date, start_time = dateTime.strftime("%d%b%Y"), dateTime.strftime("%H_%M_%S")
    # folder name
    new_folder_basename = ("encryption_" if choose == "e" else "decryption_") + Date + "@" + start_time 
    new_folder = os.path.join(os.path.dirname(Files[0]), new_folder_basename)
    os.system(f"mkdir {new_folder}")
 
    title = pyfiglet.figlet_format("KEYS", font = "slant", justify="center") if sett["figlet_styled_titles"] else "KEYS"
    # message to be written in the keys file
    msg = "-"*100 + "\n" + title + "\n" + "-"*100
    msg += f"\n\nFiles {verb}:\n"


    # read strings and write names of new files to be made
    string, new_names, basenames, files = [], [], [], []

    # check for any wildcard entry
    extras = []
    for file in Files :
        if "*" in file :   # this means it has a wildcard character
            extras += list(glob.glob(file))   # get all the files corresponding to that wildcard
            Files.remove(file)    # remove that wildcard file name from the list
    Files += extras

    for file in Files :
        # ignore the keys file while decrypting
        if os.path.basename(file) in sett["ignore_files_while_decryting"]:
            continue

        # if it is a zip file
        if re.findall(r"\.zip", file) :
            # extract all files
            
            # get all filenames and extract everything
            dst = os.path.dirname(file)
            with zipfile.ZipFile(file) as zip :
                # skip any key file if there
                inside_files = [ os.path.join(dst, i.filename) for i in zip.filelist if i.filename not in sett["ignore_files_while_decryting"]]
                files += inside_files  # add file paths to the list
                
                if zip.infolist()[0].flag_bits :
                    uncompress_passwd = getpass.getpass(f"Enter password for file '{os.path.basename(file)}': ")
                else :
                    uncompress_passwd = None
                # extract the files for reading
                zip.extractall(path=dst, pwd=bytes(uncompress_passwd, "utf-8")) 

        # if it is a folder
        elif os.path.isdir(file) :
            inside_files = []
            # this will work even if the directory is nested
            for i, _, k in os.walk(file) :
                # skip any keys file if there
                inside_files += [os.path.join(i, j) for j in k if j not in sett["ignore_files_while_decryting"]]
            files += inside_files

        else :
            inside_files = [file]

        # now reading all the files one by one
        for i in inside_files :
            # if AES decryption, file will be binary 
            if algo in ["a1","a2"] and choose == "d" :
                with open(i, "rb") as f :
                    string.append(f.read())
            # for everyone else, file will be normal text file
            else :
                with open(i, encoding="utf-8") as f :
                    string.append(f.read())
            msg += i + "\n"  # adding file name to the message

            # name formation
            base = os.path.basename(i)
            basenames.append(base)
            base = re.sub(r"(.*)\.(.*)", f"\\1_{verb}.\\2", base)  # new name of files
            new_names.append(os.path.join(new_folder, base))   # making the absolute filepath

    
    algo_dict = {"c" : "Caesar", "v" : "Vernam", "h" : "Hill cipher", "kt" : "Keyless Transposition", "ct" : "Column Transposition", "a1" : "AES (Your own key)", 
    "a2" : "AES (random key)", "r1" : "RSA (Your own public key)", "r2" : "RSA (new key pairs)"}
    if  choose == "e" :
        msg += "\n\nEncryption: " 
    else :
        msg += "\n\nDecryption: " 
    msg += algo_dict[algo]

    # key management
    if algo == "c" :
        step = int(input("Step: ")) if key is None else int(key)
        msg += f"\nStep: {step}\n"

    elif (algo in ["v", "h", "ct", "a1"]) or (algo == "a2" and choose=="d"):
        key = input("Enter key: ") if key is None else key
        msg += f"\nKey: {key}\n"

    elif algo == "a2" and choose == "e" :
        key = sc.make_key_AES() if key is None else key
        msg += f"\nKey: {key}\n"

    elif algo == "r1" and choose == "e":
        public_key = input("Enter Public key (Format: e, n): ") if key is None else key
        msg += f"\nPublic key: ({public_key})\n"
        public_key = [int(i) for i in public_key.split(",")]

    elif algo in ["r1", "r2"] and choose == "d" :
        private_key = input("Enter Private key (Format: e, n): ") if key is None else key
        msg += f"\nPrivate key: ({private_key})\n"
        private_key = [int(i) for i in private_key.split(",")]

    elif algo == "r2" and choose == "e" :
        # generating a global public and private key
        public_key, private_key = ac.generate_keys()
        msg += f"\nPublic key: {public_key}\nPrivate key: {private_key}\n"

    print("\nSTART" + "-"*50)
    for idx, text in enumerate(string) :
        printing_msg = f"{basenames[idx]} {verb}."
        if algo == "c" :
            s = sc.caesar(text, step=step) if choose == "e" else sc.caesar(text, step=step, encrypt=False)
        
        elif algo == "v" :
            s = sc.vernam(text, key=key) if choose == "e" else sc.vernam(text, key=key, encrypt=False)

        elif algo == "h" :
            s = sc.hill_cipher(text, key=key) if choose == "e" else sc.hill_cipher(text, key=key, decrypt=True)

        elif algo == "kt" :
            s = sc.transposition(text) if choose == "e" else sc.transposition(text, encrypt=False)

        elif algo == "ct" :
            s = sc.transposition(text, key=key) if choose == "e" else sc.transposition(text, key=key, encrypt=False)

        elif algo in ["a1", "a2"] :
            if choose == "e" :
                temp, dic = sc.aes(text, key=key) 
                s = dic["nonce"] + b"," + dic["tag"] + b"," + temp   # combining all the info in the encrypted text so it becomes easy to access it while decryption
            else :
                lst = text.split(b",") 
                dic = sc.aes(lst[2], key=key, nonce=lst[0], tag=lst[1], encrypt=False)
                s = dic["decipher"]
                if not dic["authentic"]:
                    printing_msg = f'{basenames[idx]} : {dic["decipher"]}'

        elif algo == "r1" :
            s = ac.RSA(text, public_key=public_key)["cipher"] if choose == "e" else ac.RSA(text, private_key=private_key, decrypt=True)["decipher"]

        else :
            s = ac.RSA(text, public_key=public_key, private_key=private_key)["cipher"] if choose == "e" else ac.RSA(text, private_key=private_key, decrypt=True)["decipher"]

        # AES encrypted file is binary
        if algo in ["a1", "a2"] and choose == "e" :
            with open(new_names[idx], "wb") as f :
                f.write(s)
        else :
            with open(new_names[idx], "w", encoding="utf-8") as f :
                    f.write(s)

        print(printing_msg)

    print("END"+"-"*50)
    print(f"\nAll files {verb} :)")

    # create password protected zip
    if ask is None and sett["password_protected_zip"]:
        ask = input("\nWant to create a password protected zip file (y/N)?\t").lower()

    if ask == "y" :
        passwd = getpass.getpass("Enter password for zip: ")

        if sett["keep_key_file_inside_zip"] :
            msg += f"\nEncrypted zipped folder path: {new_folder}.zip"
            key_file(new_folder, msg, protected_keys=protected_keys, sett=sett, arg=0)

        zipped_files = [os.path.join(new_folder, i) for i in files]
        pyminizip.compress_multiple(new_names, [], new_folder+".zip", passwd, sett["zip_compression_level"])

        print(f"\n{new_folder}.zip created. Don't forget the password. It will not be there in the key file.")

        try :
            os.system(f"rmdir /Q /S {new_folder}") if os_name == "Windows" else os.system(f"rm -rf {new_folder}")  # delete the new_folder created
        except :
            print("Can't remove the unprotected folder. Please make sure to do that manually.")

            # if this file cannot be deleted, the new file with the same name cannot be created, so the key file cannot be created.
            if not sett["keep_key_file_inside_zip"] :
                print("Key file creation failed".upper())
            return 

        if not sett["keep_key_file_inside_zip"] :
            # add the path msg
            msg += f"\nEncrypted folder path: {new_folder}\nProtected zip path: {os.path.join(new_folder, new_folder_basename)}"
    
            os.system(f"mkdir {new_folder}")  # create the folder again
            key_file(new_folder, msg, protected_keys=protected_keys, sett=sett, os_name=os_name, arg=1)

            if os_name == "Windows" :
                move_cmd, prompt = "move", "/Y"  # prompt is for force moving the files 
            else :
                move_cmd, prompt = "mv", ""  

            os.system(f"{move_cmd} {prompt} {new_folder}.zip {new_folder}")
        
    else:
        msg += f"\nEncrypted folder path: {new_folder}"
        # writing the keys file
        key_file(new_folder, msg, protected_keys=protected_keys, sett=sett, os_name=os_name, arg=1)


def CLT(sett, args) :
    choose = args[0]
    algo = args[1]

    steps, key = 0, None
    if (algo != "kt") and not (algo in ["r2","a2"] and choose != "e") :
        key = args[2]
        steps += 1
        
    if "pz" in args :
        ask = "y"
        steps += 1
    else :
        ask = "n"

    if "pk" in args :
        protected_keys = "y"
        steps += 1
    else :
        protected_keys = "n"

    Files = args[1+1+steps:]

    process(sett, choose, algo, Files, key, ask, protected_keys)


def CLI(sett) :
    clear()

    # if the titles need to be figlets or not
    width = os.get_terminal_size().columns
    title = pyfiglet.figlet_format("CIPHER SUITE", font = "slant", justify="center") if sett["figlet_styled_titles"] else "CIPHER SUITE".center(width)
    print("-"*width + "\n" + title + "\n" + "-"*width)

    choose = input("\nEncryption(e)/Decryption(d)?\t").lower()

    # getting file names
    Files = []
    print("\nFile names: (Enter q to mark end)")
    while 1 :
        file_name = input()
        if file_name in ["q", "Q"] :
            break
        Files.append(file_name)

    # getting algorithm
    algos = ["Caesar", "Vernam", "Hill cipher", "Keyless Transposition", "Column Transposition", "AES (Your own key)", 
             "AES (random key)", "RSA (Your own public key)", "RSA (new key pairs)"]
    print("\nEncryption Algorithm?")
    for idx, algo in enumerate(algos) :
        print(f"{idx+1}. {algo}")

    inpt = int(input("\n\nYour choice:\t")) - 1
    algorithm = algos[inpt]

    print(f"You chose {algorithm}")
    algo = ["c", "v", "h", "kt", "ct", "a1", "a2", "r1", "r2"][inpt]

    process(sett, choose, algo, Files)
    

def help(sett) :
    # create an HTML file from README.md file
    help_path = os.path.join(os.getcwd(), "help.html")
    with open(os.path.join(os.path.dirname(os.getcwd()), "README.md"), "r") as f1 :
        with open(help_path, "w") as f2 :
            f2.write(f1.read())
    
    # display the HTML file in the browser
    if platform.system() == "Windows" :
        s, d = "start", "del"
    else :
        s, d = "", "rm"

    os.system(f'{s} {sett["web-browser"]} {help_path}')
    time.sleep(1)
    os.system(f'{d} {help_path}'.strip()) 



if __name__ == "__main__":   

    cli = False if len(sys.argv) > 1 else True

    if cli :
        print("\nPACKAGE CHECK\n")

    if not package_check() :  # only proceed if all packages are installed
        print("Then how can we proceed further? EXITING...")
        time.sleep(0.5)
        sys.exit(0)

    if cli :
        print("\nAll set.")
        time.sleep(0.5)

    import pyminizip 
    import pyfiglet
    
    warnings.filterwarnings("ignore", category=DeprecationWarning)  # ignore the Deprecation warning raised by pyminizip while uncompressing zip
    dic = settings()
    

    if not cli :
        if sys.argv[1].lower() == "help" :
            help(dic)
        else :
            CLT(dic, sys.argv[1:])

    else :
        while 1 :
            CLI(dic)

            # ask for once more only if multiple_run is toogled on in settings
            again = "n" if not dic["multiple_runs"] else input(f"\nWant to do more (y/N)?").lower()

            if again == "n" :
                clear()
                break