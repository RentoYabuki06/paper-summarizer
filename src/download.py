# src/download.py

import argparse
import os
from datasets import load_dataset
import arxiv  # pip install arxiv

def download_hf_scientific_papers(output_dir: str):
    """
    Hugging Face の scientific_papers データセットから 1 件だけ取得し、
    JSONL 形式で保存する。
    """
    ds = load_dataset("scientific_papers", "arxiv", split="train[:1]")
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "hf_arxiv_sample.jsonl")

    with open(out_path, "w", encoding="utf-8") as f:
        for entry in ds:
            # JSONL 形式で書き出し
            f.write(f"{entry}\n")
    print(f"Hugging Face: scientific_papers arxiv サンプルを保存 → {out_path}")

def download_arxiv(query: str, max_results: int, output_dir: str):
    """
    arXiv API でクエリ検索し、最初の max_results 件を PDF 付きでダウンロードする。
    """
    os.makedirs(output_dir, exist_ok=True)
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )

    for result in search.results():
        title = result.title.replace("/", "_")[:100]
        pdf_path = os.path.join(output_dir, f"{title}.pdf")
        print(f"Downloading: {result.entry_id} → {pdf_path}")
        result.download_pdf(filename=pdf_path)
    print(f"arXiv: {max_results} 件を {output_dir} に保存しました。")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", choices=["arxiv", "hf"], default="hf",
                   help="データ取得元: arxiv or hf(scientific_papers)")
    p.add_argument("--query", type=str, default="deep learning",
                   help="arXiv 検索クエリ (source=arxiv のとき有効)")
    p.add_argument("--max_results", type=int, default=1,
                   help="取得件数 (source=arxiv のとき有効)")
    p.add_argument("--output_dir", type=str, default="data/raw",
                   help="保存先ディレクトリ")
    args = p.parse_args()

    if args.source == "hf":
        download_hf_scientific_papers(args.output_dir)
    else:
        download_arxiv(args.query, args.max_results, args.output_dir)

if __name__ == "__main__":
    main()
