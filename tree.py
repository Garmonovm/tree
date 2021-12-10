import os
import shutil
import time
from pathlib import Path
import datetime
import send2trash
import logging


time_now = datetime.datetime.now().strftime('%Y-%m-%d %H-%M')

now = time.time()
"""C:\temp\os_script"""
path_to_logs = r'C:\temp\logs'
logging.basicConfig(filename=r'C:\temp\logs\app'+time_now+'.log', filemode='a', format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S')
##archiving and deleting logs###
for file in Path(path_to_logs).glob("**/*"):
    if os.stat(file).st_mtime < now - 7 * 86400:
        if os.path.isfile(file):
            shutil.make_archive(file,'zip',path_to_logs)
            send2trash.send2trash(file)
    if os.stat(file).st_mtime < now - 30 * 86400:
        send2trash.send2trash(file)

path_to_dir = r'C:\temp\os_script'
deleted_folder = r'C:\temp\deleted_folder'

logging.warning(f'Path to deleted directory is {deleted_folder}')

p = input('Please input the path to working dirrectory\nOr put any key to choose default path to Downloads folder\n')
if os.path.isdir(p):      ### cделать проверку на директорию
  path_to_dir = p
else:
  # path_to_dir = os.getenv("TEMP")
  path_to_dir = r'C:\Users\garmonovm\Downloads'


logging.warning(f'Path to working directory is {path_to_dir}')
print(f' path to working directory is {path_to_dir}')

## Detail view without size and time
# for root, directories, files in os.walk(path_to_dir):
#     print(root)
#     for directory in directories:
#         print(directory)
#     for file in files:
#         print(file)


## To see all catalogs and files with size and datetime


for file in Path(path_to_dir).glob("**/*"):
    file_size = file.stat().st_size // 1024
    ctime = datetime.datetime.fromtimestamp(file.stat().st_ctime).strftime(
        '%Y-%m-%d')  # created time # converted to human readable format .strftime('%Y-%m-%d %H:%M')
    print(file, f'{file_size}kb', ctime)
exit()
while True:
    try:
        choice = int(input(
            "Please choose the method how to move data to folder or default values will be chosen \n 0 - Based on "
            "maximum size \n 1 - Based on created date \n"))
        if choice == 0 or choice == 1:
            logging.warning(f'Method choice has been done for {choice}')
            break
    except Exception as e:
        print(e)
        logging.exception("Exception occurred")

if choice == 0:
    try:
        new_size = int(input(
            "Please specify the maximum size in kb of the file which will be left in folder,\n Files with greater "
            "size will be moved to deleted folder\n Example : 150\n Or press any key and default size 900kb will be "
            "chosen\n"))
        if isinstance(new_size, int):
            new_size = new_size
            logging.warning(f'You have choose method to delete the file larger than size {new_size} kb')
    except Exception as e:
        e = 'Default size has been chosen and = 900 KB'
        new_size = 900
        print(e)
        logging.exception("Exception occurred")
        logging.warning(f'Default size has been set {new_size}kb')
    try:
        if not all([file.stat().st_size // 1024 > new_size for file in Path(path_to_dir).glob("**/*")]):
            for file in Path(path_to_dir).glob("**/*"):
                file_size = file.stat().st_size // 1024
                # ctime = datetime.datetime.fromtimestamp(file.stat().st_ctime)

                if file_size > new_size:
                    shutil.move(file.__str__(), deleted_folder)
                    print(f'file {file} has been moved to deleted folder as its size {file_size}kb > specified {new_size}kb')
                    logging.warning(
                        f'file {file} has been moved to deleted folder as its size {file_size}kb > specified {new_size}kb')
        else:
            print(f'all files are lower than specified size {new_size}kb')
        logging.warning(f'all files are lower than specified size {new_size}kb')
    except Exception as e:
        print(e)
        logging.exception("Exception occurred")

else:

    try:
        new_date = input(
            "Please specify the date,after which all files will be moved to deleted_folder\nformat "
            "YYYY-MM-DD\nexample 2021-12-01\nor press any key to choose default settings\n")
        year, month, day = new_date.split('-')
        # print(year,month,day)
        if datetime.datetime(int(year), int(month), int(day)):
            new_date = new_date
            logging.warning(f'You have choose the method to delete the file greater than date {new_date}')
            print(f'date is chosen {new_date} all files larger that date will be moved/deleted to deleted_folder')
    except Exception as e:
        new_date = '2021-12-01'
        print(f'Incorrect date format or default settings choosed, default settings will be in use and is {new_date}')
        logging.exception(f'Incorrect date format or default settings choosed, default settings is {new_date}')

    new_datetime = new_date.replace('-', ',')
    # print(new_datetime)

    try:
        if not all([datetime.datetime.fromtimestamp(file.stat().st_ctime).strftime('%Y,%m,%d') > new_datetime for file in Path(path_to_dir).glob("**/*")]):
            for file in Path(path_to_dir).glob("**/*"):
                ctime = datetime.datetime.fromtimestamp(file.stat().st_ctime).strftime('%Y-%m-%d')
                createtime = datetime.datetime.fromtimestamp(file.stat().st_ctime).strftime('%Y,%m,%d')
                if createtime > new_datetime:
                    shutil.move(file.__str__(), deleted_folder)
                    print(f'{file} has been moved to folder {deleted_folder} as specified date {new_date} is earlier than file create time {ctime}')
                    logging.warning(
                        f'{file} has been moved to folder {deleted_folder} as specified date {new_date} is earlier than file create time {ctime}')
        else:
            print(f'No files were moved as creation date are earlier than specified date {new_date}')
            logging.warning(f'No files were moved as creation date are earlier than specified date {new_date}')

    except Exception as e:
        print(e)
        logging.exception("Exception occurred")
