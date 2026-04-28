#!/usr/bin/env python3
"""
将 .xcstrings 文件转换为 Swift 本地化扩展代码。

用法:
  python3 gen_swift_l10n.py <xcstrings文件>...  [--table Localizable]

示例:
  python3 gen_swift_l10n.py 基础信息.xcstrings
  python3 gen_swift_l10n.py *.xcstrings
  python3 gen_swift_l10n.py 弹窗.xcstrings --table PopupLocalizable
"""

import json
import re
import sys
import os


def to_swift_var_name(key):
    """按 '.' / '_' 分割全部转为小驼峰"""
    words = re.split(r'[._]', key)
    words = [w for w in words if w]
    if not words:
        return "unknownKey"
    return words[0].lower() + "".join(word.capitalize() for word in words[1:])


def xcstrings_to_swift(xcstrings_path, output_path=None, table="Localizable", swift_name=None):
    with open(xcstrings_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    strings = data.get("strings", {})
    if not strings:
        print(f"  ⚠️  {xcstrings_path}: 无内容，跳过")
        return

    # 扩展名来源优先级: 传入的 swift_name > 文件名提取 > 回退
    if swift_name:
        ext_name = swift_name
    else:
        base = os.path.splitext(os.path.basename(xcstrings_path))[0]
        ext_name = re.sub(r'[^a-zA-Z0-9_]', '', base)
        if not ext_name or not ext_name[0].isalpha():
            ext_name = "L10n" + ext_name
    ext_name = ext_name[0].upper() + ext_name[1:]  # 首字母大写

    if output_path is None:
        output_path = f"GSL10n{ext_name}+{table}.swift"

    lines = [
        "import Foundation",
        f"// Auto-generated from {os.path.basename(xcstrings_path)}",
        "",
        f"extension GSL10n{ext_name} {{",
        f"    private static var table: String {{ \"{table}\" }}",
        ""
    ]

    for key in sorted(strings.keys()):
        val_info = strings[key]
        localizations = val_info.get("localizations", {})
        zh = localizations.get("zh-Hans", {}).get("stringUnit", {}).get("value", "")
        # 使用 en 作为 comment，zh-Hans 作为 display
        en = localizations.get("en", {}).get("stringUnit", {}).get("value", "")
        comment = (en or zh).replace("\n", "\\n").replace("\r", "\\r")

        var_name = to_swift_var_name(key)

        lines.append(f"    /// {comment}")
        lines.append(f"    public static var {var_name}: String {{")
        lines.append(f"        return BB_Localized(\"{key}\", \"{comment}\", table)")
        lines.append(f"    }}")
        lines.append("")

    lines.append("}")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

    print(f"  ✅ {xcstrings_path} → {os.path.abspath(output_path)} ({len(strings)} keys)")


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    # 解析参数
    args = sys.argv[1:]
    table = "Localizable"
    files = []
    i = 0
    while i < len(args):
        if args[i] == "--table" and i + 1 < len(args):
            table = args[i + 1]
            i += 2
        else:
            files.append(args[i])
            i += 1

    if not files:
        print("❌ 请指定至少一个 .xcstrings 文件")
        sys.exit(1)

    for f in files:
        if not os.path.exists(f):
            print(f"  ⚠️  文件不存在: {f}")
            continue
        xcstrings_to_swift(f, table=table)

    print("\n✅ 全部完成")
