import pyopenjtalk
from collections import Counter
import csv

def file_to_phonemes(file_path):
    # ファイルからテキストを読み込み、音素記号に変換
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    phonemes = pyopenjtalk.g2p(text, kana=False)  # 音素記号を返す
    return phonemes

def count_cv_combinations(phonemes):
    # CV連鎖の頻度を数える
    cv_combinations = Counter()
    vowels = set('aiueoAIUEO')  # 大文字母音も含める
    consonant = None

    for phoneme in phonemes.split():
        if phoneme == 'pau':  # 休止記号は無視する
            continue
        phoneme = phoneme.lower()  # 大文字母音を小文字に変換
        if phoneme in vowels:
            if consonant is not None:
                cv_combination = consonant + phoneme
                cv_combinations[cv_combination] += 1
            # 母音の後は次の子音を待つため、consonantをリセットする
            consonant = None
        else:
            consonant = phoneme

    return cv_combinations

def save_to_csv(cv_combinations, output_file):
    # CSVファイルに結果を保存
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['CV', 'Frequency'])
        for cv, freq in cv_combinations.items():
            csvwriter.writerow([cv, freq])

