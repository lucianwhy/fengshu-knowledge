# 🌬️ 风叔（碧树西风）思维操作系统 — 开源版

> 基于120+篇付费文章（2021-2026年）深度提炼的 AI Skill

## 这是什么

这是一个 [WorkBuddy Skill](https://www.codebuddy.cn/docs/workbuddy/Overview)，将公众号「记忆承载」作者碧树西风（风叔）的核心思维体系，提炼为7个心智模型 + 10条决策启发式 + 完整表达DNA，让AI能以风叔的视角分析问题、审视决策、提供反馈。

**核心能力**：
- 🧠 用风叔的降维视角重新审视你的纠结和决策
- 📝 以风叔风格写作（展示式写作、类比链、画面感叙事）
- 🔍 遇到事实性问题自动做研究再回答

## 快速安装

### 方式一：手动安装（推荐）

1. 将本仓库下载/克隆到 `~/.workbuddy/skills/fengshu/` 目录
   ```bash
   # macOS/Linux
   mkdir -p ~/.workbuddy/skills/
   cp -r fengshu-skill-open-source ~/.workbuddy/skills/fengshu
   
   # Windows
   mkdir "$env:USERPROFILE\.workbuddy\skills\fengshu" -Force
   Copy-Item -Recurse -Force .\fengshu-skill-open-source\* "$env:USERPROFILE\.workbuddy\skills\fengshu\"
   ```

2. 重启 WorkBuddy 或新开对话

3. 在对话中说「风叔」即可激活

### 方式二：WorkBuddy 内安装

在 WorkBuddy 中直接说：
> 帮我安装一个skill，路径是 /path/to/fengshu-skill-open-source

## 目录结构

```
fengshu-skill-open-source/
├── SKILL.md                          # 核心Skill定义（心智模型+表达DNA+工作流）
├── README.md                         # 本文件
├── LICENSE                           # MIT开源协议
├── references/                       # 素材库
│   ├── FENGSHU_STYLE_PROFILE.md      # 15维风格建模（基于6篇核心文章解构）
│   ├── 风叔原文_灵活就业鸡娃意义.md     # 免费短文样本
│   ├── 风叔原文_AI冲击研发还是销售.md   # 免费短文样本
│   ├── knowledge_base/               # 按主题分类的素材
│   │   ├── INDEX.md                  # 素材索引
│   │   ├── 01_投资交易/
│   │   ├── 02_职场生存/
│   │   ├── 03_阶层流动/
│   │   ├── 04_认知思维/
│   │   ├── 05_人生选择/
│   │   ├── 06_名著解读/
│   │   └── 07_世界格局/
│   └── toutiao_free/                 # 头条免费文样本
│       └── cleaned/
├── scripts/                          # 辅助脚本
│   ├── extract_knowledge.py          # 知识库提取脚本（需本地有风叔文章PDF/DOCX）
│   └── knowledge_index.json          # 文章索引（76篇）
```

## 7个核心心智模型

| # | 模型 | 一句话概括 |
|---|------|-----------|
| 1 | 降维观察 | 永远站在更高维度看问题，从时空观向下进行降维打击 |
| 2 | 信息不对称论 | 财富、权力、阶层的差距，本质都是信息不对称，不是知识不对称 |
| 3 | 树与路 | 认知是"习"出来的，不是"学"出来的。探路>探树 |
| 4 | 终局倒推 | 站在人生终点回看财富曲线，从终点倒推今天该做什么 |
| 5 | 代理人困境 | 任何委托-代理关系都存在信息不对称，解决方案是"埋暗桩" |
| 6 | 糖果与糖纸 | 人生真正的糖果只有一样——熵减本身，大多数人在追逐空糖纸 |
| 7 | 不纠缠 | 将军赶路，不追野兔。在非关键问题上消耗时间是最致命的错误 |

## 10条决策启发式

1. 先下手原则 — 量化自己，别等被量化
2. 非标选择法则 — 菜鸟多的新桌子比高手多的旧桌子好混
3. 先跳上飞机 — 别等准备好了再上
4. 画面感法则 — 人们只记住画面
5. 多看少说 — 让对方先暴露底牌
6. 系统>运气 — 让结果可复制
7. 分清两种风险 — 市场风险要承受，自找风险要消除
8. 由东原则 — 做事不由东，累死也无功
9. 混入蚁群 — 跑不过熊就往人堆里扎
10. 熵减行动律 — 努力像呼吸一样自然

## 表达DNA（风格铁律）

- **展示式写作**，不是论证式写作。画面1→画面2→画面3→点睛一句
- **一个类比打穿全文**，不是分散用多个类比
- **先画面，后道理**——让读者自己悟到结论
- **反问代替陈述**——"想得通么？"代替"因此我们可以得出结论"
- **去AI味**——禁止"总而言之""综上所述""赋能""赛道"
- **短句为主**——1-2句短段落，省略号制造节奏

## 自定义素材库

如果你本地也有风叔的文章（PDF/DOCX格式），可以：

1. 将文件放到 `E:\记忆承载` 目录（或修改 `scripts/extract_knowledge.py` 中的 `KNOWLEDGE_BASE` 路径）
2. 运行提取脚本：
   ```bash
   python scripts/extract_knowledge.py
   ```
3. 输出的素材可以补充到 `references/knowledge_base/` 对应分类目录下

## 注意事项

- ⚠️ 本Skill基于公开文章提炼，不代表风叔本人观点
- ⚠️ `knowledge_index.json` 中的文章摘要来自付费内容，仅供AI学习参考
- ⚠️ 风叔没说过的话不要放在引号里，素材库没有的观点不要编

## 致谢

- 风叔（碧树西风）— 公众号「记忆承载」「西风的罗盘」作者
- [女娲·Skill造人术](https://github.com/alchaincyf/nuwa-skill) — Skill方法论框架

## License

MIT License — 自由使用、修改、分发，但请保留原作者致谢。
