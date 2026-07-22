import subprocess
import shutil
import os


def run_tests(project_path:str) ->str:
    result = subprocess.run(
        ["python","-m","pytest","-v"],
       ##当前工作目录
        cwd=project_path,
        capture_output=True,
        text=True
)
    return result.stdout + result.stderr
###读取文件
def read_file(file_path:str) -> str:
    with open(file_path ,"r",encoding="utf-8")as file:
        return file.read()
###写入文件
def write_file(file_path:str,content:str) ->None:
    with open(file_path,"w",encoding="utf-8") as file:
        file.write(content)

###复制文件
def backup_file(file_path:str,backup_path:str)-> None:
     shutil.copy(file_path,backup_path)

def list_files(project_path:str) -> list[str]:
    files = []
    for file_name in os.listdir(project_path):
        files.append(file_name)

    return files