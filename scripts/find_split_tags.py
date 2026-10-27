"""列出台詞中間插入說話標記的段落（中斷式說話標記），附前段供判定。

用法：python find_split_tags.py <檔案> [--lang auto|zh|ja|en]
只找候選，作用是否成立依 SKILL.md 判定。
"""
import argparse
import re
import sys

PATTERNS = {
    # 「……」某人說，「……」（繁簡；「」、“”、半形引號皆可）
    "zh": re.compile(r'[」”"]([^「」“”"。！？\n]{0,12}?(?:說|说|道|問|问|喊|吼|傳來|传来|表示|指出|強調|强调)[^「」“”"。！？\n]{0,4}?)，[「“"]'),
    # 「……」と彼は言った。「……」／「……」ジェイコブが言った。「……」
    "ja": re.compile(r'」([^「」\n]{0,20}?(?:言っ|言う|言い|尋ね|答え|呟い|つぶやい|叫ん|続け|声が)[^「」\n]{0,8}?)[。、]「'),
    # "…," she said, "…"／"…," Corone said. "…"
    "en": re.compile(r'[,?!…—]["”]\s+([^"“”\n]{1,40}?\b(?:said|says|asked|replied|added|whispered|shouted|called|muttered|continued|answered|told|noted|explained)\b[^"“”\n]{0,30}?)[,.]\s+["“]'),
}


def detect_lang(text):
    if re.search(r"[぀-ヿ]", text):
        return "ja"
    if len(re.findall(r"[一-鿿]", text)) > len(re.findall(r"[A-Za-z]", text)):
        return "zh"
    return "en"


def find_split_tags(lines, lang):
    pat = PATTERNS[lang]
    paragraphs = [(no, line.strip()) for no, line in enumerate(lines, 1) if line.strip()]
    found = []
    for i, (no, text) in enumerate(paragraphs):
        for tag in pat.findall(text):
            prev = paragraphs[i - 1][1] if i else ""
            found.append((no, tag.strip(), prev))
    return found


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--lang", default="auto", choices=["auto", "zh", "ja", "en"])
    args = ap.parse_args()
    with open(args.path, encoding="utf-8") as f:
        text = f.read()
    lang = detect_lang(text) if args.lang == "auto" else args.lang
    found = find_split_tags(text.split("\n"), lang)
    print(f"中斷式說話標記 {len(found)} 處（{lang}）")
    for no, tag, prev in found:
        print(f"  - L{no} {tag} ← 前段：{prev[:30]}")


if __name__ == "__main__":
    main()
