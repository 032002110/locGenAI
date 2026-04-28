# locGenAI 使用说明

Excel 多语言文案 → iOS 本地化文件 + Swift 代码，一键生成。

---

## 一、环境准备（首次使用，仅需一次）

### 1. 安装 Python

macOS 自带 Python 3，终端输入 `python3 --version` 确认版本 ≥ 3.9 即可。

### 2. 下载脚本

```bash
git clone https://github.com/032002110/locGenAI.git
cd locGenAI
```

### 3. 安装依赖

```bash
pip3 install -r requirements.txt
```

### 4. 配置 API Key

在终端执行（每次打开新终端窗口都要执行，或写入 `~/.zshrc`）：

```bash
export DEEPSEEK_API_KEY=sk-你的密钥
```

> 密钥找项目负责人获取。也可以换成其他兼容 OpenAI 接口的服务，设置 `DEEPSEEK_BASE_URL` 和 `DEEPSEEK_MODEL` 即可。

---

## 二、使用方式

### 基础用法

```bash
# 预览模式（只跑前 5 行，不改任何文件）
python3 locGenAI.py 国际化多语言.xlsx --test

# 正式运行（生成 Key + xcstrings）
python3 locGenAI.py 国际化多语言.xlsx

# 正式运行 + 生成 Swift 代码
python3 locGenAI.py 国际化多语言.xlsx --swift
```

### Excel 文件要求

| 行 | 内容 |
|----|------|
| 第 1 行 | 标题（可合并单元格） |
| 第 2 行 | 列名（表头） |
| 第 3 行起 | 数据 |

- **必须**有一列的列名包含「中文」
- 支持的语言列会**自动识别**：英文、日语、印度尼西亚语、繁体中文
- 层级列自动按**前两列位置**识别，无需指定列名

---

## 三、输出文件

| 文件 | 说明 |
|------|------|
| `xxx.xcstrings` | iOS String Catalog，每个 Sheet 一个文件 |
| `GSL10nXxx+Localizable.swift` | Swift 本地化扩展代码（需 `--swift`） |
| `translation_cache.json` | 翻译缓存（自动复用，不要删除） |

> 所有输出文件在 `locGenAI` 目录下。

---

## 四、日常使用场景

### 场景 1：Excel 新增了文案

产品在表格里加了新行 → 直接重新跑脚本：

```bash
python3 locGenAI.py 国际化多语言.xlsx --swift
```

已有 Key 的行**自动跳过**，只处理新增行。

### 场景 2：只更新 Swift 代码

xcstrings 已经有内容，只想重新生成 Swift：

```bash
python3 gen_swift_l10n.py *.xcstrings
```

### 场景 3：换了 Excel 文件

```bash
python3 locGenAI.py 新的文件.xlsx --test   # 先预览
python3 locGenAI.py 新的文件.xlsx --swift   # 确认无误正式跑
```

---

## 五、Key 命名规则

```
page_key.ui_key.text_key
```

例如：`general.page_loading.loading`

- 每个 Sheet 生成独立的 xcstrings 文件，文件名即命名空间
- AI 自动将中文文案压缩为 ≤ 3 个英文单词，下划线连接
- Sheet 内 Key 保证唯一，重复自动追加 `_2`、`_3`

---

## 六、常见问题

**Q: 提示 "找不到中文列"？**
Excel 表头（第 2 行）必须有一列包含「中文」二字。

**Q: 提示 "请设置环境变量 DEEPSEEK_API_KEY"？**
每次新开终端需要重新 `export`，或写入 `~/.zshrc` 一劳永逸。

**Q: 某行不想生成 Key？**
把该行的 Key 列清空，脚本就会重新生成。

**Q: 想用其他 AI 服务？**
```bash
export DEEPSEEK_BASE_URL=https://api.openai.com/v1
export DEEPSEEK_MODEL=gpt-4o
```

---

## 七、项目地址

https://github.com/032002110/locGenAI

有问题联系 @3c
