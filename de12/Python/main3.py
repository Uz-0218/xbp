import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import schedule

            
            # メール通知の設定
            SMTP_SERVER = 'smtp.gmail.com'
            SMTP_PORT = 587
            EMAIL_ADDRESS = 'sys.klavier1024@gmail.com' 
            EMAIL_PASSWORD = 'uspc uqhp qldu yzvs'  # アプリパスワード
            
            TO_EMAIL = 'sys.klavier1024@gmail.com'
            
            # 監視対象URL
            TARGET_URL = 'https://online-shop.mb.softbank.jp/sbols/ModelPlanSelectPage'
            
            # 前回の在庫状況を記録
            previous_stock = {}
            
            # 在庫情報を取得する関数
            def check_stock():
                global previous_stock
                response = requests.get(TARGET_URL)
                soup = BeautifulSoup(response.text, 'html.parser')
            
                # 在庫情報を取得
                items = soup.find_all('div', class_='button-size')
                current_stock = {}
                for item in items:
                    name = item.find('span', class_='name').find_all('span')[0].text  # 商品名
                    status = item.find('span', class_='name').find_all('span')[1].text  # 在庫状況
                    current_stock[name] = status
            
                # 在庫の変化を検出
                changes = []
                for name, status in current_stock.items():
                    if name in previous_stock and previous_stock[name] != status:
                        if status == "在庫あり":  # 在庫が追加された場合のみ通知
                            changes.append(name)
            
                # 在庫の変化をメールで通知
                if changes:
                    send_email_notification(changes)
            
                # 現在の在庫状況を保存
                previous_stock = current_stock
            
            # メール通知を送信する関数
            def send_email_notification(changes):
                subject = "在庫通知: 新しい在庫が追加されました"
                body = f"以下の商品に在庫が追加されました:\n\n" + "\n".join(changes)
            
                # メールの内容を構築
                message = MIMEMultipart()
                message['From'] = EMAIL_ADDRESS
                message['To'] = TO_EMAIL
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))
            
                # メールを送信
                with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                    server.starttls()
                    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                    server.send_message(message)
            
                print(f"通知を送信しました: {changes}")
            
            # 定期的に在庫をチェック
            schedule.every(10).minutes.do(check_stock)  # 10分ごとに実行
            
            # プログラムを実行
            print("在庫監視を開始します...")
            while True:
                schedule.run_pending()
                time.sleep(1)