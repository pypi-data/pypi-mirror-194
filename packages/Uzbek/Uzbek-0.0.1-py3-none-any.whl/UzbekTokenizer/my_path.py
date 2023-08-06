from pathlib import Path
import os

__this_directory = Path(__file__).parent


#print(__this_directory)


def read_text_files_name_from_dir(local_folder):
    dir=__this_directory.joinpath(local_folder)
    entrs = os.listdir(dir)
    new_entrs=[]

    for i in entrs:
        if(os.path.splitext(i)[1]==".txt"):
            new_entrs.append(i);
    return new_entrs

def create_and_write_to_text_files(folder,files_name, text):
    f = open(folder+'/analysis_' + files_name, 'w', encoding='utf8')
    f.write(text)
    print("to write analysis text is succesful")


#print(read_text_files_name_from_dir("text"))