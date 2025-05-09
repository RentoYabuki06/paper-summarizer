# src/preprocess.py

import os
import re
import argparse
from pdfminer.high_level import extract_text

# --- 1. テキスト抽出 ---
def extract_text_from_pdf(pdf_path: str) -> str:
    """
    pdfminer を使って PDF から全テキストを抽出する。
    """
    text = extract_text(pdf_path)
    return text

# --- 2. 不要文字・改行の正規化 ---
def clean_text(raw_text: str) -> str:
    """
    ・複数改行を1つにまとめる
    ・脚注番号や [] 内の参照番号を削除
    ・全角スペース・タブを半角スペースに統一
    """
    t = raw_text
    t = re.sub(r'\[\d+\]', '', t)                    # 参考文献番号除去
    t = re.sub(r'\s+', ' ', t)                       # 連続スペース/改行を1つの半角スペースに
    t = t.replace('\u3000', ' ')                     # 全角スペース→半角
    return t.strip()

# --- 3. セクション分割（例：“Introduction”, “Methods”…） ---
def split_sections(cleaned_text: str) -> dict:
    """
    セクションヘッダ（大文字で始まる単語+改行）をキーに全文を分割する。
    """
    sections = {}
    # ヘッダ行のパターン例
    pattern = re.compile(r'([A-Z][A-Za-z ]+)\s*?')
    parts = pattern.split(cleaned_text)
    # split の結果は、['','Section1','内容','Section2','内容',...]
    for i in range(1, len(parts), 2):
        header = parts[i].strip()
        body   = parts[i+1].strip()
        sections[header] = body
    return sections

# --- 4. メイン関数 & CLI対応 ---
def main():
    p = argparse.ArgumentParser()
    p.add_argument('--pdf',      required=True, help='入力 PDF ファイルパス')
    p.add_argument('--out_text', required=True, help='出力プレーンテキスト保存先 (.txt)')
    p.add_argument('--out_json', required=False, help='セクション分割結果保存先 (.json)')
    args = p.parse_args()

    # (1) PDF → 生テキスト
    raw = extract_text_from_pdf(args.pdf)

    # (2) クリーニング
    cleaned = clean_text(raw)

    # (3) 全文テキストを書き出し
    os.makedirs(os.path.dirname(args.out_text), exist_ok=True)
    with open(args.out_text, 'w', encoding='utf-8') as f:
        f.write(cleaned)
    print(f'Cleaned text saved to {args.out_text}')

    # (4) セクション分割＆JSON出力（オプション）
    if args.out_json:
        import json
        sections = split_sections(cleaned)
        with open(args.out_json, 'w', encoding='utf-8') as f:
            json.dump(sections, f, ensure_ascii=False, indent=2)
        print(f'Sections saved to {args.out_json}')

if __name__ == '__main__':
    main()
