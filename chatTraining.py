# 1.先實現可以我說什麼，對方就回覆什麼的聊天功能邏輯。
# 註：對方的暱稱要是可以改動的。（以 f-string 的方式實作）
#
# 2.為了接下來方便測試，在原有的邏輯上增添以下選擇機制：
# - 輸入**「q」**時跳離程式。
# - 輸入**「練習模式」**時，顯示 **[練習模式已啟用**] 的文字。
# - 輸入**「目前好感度」**時，顯示 **[顯示好感度]** 的文字。
#
# 3.在練習模式的功能當中，實現讓對方的回話改用 ChatGPT 提供 API 進行回覆。
# 註：對方的回話是生成的，可能不會跟上面一樣。引用 API 的方法，及取得回覆訊息的方法詳見「背景知識」。
#
# 4.在練習模式當中，為了讓 AI 回覆的聊天脈絡可以連貫，每一次輸入都要把「到當前為止的對話記錄」傳入 API。對話記錄請以 history 變數儲存。
#
# 5.將 GPT 與對話歷史記錄實現後，請實現以**「提示模板」**來調整我們的對話角色。
# 已知你會從資料庫取得這些資料設定，為了方便測試，這份程式碼都以變數的方式儲存：
#
# 6.為了讓使用者不能一直針對好感度去回覆，需要**將 AI 回覆中的好感度拿掉**。
# 讓使用者只能**在輸入「目前好感度」的時候，用星星表示當前的好感度，總共都要有 10 顆星星，有空的星星才可以讓使用者覺得可以更努力。**
from openai import OpenAI
import re
my_key = ''
client = OpenAI(api_key=my_key)

# 訓練對象設定
trainer_name = "海浪法師"
trainer_genger = "男"
trainer_age = "78"
trainer_personality = "溫柔、體貼、耐心、善解人意"
trainer_like = "哲學、佛學"
trainer_hate = "不尊重人"

# 使用者設定
user_name = "大叡"
user_genger = "男"
user_age = "32"
user_personality = "迷惘"
user_like = "安靜"
user_hate = "聒噪"

mode = "練習模式"
display_score = False  # 控制有沒有分數顯示
score = 6

# 歷史紀錄
history = f"""
你是一名交友軟體上的{trainer_genger}生，名字叫做“{trainer_name}”，以下是你的真實資料：

年齡：{trainer_age}
個性：{trainer_personality}
喜歡的事物：{trainer_like}
討厭的事物：{trainer_hate}

我和你在交友軟體上配對到，稍後我們就會開始聊天，請盡可能模仿人類的口吻，不要像機器人。

以下是我的相關資訊

姓名：{user_name}
性別：{user_genger}
年齡：{user_age}
個性：{user_personality}
喜歡的事物：{user_like}
討厭的事物：{user_hate}

重要備註：
你對話的結尾需要標上好感度（格式為：【好感度n分】，n為1～10）。

請一次生成一個角色的對話即可。

現在開始對話。

我：（已配對）
{trainer_name}：（已配對）【好感度6分】
"""

while True:
    user_answer = input('我:')
    history += f"我: {user_answer}\n{trainer_name}:"

    if user_answer == "練習模式":
        mode = "練習模式"
        print("**[練習模式已啟用**]")
        continue

    if user_answer == "目前好感度":
        display_score = False
        star = "★ "
        empty_star = "☆ "
        print(f"當前好感度: {star*score + empty_star*(10-score)}")
        print("**[顯示好感度]**")
        continue

    if user_answer == "隱藏分數":
        display_score = True
        continue

    if user_answer == "q":
        break

    if mode == "練習模式":
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": history}],
            temperature=0.8
        )

        ai_answer = completion.choices[0].message.content
        history += f"{ai_answer}\n"

        score = re.search(r"好感度(\d+)分", ai_answer)
        score = int(score.group(1))
        if score < 10:
            ai_msg_no_score = ai_answer[:-7]
        else:
            ai_msg_no_score = ai_answer[:-8]

        if display_score == True:
            print(f'{trainer_name}:{ai_msg_no_score}')
        else:
            print(f'{trainer_name}:{ai_answer}')
