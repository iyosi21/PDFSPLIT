# -*- coding: UTF-8 -*-

import wx
import os
import PyPDF2
import tkinter
from tkinter import messagebox

#tkinterのrootを非表示にするおまじない
root = tkinter.Tk()
root.withdraw()

class FileDropTarget(wx.FileDropTarget):
    """ Drag & Drop Class """
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, files):
        self.window.text_entry.SetLabel(files[0])
        #トグルスイッチに値をspin_valueに代入
        spin_value =  int(self.window.spinS.GetValue())

        file_path = os.path.dirname(files[0])
        file_name = os.path.basename(files[0])
        name,ext = os.path.splitext(file_name)

        #PDFファイルかどうか判定
        if not ext == ".pdf":
            messagebox.showerror('エラー', "pdfファイルではありません")
            return 0

        #PDFファイルを格納
        source_pdf = open(file_path + "\\" + file_name, 'rb')
        source = PyPDF2.PdfFileReader(source_pdf, strict=False)

        #トグルスイッチのページ数とＰＤＦファイルのページ数を比較
        if spin_value > source.numPages:
            messagebox.showerror('エラー', "指定ページ数がPDFの総ページ数より多いです")
            #PDFのページ数よりトグルの数が多いと処理中断
            return 0

        #PDF分割処理
        for x in range(0, source.numPages, spin_value):
            #ファイル名のページ数の桁数合わせ(例：1→001)
            num_len = int(len(str(source.numPages)))
            page_str = str(x + 1)
            page_num = str(page_str.rjust(num_len, '0'))

            output = PyPDF2.PdfFileWriter()

            #トグルスイッチで指定したページずつ切り離していく
            for y in range(0,spin_value):
                #今切り離そうとしているページが最終ページ以上のページだとループ終了
                if x + y <= source.numPages -1:
                    output.addPage(source.getPage(x + y))
                else:
                    break

            #切出用のファイル(output)がオープンになっていれば切出用ファイルを保存
            if not output.getNumPages is None:
                output_pdf = open(file_path + "\\" + name + "-" + page_num + ext, 'wb')
                output.write(output_pdf)
                output_pdf.close()
            
        #オリジナルのPDFを閉じる
        source_pdf.close()

        return 0


class App(wx.Frame):
    """ GUI """
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(380, 300), style=wx.DEFAULT_FRAME_STYLE)

        # パネル
        p = wx.Panel(self, wx.ID_ANY)

        label_1 = wx.StaticText(p, wx.ID_ANY, '緑の枠にPDFファイルをドラッグしてください。\nPDFファイルを分割します', style=wx.SIMPLE_BORDER | wx.TE_CENTER)
        label_1.SetBackgroundColour("#e0ffff")

        # ドロップ対象の設定
        label_1.SetDropTarget(FileDropTarget(self))
        label_2 = wx.StaticText(p, wx.ID_ANY, '分割するページ数を選択してください（デフォルト1ページずつ）')

        # テキスト入力ウィジット
        self.text_entry = wx.TextCtrl(p, wx.ID_ANY)

        #スピン
        self.spinS = wx.SpinCtrl(p, wx.ID_ANY, value='1', min=1, size=(30, 25))
       
        # レイアウト
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(label_1, flag=wx.EXPAND | wx.ALL, border=10, proportion=1)
        layout.Add(label_2, flag=wx.EXPAND | wx.ALL)
        layout.Add(self.spinS, flag=wx.EXPAND | wx.ALL)
        layout.Add(self.text_entry, flag=wx.EXPAND | wx.ALL, border=10)
        p.SetSizer(layout)

        self.Show()



app = wx.App()
App(None, -1, 'PDF分割 ver1.10')
app.MainLoop()
