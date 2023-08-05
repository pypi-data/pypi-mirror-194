# A3RT-TalkPy
A3RT-TalkPyは、[A3RT TalkAPI](https://a3rt.recruit-tech.co.jp/product/talkAPI/)をPythonから利用するための、非公式ラッパーライブラリです。

[![Test Program Normal](https://github.com/nattyan-tv/a3rt-talkpy/actions/workflows/test-program-normal.yml/badge.svg?branch=master)](https://github.com/nattyan-tv/a3rt-talkpy/actions/workflows/test-program-normal.yml) [![Test Program Async](https://github.com/nattyan-tv/a3rt-talkpy/actions/workflows/test-program-async.yml/badge.svg?branch=master)](https://github.com/nattyan-tv/a3rt-talkpy/actions/workflows/test-program-async.yml)

[![Upload pypi package release](https://github.com/nattyan-tv/a3rt-talkpy/actions/workflows/python-publish.yml/badge.svg?branch=master)](https://github.com/nattyan-tv/a3rt-talkpy/actions/workflows/python-publish.yml)

# なぜ作ったのか？
俺が使う理由もなく無駄なライブラリをわざわざ作るわけがないだろう...

# A3RT TalkAPIとは？
[株式会社リクルート](https://www.recruit.co.jp/)が立ち上げた新規事業の１つである[A3RT](https://a3rt.recruit-tech.co.jp/)という機械学習API群のAPIの１つで、TalkAPIでは会話を行うことができます。  
詳しくは、[A3RT TalkAPIのページ](https://a3rt.recruit-tech.co.jp/product/talkAPI/)をご覧ください。

# A3RT-TalkPyとは？
上記で述べた、A3RT TalkAPIをPythonから利用するための、非公式ラッパーライブラリです。  
非同期による処理が可能です。

# 必要条件
このライブラリを使用するには、以下の環境が必要です。

- Python 3.10 以上
- TalkAPIのAPIキー （[こちら](https://a3rt.recruit.co.jp/product/talkAPI/)から発行できます。）

# インストール
```bash
pip install a3rt-talkpy
```

# 使い方
## 同期処理
```python
from a3rt_talkpy import TalkClient

API_KEY = "aaabbbcccddd"  # APIキーを入力してください。

client = TalkClient(API_KEY)

def main():
    query = input("> ")
    response = client.talk(query)
    print(response.reply)

if __name__ == "__main__":
    main()
```

## 非同期処理
```python
import asyncio
from a3rt_talkpy import AsyncTalkClient

API_KEY = "aaabbbcccddd"  # APIキーを入力してください。

client = AsyncTalkClient(API_KEY)

async def main():
    query = input("> ")
    response = await client.talk(query)
    print(response.reply)

if __name__ == "__main__":
    asyncio.run(main())
```

# ライセンス
[LICENSE](LICENSE)をご確認ください。

