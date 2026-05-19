import customtkinter as ctk
from ollama import chat
from ollama import ChatResponse

def UserInsertText(text):
    if text != "":
        textbox.insert("end",f"you:{text}\n")

def AiInsertText(text):
    entry.delete(0,"end") #入力欄のデータ削除

    response: ChatResponse = chat(model='gemma3:270m', messages=[
        {
    'role': 'user',
    'content': text,
        },
    ])
    textbox.insert("end",f"nyx:{response.message.content}\n")

ctk.set_appearance_mode("dark") #ダークモード
app = ctk.CTk() #ウィンドウの起動
app.geometry("800x400") #ウィンドウの大きさ(横*縦)
app.title("Nyx") #タイトル

textbox = ctk.CTkTextbox(app)
textbox.pack()

entry = ctk.CTkEntry(app)
entry.pack()

button = ctk.CTkButton(
    app,
    text = "Push",
    command = lambda:(UserInsertText(entry.get()),AiInsertText(entry.get()))
    )
button.pack() #ボタンの設置

app.mainloop()