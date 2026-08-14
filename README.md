# Amazon × X アフィリエイト自動投稿ツール

`products.csv` に登録した商品から、Amazonアフィリエイトリンク付きのツイート文を自動生成し、X(旧Twitter)に自動投稿するツールです。

## 現在の状態(重要)

- **PA-APIキー・X APIキーはまだ未取得**なので、今は次のように動きます。
  - 商品情報は `products.csv` に**手入力**する運用(PA-APIキー取得後、`src/pa_api_client.py` を使って自動取得に切り替え可能)。
  - X APIキー未設定の間は実際には投稿せず、`drafts/` フォルダにツイート文を保存する **dry-run モード** になります。中身を確認してから手動でXに投稿してください。
- どちらのキーも `.env` に追記するだけで、コード変更なしに本番運用へ移行できます。

## セットアップ

PowerShellで、`amazon_x_affiliate_bot` フォルダの中に移動してから実行してください(`src`はこのフォルダ内のパッケージなので、一つ上の階層で実行するとエラーになります)。

```powershell
cd amazon_x_affiliate_bot
pip install -r requirements.txt
copy .env.example .env
```

仮想環境(venv)は必須ではありません。使いたい場合のみ以下を`pip install`の前に実行してください。

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## 使い方(今すぐ試せる: dry-run)

1. `products.csv` に商品を追加する。
   - `affiliate_url` は、Amazonアソシエイトの管理画面 → SiteStripe(商品ページ上部に出るツールバー)から発行した短縮アフィリエイトリンクを貼り付けてください。
   - `tags` は `|` 区切りでハッシュタグ候補を入れます(例: `イヤホン|ガジェット`)。
2. 実行する。

   ```bash
   python -m src.main
   ```

3. `drafts/` フォルダに生成されたツイート文の `.txt` が保存されます。中身を確認し、問題なければ手動でXに投稿してください。
4. 投稿済みの商品は `products.csv` の `posted` 列が自動で `true` になり、次回実行時はスキップされます。

## 本番運用への移行手順

### 1. PA-APIキーが発行されたら

Amazonアソシエイト・セントラルの「ツール」→「Product Advertising API」からアクセスキー・シークレットキーを取得し、`.env` に設定してください。

```
AMAZON_ASSOCIATE_TAG=あなたのトラッキングID
AMAZON_ACCESS_KEY=xxxxx
AMAZON_SECRET_KEY=xxxxx
```

`src/pa_api_client.py` の `fetch_products(asins, config)` が使えるようになります。`products.csv` に ASIN だけ入れておき、このメソッドで商品名・価格・最新アフィリエイトリンクを自動取得する運用に切り替えられます(呼び出し部分は `src/main.py` に数行追加するだけです)。

> 補足: PA-APIの利用には、初回申請から180日以内に一定数の紹介実績(売上)が必要です。実績がない状態ではキーが失効することがあるため、それまでは本ツールの手入力運用で継続してください。

### 2. X APIキーが発行されたら

1. [X Developer Portal](https://developer.x.com/) でアプリを作成し、**Read and Write** 権限を付与します。
2. API Key / API Key Secret / Access Token / Access Token Secret を発行します(Access Token は Read and Write 権限で再生成が必要な場合があります)。
3. `.env` に設定します。

   ```
   X_API_KEY=xxxxx
   X_API_SECRET=xxxxx
   X_ACCESS_TOKEN=xxxxx
   X_ACCESS_SECRET=xxxxx
   ```

4. 以降 `python -m src.main` を実行すると、dry-run ではなく実際にXへ自動投稿されます。

> **現在の状態**: X APIキーは取得済みですが、Xの利用プランが従量課金(Pay Per Use)でクレジット未チャージのため `402 Payment Required` エラーになることを確認しています。実売上が軌道に乗って自動化に進める段階になったら、`.env` 内の `# PENDING_CREDIT_CHARGE X_API_KEY=...` などコメントアウトされている4行の先頭 `# PENDING_CREDIT_CHARGE ` を削除して有効化し、X Developer Portalでクレジットをチャージしてから再実行してください。

### 定期実行したい場合

Windowsのタスクスケジューラに `python -m src.main` を登録すれば、一定間隔での自動投稿ができます。`POSTS_PER_RUN`(`.env`)で1回の実行あたりの投稿数を調整してください。X APIの自動化ポリシー上、短時間の連続投稿・同一文面の繰り返しはアカウント制限のリスクがあるため、1〜数時間に1件程度のペースを推奨します。

## 法的・規約上の注意

- **ステルスマーケティング規制(景品表示法)**: 2023年10月施行の規制により、広告であることを明示しないアフィリエイト投稿は違法となる可能性があります。本ツールは自動的に投稿冒頭へ `【PR】` を付与しています。表記を変更・削除しないでください。
- **Amazonアソシエイト運営規約**: 投稿には「Amazonアソシエイトとして、Amazon.co.jpの適格販売により収入を得ています」旨の開示が別途求められる場合があります。プロフィール欄への記載など、規約の最新版を確認してください。
- **Xの自動化ルール**: 自動投稿を行うアカウントであることの明示や、過度な連続投稿・重複投稿の禁止など、X Developer Agreementの自動化ポリシーに従ってください。

## ファイル構成

```
amazon_x_affiliate_bot/
├── products.csv          # 投稿キュー(手入力 / 将来はPA-APIで自動化)
├── drafts/                # dry-runで生成されたツイート案(X未設定時)
├── .env                   # APIキー(gitignore対象)
└── src/
    ├── config.py           # .env読み込み
    ├── models.py            # Productデータモデル
    ├── product_source.py    # CSV読み書き・投稿済み管理
    ├── pa_api_client.py     # PA-API連携(キー取得後に有効化)
    ├── tweet_generator.py   # ツイート文生成(文字数調整・PR表記)
    ├── x_client.py           # X投稿 / dry-runドラフト出力
    └── main.py               # 実行エントリーポイント
```
