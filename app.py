import tkinter as tk
from tkinter import messagebox, filedialog
import os
import cvchain  # cvchain.pyをインポートする
import customtkinter as ctk  # customtkinterをインポートする
import markdown  # markdownをインポートする
import tkinterweb  # tkinterwebをインポートする

ctk.set_appearance_mode("System")  # ダークモードとライトモードの自動切り替え
ctk.set_default_color_theme("blue")  # デフォルトのカラーテーマを設定

class CVChainGUI:
    def __init__(self, master):
        self.master = master
        master.title('CV連鎖頻度計算ツール')
        self.corpus_dir = None  # 初期状態ではディレクトリが選択されていません

        # ディレクトリ選択エリア
        self.directory_frame = ctk.CTkFrame(master)
        self.directory_label = ctk.CTkLabel(self.directory_frame, text="ディレクトリ：")
        self.directory_label.pack(side=tk.LEFT)
        self.directory_entry = ctk.CTkEntry(self.directory_frame, width=400)
        self.directory_entry.pack(side=tk.LEFT)
        self.directory_button = ctk.CTkButton(self.directory_frame, text="選択", command=self.select_directory)
        self.directory_button.pack(side=tk.LEFT)
        self.directory_frame.pack(pady=10)

        # テキスト入力エリア
        self.text_area = ctk.CTkTextbox(master, height=150, width=700)  # 高さと幅を調整
        self.text_area.pack(pady=10)

        # ボタンエリア
        self.button_frame = ctk.CTkFrame(master)
        self.button_frame.pack(pady=5)

        # ファイル保存ボタン
        self.save_button = ctk.CTkButton(self.button_frame, text="テキストを保存", command=self.save_text)
        self.save_button.pack(side=tk.LEFT, padx=5)

        # ファイル削除ボタン
        self.delete_button = ctk.CTkButton(self.button_frame, text="テキストを削除", command=self.delete_text)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # 個別ファイルボタン
        self.file_button = ctk.CTkButton(self.button_frame, text="個別ファイルで計算", command=self.run_script_for_single_file)
        self.file_button.pack(side=tk.LEFT, padx=5)

        # スクリプト実行ボタン
        self.run_button = ctk.CTkButton(self.button_frame, text="CV連鎖頻度を計算", command=self.run_script)
        self.run_button.pack(side=tk.LEFT, padx=5)

        # 結果表示エリア（HTML形式での表示に変更）
        self.result_area = tkinterweb.HtmlFrame(master, height=150, width=700)  # 高さと幅を調整、HTML形式での表示に対応
        self.result_area.pack(pady=10)

    def select_directory(self):
        directory = filedialog.askdirectory(initialdir="./corpus/", title="ディレクトリを選択")
        if directory:
            self.corpus_dir = directory
            self.directory_entry.delete(0, tk.END)
            self.directory_entry.insert(0, directory)

    def save_text(self):
        text = self.text_area.get("1.0", tk.END)
        if not self.corpus_dir:
            messagebox.showerror("エラー", "ディレクトリが選択されていません。")
            return
        file_number = 1
        while True:
            file_path = os.path.join(self.corpus_dir, f"{os.path.basename(self.corpus_dir)}_{file_number:03}.txt")
            if not os.path.exists(file_path):
                break
            file_number += 1
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)
        messagebox.showinfo("保存成功", f"テキストが{file_path}に保存されました。")

    def delete_text(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], initialdir=self.corpus_dir)
        if file_path:
            os.remove(file_path)
            messagebox.showinfo("削除成功", "ファイルが削除されました。")

    def run_script(self):
        if not self.corpus_dir:
            messagebox.showerror("エラー", "ディレクトリが選択されていません。")
            return
        all_cv_combinations = {}
        for file_name in os.listdir(self.corpus_dir):
            if file_name.endswith('.txt'):
                file_path = os.path.join(self.corpus_dir, file_name)
                phonemes = cvchain.file_to_phonemes(file_path)
                cv_combinations = cvchain.count_cv_combinations(phonemes)
                for cv, freq in cv_combinations.items():
                    if cv in all_cv_combinations:
                        all_cv_combinations[cv] += freq
                    else:
                        all_cv_combinations[cv] = freq

                # 結果をマークダウン形式の文字列として生成
                markdown_result = self.generate_markdown_result(all_cv_combinations)

                # マークダウンをHTMLに変換して表示
                html_result = markdown.markdown(markdown_result, extensions=['tables'])
                self.result_area.load_html(html_result)
                messagebox.showinfo("計算結果", "ディレクトリ内のファイルのCV連鎖頻度の結果が表示されました。")

    def run_script_for_single_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], initialdir=self.corpus_dir)
        if file_path:
            all_cv_combinations = {}
            phonemes = cvchain.file_to_phonemes(file_path)
            cv_combinations = cvchain.count_cv_combinations(phonemes)
            for cv, freq in cv_combinations.items():
                if cv in all_cv_combinations:
                    all_cv_combinations[cv] += freq
                else:
                    all_cv_combinations[cv] = freq

            # 結果をマークダウン形式の文字列として生成
            markdown_result = self.generate_markdown_result(all_cv_combinations)

            # マークダウンをHTMLに変換して表示
            html_result = markdown.markdown(markdown_result, extensions=['tables'])
            self.result_area.load_html(html_result)
            messagebox.showinfo("計算結果", "選択されたファイルのCV連鎖頻度の結果が表示されました。")

    def generate_markdown_result(self, all_cv_combinations):
        markdown_result = "| CV | a | i | u | e | o |\n|---|---|---|---|---|---|\n"
        vowels = ['a', 'i', 'u', 'e', 'o']
        consonants = ['b', 'by', 'ch', 'd', 'dy', 'f', 'g', 'gy', 'h', 'hy', 'j', 'k', 'ky', 'm', 'my', 'n', 'ny', 'p', 'py', 'r', 'ry', 's', 'sh', 't', 'ts', 'ty', 'v', 'w', 'y', 'z']
        for consonant in consonants:
            line = f"| {consonant} "
            for vowel in vowels:
                cv = consonant + vowel
                freq = all_cv_combinations.get(cv, 0)
                line += f"| {freq} "
            markdown_result += line + "|\n"
        return markdown_result



if __name__ == "__main__":
    root = tk.Tk()
    gui = CVChainGUI(root)
    root.mainloop()
