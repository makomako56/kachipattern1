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
