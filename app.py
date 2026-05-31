# app.py: シンプル練習管理アプリ（記録フォーム＋一覧）
# データはSupabaseに保存。スマホブラウザからの入力を想定。
from __future__ import annotations

from datetime import date, datetime, timedelta

import streamlit as st
from supabase import Client, create_client

st.set_page_config(page_title="練習ログ", page_icon="🎱", layout="centered")

TABLE = "practice_logs"


@st.cache_resource
def get_client() -> Client:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)


def fetch_logs(client: Client) -> list[dict]:
    res = (
        client.table(TABLE)
        .select("*")
        .order("practice_date", desc=True)
        .order("created_at", desc=True)
        .execute()
    )
    return res.data or []


def add_log(client: Client, row: dict) -> None:
    client.table(TABLE).insert(row).execute()


def delete_log(client: Client, log_id: int) -> None:
    client.table(TABLE).delete().eq("id", log_id).execute()


client = get_client()

st.title("🎱 練習ログ")

# ---------- 記録フォーム ----------
with st.form("entry", clear_on_submit=True):
    st.subheader("📝 今日の練習を記録")
    col1, col2 = st.columns(2)
    with col1:
        d = st.date_input("練習した日", value=date.today())
    with col2:
        duration = st.number_input("練習時間（分）", min_value=0, max_value=600, value=60, step=15)

    menu = st.text_input("練習メニュー", placeholder="例: ストップショット、9ボール ゴースト戦")
    result = st.text_input("結果", placeholder="例: 10球中7球成功 / ゴースト 4勝6敗")
    memo = st.text_area("気づき・メモ（任意）", placeholder="例: 引き玉のフォロースルーが甘かった")

    submitted = st.form_submit_button("記録する", use_container_width=True, type="primary")
    if submitted:
        add_log(
            client,
            {
                "practice_date": d.isoformat(),
                "duration_min": int(duration),
                "menu": menu.strip(),
                "result": result.strip(),
                "memo": memo.strip(),
            },
        )
        st.success("記録したよ！👏")
        st.rerun()

st.divider()

# ---------- 記録一覧 ----------
logs = fetch_logs(client)

# 今週サマリ（月曜始まり）
today = date.today()
week_start = today - timedelta(days=today.weekday())
this_week = [
    log for log in logs
    if log.get("practice_date") and date.fromisoformat(log["practice_date"]) >= week_start
]
week_count = len(this_week)
week_minutes = sum(int(log.get("duration_min") or 0) for log in this_week)

c1, c2 = st.columns(2)
c1.metric("今週の練習回数", f"{week_count} 回")
c2.metric("今週の合計時間", f"{week_minutes} 分")

st.subheader("📚 記録一覧")

if not logs:
    st.info("まだ記録がないよ。上のフォームから最初の1件を入れてみてね。")
else:
    for log in logs:
        d_str = log.get("practice_date", "")
        dur = log.get("duration_min", 0)
        header = f"**{d_str}**　{dur}分　{log.get('menu', '') or '（メニュー未記入）'}"
        with st.expander(header):
            if log.get("result"):
                st.markdown(f"**結果:** {log['result']}")
            if log.get("memo"):
                st.markdown(f"**メモ:** {log['memo']}")
            if st.button("🗑 この記録を削除", key=f"del_{log['id']}"):
                delete_log(client, log["id"])
                st.rerun()
