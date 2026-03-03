# 📸 東京の写真展カレンダー 自動更新セットアップ

GitHub Actionsを使って、週1回自動的に展示会情報を更新し、GitHub Pagesで公開する方法を説明します。

## 📋 概要

このシステムは以下の3つのコンポーネントで構成されています：

1. **scrape_exhibitions.py** - ウェブサイトから展示会情報をスクレイピング
2. **generate_calendar.py** - カレンダーHTMLを生成
3. **.github/workflows/update-calendar.yml** - 週1回自動実行

## 🚀 セットアップ手順

### 1. GitHubリポジトリの準備

```bash
# Gitリポジトリを初期化（まだの場合）
git init

# ファイルをコミット
git add .
git commit -m "Initial commit: Photo exhibition calendar with auto-update"

# GitHubリポジトリを作成してプッシュ
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

### 2. GitHub Pagesの有効化

1. GitHubリポジトリのページを開く
2. **Settings** > **Pages** に移動
3. **Source** を `Deploy from a branch` に設定
4. **Branch** を `main` / `(root)` に設定
5. **Save** をクリック

数分後、`https://YOUR_USERNAME.github.io/YOUR_REPO/tokyo_photo_calendar_2026.html` でアクセス可能になります。

### 3. GitHub Actionsの権限設定

1. リポジトリの **Settings** > **Actions** > **General** に移動
2. **Workflow permissions** セクションで:
   - **Read and write permissions** を選択
   - **Allow GitHub Actions to create and approve pull requests** にチェック
3. **Save** をクリック

### 4. 手動で初回実行

1. リポジトリの **Actions** タブを開く
2. **Update Photo Exhibition Calendar** ワークフローを選択
3. **Run workflow** > **Run workflow** をクリック

## ⏰ 自動更新スケジュール

- **毎週日曜日の午前9時（日本時間）**に自動実行
- 変更があった場合のみコミット・プッシュされます

### スケジュールの変更方法

`.github/workflows/update-calendar.yml` の cron 設定を変更:

```yaml
schedule:
  - cron: '0 0 * * 0'  # 毎週日曜日 UTC 0:00 = JST 9:00
```

**cronの例:**
- `'0 0 * * 0'` - 毎週日曜日 0:00 UTC
- `'0 0 * * 3'` - 毎週水曜日 0:00 UTC
- `'0 0 1 * *'` - 毎月1日 0:00 UTC
- `'0 */12 * * *'` - 12時間ごと

## 🛠️ ローカルでのテスト

```bash
# 依存関係をインストール
pip install -r requirements.txt

# スクレイピングを実行
python scrape_exhibitions.py

# カレンダーHTMLを生成
python generate_calendar.py

# 生成されたファイルをブラウザで確認
start tokyo_photo_calendar_2026.html  # Windows
# または
open tokyo_photo_calendar_2026.html   # macOS
# または
xdg-open tokyo_photo_calendar_2026.html  # Linux
```

## 📁 ファイル構成

```
.
├── .github/
│   └── workflows/
│       └── update-calendar.yml          # GitHub Actions ワークフロー
├── scrape_exhibitions.py                # スクレイピングスクリプト
├── generate_calendar.py                 # カレンダー生成スクリプト
├── requirements.txt                     # Python依存パッケージ
├── exhibitions_data.json                # 展示会データ（自動生成）
├── tokyo_photo_calendar_2026.html       # カレンダーHTML（自動生成）
└── README_CALENDAR_SETUP.md             # このファイル
```

## 🔧 カスタマイズ

### スクレイピング対象URLの変更

`scrape_exhibitions.py` の `scrape_tokyo_exhibitions()` 関数:

```python
def scrape_tokyo_exhibitions(url: str = "https://YOUR_URL_HERE/"):
    # ...
```

### カレンダーデザインの変更

`generate_calendar.py` の `HTML_TEMPLATE` 変数内のCSSを編集

### データ取得ロジックの調整

ウェブサイトの構造に応じて、`scrape_exhibitions.py` のセレクタを調整:

```python
# 例: 記事要素の検索パターンを変更
articles = soup.find_all('div', class_='your-class-name')
```

## ⚠️ トラブルシューティング

### GitHub Actionsが失敗する場合

1. **Actions** タブでエラーログを確認
2. スクレイピング対象サイトの構造が変わっていないか確認
3. `scrape_exhibitions.py` を手動実行してエラー内容を確認

### カレンダーが表示されない場合

1. GitHub Pagesが有効になっているか確認
2. ファイル名が `tokyo_photo_calendar_2026.html` であることを確認
3. ブラウザのキャッシュをクリアして再読み込み

### 展示会情報が取得できない場合

- スクレイピング対象サイトの構造が変更された可能性があります
- `scrape_exhibitions.py` のセレクタを更新する必要があります

## 📊 ワークフローの確認

GitHub Actionsの実行状況は以下で確認できます：

1. リポジトリの **Actions** タブ
2. 各実行の詳細ログ
3. 成果物（Artifacts）のダウンロード

## 📱 Googleカレンダーへのインポート

生成されたカレンダーページの「Googleカレンダーにエクスポート」ボタンをクリックすると、.icsファイルがダウンロードされます。

**インポート手順:**
1. Googleカレンダーを開く
2. 左側のメニューで「設定」をクリック
3. 「インポート/エクスポート」を選択
4. ダウンロードした.icsファイルを選択してインポート

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

---

**情報源:** [CAPA - 東京の写真展](https://getnavi.jp/capa/exhibition/tokyo/)

**注意:** スクレイピングは対象サイトの利用規約を遵守して実施してください。
