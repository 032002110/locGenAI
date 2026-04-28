# locGenAI

Excel 多语言 → iOS `.xcstrings` + Swift 代码，一键自动生成。

## 快速开始

```bash
# 1. 克隆
git clone <repo-url> && cd locGenAI

# 2. 安装依赖
pip install -r requirements.txt

# 3. 设置 API Key
export DEEPSEEK_API_KEY=sk-xxx

# 4. 预览（不写文件，看前 5 行效果）
python3 locGenAI.py 你的文件.xlsx --test

# 5. 正式运行
python3 locGenAI.py 你的文件.xlsx

# 6. 同时生成 Swift 代码
python3 locGenAI.py 你的文件.xlsx --swift
```

## 环境变量

| 变量 | 必填 | 默认值 |
|------|:----:|--------|
| `DEEPSEEK_API_KEY` | 是 | - |
| `DEEPSEEK_BASE_URL` | 否 | `https://api.deepseek.com` |
| `DEEPSEEK_MODEL` | 否 | `deepseek-v4-flash` |

## Excel 格式

- 第 1 行：标题
- 第 2 行：列名（表头）
- 必须有「中文」列
- 前几列按位置自动识别为层级分组列
- 其他语言列按关键词自动识别（英文、日语、印度尼西亚语、繁体中文）

## 输出

| 文件 | 说明 |
|------|------|
| `xxx.xcstrings` | iOS String Catalog，每个 Sheet 一个文件 |
| `GSL10nXxx+Localizable.swift` | Swift 本地化扩展（需 `--swift`） |
| `translation_cache.json` | 翻译缓存，重复运行自动复用 |

## 特性

- 列结构全自动检测，兼容不同 Sheet 布局
- 多语言支持（中/英/日/印尼/繁体）
- 重复运行只处理新增行，已有 Key 自动跳过
- AI 翻译结果持久化缓存
- xcstrings 增量合并，不覆盖已有内容
