# Day 6 幻灯片配图 —— AI 图像生成提示词集

**项目**：可重复使用运载火箭 AI 协同设计暑期课程（11–20 July 2026）
**交付日**：Day 6 · 2026年7月16日
**配套文件**：`presentations/day06_reusability.pptx`（15 页）、`docs/reports/day06_reusability_strategy.md`

---

## 1. 使用说明（生成通则）

1. **示意图已齐备，本文件仅覆盖"渲染/写实类"配图。** 四幅技术示意图（飞行序列、负载路径、Δv 闭合瀑布图、悬停猛击点火窗口）已作为矢量 SVG 完成并嵌入 PPT（位于 `assets/diagrams/`，PNG 渲染同源）。本文件为剩余 6 幅写实配图提供提示词。
2. **提示词中英双列**：图像生成模型（Midjourney / DALL·E / Stable Diffusion / Flux 等）对英文提示词响应更稳定，**建议直接使用英文版**；中文版供人工校对语义。
3. **通用负面提示词（negative prompt）**——所有图统一附加：
   > `text, letters, watermark, logo, brand name, flag insignia, company insignia, people faces, distorted rocket, extra engines, cartoon, low detail, oversaturated`
   > （不出现文字、水印、商标、国旗/公司徽标——避免与 SpaceX / CASC 实际涂装混淆；本项目为通用药代构型。）
4. **通用风格锚点**（附加在每条提示词末尾，保持全套视觉一致）：
   > `photorealistic, cinematic industrial photography, muted navy-and-steel color palette with restrained orange accents, high dynamic range, 8k detail`
5. **构型一致性**（重要，避免穿帮）：一级助推器统一描述为 —— 白/浅灰箭体、顶部四片钛栅格翼、顶部四只上置捕获耳（无着陆腿）、尾部九台发动机喷口成排（3×3 布局可见 3–4 台即可）、箭体带再入烧蚀的轻微熏黑。
6. **画幅**：封面图 16:9（1920×1080 或更高）；插图 3:2 或 4:3；竖幅特写 2:3。生成后裁剪至幻灯片版心；深色场景置于标题页时需叠加 `rgba(22,50,79,0.55)` 藏青蒙版保证白字可读。

---

## 2. 配图清单与落位

| 编号 | 图名 | 建议落位（幻灯片） | 画幅 |
|---|---|---|---|
| IMG-01 | 远海网/绳捕获主视觉（英雄图） | 第 1 页（标题页背景） | 16:9 |
| IMG-02 | 捕获船"立体捕获架"海上作业 | 第 7 页（外部锚点区） | 3:2 |
| IMG-03 | 悬停猛击末段点火渲染 | 第 10 页（右侧/整幅备选） | 4:3 |
| IMG-04 | 捕获耳磨损靴特写（工程细节） | 第 11 页（角落插图） | 2:3 |
| IMG-05 | FBG 光纤应变传感贴片特写 | 第 14 页（角落插图） | 2:3 |
| IMG-06 | 复飞周转：船队返港与检查厂房 | 第 13 页（流程图下方横幅） | 16:9 |

---

## 3. 逐条提示词

### IMG-01 · 远海网/绳捕获主视觉（标题页英雄图）

**中文**：
> 黄昏远海，一艘大型海上回收船，甲板后方矗立升高的立体方框架，架间张紧多股钢索形成捕获网面；一枚一级运载火箭助推器（白色箭体、顶部四片栅格翼张开、四只上置捕获耳、无着陆腿、尾部喷口带轻微熏黑）正垂直悬停在框架上方数米处，单台发动机长焰向下，尾焰照亮海面水雾；助推器捕获耳与最上方一根钢索即将接触；低空俯视与平视结合的广角构图，浪高约一米，天空藏青与橙红渐变，远景海天线上有第二艘警戒船剪影。照片级写实，电影感工业摄影，藏青-钢灰主色调加克制橙色点缀，高动态范围，8K 细节。

**English (recommended)**：
> A first-stage rocket booster hovering vertically a few meters above a raised cubic steel catching frame mounted on a large ocean recovery ship at dusk; multiple tensioned steel cables span the frame like a net, and the booster's four upward-facing catch lugs are about to engage the top cable; white rocket body with four deployed grid fins at the top, no landing legs, single engine long flame pointing downward, exhaust plume illuminating sea spray; light scorch marks near the base; wide-angle cinematic composition between low-aerial and eye level, one-metre swell, deep navy-to-orange gradient sky, silhouette of a second guard ship on the horizon — photorealistic, cinematic industrial photography, muted navy-and-steel color palette with restrained orange accents, high dynamic range, 8k detail

**负面**：见 §1.3 通用负面提示词。
**版式备注**：用作第 1 页全幅背景；叠加藏青蒙版（透明度 55%）后放置白色标题文字；船与火箭置于画面右 2/3，左侧留白供标题。

---

### IMG-02 · 捕获船"立体捕获架"海上作业（外部锚点插图）

**中文**：
> 白天南海，一艘改装工程回收船，船尾甲板上为三层楼高的立方体钢框架捕获架，四角立柱间张紧可动钢索，框架侧面有缓冲阻尼滑车与绞盘；甲板前部为控制室与天线罩；海况 3–4 级，船体轻微横摇，两名穿橙色工作服（无面部细节）的船员在左舷巡视；侧前方 45° 中焦视角，气压晴朗的高对比日光。照片级写实，电影感工业摄影，藏青-钢灰主色调加克制橙色点缀，高动态范围，8K 细节。

**English (recommended)**：
> A converted offshore engineering vessel in the South China Sea by day, its aft deck dominated by a three-storey cubic steel catching frame with movable tensioned cables strung between corner posts; damping trolleys and winches visible on the frame sides; forward deck carries a control room and radomes; sea state 3–4 with slight roll, two crew in orange coveralls (faces not visible) walking the port rail; 45-degree front-quarter view at medium focal length, crisp high-contrast daylight — photorealistic, cinematic industrial photography, muted navy-and-steel color palette with restrained orange accents, high dynamic range, 8k detail

**负面**：见 §1.3。
**版式备注**：第 7 页"长征十号B"卡片右半部；裁剪为 3:2。用于直观说明"升高立体架＋张紧钢索"概念，不可标注真实船名。

---

### IMG-03 · 悬停猛击末段点火渲染（第 10 页配图）

**中文**：
> 夜间低空，抓拍一级助推器动力下降的最后数秒：单台中心发动机全焰，马赫环清晰可见，燃气冲击海面形成放射状雾环；箭体近乎垂直、轻微倾角 <2°，四片栅格翼在顶部微偏；背景为捕获船框架的轮廓（带航行灯）在右侧远处，左侧海天漆黑；慢门稍拉出的火焰丝滑质感与机身冷冽金属反光对比；低机位仰拍。照片级写实，电影感工业摄影，藏青-钢灰主色调加克制橙色点缀，高动态范围，8K 细节。

**English (recommended)**：
> Night-time low-altitude shot of a rocket first stage in the final seconds of a powered descent (hover-slam): single center engine at full flame with visible Mach diamonds, exhaust impinging on the ocean surface forming a radial spray ring; booster nearly vertical with under-two-degree tilt, four grid fins slightly deflected at the top; the silhouette of a catching-frame ship with navigation lights far right, black sea-sky horizon left; slight long-exposure silkiness in the flame against crisp cold metal reflections on the fuselage; low-angle upward camera — photorealistic, cinematic industrial photography, muted navy-and-steel color palette with restrained orange accents, high dynamic range, 8k detail

**负面**：见 §1.3。
**版式备注**：第 10 页现有 SVG 点火窗口图的替换/并置备选（若追求写实演示效果）；4:3，置于右侧栏。

---

### IMG-04 · 捕获耳磨损靴特写（第 11 页工程细节）

**中文**：
> 微距工程摄影：火箭顶部捕获耳（锻铝合金基体）外覆可更换的牺牲性磨损靴（烧结合金/工程陶瓷复合，带螺栓固定与倒角），靴面有数次捕获滑移留下的均匀磨痕；背景虚化的箭体白色蒙皮与一枚栅格翼根部；棚拍无影灯与一枚侧逆光勾勒金属质感，景深极浅；画面右下角留出空白。照片级写实，电影感工业摄影，藏青-钢灰主色调加克制橙色点缀，高动态范围，8K 细节。

**English (recommended)**：
> Macro engineering photograph of a rocket catch lug: a forged aluminium-alloy lug base clad in a replaceable sacrificial wear boot (sintered-alloy / engineered-ceramic composite) with visible bolt fasteners and chamfers; the boot surface shows even scoring marks from several capture-slip engagements; shallow depth of field with blurred white fuselage skin and the root of one grid fin behind; soft studio key light plus one rim light tracing the metal edges; negative space in the lower-right corner — photorealistic, cinematic industrial photography, muted navy-and-steel color palette with restrained orange accents, high dynamic range, 8k detail

**负面**：见 §1.3。
**版式备注**：第 11 页负载路径 SVG 的角落小图；2:3 竖幅，宽不超过版心 25%；用于说明"磨损靴为耗材、每次检查更换"。

---

### IMG-05 · FBG 光纤应变传感贴片特写（第 14 页工程细节）

**中文**：
> 微距：一段直径约 0.25 mm 的光纤布拉格光栅应变传感链路，以航空胶粘贴合在捕获环的环形锻件内侧面，尾端接入细铠装光缆；金属表面有激光刻蚀的基准标记（无文字）；极浅景深，冷白实验室照明，背景虚化为栅格阵列工装；整体呈银蓝冷色调。照片级写实，电影感工业摄影，藏青-钢灰主色调加克制橙色点缀，高动态范围，8K 细节。

**English (recommended)**：
> Macro photograph of a fibre-Bragg-grating strain-sensing fibre, about 0.25 mm in diameter, bonded with aerospace adhesive along the inner face of a capture-ring ring forging, the pigtail transitioning into a thin armoured cable; the metal surface carries laser-etched fiducial marks (no readable text); very shallow depth of field, cool white laboratory lighting, background blurred into a grid of assembly tooling; overall silver-blue cool tone — photorealistic, cinematic industrial photography, muted navy-and-steel color palette with restrained orange accents, high dynamic range, 8k detail

**负面**：见 §1.3（特别提醒：避免生成带文字的刻度尺/标签）。
**版式备注**：第 14 页失效模式表（F-4 非对称挂接 / FBG 见证行）角落小图；2:3 竖幅。

---

### IMG-06 · 复飞周转：船队返港与检查厂房（第 13 页横幅）

**中文**：
> 宽幅分割感画面：左侧远景为回收船载运竖直助推器进港（黄昏、港塔吊剪影），右侧近景为恒温检查厂房内，平躺的一级助推器旁，两名技师（无面部）使用超声相控阵设备检查捕获环焊缝，地面黄色标线、顶部行吊；两侧以景深自然过渡，整体写实迎合作战图风格但克制不科幻；横幅构图。照片级写实，电影感工业摄影，藏青-钢灰主色调加克制橙色点缀，高动态范围，8K 细节。

**English (recommended)**：
> Wide banner composition with a natural split feel: left distance shows a recovery ship carrying a vertical rocket booster entering harbour at dusk, gantry-crane silhouettes; right foreground shows a climate-controlled inspection hangar where the horizontal booster lies beside two technicians (faces not visible) running phased-array ultrasonic inspection on the capture-ring weld, yellow floor markings and an overhead crane; depth of field transitions naturally across the split; grounded and documentary in tone, restrained rather than sci-fi — photorealistic, cinematic industrial photography, muted navy-and-steel color palette with restrained orange accents, high dynamic range, 8k detail

**负面**：见 §1.3。
**版式备注**：第 13 页流程 chevron 之下、指标表之上的横幅；裁剪 16:4.5 左右；必要时加深 30% 蒙版。

---

## 4. 生成后处理清单

1. **一致性复查**：逐图核对构型六要素（白色箭体／四栅格翼／四捕获耳／无着陆腿／九机尾部布局／轻度熏黑）。任何一张出现着陆腿或星舰式黑色隔热瓦箭体即弃用重生。
2. **版权与肖像**：确认无真实徽标、船名、国旗、可读文字、可辨识人脸。
3. **压缩**：导出 JPEG（质量 85）或 PNG-24；单幅 ≤ 600 KB；嵌入前用 `python-pptx` 重插或手动粘贴于占位矩形。
4. **溯源登记**：在 PPT 备注页记录"AI 生成配图 + 生成日期 + 所用提示词编号（IMG-0x）"，与课程 AI 工程日志（blueprint §3 要求）保持一致。
5. **免责声明**（建议加入第 1 页备注）：写实配图为 AI 生成的概念渲染，非任何真实型号的真实影像。

---

*文件结束 · 与 `presentations/day06_reusability.pptx`、`docs/reports/day06_reusability_strategy.md` 配套使用*
