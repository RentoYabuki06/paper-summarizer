# Paper Summarizer

論文要約パイプラインツール

## 概要

Paper Summarizer は、学術論文のテキストを取得し、抽出型・生成型要約モデルを用いて TL;DR を自動生成するエンドツーエンドのパイプラインを提供します。データ取得から前処理、モデル学習・要約、評価、デプロイまで一貫して学習・実装できる構成になっています。

## 主な機能

* **データ取得**

  * arXiv API または Hugging Face Datasets (`scientific_papers`) から論文データをダウンロード
* **前処理**

  * GROBID/pdfminer による PDF→テキスト抽出
  * セクション分割、不要文字除去、トークナイザー適用
* **要約モデル**

  * 抽出型：TextRank（gensim）
  * 生成型：Hugging Face Transformers（`facebook/bart-large-cnn`, `t5-base`）の微調整
* **評価**

  * 自動評価指標：ROUGE-1/2/L、BLEU
  * 学習経過の可視化（学習曲線プロット）
* **デプロイ**

  * Streamlit または FastAPI を使った Web UI/API
  * Docker コンテナ化 & GitHub Actions による CI/CD

## テーブルオブコンテンツ

1. [インストール](#インストール)
2. [クイックスタート](#クイックスタート)
3. [データソース](#データソース)
4. [プロジェクト構成](#プロジェクト構成)
5. [パイプライン概要](#パイプライン概要)
6. [使用例](#使用例)
7. [ロードマップ](#ロードマップ)
8. [貢献](#貢献)
9. [ライセンス](#ライセンス)

---

## インストール

```bash
# リポジトリをクローン
git clone git@github.com:<ユーザー名>/paper-summarizer.git
cd paper-summarizer

# Python 仮想環境の作成・有効化
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 必要ライブラリのインストール
pip install --upgrade pip
pip install -r requirements.txt
```

## クイックスタート

1. `src/download.py` を編集し、arXiv API キーやダウンロード先を設定
2. データ取得:

   ```bash
   python src/download.py --query "deep learning" --max_results 1
   ```
3. 前処理:

   ```bash
   jupyter notebook notebooks/preprocess.ipynb
   ```
4. 要約:

   ```bash
   python src/summarize.py --model bart --input data/text/example.txt --output results/summary.txt
   ```
5. デプロイ (Streamlit UI):

   ```bash
   streamlit run src/app.py
   ```

## データソース

* **Hugging Face Datasets** の `scientific_papers` (arXiv/PubMed)
* **arXiv API** を直接利用してメタデータ & PDF を取得
* **PubMed Central Open Access** データセット (オプション)

## プロジェクト構成

```
paper-summarizer/
├── README.md        # このファイル
├── requirements.txt # 依存ライブラリ
├── data/
│   ├── raw/         # ダウンロードした PDF/JSON
│   ├── text/        # 抽出テキスト
│   └── splits/      # train/val/test 用 .jsonl
├── notebooks/       # 前処理・モデル検証用ノートブック
├── src/
│   ├── download.py  # データ取得スクリプト
│   ├── preprocess.py# テキストクリーニング関数
│   ├── summarize.py # 要約ロジック雛形
│   └── app.py       # Streamlit/FastAPI アプリ
├── results/         # 出力サマリーや評価結果
└── .github/workflows/
    └── ci-cd.yml    # GitHub Actions CI/CD 設定
```

## パイプライン概要

1. **データ取得** → arXiv/HF Datasets
2. **前処理** → PDF→テキスト抽出、クリーニング
3. **モデル学習・要約** → 抽出型／生成型モデルの実行
4. **評価** → ROUGE, BLEU スコア算出＆学習曲線可視化
5. **デプロイ** → Streamlit UI／FastAPI API

## 使用例

* **データ取得 (Hugging Face scientific\_papers):**

  ```bash
  python src/download.py --source hf --output_dir data/raw
  ```
* **データ取得 (arXiv API):**

  ```bash
  python src/download.py --source arxiv --query "covid-19" --max_results 1 --output_dir data/raw
  ```
* **要約 (コマンドライン):**

  ```bash
  python src/summarize.py --model t5 --input data/text/paper.txt --output results/summary.txt
  ```
* **Web UI へのアクセス (Streamlit):**

  ```bash
  http://localhost:8501
  ```

## ロードマップ

* [ ] GROBID 連携で節ラベル取得
* [ ] Hugging Face Hub へのモデル公開
* [ ] 多言語対応 (日本語論文要約)
* [ ] Airflow による定期実行ワークフロー

## 貢献

バグ報告や機能要望は Issue へどうぞ。Pull Request 大歓迎です。コードスタイルは `flake8` を使用。

## ライセンス

MIT License

