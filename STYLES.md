# Creator Style Kit · 风格目录（18 套）

同一套标记（`.csk-chapter / .csk-head / .csk-list / .csk-stat`），同一组调用（`kit.textIn / emphasis / number / list / transition / ambient`），换 `data-csk` 就换整套字体、配色、动效和音效。

已做成 Claude Code skill：`~/.claude/skills/creator-style-kit` → 本文件夹（`SKILL.md` 选风格流程，`REFERENCE.md` 标记/API/新增风格）。做视频时直接说「用 creator-style-kit 选个风格」即可。

```bash
python3 scripts/list_styles.py [<id>]                              # 风格目录 / 单个风格的完整说明
python3 scripts/scaffold.py <style_id> <project> --content beats.json [--init]   # 内容 → 成品场景
python3 scripts/build_style.py <style_id|all> <project_dir>     # 编译 token + skin + 子集化字体 + 音效
python3 scripts/lookbook.py <project_dir> [--from-order 7]       # 生成样张（--only a,b 只渲染指定风格）
python3 scripts/sound_pass.py <project> renders/x.mp4 [--voice vo.wav] [--music bed.wav]  # 渲染后：混音 + 响度 + 音效质检
```

节奏与音效由 `scripts/compose.py` 统一计算：每段时长 = 该风格的入场时长 + 阅读停留（关键数字定格 ≥ 2.2 秒），一次只动一件事；音效按风格的 `sound.rules` 限密度，列表只配一声，揭晓音落在数字定格那一帧，并按音效峰值对齐。

## 按视频类型选风格

| 场景 | 首选 | 备选 |
|---|---|---|
| 模型评测 · 跑分揭晓 | 数据新闻 data-journal | 评测仪表 benchmark-hud |
| 新旧版本 / 多模型对比 | 数据新闻 data-journal | 仪器面板 instrument-panel |
| 价格 / 速度 / 上下文等参数 | 仪器面板 instrument-panel | 瑞士网格 swiss-grid |
| 新模型发布开场 · 片头 | 弥散玻璃 frosted-aurora | 暗场发布会 dark-keynote / 粒子星云 particle-field |
| 论文 / 技术报告解读 | 论文图表 paper-figure | 数学动画 manim-morph |
| 原理科普（注意力、推理、嵌入） | 数学动画 manim-morph | 粒子星云 particle-field |
| 架构 / Agent 工作流 / 机制 | 蓝图线稿 blueprint | 等轴架构 isometric-stack |
| 分层结构（技术栈、上下文构成） | 等轴架构 isometric-stack | 蓝图线稿 blueprint |
| 概念拆解 · 三要素框架 | 包豪斯构成 bauhaus-geometry | 瑞士网格 swiss-grid |
| Claude / Opus 专题 · 观点口播 | 暖陶书卷 clay-serif | 报刊纸感 editorial-paper |
| 工具实操 / 录屏教程 | 终端控制台 dev-console | 仪器面板 instrument-panel |
| 新手教程 · 亲切讲解 | 暖调手账 warm-notebook | 暖陶书卷 clay-serif |
| 人文 / 历史 / 节日特辑 | 水墨留白 ink-wash | 报刊纸感 editorial-paper |
| 前 3 秒钩子 · 章节卡 | 海报撞色 poster-kinetic | 包豪斯构成 bauhaus-geometry |

一支视频建议 **1 套主风格 + 1 套点缀风格**（例：评测视频用 data-journal 做主体，开头用 frosted-aurora，代码段落切 dev-console）。

## 全部风格

| # | id | 中文名 | 底色 / 强调 | 文字入场 | 强调 | 数字 | 列表 | 转场 |
|---|---|---|---|---|---|---|---|---|
| 01 | dark-keynote | 暗场发布会 | 近黑 / 青柠 | blur-rise | accent-glint | scramble-lock | rise-dim | light-sweep |
| 02 | swiss-grid | 瑞士网格 | 纸灰 / 信号红 | clip-rise | knife-underline | step-climb | index-snap | column-wipe |
| 03 | editorial-paper | 报刊纸感 | 米纸 / 荧光黄 | paper-slap | highlighter | stamp | index-cards | sheet-wipe |
| 04 | warm-notebook | 暖调手账 | 奶油 / 橘红 | spring-pop | scribble | bubble-count | sticker-cards | card-zoom |
| 05 | poster-kinetic | 海报撞色 | 黑/荧光/蓝 轮换 | drop-letters | recolor-char | odometer | slam-alternate | ground-slats |
| 06 | dev-console | 终端控制台 | GitHub 暗 / 绿 | type-scramble | selection | scramble-lock | terminal-lines | glitch-slice |
| 07 | **data-journal** | 数据新闻 | FT 三文鱼纸 / 牛津蓝 + 酒红 | clip-rise | knife-underline | **bar-grow** | **bar-chart** | **edge-wipe** |
| 08 | **paper-figure** | 论文图表 | 白纸 / matplotlib 蓝 | **fade-up** | **boxed** | **decimal-tracker** | **fade-rows** | **dip** |
| 09 | **manim-morph** | 数学动画 | 纯黑 / 蓝·绿·黄（语义色） | **write** | **circumscribe** | decimal-tracker | **grow-in** | dip |
| 10 | **blueprint** | 蓝图线稿 | 普鲁士蓝 / 浅青 | **draft-in** | **dimension** | step-climb | **leader-lines** | **draft-wipe** |
| 11 | **benchmark-hud** | 评测仪表 | 近黑青 / 琥珀（仅锁定值） | **scan-in** | **bracket-lock** | **gauge** | **readout** | edge-wipe |
| 12 | **particle-field** | 粒子星云 | 深空黑 / 紫 | **converge** | **halo** | **particle-form** | **converge-rows** | **particle-warp** |
| 13 | **frosted-aurora** | 弥散玻璃 | 暗底极光 / 青→紫 | blur-rise | **gradient-sweep** | **soft-count** | **glass-cards** | **frost** |
| 14 | **isometric-stack** | 等轴架构 | 浅灰蓝 / 靛蓝 | clip-rise | knife-underline | soft-count | **iso-stack** | **iso-slide** |
| 15 | **bauhaus-geometry** | 包豪斯构成 | 米白 / 红黄蓝 | **slide-block** | **shape-mark** | **geo-count** | **geo-blocks** | **shape-iris** |
| 16 | **ink-wash** | 水墨留白 | 宣纸 / 胭脂 + 朱砂印 | **ink-bleed** | **seal-stamp** | **ink-count** | **ink-rows** | **ink-spread** |
| 17 | **clay-serif** | 暖陶书卷 | 象牙白 / 黏土橙 | fade-up | **underline-soft** | soft-count | fade-rows | dip |
| 18 | **instrument-panel** | 仪器面板 | 铝灰 / 信号橙 | **segment-on** | **led-tag** | **segment** | **key-press** | **shutter** |

构图按风格区分（`style.yaml` 的 `layout`，原型定义在 `runtime/kit.css`）：
- **居中**：暗场发布会、暖调手账、论文图表、数学动画、评测仪表、粒子星云、弥散玻璃
- **偏下留白**：报刊纸感、蓝图线稿、暖陶书卷；水墨留白的标题靠右
- **上下分割**（编号顶天、标题落地）：瑞士网格、海报撞色、包豪斯构成
- **文章式靠上**：数据新闻、仪器面板、终端控制台、等轴架构

加粗 = 2026-10 新增的运行时动效。每套风格的「不要做什么」写在各自 `styles/<id>/style.yaml` 的 `not:` 里，动手前先读一遍——高级感主要来自克制。

## 新增风格的来源

- 从「24 种风格」清单中选出：粒子 → 粒子星云，等轴 2.5D → 等轴架构，弥散玻璃 + 液态流动 → 弥散玻璃，赛博 HUD → 评测仪表（克制版），几何构成 → 包豪斯构成，线条动画 → 蓝图线稿，形变动画 → 数学动画，国风水墨 → 水墨留白。
- 未选：黏土定格、复古合成波、纸艺立体书、酸性 Y2K、综艺花字、3D 渲染、像素风、拼贴剪贴、漫画分镜、手绘动画、水彩、快闪字（偏娱乐或需要大量手绘/3D 素材，与评测/教程的高级感不符）；故障艺术、贴纸科普 已分别被 终端控制台、暖调手账 覆盖。
- 上网调研新增：数据新闻（FT / Economist / OWID）、论文图表（arXiv / Distill）、暖陶书卷（Anthropic 公开色板气质，不使用任何 Logo）、仪器面板（Teenage Engineering / Braun）。
- 调研笔记：`references/research/opus55_styles.md`（Opus 5.5 风格生态：lemo-opuscar 43 套 STYLE.md 等）、`references/research/premium_styles.md`（色值、字体授权与下载地址）。

## 新增字体（均可免费商用）

| 字体 | 授权 | 用于 |
|---|---|---|
| CMU Serif（Roman / Italic / Bold） | OFL-1.1 | 论文图表、数学动画 |
| Newsreader（静态实例 opsz72 / 500） | OFL-1.1 | 数据新闻 |
| Fraunces（静态实例 opsz144 / 600 / SOFT50） | OFL-1.1 | 暖陶书卷 |
| Space Grotesk 500 / 700 | OFL-1.1 | 评测仪表、粒子、玻璃、等轴 |
| Space Mono Bold | OFL-1.1 | 评测仪表、包豪斯、仪器面板 |
| Doto（点阵，静态实例 900） | OFL-1.1 | 仪器面板数字 |
| 马善政楷书 Ma Shan Zheng | OFL-1.1 | 水墨标题 |
| 思源宋体 Noto Serif SC Regular / SemiBold | OFL-1.1 | 数据新闻、论文、数学、暖陶 |
| 思源黑体 Noto Sans SC Light / Medium | OFL-1.1 | 玻璃、蓝图、粒子 |

## 样张数据

样张里的「87.6% 一次通过 / 92 · 78 · 64」均为**示例数据**，画面上已标注，仅用于展示排版，请勿当作真实评测结果引用。
