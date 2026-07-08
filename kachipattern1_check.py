
Claudeが応答を完了しました
アップロード済み画像
これでいいか？


思考プロセス
思考プロセス
設定は完璧です。では接続テストを仕込みます。


3個のコマンドを実行しました, ファイルを編集しました, 読み込まれたツール
3個のコマンドを実行しました, ファイルを編集しました, 読み込まれたツール
C

create_scheduled_task
C

create_scheduled_task
C

create_scheduled_task
スケジュール済みタスクを作成：Kachipattern1 line test
スケジュール済みタスクを作成：Kachipattern1 daily check
次において実施07:10 AM、火曜日 から 土曜日 まで
状況を整理してお答えします。

何に詰まっていたか: 接続テストを「数分後に1回だけ自動実行」で予約しようとしたら、スケジューラに時刻指定を弾かれ続けたため、手動実行型のテストタスクに切り替えました。解決済みです。

実装は終わっているか: はい、仕組み自体は完成・登録済みです。

本番タスク「kachipattern1-daily-check」: 登録完了。次回実行は明日(木)朝7:13、以降毎朝(火〜土)自動で54通貨ペアを判定し、勝ちパターン1が出たペアをLINEに送ります(シグナルなしの日は通知なし)
未確認なのは1点だけ: LINEに実際に届くかの疎通テスト
そこで最後のお願いです。左サイドバーの**「スケジュール」を開き、「kachipattern1-line-test」を今すぐ実行(Run now)**してください。数分後にスマホのLINEに「【テスト】勝ちパターン1通知の接続確認OK」が届けば完成です。届かなければ結果を教えてください。

注意点: 定期実行はMacが起きていてClaudeアプリが開いている間のみ動きます。朝7時台にMacがスリープしていると、次にアプリを開いた時に実行されます。

7時はMacがスリープ状態の可能性が高い。
スリープでも実行されるようにして


思考プロセス
思考プロセス
Macのスリープ中はCowork のスケジュール実行が動かないのは仕組み上の制約で、スリープ解除後に遅れて実行されます。確実に7時台に動かすには方法が2つあります。

スリープ問題の解決方法をどうしますか?
お金がかからない方法にして
「【テスト】勝ちパターン1通知の接続確認OK」が届いてた


思考プロセス
思考プロセス
方法が2つあります。
クラウドの方法は有料か？


2個のファイルを読み込み, ファイルを編集しました, ファイルを作成しました
2個のファイルを読み込み, ファイルを編集しました, ファイルを作成しました
テスト通知が届いたとのこと、これでLINE連携・データ取得とも動作確認完了です。

クラウド(GitHub Actions)は無料です。 プライベートリポジトリでも月2,000分まで無料枠があり、このチェックは1日2〜3分(月約60〜90分)しか使わないので、余裕で無料枠内です。クレジットカード登録も不要です。

上の2ファイルを使って、以下の手順で設定してください(約10分)。

https://github.com で無料アカウント作成(すでにあればログイン)
右上「+」→ New repository → 名前は任意(例: kachipattern1)→ Private を選択 → Create repository
「creating a new file」(または Add file → Create new file)をクリック → ファイル名 kachipattern1_check.py → kachipattern1_check.py の中身をコピペ → Commit changes
同様に Add file → Create new file → ファイル名に .github/workflows/check.yml と入力(スラッシュ含めてそのまま)→ check.yml の中身をコピペ → Commit changes
リポジトリの Settings → Secrets and variables → Actions → New repository secret で2つ登録:
Name: LINE_CHANNEL_ACCESS_TOKEN / Secret: 先ほどのトークン
Name: LINE_USER_ID / Secret: U0fcd7a0efa6ff5737fe09f59fd42d37d
動作確認: Actions タブ → 左の「kachipattern1」→ Run workflow → mode に test と入力 → Run。1分ほどでLINEにテストメッセージが届けば完成
これで毎朝7:10(JST、火〜土)にクラウド側で自動実行され、Macがスリープでも電源オフでも通知が届きます(GitHubの仕様上、数分〜十数分遅れることがあります)。

完成したら教えてください。二重通知を防ぐため、Claude側の毎朝のタスクを停止します。


Kachipattern1 check
PY 

Check
YML 
アップロード済み画像
どれ？


思考プロセス
思考プロセス
青い枠内の 「creating a new file」 というリンクをクリックしてください(「Get started by creating a new file or...」の部分)。

その後は:

ファイル名欄に kachipattern1_check.py と入力 → 下の編集エリアに kachipattern1_check.py の中身を全部コピペ → 右上「Commit changes...」→ そのまま Commit
コミット後、Add file → Create new file → ファイル名欄に .github/workflows/check.yml と入力(/を打つとフォルダに変わります)→ check.yml の中身をコピペ → Commit
Settings → Secrets and variables → Actions → New repository secret で LINE_CHANNEL_ACCESS_TOKEN と LINE_USER_ID を登録
Actions タブ → kachipattern1 → Run workflow → mode欄に test → Run
ファイルの中身は先ほどチャットに貼った2つのファイルカードから開いてコピーできます。



Fable 5は最も高性能なモデルであり、Opus 4.8よりもはるかに速く使用量を消費します。




ClaudeはAIであり、間違いを起こす可能性があります。回答内容をご確認ください。フィードバックを送信
Kachipattern1 check · PY
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
鹿子木式 勝ちパターン1 検知 → LINE通知
対象: ヒロセ通商 LION FX 取扱54通貨ペア / 日足 / ボリンジャーバンド期間21
判定:
  買い: 終値が-1σ未満のバンドウォークが9本以上続いた後、直近終値が-1σを上抜け
  売り: 終値が+1σ超のバンドウォークが9本以上続いた後、直近終値が+1σを下抜け
データ: Yahoo Finance chart API (日足終値)。直接ティッカーが無い場合はUSDクロスから合成。
通知: LINE Messaging API push (要 channel access token / user ID)
使い方:
  python3 kachipattern1_check.py            # 判定してシグナルがあればLINE送信
  python3 kachipattern1_check.py --dry-run  # LINE送信せず結果を表示
  python3 kachipattern1_check.py --test     # LINEにテストメッセージを送信
  python3 kachipattern1_check.py --selftest # 合成データで判定ロジックを検証
環境変数または同階層の line_config.json で認証情報を渡す:
  LINE_CHANNEL_ACCESS_TOKEN / LINE_USER_ID
  {"channel_access_token": "...", "user_id": "U..."}
"""
import json, math, os, sys, time, datetime, urllib.request, urllib.error
 
PAIRS = [
    "AUD/CAD","AUD/CHF","AUD/JPY","AUD/NZD","AUD/USD",
    "CAD/CHF","CAD/JPY","CHF/JPY","CNH/JPY","CZK/JPY",
    "EUR/AUD","EUR/CAD","EUR/CHF","EUR/GBP","EUR/JPY",
    "EUR/NOK","EUR/NZD","EUR/PLN","EUR/SEK","EUR/SGD",
    "EUR/TRY","EUR/USD","EUR/ZAR","GBP/AUD","GBP/CAD",
    "GBP/CHF","GBP/JPY","GBP/NZD","GBP/USD","HKD/JPY",
    "HUF/JPY","ILS/JPY","MXN/JPY","NOK/JPY","NZD/CAD",
    "NZD/CHF","NZD/JPY","NZD/USD","PLN/JPY","SEK/JPY",
    "SGD/JPY","TRY/JPY","THB/JPY","USD/CAD","USD/CHF",
    "USD/HKD","USD/HUF","USD/JPY","USD/MXN","USD/PLN",
    "USD/SGD","USD/TRY","USD/ZAR","ZAR/JPY",
]
BB_PERIOD = 21
MIN_WALK = 9
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
 
 
def http_get_json(url, retries=3):
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code in (400, 404):  # 存在しないティッカーは再試行しない
                raise RuntimeError(f"not found: {url}")
            last = e
            time.sleep(1 + i)
        except Exception as e:
            last = e
            time.sleep(1 + i)
    raise RuntimeError(f"GET failed: {url}: {last}")
 
 
def fetch_daily_closes(yahoo_symbol):
    """date(str)->close の辞書を返す。取得不可なら None。"""
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_symbol}"
           f"?range=6mo&interval=1d")
    try:
        data = http_get_json(url)
    except Exception:
        return None
    try:
        res = data["chart"]["result"][0]
        ts = res["timestamp"]
        closes = res["indicators"]["quote"][0]["close"]
    except (KeyError, TypeError, IndexError):
        return None
    out = {}
    for t, c in zip(ts, closes):
        if c is None:
            continue
        d = datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime("%Y-%m-%d")
        out[d] = float(c)
    return out if len(out) >= BB_PERIOD + MIN_WALK + 2 else None
 
 
_usd_cache = {}
 
def usd_series(cur):
    """USD/cur の日足終値 (date->rate)。"""
    if cur == "USD":
        return "CONST1"
    if cur in _usd_cache:
        return _usd_cache[cur]
    s = fetch_daily_closes(f"USD{cur}=X")
    if s is None:
        inv = fetch_daily_closes(f"{cur}USD=X")
        if inv:
            s = {d: 1.0 / v for d, v in inv.items() if v}
    _usd_cache[cur] = s
    return s
 
 
def pair_closes(pair):
    """通貨ペアの日足終値リスト(日付昇順)。直接→USDクロス合成の順で取得。"""
    base, quote = pair.split("/")
    direct = fetch_daily_closes(f"{base}{quote}=X")
    if direct:
        return [direct[d] for d in sorted(direct)]
    sb, sq = usd_series(base), usd_series(quote)
    if sb is None or sq is None:
        return None
    if sb == "CONST1":  # USD/quote
        return [sq[d] for d in sorted(sq)] if isinstance(sq, dict) else None
    if sq == "CONST1":  # base/USD = 1/(USD/base)
        return [1.0 / sb[d] for d in sorted(sb) if sb[d]]
    days = sorted(set(sb) & set(sq))
    if len(days) < BB_PERIOD + MIN_WALK + 2:
        return None
    return [sq[d] / sb[d] for d in days if sb[d]]
 
 
def bollinger(closes, i, n=BB_PERIOD):
    """closes[i]時点のBB (mean, sigma)。母標準偏差。"""
    win = closes[i - n + 1: i + 1]
    m = sum(win) / n
    var = sum((x - m) ** 2 for x in win) / n
    return m, math.sqrt(var)
 
 
def detect(closes):
    """勝ちパターン1判定。'BUY' / 'SELL' / None"""
    n = len(closes)
    if n < BB_PERIOD + MIN_WALK + 1:
        return None
    last = n - 1
    m, s = bollinger(closes, last)
    lower, upper = m - s, m + s
 
    def walk(cond):
        cnt = 0
        j = last - 1
        while j >= BB_PERIOD - 1:
            mj, sj = bollinger(closes, j)
            if cond(closes[j], mj, sj):
                cnt += 1
                j -= 1
            else:
                break
        return cnt
 
    if closes[last] > lower and walk(lambda c, m_, s_: c < m_ - s_) >= MIN_WALK:
        return "BUY"
    if closes[last] < upper and walk(lambda c, m_, s_: c > m_ + s_) >= MIN_WALK:
        return "SELL"
    return None
 
 
def load_line_config():
    token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
    uid = os.environ.get("LINE_USER_ID")
    if token and uid:
        return token, uid
    cfg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "line_config.json")
    if os.path.exists(cfg):
        with open(cfg) as f:
            j = json.load(f)
        return j["channel_access_token"], j["user_id"]
    raise RuntimeError("LINE認証情報が見つかりません (env or line_config.json)")
 
 
def send_line(text):
    token, uid = load_line_config()
    body = json.dumps({"to": uid, "messages": [{"type": "text", "text": text[:4900]}]}).encode()
    req = urllib.request.Request(
        "https://api.line.me/v2/bot/message/push", data=body, method="POST",
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.status
 
 
def selftest():
    base = [100.0] * 30
    # 下落トレンド: 9本以上 -1σ下バンドウォーク → 直近で-1σ上抜け
    down = base + [100 - 0.8 * k for k in range(1, 15)]   # 急落継続 → 終値が-1σ下に張り付く
    down_rev = down[:-1] + [down[-2] + 4.0]               # 最後に反発
    assert detect(down) is None, "継続中はシグナルなしのはず"
    assert detect(down_rev) == "BUY", f"BUYのはず: {detect(down_rev)}"
    up = base + [100 + 0.8 * k for k in range(1, 15)]
    up_rev = up[:-1] + [up[-2] - 4.0]
    assert detect(up) is None
    assert detect(up_rev) == "SELL", f"SELLのはず: {detect(up_rev)}"
    flat = base + [100 + (0.1 if i % 2 else -0.1) for i in range(15)]
    assert detect(flat) is None
    print("selftest OK: BUY/SELL/None すべて期待通り")
 
 
def main():
    if "--selftest" in sys.argv:
        selftest(); return
    if "--test" in sys.argv:
        st = send_line("【テスト】勝ちパターン1通知の接続確認OK")
        print("LINE test sent, status", st); return
    dry = "--dry-run" in sys.argv
    jst = datetime.timezone(datetime.timedelta(hours=9))
    today = datetime.datetime.now(jst).strftime("%Y-%m-%d")
    buys, sells, errors = [], [], []
    for p in PAIRS:
        try:
            closes = pair_closes(p)
            if not closes:
                errors.append(p); continue
            sig = detect(closes)
            if sig == "BUY":
                buys.append(p)
            elif sig == "SELL":
                sells.append(p)
        except Exception:
            errors.append(p)
        time.sleep(0.3)  # rate limit配慮
    print(f"[{today}] BUY: {buys} SELL: {sells} 取得失敗: {errors}")
    if buys or sells:
        lines = [f"【鹿子木式 勝ちパターン1】{today} 日足"]
        if buys:
            lines.append("▲ 買いシグナル(下落→反転):\n" + "\n".join("  " + p for p in buys))
        if sells:
            lines.append("▼ 売りシグナル(上昇→反転):\n" + "\n".join("  " + p for p in sells))
        lines.append("※-1σ/+1σバンドウォーク9本以上→終値で±1σ回復")
        msg = "\n".join(lines)
        if dry:
            print("--- dry-run: 送信内容 ---\n" + msg)
        else:
            send_line(msg)
            print("LINE通知を送信しました")
    else:
        print("本日シグナルなし(通知なし)")
 
 
if __name__ == "__main__":
    main()
 
