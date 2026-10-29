# text_summary

日本語のプレーンテキストから重要な文を選び、要約ファイルとして書き出すコマンドラインツールです。
<img width="1178" height="973" alt="image" src="https://github.com/user-attachments/assets/875fd223-cd9d-403d-be30-195067e9bd65" />

形態素解析と文のスコアリングによる抽出型要約を、設定ファイル・入出力ディレクトリ・実行ログと分けてあります。同じ手順で、手元の文章を繰り返し要約できます。

## できること

- UTF-8 のテキストファイルを読み、要約結果を別ファイルへ保存する
- 日本語を MeCab で分かち書きし、文ごとに重要度を計算する
- 採用した文を、原文での出現順のまま出力する
- 実行の開始と終了を、コンソールとログファイルの両方に残す

出力されるのは、原文から選んだ文です。別の表現へ言い換えた文章は作りません。

## 要約の流れ

```mermaid
flowchart LR
  input[text/input の原文] --> split[文に分割]
  split --> mecab[MeCab で形態素解析]
  mecab --> score[文ごとに採点]
  score --> pick[上位の文を採用]
  pick --> output[出現順で text/output へ保存]
```

1. `text/input/` の対象ファイルを UTF-8 で読み込みます。
2. 「。」と改行を区切りにして文へ分割します。
3. MeCab（辞書は unidic-lite）で形態素に分けます。
4. 文書全体で出現頻度の高い語を重要語とします。
5. 各文について、重要語が近くにまとまっている区間の密度をスコアにします。
6. スコア上位 10 文を残し、原文での出現順に並べます。
7. `text/output/【要約】<元のファイル名>` へ書き出します。

採点は [pysummarization](https://github.com/accel-brain/accel-brain-code/tree/master/Automatic-Summarization) の `AutoAbstractor` が行います。高頻度語を重要語とみなし、その語が密集している区間の密度で文を評価する、Luhn の抽出型要約に沿った方法です。文の採否は `TopNRankAbstractor` が担当し、既定の上位 10 文を選んだあと、文番号順に戻します。

このツールが指定しているのは、次の 2 点です。

- トークナイザは `MeCabTokenizer`
- 文の区切りは「。」と改行

採用文数や重要語の上限は、ライブラリの既定値のままです。

## 技術スタック

| 項目 | 内容 |
| --- | --- |
| 言語 | Python 3.11 |
| 要約 | pysummarization（`AutoAbstractor` / `TopNRankAbstractor`） |
| 形態素解析 | MeCab（mecab-python3 + unidic-lite） |
| 語の頻度集計 | NLTK の `FreqDist`（pysummarization が内部で使用） |
| 設定 | JSON |
| ログ | 標準ライブラリの `logging` |

## ディレクトリ構成

```
text_summary/
├── conf/
│   ├── common.json    要約するファイル名
│   └── log.json       ログ出力の設定
├── src/
│   ├── main.py        要約処理の組み立てと実行
│   └── common.py      設定の読み込み、ログの準備、テキストの入出力
├── text/              Git 管理外
│   ├── input/         原文（実行前に置く）
│   └── output/        要約結果（実行時に自動作成）
├── log/               実行時に自動作成する（Git 管理外）
├── .gitignore
└── README.md
```

`src/main.py` が要約の手順を持ち、`src/common.py` が入出力と設定を担います。原文・要約・ログはリポジトリに含めず、実行した環境だけに残します。

## 動作環境

開発時のバージョンは Python 3.11.7 です。Python 3.11 系で動作することを想定しています。MeCab の Python バインディングを導入できる Windows、macOS、Linux で使えます。

## セットアップ

以降のコマンドは、リポジトリのルートで実行します。

仮想環境を作り、依存パッケージを入れます。

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install pysummarization mecab-python3 unidic-lite nltk
```

bash の場合は、有効化だけ次のコマンドに読み替えます。

```bash
source .venv/bin/activate
```

`mecab-python3` の導入に失敗するときは、その Python 向けのビルド済みパッケージが無いことがほとんどです。Python 3.11 系の仮想環境で入れ直してください。

原文を置く `text/input/` はリポジトリに含まれていません。初回だけ作成します。`text/output/` と `log/` は実行時に自動で作られます。

```powershell
New-Item -ItemType Directory -Force -Path text/input
```

```bash
mkdir -p text/input
```

## 使い方

1. 要約したい文章を UTF-8 のテキストファイルにし、`text/input/` に置きます。
2. `conf/common.json` の `filename` を、そのファイル名に合わせます。
3. リポジトリのルートで実行します。

PowerShell:

```powershell
$env:PYTHONPATH = "src"
$env:PYTHONUTF8 = "1"
python src/main.py
```

bash:

```bash
PYTHONPATH=src PYTHONUTF8=1 python src/main.py
```

`PYTHONPATH=src` は、`src/common.py` を読み込むために必要です。入出力のパスはカレントディレクトリからの相対パスなので、コマンドはリポジトリのルートで実行します。

`PYTHONUTF8=1` は、UTF-8 で保存された `conf/common.json` を、OS の既定エンコーディングに依存せず読むための指定です。設定ファイルには日本語のファイル名を書けます。入力テキスト自体は、コード側で UTF-8 を指定して読みます。

現在の設定例は `人間失格.txt` です。本文はリポジトリに含まれないため、同じ名前の UTF-8 テキストを `text/input/` に置くか、`filename` を手持ちのファイル名へ変更してください。青空文庫などのプレーンテキストを、そのまま入力に使えます。

## 設定

### 要約対象 (`conf/common.json`)

要約するファイル名だけを持ちます。ディレクトリは書かず、`text/input/` 直下の名前を指定します。

```json
{
  "filename": "人間失格.txt"
}
```

### ログ (`conf/log.json`)

Python の `logging` 設定です。コンソールとファイルの両方へ、`INFO` 以上を出します。

起動のたびに `src/common.py` がログファイル名を `log/YYYYMMDDHHMMSS.log` へ差し替えます。この時刻は UTC です。

```
%(asctime)s %(name)s:%(lineno)s %(funcName)s [%(levelname)s]: %(message)s
```

## 出力

処理が終わると、次のファイルができます。ファイル名の例は、設定が `人間失格.txt` の場合です。

```
text/output/【要約】人間失格.txt
```

中身は、採用された文を順に書き出したものです。区切りの「。」は文に含まれたまま保存されます。

標準出力には、要約文に加えて各文の番号とスコアが入った辞書が表示されます。

- `summarize_result`: 採用された文のリスト
- `scoring_data`: 文番号とスコアの組

ログには、処理の開始と終了が残ります。

```
... __main__:35 <module> [INFO]: START
... __main__:37 <module> [INFO]: END
```

## 制約

- 出力は、原文から選んだ文だけです。文の結合や、別表現への書き換えは行いません。
- 文の境界は「。」と改行です。「！」「？」だけでは分割されません。
- 採用数はライブラリ既定の 10 文です。元の文が 10 未満のときは、ほぼ全文が残ります。
- 改行が多いテキストは、段落やセリフの単位で細かく分割されます。
- `conf/common.json` と `conf/log.json` は、オープン時にエンコーディングを指定していません。UTF-8 の設定ファイルを使うときは `PYTHONUTF8=1` を付けてください。

## 参考

- [pysummarization](https://pypi.org/project/pysummarization/)（accel-brain）
- [MeCab: Yet Another Part-of-Speech and Morphological Analyzer](https://taku910.github.io/mecab/)
