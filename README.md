# 🎱 Cue Note

ビリヤード練習を記録するシンプルなアプリ。スマホからサッと入力できる。

記録する内容：
- 練習した日と時間
- 練習メニューと結果
- 気づき・メモ

## 技術構成

- **Streamlit**（UI）
- **Supabase**（データ保存・無料DB）

## ローカルで動かす

```bash
pip install -r requirements.txt
streamlit run app.py
```

`.streamlit/secrets.toml` にSupabaseの接続情報が必要（このファイルはGit管理外）。

## ネット公開（Streamlit Community Cloud）

1. このフォルダをGitHubリポジトリにpush
2. https://share.streamlit.io でリポジトリを連携
3. アプリの Settings → Secrets に以下を登録：
   ```toml
   [supabase]
   url = "https://xxxx.supabase.co"
   key = "（Supabaseのanonキー / JWT形式 eyJ... ）"
   ```
   ※ supabase-py は新形式の publishable キーを受け付けないため、旧来の anon キー（`eyJ...` で始まるJWT）を使う。
4. 発行されたURLをスマホのホーム画面に追加するとアプリ風に使える

## Supabaseテーブル

`practice_logs`

| カラム | 型 |
|--------|-----|
| id | bigint (PK) |
| practice_date | date |
| duration_min | int |
| menu | text |
| result | text |
| memo | text |
| created_at | timestamptz |
