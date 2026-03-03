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
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')

        exhibitions = []

        # 日付パターンを含むdiv要素を探す（実際のサイト構造に基づく）
        date_pattern = re.compile(r'^\s*\d+/\d+')
        date_divs = soup.find_all('div', string=date_pattern)

        print(f"見つかった展示会数: {len(date_divs)}")

        for date_div in date_divs:
            try:
                # li要素（展示会情報の親）を取得
                li = date_div.parent
                if not li or li.name != 'li':
                    continue

                # 日付とタイトルを取得
                date_text = date_div.get_text(strip=True)
                title_p = li.find('p')
                if not title_p:
                    continue

                title = title_p.get_text(strip=True)

                # ギャラリー名を取得（ulの前のh4）
                ul = li.parent
                gallery = "東京都内"
                if ul and ul.name == 'ul':
                    h4 = ul.find_previous('h4')
                    if h4:
                        gallery = h4.get_text(strip=True)

                # 日付をパース
                start_date, end_date = parse_date_range(date_text)

                if title and start_date:
                    exhibitions.append({
                        'title': title,
                        'start_date': start_date,
                        'end_date': end_date,
                        'location': gallery,
                        'date_text': date_text,
                        'link': url,
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

    例:
    - "2/3〜14" -> ("2026-02-03", "2026-02-14")
    - "3/31〜4/11" -> ("2026-03-31", "2026-04-11")
    - "2026年4月1日～4月30日" -> ("2026-04-01", "2026-04-30")
    """
    if not date_text:
        return None, None

    try:
        # 現在の年を取得（2026年を想定）
        current_year = 2026

        # パターン1: "2/3〜14" や "3/31〜4/11" のような形式
        # 月/日〜日 または 月/日〜月/日
        simple_pattern = r'(\d{1,2})/(\d{1,2})\s*[〜~～-]\s*(?:(\d{1,2})/)?(\d{1,2})'
        simple_match = re.search(simple_pattern, date_text)

        if simple_match:
            start_month = int(simple_match.group(1))
            start_day = int(simple_match.group(2))
            end_month = int(simple_match.group(3)) if simple_match.group(3) else start_month
            end_day = int(simple_match.group(4))

            start = f"{current_year}-{str(start_month).zfill(2)}-{str(start_day).zfill(2)}"
            end = f"{current_year}-{str(end_month).zfill(2)}-{str(end_day).zfill(2)}"
            return start, end

        # パターン2: 年月日のフル形式
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

        # パターン3: 月日のみのパターン（年が前にある場合）
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
        print(f"\n成功: {len(exhibitions)}件の展示会情報を取得しました")
    else:
        print("\n警告: 展示会情報を取得できませんでした")
        # 空のデータを保存（エラーでビルドが止まらないように）
        save_exhibitions([])


if __name__ == "__main__":
    main()
