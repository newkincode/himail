from fastapi import FastAPI
import smtplib  # SMTP 사용을 위한 모듈
import re  # Regular Expression을 활용하기 위한 모듈
from email.mime.multipart import MIMEMultipart  # 메일의 Data 영역의 메시지를 만드는 모듈
from email.mime.text import MIMEText  # 메일의 본문 내용을 만드는 모듈
from email.mime.image import MIMEImage

app = FastAPI()

@app.get("/sandmain/")
def sandmail(content: str, title: str, password: str, mailAddress: str, destination: str):
    # smpt 서버와 연결
    gmail_smtp = "smtp.gmail.com"  # gmail smtp 주소
    gmail_port = 465  # gmail smtp 포트번호. 고정(변경 불가)
    smtp = smtplib.SMTP_SSL(gmail_smtp, gmail_port)
    
    # 로그인
    my_account = mailAddress
    my_password = password
    smtp.login(my_account, my_password)

    # 메일을 받을 계정
    to_mail = destination

    # 메일 기본 정보 설정
    msg = MIMEMultipart()
    msg["Subject"] = title
    msg["From"] = my_account
    msg["To"] = to_mail

    # 메일 본문 내용
    content_part = MIMEText(content, "plain")
    msg.attach(content_part)
    # 받는 메일 유효성 검사 거친 후 메일 전송
    reg = "^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$"  # 유효성 검사를 위한 정규표현식
    if re.match(reg, to_mail):
        smtp.sendmail(my_account, to_mail, msg.as_string())
        smtp.quit()
        return "정상적으로 메일이 발송되었습니다."
    else:
        smtp.quit()
        return "받으실 메일 주소를 정확히 입력하십시오."
   