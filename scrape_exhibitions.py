#!/usr/bin/env python3
"""
東京の写真展情報をスクレイピングするスクリプト
https://getnavi.jp/capa/exhibition/tokyo/ からデータを取得
"""

import json
import re
from datetime import datetime
from typing import List, Dict
import requests
from bs4 import BeautifulSoup


def scrape_tokyo_exhibitions(url: str = "https://getnavi.jp/capa/exhibition/tokyo/") -> List[Dict]:
    """
    東京の写真展情報をスクレイピング

    Args:
        url: スクレイピング対象のURL

    Returns:
        展示会情報のリスト
    """
    print(f"スクレイピング開始: {url}")

    try:
        # ユーザーエージェントを設定
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        response.encoding = response.apparent_encoding

        soup = BeautifulSoup(response.text, 'html.parser')

        exhibitions = []

        # 記事要素を検索（サイト構造に応じて調整が必要）
        # 一般的な写真展リストの構造を想定
        articles = soup.find_all(['article', 'div'], class_=re.compile(r'exhibition|event|post|item'))

        if not articles:
            # 別のセレクタを試す
            articles = soup.find_all(['div', 'li'], class_=re.compile(r'entry|list-item'))

        print(f"見つかった記事数: {len(articles)}")

        for article in articles:
            try:
                # タイトルを取得
                title_elem = article.find(['h2', 'h3', 'h4', 'a'], class_=re.compile(r'title|heading'))
                if not title_elem:
                    title_elem = article.find(['h2', 'h3', 'h4'])
                if not title_elem:
                    title_elem = article.find('a')

                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)

                # 日付情報を取得
                date_elem = article.find(['time', 'span', 'div'], class_=re.compile(r'date|time|period'))
                date_text = date_elem.get_text(strip=True) if date_elem else ""

                # 場所情報を取得
                location_elem = article.find(['span', 'div', 'p'], class_=re.compile(r'location|venue|place'))
                location = location_elem.get_text(strip=True) if location_elem else "東京都内"

                # リンクを取得
                link_elem = article.find('a', href=True)
                link = link_elem['href'] if link_elem else ""
                if link and not link.startswith('http'):
                    link = f"https://getnavi.jp{link}"

                # 日付をパース
                start_date, end_date = parse_date_range(date_text)

                if title and start_date:
                    exhibitions.append({
                        'title': title,
                        'start_date': start_date,
                        'end_date': end_date,
                        'location': location,
                        'date_text': date_text,
                        'link': link,
                        'tag': 'exhibition'
                    })

            except Exception as e:
                print(f"記事のパースエラー: {e}")
                continue

        print(f"取得した展示会数: {len(exhibitions)}")
        return exhibitions

    except Exception as e:
        print(f"スクレイピングエラー: {e}")
        return []


def parse_date_range(date_text: str) -> tuple:
    """
    日付テキストから開始日と終了日を抽出

    例: "2026年4月1日～4月30日" -> ("2026-04-01", "2026-04-30")
    """
    if not date_text:
        return None, None

    try:
        # 年月日のパターン
        pattern_full = r'(\d{4})年(\d{1,2})月(\d{1,2})日'
        matches = re.findall(pattern_full, date_text)

        if len(matches) >= 2:
            # 開始日と終了日がある場合
            start = f"{matches[0][0]}-{matches[0][1].zfill(2)}-{matches[0][2].zfill(2)}"
            end = f"{matches[1][0]}-{matches[1][1].zfill(2)}-{matches[1][2].zfill(2)}"
            return start, end
        elif len(matches) == 1:
            # 開始日のみの場合
            start = f"{matches[0][0]}-{matches[0][1].zfill(2)}-{matches[0][2].zfill(2)}"
            return start, start

        # 月日のみのパターン（年が前にある場合）
        year_match = re.search(r'(\d{4})年', date_text)
        if year_match:
            year = year_match.group(1)
            month_day_pattern = r'(\d{1,2})月(\d{1,2})日'
            month_day_matches = re.findall(month_day_pattern, date_text)

            if len(month_day_matches) >= 2:
                start = f"{year}-{month_day_matches[0][0].zfill(2)}-{month_day_matches[0][1].zfill(2)}"
                end = f"{year}-{month_day_matches[1][0].zfill(2)}-{month_day_matches[1][1].zfill(2)}"
                return start, end
            elif len(month_day_matches) == 1:
                start = f"{year}-{month_day_matches[0][0].zfill(2)}-{month_day_matches[0][1].zfill(2)}"
                return start, start

        return None, None

    except Exception as e:
        print(f"日付パースエラー: {e} - {date_text}")
        return None, None


def save_exhibitions(exhibitions: List[Dict], output_file: str = "exhibitions_data.json"):
    """展示会データをJSONファイルに保存"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'last_updated': datetime.now().isoformat(),
            'count': len(exhibitions),
            'exhibitions': exhibitions
        }, f, ensure_ascii=False, indent=2)

    print(f"データを保存しました: {output_file}")


def main():
    """メイン処理"""
    exhibitions = scrape_tokyo_exhibitions()

    if exhibitions:
        save_exhibitions(exhibitions)
        print(f"\n✅ 成功: {len(exhibitions)}件の展示会情報を取得しました")
    else:
        print("\n⚠️ 警告: 展示会情報を取得できませんでした")
        # 空のデータを保存（エラーでビルドが止まらないように）
        save_exhibitions([])


if __name__ == "__main__":
    main()
