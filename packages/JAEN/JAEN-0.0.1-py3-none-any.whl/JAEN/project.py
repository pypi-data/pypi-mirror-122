import json
import datetime
import requests

class Project:
    def __init__(self, project_name, edu_name, class_info, email):
        self.project_name = project_name
        self.edu_name = edu_name
        self.edu_rnd, self.edu_class = class_info.split()
        self.email = email

    def __make_submission(self, submission):
        timestring = datetime.datetime.now().strftime('%H-%M-%S')
        filename = 'submission-{}.csv'.format(timestring)
        submission.to_csv(filename, index=False)
        print('파일을 저장하였습니다. 파일명: {}'.format(filename))
        return filename

    def __project_submission(self, file_name):
        file_path = './'
        url = f'http://manage.jaen.kr/api/studentProject/apiScoring?edu_name={self.edu_name}&edu_rnd={self.edu_rnd}&edu_class={self.edu_class}&mail={self.email}&project_name={self.project_name}&file_name={file_name}'

        files = {'file': (file_name, open(file_path + file_name, 'rb'), 'text/csv')}
        r = requests.post(url, files=files)
        r.encoding = 'utf-8'
        message = ''
        if 'msg' in r.text:
            data = json.loads(r.text)
            message = '제출 여부 :{}\n오늘 제출 횟수 : {}\n제출 결과:{}'.format(data['msg'], data['trial'], data['score'])
        else:
            message = r.text
        return message

    def submit(self, submission):
        filename = self.__make_submission(submission)
        print(self.__project_submission(filename))

def submit(submission_file):
    global project
    project.submit(submission_file)


