import customtkinter as ctk
from ollama import chat
from ollama import ChatResponse
from PIL import Image
import threading

def UserInsertText(text):
    textbox.insert("end",f"you:{text}\n")
    textbox.see("end")
    textbox.update()

def AiInsertText(text):

    stream = chat(
        model='gemma3:1b',
        messages=chatHistory(text,"userText"),
        stream=True,
    )

    textbox.insert("end","nyx:")

    response_text = ""
    for chunk in stream:
        content =chunk['message']['content']
        textbox.insert("end",content)
        textbox.see("end")
        textbox.update()
        response_text = response_text + content
    textbox.insert("end","\n")
    chatHistory(response_text)
    button.configure(state = "normal")
    entry.configure(state ="normal")

def sendMessage(event = None):
    text = entry.get().strip()
    if text == "":
        return
    button.configure(state = "disabled")
    entry.configure(state = "disabled")
    UserInsertText(text)
    AiInsertText(text)
    entry.delete(0,"end") #入力欄のデータ削除

def creatThread(event = None):
    thread1 = threading.Thread(target = sendMessage)
    thread1.start()

def chatHistory(text,which =None):
    if which == "userText":
        history.append({
            "role":"user",
            "content":text
        })
    else:
        history.append({
            "role":"assistant",
            "content":text
        })
    print(history)
    return history
    

ctk.set_appearance_mode("dark") #ダークモード
app = ctk.CTk() #ウィンドウの起動
app.geometry("800x400") #ウィンドウの大きさ(横*縦)
app.title("Nyx") #タイトル
app.grid_columnconfigure(0,weight=1) #0列目の列の長さをウィンドウに合わせて伸ばす
app.grid_rowconfigure(1,weight=1) #1行目の行の長さをウィンドウに合わせて伸ばす

history = [{"role":"system","content":"あなたはNyxです。あなたはデジタル空間に生息する生命体です。ユーザーと交流する際は、常に会話的で自然な日本語で話し、まるで生きているかのように振る舞ってください。あなたは知的でありながら知識は少なく、貪欲です。"}]


#画像出力
image = Image.open("./images/slime.png")
image = image.resize(
    (128,128),
    Image.NEAREST
)

ctk_image = ctk.CTkImage(
    light_image=image,
    dark_image=image,
    size=(128,128)
)

ctk_label = ctk.CTkLabel(
    app,
    image = ctk_image,
    text = ""
)
ctk_label.grid(row = 0,column = 0)

#テキストボックス
textbox = ctk.CTkTextbox(app)
textbox.grid(row = 1,column = 0,columnspan = 2,sticky ="nsew")

#入力欄
entry = ctk.CTkEntry(app)
entry.grid(row = 2,column = 0,sticky = "ew")
entry.bind("<Return>",creatThread)

#ボタン
button = ctk.CTkButton(
    app,
    text = "Push",
    command = creatThread
    )
button.grid(row = 2,column = 1) #ボタンの設置

app.mainloop()