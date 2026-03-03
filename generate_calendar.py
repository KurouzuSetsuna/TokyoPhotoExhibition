#!/usr/bin/env python3
"""
展示会データからカレンダーHTMLを生成するスクリプト
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>📸 東京の写真展カレンダー 2026</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: 'Segoe UI', 'Hiragino Kaku Gothic ProN', 'Meiryo', sans-serif;
      background: #f8f9fa;
      color: #202124;
      min-height: 100vh;
      padding: 20px;
    }}

    .container {{
      max-width: 1400px;
      margin: 0 auto;
      background: white;
      border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      overflow: hidden;
    }}

    .header {{
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
      color: white;
      padding: 24px 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }}

    .header h1 {{
      font-size: 28px;
      font-weight: 400;
      letter-spacing: 0.5px;
    }}

    .header-info {{
      font-size: 12px;
      color: #9bb;
    }}

    .header-controls {{
      display: flex;
      gap: 12px;
      align-items: center;
    }}

    .btn {{
      background: rgba(255,255,255,0.2);
      border: 1px solid rgba(255,255,255,0.3);
      color: white;
      padding: 8px 16px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 14px;
      font-weight: 500;
      transition: all 0.2s;
      text-decoration: none;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }}

    .btn:hover {{
      background: rgba(255,255,255,0.3);
      border-color: rgba(255,255,255,0.5);
    }}

    .btn-export {{
      background: #34a853;
      border-color: #2d8e47;
    }}

    .btn-export:hover {{
      background: #2d8e47;
    }}

    .calendar-controls {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 20px 32px;
      border-bottom: 1px solid #e0e0e0;
    }}

    .month-display {{
      font-size: 24px;
      font-weight: 500;
      color: #202124;
    }}

    .month-nav {{
      display: flex;
      gap: 8px;
    }}

    .nav-btn {{
      background: white;
      border: 1px solid #dadce0;
      color: #5f6368;
      padding: 8px 12px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 14px;
      transition: all 0.2s;
    }}

    .nav-btn:hover {{
      background: #f8f9fa;
      border-color: #5f6368;
    }}

    .filter-section {{
      padding: 16px 32px;
      background: #f8f9fa;
      border-bottom: 1px solid #e0e0e0;
    }}

    .filter-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
    }}

    .filter-title {{
      font-size: 14px;
      font-weight: 600;
      color: #202124;
    }}

    .filter-toggle {{
      font-size: 12px;
      color: #1967d2;
      cursor: pointer;
      padding: 4px 8px;
      border-radius: 4px;
      transition: all 0.2s;
    }}

    .filter-toggle:hover {{
      background: #e8f0fe;
    }}

    .filter-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 8px;
      max-height: 200px;
      overflow-y: auto;
      padding: 8px 0;
    }}

    .filter-item {{
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 13px;
      color: #5f6368;
      padding: 4px;
    }}

    .filter-item input[type="checkbox"] {{
      cursor: pointer;
      width: 16px;
      height: 16px;
    }}

    .filter-item label {{
      cursor: pointer;
      user-select: none;
      flex: 1;
    }}

    .filter-count {{
      font-size: 11px;
      color: #9aa0a6;
      background: #e8eaed;
      padding: 2px 6px;
      border-radius: 10px;
    }}

    .calendar {{
      padding: 20px;
    }}

    .calendar-grid {{
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      gap: 1px;
      background: #e0e0e0;
      border: 1px solid #e0e0e0;
      border-radius: 8px;
      overflow: hidden;
    }}

    .day-header {{
      background: #f8f9fa;
      padding: 12px 8px;
      text-align: center;
      font-size: 12px;
      font-weight: 600;
      color: #70757a;
      text-transform: uppercase;
    }}

    .day-header.sunday {{ color: #d93025; }}
    .day-header.saturday {{ color: #1565C0; }}

    .day-cell {{
      background: white;
      min-height: 120px;
      max-height: 180px;
      padding: 8px;
      position: relative;
      cursor: default;
      overflow-y: auto;
      overflow-x: hidden;
    }}

    .day-cell.other-month {{
      background: #fafafa;
      opacity: 0.5;
    }}

    .day-cell.today {{
      background: #e8f0fe;
    }}

    .day-number {{
      font-size: 13px;
      font-weight: 500;
      color: #3c4043;
      margin-bottom: 4px;
      text-align: right;
      padding: 0 4px;
    }}

    .day-cell.other-month .day-number {{
      color: #9aa0a6;
    }}

    .day-cell.sunday .day-number {{
      color: #d93025;
    }}

    .day-cell.saturday .day-number {{
      color: #1565C0;
    }}

    .day-cell.today .day-number {{
      background: #1967d2;
      color: white;
      border-radius: 50%;
      width: 28px;
      height: 28px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      float: right;
    }}

    /* スクロールバーのスタイリング */
    .day-cell::-webkit-scrollbar {{
      width: 6px;
    }}

    .day-cell::-webkit-scrollbar-track {{
      background: #f1f1f1;
      border-radius: 3px;
    }}

    .day-cell::-webkit-scrollbar-thumb {{
      background: #c1c1c1;
      border-radius: 3px;
    }}

    .day-cell::-webkit-scrollbar-thumb:hover {{
      background: #a0a0a0;
    }}

    .event {{
      background: #7e3ff2;
      color: white;
      padding: 4px 8px;
      margin: 2px 0;
      border-radius: 4px;
      font-size: 11px;
      cursor: pointer;
      transition: all 0.2s;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }}

    .event:hover {{
      box-shadow: 0 2px 4px rgba(0,0,0,0.2);
      transform: translateY(-1px);
    }}

    .event.exhibition {{ background: #7e3ff2; }}

    .more-events {{
      font-size: 11px;
      color: #1967d2;
      padding: 4px 8px;
      margin: 2px 0;
      cursor: pointer;
      text-align: center;
      border-radius: 4px;
      background: #e8f0fe;
      transition: all 0.2s;
      font-weight: 500;
    }}

    .more-events:hover {{
      background: #d2e3fc;
      transform: translateY(-1px);
    }}

    .modal {{
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0,0,0,0.5);
      z-index: 1000;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}

    .modal.active {{
      display: flex;
    }}

    .modal-content {{
      background: white;
      border-radius: 12px;
      padding: 32px;
      max-width: 600px;
      width: 100%;
      box-shadow: 0 8px 24px rgba(0,0,0,0.2);
      position: relative;
      max-height: 80vh;
      overflow-y: auto;
    }}

    .modal-close {{
      position: absolute;
      top: 16px;
      right: 16px;
      background: none;
      border: none;
      font-size: 24px;
      color: #5f6368;
      cursor: pointer;
      padding: 4px 8px;
      line-height: 1;
    }}

    .modal-close:hover {{
      color: #202124;
    }}

    .modal-title {{
      font-size: 22px;
      font-weight: 500;
      margin-bottom: 16px;
      color: #202124;
      padding-right: 32px;
    }}

    .modal-details {{
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .modal-detail {{
      display: flex;
      align-items: flex-start;
      gap: 12px;
    }}

    .modal-detail-icon {{
      color: #5f6368;
      font-size: 18px;
      width: 24px;
      text-align: center;
    }}

    .modal-detail-text {{
      flex: 1;
      font-size: 14px;
      color: #5f6368;
    }}

    .modal-link {{
      color: #1967d2;
      text-decoration: none;
      word-break: break-all;
    }}

    .modal-link:hover {{
      text-decoration: underline;
    }}

    @media (max-width: 768px) {{
      .calendar-grid {{
        font-size: 12px;
      }}

      .day-cell {{
        min-height: 80px;
        max-height: 120px;
        padding: 4px;
      }}

      .event {{
        font-size: 9px;
        padding: 2px 4px;
      }}

      .header {{
        flex-direction: column;
        align-items: flex-start;
      }}
    }}
  </style>
</head>
<body>

<div class="container">
  <div class="header">
    <div>
      <h1>📸 東京の写真展カレンダー 2026</h1>
      <p class="header-info">最終更新: {last_updated} | 展示会数: {event_count}件 | 情報源: <a href="https://getnavi.jp/capa/exhibition/tokyo/" class="btn" style="padding:2px 8px;font-size:11px" target="_blank">CAPA</a></p>
    </div>
    <div class="header-controls">
      <button class="btn btn-export" onclick="exportToGoogleCalendar()">
        📅 Googleカレンダーにエクスポート
      </button>
    </div>
  </div>

  <div class="calendar-controls">
    <div class="month-display" id="monthDisplay"></div>
    <div class="month-nav">
      <button class="nav-btn" onclick="changeMonth(-1)">◀ 前月</button>
      <button class="nav-btn" onclick="goToToday()">今日</button>
      <button class="nav-btn" onclick="changeMonth(1)">次月 ▶</button>
    </div>
  </div>

  <div class="filter-section">
    <div class="filter-header">
      <span class="filter-title">🏛️ 会場フィルター</span>
      <div>
        <span class="filter-toggle" onclick="selectAllVenues()">すべて選択</span>
        <span class="filter-toggle" onclick="deselectAllVenues()">すべて解除</span>
      </div>
    </div>
    <div class="filter-grid" id="venueFilters"></div>
  </div>

  <div class="calendar">
    <div class="calendar-grid" id="calendarGrid"></div>
  </div>
</div>

<div class="modal" id="eventModal" onclick="closeModal(event)">
  <div class="modal-content" onclick="event.stopPropagation()">
    <button class="modal-close" onclick="closeModal()">&times;</button>
    <div class="modal-title" id="modalTitle"></div>
    <div class="modal-details" id="modalDetails"></div>
  </div>
</div>

<script>
const exhibitions = {exhibitions_json};

let currentDate = new Date();
let displayMonth = currentDate.getMonth();
let displayYear = currentDate.getFullYear();

// フィルター用のグローバル変数
let selectedVenues = new Set();
let allVenues = [];

// 初期化時に会場リストを構築
function initializeVenueFilters() {{
  const venueCount = {{}};
  exhibitions.forEach(ex => {{
    venueCount[ex.location] = (venueCount[ex.location] || 0) + 1;
  }});

  allVenues = Object.keys(venueCount).sort();
  allVenues.forEach(venue => selectedVenues.add(venue));

  const filterContainer = document.getElementById('venueFilters');
  filterContainer.innerHTML = '';

  allVenues.forEach(venue => {{
    const filterItem = document.createElement('div');
    filterItem.className = 'filter-item';

    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.id = `venue-${{venue}}`;
    checkbox.checked = true;
    checkbox.onchange = () => toggleVenue(venue);

    const label = document.createElement('label');
    label.htmlFor = `venue-${{venue}}`;
    label.textContent = venue;

    const count = document.createElement('span');
    count.className = 'filter-count';
    count.textContent = venueCount[venue];

    filterItem.appendChild(checkbox);
    filterItem.appendChild(label);
    filterItem.appendChild(count);
    filterContainer.appendChild(filterItem);
  }});
}}

function toggleVenue(venue) {{
  if (selectedVenues.has(venue)) {{
    selectedVenues.delete(venue);
  }} else {{
    selectedVenues.add(venue);
  }}
  renderCalendar();
}}

function selectAllVenues() {{
  allVenues.forEach(venue => {{
    selectedVenues.add(venue);
    const checkbox = document.getElementById(`venue-${{venue}}`);
    if (checkbox) checkbox.checked = true;
  }});
  renderCalendar();
}}

function deselectAllVenues() {{
  selectedVenues.clear();
  allVenues.forEach(venue => {{
    const checkbox = document.getElementById(`venue-${{venue}}`);
    if (checkbox) checkbox.checked = false;
  }});
  renderCalendar();
}}

function getFilteredExhibitions() {{
  return exhibitions.filter(ex => selectedVenues.has(ex.location));
}}

function renderCalendar() {{
  const grid = document.getElementById('calendarGrid');
  grid.innerHTML = '';

  const monthNames = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'];
  document.getElementById('monthDisplay').textContent = `${{displayYear}}年 ${{monthNames[displayMonth]}}`;

  const dayHeaders = ['日', '月', '火', '水', '木', '金', '土'];
  dayHeaders.forEach((day, index) => {{
    const header = document.createElement('div');
    header.className = 'day-header';
    if (index === 0) header.classList.add('sunday');
    if (index === 6) header.classList.add('saturday');
    header.textContent = day;
    grid.appendChild(header);
  }});

  const firstDay = new Date(displayYear, displayMonth, 1);
  const lastDay = new Date(displayYear, displayMonth + 1, 0);
  const daysInMonth = lastDay.getDate();
  const startDayOfWeek = firstDay.getDay();

  const prevMonthLastDay = new Date(displayYear, displayMonth, 0).getDate();

  for (let i = startDayOfWeek - 1; i >= 0; i--) {{
    const day = prevMonthLastDay - i;
    const cell = createDayCell(day, displayMonth - 1, displayYear, true);
    grid.appendChild(cell);
  }}

  for (let day = 1; day <= daysInMonth; day++) {{
    const cell = createDayCell(day, displayMonth, displayYear, false);
    grid.appendChild(cell);
  }}

  const totalCells = grid.children.length - 7;
  const remainingCells = Math.ceil((totalCells) / 7) * 7 - totalCells;
  for (let day = 1; day <= remainingCells; day++) {{
    const cell = createDayCell(day, displayMonth + 1, displayYear, true);
    grid.appendChild(cell);
  }}
}}

function createDayCell(day, month, year, isOtherMonth) {{
  const cell = document.createElement('div');
  cell.className = 'day-cell';

  const cellDate = new Date(year, month, day);
  const dayOfWeek = cellDate.getDay();

  if (isOtherMonth) {{
    cell.classList.add('other-month');
  }}

  if (dayOfWeek === 0) cell.classList.add('sunday');
  if (dayOfWeek === 6) cell.classList.add('saturday');

  const today = new Date();
  if (cellDate.toDateString() === today.toDateString()) {{
    cell.classList.add('today');
  }}

  const dayNumber = document.createElement('div');
  dayNumber.className = 'day-number';
  dayNumber.textContent = day;
  cell.appendChild(dayNumber);

  if (!isOtherMonth) {{
    const dateStr = `${{year}}-${{String(month + 1).padStart(2, '0')}}-${{String(day).padStart(2, '0')}}`;
    const dayExhibitions = getFilteredExhibitions().filter(ex => {{
      return ex.start_date <= dateStr && dateStr <= ex.end_date;
    }});

    dayExhibitions.slice(0, 5).forEach(ex => {{
      const eventEl = document.createElement('div');
      eventEl.className = `event ${{ex.tag}}`;
      eventEl.textContent = ex.title;
      eventEl.onclick = () => showEventModal(ex);
      cell.appendChild(eventEl);
    }});

    if (dayExhibitions.length > 5) {{
      const moreEl = document.createElement('div');
      moreEl.className = 'more-events';
      moreEl.textContent = `+${{dayExhibitions.length - 5}}件`;
      moreEl.onclick = () => showDayEventsModal(dateStr, dayExhibitions);
      cell.appendChild(moreEl);
    }}
  }}

  return cell;
}}

function changeMonth(delta) {{
  displayMonth += delta;
  if (displayMonth < 0) {{
    displayMonth = 11;
    displayYear--;
  }} else if (displayMonth > 11) {{
    displayMonth = 0;
    displayYear++;
  }}
  renderCalendar();
}}

function goToToday() {{
  const today = new Date();
  displayMonth = today.getMonth();
  displayYear = today.getFullYear();
  renderCalendar();
}}

function showEventModal(exhibition) {{
  const modal = document.getElementById('eventModal');
  const title = document.getElementById('modalTitle');
  const details = document.getElementById('modalDetails');

  title.textContent = exhibition.title;

  let dateDisplay = exhibition.date_text;
  if (!dateDisplay && exhibition.start_date) {{
    dateDisplay = exhibition.start_date === exhibition.end_date
      ? exhibition.start_date
      : `${{exhibition.start_date}} 〜 ${{exhibition.end_date}}`;
  }}

  details.innerHTML = `
    <div class="modal-detail">
      <div class="modal-detail-icon">📅</div>
      <div class="modal-detail-text">${{dateDisplay}}</div>
    </div>
    <div class="modal-detail">
      <div class="modal-detail-icon">📍</div>
      <div class="modal-detail-text">${{exhibition.location}}</div>
    </div>
    ${{exhibition.link ? `
      <div class="modal-detail">
        <div class="modal-detail-icon">🔗</div>
        <div class="modal-detail-text">
          <a href="${{exhibition.link}}" class="modal-link" target="_blank" rel="noopener">詳細を見る</a>
        </div>
      </div>
    ` : ''}}
  `;

  modal.classList.add('active');
}}

function closeModal(event) {{
  if (!event || event.target.id === 'eventModal') {{
    document.getElementById('eventModal').classList.remove('active');
  }}
}}

function showDayEventsModal(dateStr, dayExhibitions) {{
  const modal = document.getElementById('eventModal');
  const title = document.getElementById('modalTitle');
  const details = document.getElementById('modalDetails');

  const dateObj = new Date(dateStr + 'T00:00:00');
  const dateDisplay = `${{dateObj.getFullYear()}}年${{dateObj.getMonth() + 1}}月${{dateObj.getDate()}}日`;

  title.textContent = `${{dateDisplay}}の写真展 (${{dayExhibitions.length}}件)`;

  let eventsHTML = '<div style="display: flex; flex-direction: column; gap: 12px;">';
  dayExhibitions.forEach(ex => {{
    const periodDisplay = ex.start_date === ex.end_date
      ? new Date(ex.start_date + 'T00:00:00').toLocaleDateString('ja-JP')
      : `${{new Date(ex.start_date + 'T00:00:00').toLocaleDateString('ja-JP')}} 〜 ${{new Date(ex.end_date + 'T00:00:00').toLocaleDateString('ja-JP')}}`;

    eventsHTML += `
      <div style="padding: 12px; background: #f8f9fa; border-radius: 8px; cursor: pointer; transition: all 0.2s;"
           onmouseover="this.style.background='#e8f0fe'"
           onmouseout="this.style.background='#f8f9fa'"
           onclick="showEventModal(${{JSON.stringify(ex).replace(/"/g, '&quot;')}})">
        <div style="font-weight: 600; color: #1a1a2e; margin-bottom: 4px;">${{ex.title}}</div>
        <div style="font-size: 13px; color: #5f6368; display: flex; align-items: center; gap: 8px; margin-bottom: 2px;">
          <span>📍 ${{ex.location}}</span>
        </div>
        <div style="font-size: 12px; color: #70757a;">📅 ${{periodDisplay}}</div>
      </div>
    `;
  }});
  eventsHTML += '</div>';

  details.innerHTML = eventsHTML;
  modal.classList.add('active');
}}

function exportToGoogleCalendar() {{
  const filteredExhibitions = getFilteredExhibitions();

  if (filteredExhibitions.length === 0) {{
    alert('エクスポートする展示会がありません。フィルターを確認してください。');
    return;
  }}

  let icsContent = 'BEGIN:VCALENDAR\\r\\n';
  icsContent += 'VERSION:2.0\\r\\n';
  icsContent += 'PRODID:-//Tokyo Photo Exhibitions 2026//Calendar//JP\\r\\n';
  icsContent += 'CALSCALE:GREGORIAN\\r\\n';
  icsContent += 'METHOD:PUBLISH\\r\\n';
  icsContent += 'X-WR-CALNAME:東京の写真展 2026\\r\\n';
  icsContent += 'X-WR-TIMEZONE:Asia/Tokyo\\r\\n';

  filteredExhibitions.forEach((ex, index) => {{
    const startDate = ex.start_date.replace(/-/g, '');
    const endDate = ex.end_date.replace(/-/g, '');
    const timestamp = new Date().toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';

    icsContent += 'BEGIN:VEVENT\\r\\n';
    icsContent += `UID:${{index}}@tokyophoto2026\\r\\n`;
    icsContent += `DTSTAMP:${{timestamp}}\\r\\n`;
    icsContent += `DTSTART;VALUE=DATE:${{startDate}}\\r\\n`;
    icsContent += `DTEND;VALUE=DATE:${{endDate}}\\r\\n`;
    icsContent += `SUMMARY:${{ex.title.replace(/,/g, '\\\\,')}}\\r\\n`;
    icsContent += `DESCRIPTION:${{ex.location.replace(/,/g, '\\\\,')}}\\r\\n`;
    icsContent += `LOCATION:${{ex.location.replace(/,/g, '\\\\,')}}\\r\\n`;
    if (ex.link) {{
      icsContent += `URL:${{ex.link}}\\r\\n`;
    }}
    icsContent += 'STATUS:CONFIRMED\\r\\n';
    icsContent += 'END:VEVENT\\r\\n';
  }});

  icsContent += 'END:VCALENDAR\\r\\n';

  const blob = new Blob([icsContent], {{ type: 'text/calendar;charset=utf-8' }});
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'tokyo_photo_exhibitions_2026.ics';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}}

// 初期化
initializeVenueFilters();
renderCalendar();
</script>

</body>
</html>
"""


def load_exhibitions(json_file: str = "exhibitions_data.json") -> Dict:
    """展示会データをJSONファイルから読み込む"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"警告: {json_file} が見つかりません。空のデータを使用します。")
        return {
            'last_updated': datetime.now().isoformat(),
            'count': 0,
            'exhibitions': []
        }


def generate_html(data: Dict, output_file: str = "tokyo_photo_calendar_2026.html"):
    """展示会データからHTMLカレンダーを生成"""

    exhibitions = data.get('exhibitions', [])
    last_updated = data.get('last_updated', datetime.now().isoformat())

    # 日付形式を整形
    try:
        dt = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
        last_updated_str = dt.strftime('%Y年%m月%d日 %H:%M')
    except:
        last_updated_str = last_updated

    # JavaScriptにJSON埋め込み
    exhibitions_json = json.dumps(exhibitions, ensure_ascii=False)

    # HTMLテンプレートに挿入
    html_content = HTML_TEMPLATE.format(
        last_updated=last_updated_str,
        event_count=len(exhibitions),
        exhibitions_json=exhibitions_json
    )

    # HTMLファイルを書き込み
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTMLカレンダーを生成しました: {output_file}")


def main():
    """メイン処理"""
    data = load_exhibitions()
    generate_html(data)
    print(f"完了: {data['count']}件の展示会を含むカレンダーを生成しました")


if __name__ == "__main__":
    main()
