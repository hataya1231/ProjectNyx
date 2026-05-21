import customtkinter as ctk
from ollama import chat
from ollama import ChatResponse
from PIL import Image

def UserInsertText(text):
    if text != "":
        textbox.insert("end",f"you:{text}\n")
        textbox.see("end")
        textbox.update()

def AiInsertText(text):
    entry.delete(0,"end") #入力欄のデータ削除

    stream = chat(
        model='gemma3:1b',
        messages=[{'role': 'user', 'content': f"あなたはキリスト教祖です。カッコの中の文章に対して相応の返事をしてください。「{text}」また必ず語り口調で答えてください"}],
        stream=True,
    )

    textbox.insert("end","jesus:")

    for chunk in stream:
        content =chunk['message']['content']
        textbox.insert("end",content)
        textbox.see("end")
        textbox.update()
    textbox.insert("end","\n")

ctk.set_appearance_mode("dark") #ダークモード
app = ctk.CTk() #ウィンドウの起動
app.geometry("800x400") #ウィンドウの大きさ(横*縦)
app.title("Nyx") #タイトル
app.grid_columnconfigure(0,weight=1) #0列目の列の長さをウィンドウに合わせて伸ばす
app.grid_rowconfigure(1,weight=1) #1行目の行の長さをウィンドウに合わせて伸ばす

#画像出力
image = Image.open("./images/jesus.png")
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

entry.bind("<Return>",lambda:(UserInsertText(entry.get(),AiInsertText(entry.get())))) #ENTERキー実行

#ボタン
button = ctk.CTkButton(
    app,
    text = "Push",
    command = lambda:(UserInsertText(entry.get()),AiInsertText(entry.get()))
    )
button.grid(row = 2,column = 1) #ボタンの設置

app.mainloop()