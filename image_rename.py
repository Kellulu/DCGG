import os
from zipfile import ZipFile
import shutil
from uuid import uuid1

def filter_list(dir_input):
    print('Filtering file list...')
    file_array = os.listdir(dir_input)
    os.chdir(dir_input)
    print('Imported... \n ',len(file_array), 'files')
    
    for i in file_array:       
        split_text = os.path.splitext(i)
        if split_text[1] != '.jpg':
            file_array.remove(i) 
            print(i, 'is removed from list')
    print('End of filter. \n')
    
    img_count = len(file_array)
    print('Total Image: ', img_count)    
    
    return file_array       

def unzip(usr_folder, filename):

    zip_path = usr_folder +"/"+ filename
    zip_folder = usr_folder +"/"+ filename[0:len(filename)-4]

    if os.path.exists(zip_folder) != True:
        os.makedirs(zip_folder)

    with ZipFile(zip_path, 'r') as zipObj:
        zipObj.extractall(zip_folder)
    
    #zip_folder = zip_folder +"/dataset"
    usr_dataset = [[],""]
    usr_dataset[0].append(filename)
    usr_dataset[0].append(filename[20:])
    #usr_dataset[1] = os.listdir(path=zip_folder)

    print('Filtering file list...')
    file_array = os.listdir(path=zip_folder)
    print('Imported... : ',len(file_array), 'files')

    for i in file_array:       
        split_text = os.path.splitext(i)
        
        if split_text[1] != '.jpg':
            file_array.remove(i) 
            print(i, 'is removed from list')

    print(file_array)
    usr_dataset[1] = file_array
    print('End of filter. \n')

    return usr_dataset

def rename(x, y, bot_type, filename_old, path):
    current_path = 'static/' + path
    x = int(x)
    y = int(y)

    if bot_type == "JetBot":
        filename_new = 'xy_%03d_%03d_%s' % (x, y, uuid1())
        filename_new = filename_new + '.jpg'

    elif bot_type == "JetRacer":
        filename_new = '%d_%d_%s' % (x, y, uuid1())
        filename_new = filename_new + '.jpg'

    filename_new_path = current_path + filename_new

    current_file_path = 'static/' + path + filename_old
    os.rename(current_file_path, filename_new_path)

    print("Old file name :", filename_old)
    print("New file name :", filename_new)

    print('completed')
    return filename_new

def zip(outputname, dir_name):
    shutil.make_archive(outputname, 'zip', dir_name)