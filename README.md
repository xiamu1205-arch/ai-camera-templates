# ai-camera-templates

「AI拍照」App 的在线姿势模板库。App 启动时从本仓库的 `templates.json` 拉取最新模板包（raw 链接），校验通过后替换内置库；拉取失败则用上次缓存，再不行回退 App 内置的 5 个种子模板。

更新模板 = 直接改 `templates.json` 提交，App 下次启动自动生效，不用发新版安装包。

## 格式

```json
{
  "version": 1,
  "updated": "2026-10-21",
  "templates": [
    {
      "id": "standing_natural",
      "name": "站立·自然",
      "category": "站姿",
      "points": {"0": [0.0, -1.52], "11": [0.30, -1.00], "...": "..."},
      "scored": [0, 11, 12],
      "framing": {"hipX": 0.5, "hipY": 0.49, "torso": 0.25},
      "tip": "自然站立，双臂放松垂在身侧"
    }
  ]
}
```

- `points`：MediaPipe BlazePose 33 点索引 → 规范空间坐标（原点=髋中心、单位=躯干长、面朝镜头，肩中心必须在 (0,-1)、髋中心必须在 (0,0)）。
- `scored`：参与对齐评分的点，必须都在 `points` 里（半身类不要把腿放进来）。
- `framing`：髋中心在画面中的目标位置 + 躯干占画面高度比。
- App 侧校验（与 `validate_templates.py` 同规则）：id 唯一、坐标范围、构图范围、肩/髋中心不变量；坏条目单条跳过，整包全坏才拒收。

提交前先跑：`python3 validate_templates.py templates.json`

## 首批模板的蓝本来源

姿势均转写自网上流行的拍照姿势参考（不是凭空发明）：

- 站姿：小红书热门合集（徐大囍Nancy、MUMU是木木、睿睿_wan 的姿势教学，经女子漾/udn、PopDaily 整理转载）——单手叉腰、双手叉腰脚内扣、腰间比耶、额头遮阳/敬礼、交叉腿、手举高、抱臂、捂嘴笑、手扶头发；英文经典人像 pose guide——The Lean（靠墙）、Looking Over Shoulder（回头看）。
- 半身：同上小红书合集 + Lemon8 半身人像合集——双手比心、脸颊比心、单手托腮、竖大拇指、脸旁比耶、捂嘴笑。
- 坐姿：英文 pose guide 的 Seated Cross-Leg / Knees to Chest / Mermaid，加小红书元气街拍合集（劉小瑜咯/不困妮妮/周多鱼）的盘腿坐。
- 全身：pose guide 的 The Step（迈步）/ Arms Above Head（伸懒腰），加单脚站立、踮脚伸手等社交平台常见动态姿势。
