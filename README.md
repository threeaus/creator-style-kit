# Creator Style Kit

18 套 9:16 竖屏视频风格（HyperFrames），用于 AI 模型评测、教程、科普视频。每套风格都包含字体、配色、动效、音效和构图，内容一键套用。

本仓库同时是一个 Claude Code skill：

```bash
git clone https://github.com/threeaus/creator-style-kit.git
ln -s "$PWD/creator-style-kit" ~/.claude/skills/creator-style-kit
python3 creator-style-kit/scripts/fetch_fonts.py   # 下载 MiSans、优设标题黑（不随仓库分发）
```

- `SKILL.md`：选风格、出片流程（skill 入口）
- `STYLES.md`：风格目录，以及按视频类型选风格的对照表
- `REFERENCE.md`：标记、API、节奏与音效规则，以及如何新增风格

```bash
python3 scripts/list_styles.py                                   # 风格目录
python3 scripts/scaffold.py <style_id> <project> --content beats.json --init
python3 scripts/lookbook.py <project>                            # 全部风格样张
python3 scripts/sound_pass.py <project> renders/x.mp4            # 混音 + 质检
```

依赖：Python 3（PyYAML、fonttools、numpy）、Node（`npx hyperframes`）、ffmpeg、uv。

## 授权说明

- `vendor/sound-layer`：MIT，见其 LICENSE。
- `sfx/`：Kenney 与 uisfx 音效均为 CC0，见 `sfx/LICENSE-*.txt`。
- `fonts/src`：仓库内的字体均为 OFL-1.1。**MiSans、优设标题黑**是免费商用字体，但不允许再分发，所以不放进仓库，由 `scripts/fetch_fonts.py` 下载并校验 sha256。使用前请阅读各自的授权：[MiSans](https://hyperos.mi.com/font/)、[优设](https://www.uisdc.com/)。
- 样张中的数字均为示例数据，不是真实评测结果。
