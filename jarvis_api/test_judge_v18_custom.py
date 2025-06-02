from logic import judge_memory_intent

test_cases = [
    "記録しといて",
    "これは記録しておくべきだな",
    "覚えておいて、次に活かす",
    "記憶しといてよ",
    "メモリしろ、絶対に",
    "ログに残せ、それで十分だ",
    "ただの雑談だけど",
    "これは残すやつだな",
    "記録って言ったっけ？",
    "捨ててもいいや"
]

for text in test_cases:
    result = judge_memory_intent(text)
    if result:
        print(f"✅ 判定: 『{text}』 → 保存対象: 『{result}』")
    else:
        print(f"🟡 スルー: 『{text}』 → 対象外")
