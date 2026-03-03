# 📸 東京写真展カレンダー

東京で開催される写真展の情報を自動的にスクレイピングし、見やすいカレンダー形式で表示するWebアプリケーションです。

## 🌐 デモ

**Live:** [https://KurouzuSetsuna.github.io/TokyoPhotoExhibition/](https://KurouzuSetsuna.github.io/TokyoPhotoExhibition/)

## ✨ 特徴

- 📅 **月別カレンダー表示** - 写真展をカレンダー形式で一目で確認
- 🔄 **自動更新** - GitHub Actionsで毎週日曜日に自動更新
- 📱 **レスポンシブデザイン** - PC・タブレット・スマートフォンに対応
- 📥 **Googleカレンダー連携** - .ics形式でエクスポート可能
- 🎨 **美しいUI** - グラデーションとアニメーションを活用した現代的なデザイン
- 🔍 **詳細情報表示** - 展示会名、会場、期間、説明を表示

## 🚀 使い方

1. [カレンダーページ](https://KurouzuSetsuna.github.io/TokyoPhotoExhibition/)にアクセス
2. 月を選択して写真展を確認
3. 気になる展示会をクリックして詳細を確認
4. 「Googleカレンダーにエクスポート」ボタンで予定に追加

## 🛠️ 技術スタック

- **言語**: Python 3.11
- **スクレイピング**: BeautifulSoup4, Requests
- **自動化**: GitHub Actions
- **ホスティング**: GitHub Pages

## 📋 主な機能

### 自動データ収集
- CAPA東京写真展ページから最新情報を取得
- 展示会名、会場、開催期間、説明を自動抽出
- JSONファイルに構造化データとして保存

### カレンダー生成
- 2026年の12ヶ月分のカレンダーを自動生成
- 開催中の展示会を日付ごとに表示
- インタラクティブなUI（クリックで詳細表示）

### GitHub Actions による自動運用
- 毎週日曜日 午前9時（JST）に自動実行
- 変更があった場合のみコミット
- デプロイまで完全自動化

## 📁 プロジェクト構成

```
.
├── .github/
│   └── workflows/
│       └── update-calendar.yml       # GitHub Actions ワークフロー
├── scrape_exhibitions.py             # 展示会情報スクレイピング
├── generate_calendar.py              # カレンダーHTML生成
├── index.html                        # ランディングページ
├── requirements.txt                  # Python依存パッケージ
├── README.md                         # このファイル
└── README_CALENDAR_SETUP.md          # 詳細なセットアップガイド
```

## 🔧 セットアップ

詳細なセットアップ手順は [README_CALENDAR_SETUP.md](./README_CALENDAR_SETUP.md) をご覧ください。

### クイックスタート

```bash
# リポジトリをクローン
git clone https://github.com/KurouzuSetsuna/TokyoPhotoExhibition.git
cd TokyoPhotoExhibition

# 依存パッケージをインストール
pip install -r requirements.txt

# 展示会情報を取得
python scrape_exhibitions.py

# カレンダーを生成
python generate_calendar.py

# HTMLファイルを開く
open tokyo_photo_calendar_2026.html
```

## 🤝 貢献

プルリクエストを歓迎します。大きな変更の場合は、まずissueを開いて変更内容を議論してください。

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 🙏 謝辞

- 展示会情報: [CAPA - 東京の写真展](https://getnavi.jp/capa/exhibition/tokyo/)

## ⚠️ 注意事項

このプロジェクトは個人的な学習・利用目的で作成されています。スクレイピングは対象サイトの利用規約を遵守して実施してください。

---

**作成者**: [KurouzuSetsuna](https://github.com/KurouzuSetsuna)
**最終更新**: 2026年3月
