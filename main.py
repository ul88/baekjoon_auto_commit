import requests
from bs4 import BeautifulSoup
import os
import fnmatch
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor

PS_REPO_PATH = "[저장할 데이터 디렉토리]"
GIT_REPO_PATH = "[저장소 디렉토리]"

url = 'https://solved.ac/api/v3/problem/show?problemId='

dict_level = {0: "Unrated", 1: "Bronze V", 2: "Bronze IV", 3: "Bronze III", 4: "Bronze II", 5: "Bronze I",
                6: "Silver V", 7: "Silver IV", 8: "Silver III", 9: "Silver II", 10: "Silver I",
                11: "Gold V", 12: "Gold IV", 13: "Gold III", 14: "Gold II", 15: "Gold I",
                16: "Platinum V", 17: "Platinum IV", 18: "Platinum III", 19: "Platinum II", 20: "Platinum I",
                21: "Diamond V", 22: "Diamond IV", 23: "Diamond III", 24: "Diamond II", 25: "Diamond I",
                26: "Ruby V", 27: "Ruby IV", 28: "Ruby III", 29: "Ruby II", 30: "Ruby I"}

def git_pull(remote='origin', branch='main'):
    try:
        # Git pull
        subprocess.run(['git', 'pull', remote, branch], check=True)
        print("원격 저장소에서 변경 사항을 가져왔습니다.")
    except subprocess.CalledProcessError as e:
        print(f"오류 발생: {e}")

def git_commit_push(commit_message):
    os.chdir(GIT_REPO_PATH)

    git_pull()

    try:
        # Git add
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Git commit
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Git push
        subprocess.run(['git', 'push'], check=True)
        
        print("커밋 및 푸시가 완료되었습니다.")
    except subprocess.CalledProcessError as e:
        print(f"오류 발생: {e}")

def check_level(number):
    response = requests.get(url + number)
    if response.status_code == 200:  # 정상 응답 반환 시 아래 코드블록 실행
        return dict_level[response.json().get("level")]
    else:
        print(f"error: {response.status_code}")
    return "ERROR"

def upload(file):    
    problem_number = file.split()[0]

    level = check_level(problem_number)
            
    now_path = GIT_REPO_PATH + "\\" + level
    if not os.path.exists(now_path):
        os.makedirs(now_path)
            
    file_from = PS_REPO_PATH + "\\" + file
    file_to = now_path + "\\" + file
    shutil.copy(file_from, file_to)
    
def upload_all():
    flag = True

    files = [file for file in os.listdir(PS_REPO_PATH) if fnmatch.fnmatch(file, '*.cpp') or fnmatch.fnmatch(file, '*.c')]

    with ThreadPoolExecutor(max_workers=os.cpu_count())  as executor:
        executor.map(upload, files)
        
    if flag == True:
        git_commit_push("add problem")
    else:
        print("커밋 & 푸시를 진행하지 않습니다.")

upload_all()
