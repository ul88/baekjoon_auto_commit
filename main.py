import requests
from bs4 import BeautifulSoup
import os
import fnmatch
import shutil
import subprocess

PS_REPO_PATH = "C:\\Users\\hkimo\\OneDrive\\Desktop\\coding\\C++\\PS\\boj"
GIT_REPO_PATH = "C:\\Users\\hkimo\\github_repo\\problem-solving"

url = 'https://solved.ac/search?query='

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
    response = requests.get(url + number)  # GET 메소드를 사용하여 url에 HTTP Request 전송
    if response.status_code == 200:  # 정상 응답 반환 시 아래 코드블록 실행
        soup = BeautifulSoup(response.content, 'html.parser')  # 응답 받은 HTML 파싱
        a_tag = soup.find('a', class_='css-q9j30p', href="https://www.acmicpc.net/problem/" + number)

        if a_tag:
            images = soup.find_all('img', class_="css-1vnxcg0")
            return images[0].get('alt')
        else:
            print("not found")
    else:
        print('error')  # 오류 시 메시지 출력
    return "ERROR"

def upload():
    flag = False
    cnt = 0

    for file in os.listdir(PS_REPO_PATH) :
        # 해당 파일이 엑셀 파일이면 수행할 작업
        if fnmatch.fnmatch(file, '*.cpp') or fnmatch.fnmatch(file, '*.c'):
            problem_number = file.split()[0]

            level = check_level(problem_number)
            if level == "ERROR":
                print("문제 번호가 잘못되었습니다.")
                continue
            
            now_path = GIT_REPO_PATH + "\\" + level
            if not os.path.exists(now_path):
                os.makedirs(now_path)
            
            if file in os.listdir(now_path):
                print("존재합니다")
            else:
                flag = True
                cnt += 1
                file_from = PS_REPO_PATH + "\\" + file
                file_to = now_path + "\\" + file
                shutil.copy(file_from, file_to)
    if flag == True:
        git_commit_push("add problem "+str(cnt)+"개")
    else:
        print("커밋 & 푸시를 진행하지 않습니다.")

upload()
    
        