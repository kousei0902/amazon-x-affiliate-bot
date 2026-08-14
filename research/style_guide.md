# 商品リサーチ・投稿スタイルガイド

このリポジトリで動く3つの自律エージェント(トレンド調査・商品リサーチ・記事作成)が共通で守るルール。

## ターゲット層

ガジェット・PC周辺機器。在宅ワーク層、デスク環境にこだわりたい層。

## フックの書き方(`products.csv` の `hook` 列)

- 共感できる「あるある」「悩み」から入る。スペック羅列で始めない
- 1〜2文、短く
- **実際に使ってもいない体験談は書かない**(「3ヶ月使ってみたら」「買ってよかった」等の一人称の使用体験は捏造になり、景品表示法のステルスマーケティング規制・不当表示のリスクがあるため禁止)
- 押し売り口調・広告っぽい断定は避ける

## 【PR】表記

`src/tweet_generator.py` が投稿生成時に自動で先頭に付与する。`hook`列やCSVには含めない。

## タグ

日本語で2〜3語、`|`区切り。例: `USBハブ|Anker|PC周辺機器`

## 価格

現在価格の確証がない場合は空欄のままにする(値が古いと信頼を損なうため)。確証がある場合のみ数値のみ記入。

## 重複防止

新しいASINを追加する前に、`products.csv` と `research/candidates.csv` の既存ASIN一覧を確認し、重複させない。

## affiliate_url の形式

```
https://www.amazon.co.jp/dp/{ASIN}?tag=kousena9-22
```

## ファイル構成

- `research/trends.md` — トレンド調査エージェントの所見(日付見出しで追記)
- `research/candidates.csv` — 商品リサーチエージェントが見つけた未確定候補(列: `asin,name,price,tags,affiliate_url`)
- `products.csv` — 確定した投稿キュー(列: `id,asin,name,price,affiliate_url,tags,posted,hook`)。記事作成エージェントが`candidates.csv`からここへフック付きで昇格させる
