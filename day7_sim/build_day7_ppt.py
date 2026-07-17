# -*- coding: utf-8 -*-
"""Build Day 7 PPT deck — AI辅助轨迹优化与设计迭代, fully Simplified Chinese."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

NAVY   = RGBColor(0x16, 0x32, 0x4F)
BLUE   = RGBColor(0x2E, 0x5E, 0x8C)
ORANGE = RGBColor(0xE0, 0x56, 0x1E)
RED    = RGBColor(0xC0, 0x39, 0x2B)
GREEN  = RGBColor(0x2E, 0x8B, 0x57)
GRAY   = RGBColor(0x5B, 0x66, 0x70)
LIGHT  = RGBColor(0xF2, 0xF5, 0xF9)
CARD   = RGBColor(0xEE, 0xF3, 0xF8)
PEACH  = RGBColor(0xFB, 0xEE, 0xE6)
MINT   = RGBColor(0xE8, 0xF2, 0xEC)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
DARK   = RGBColor(0x33, 0x47, 0x5B)
FONT   = "Microsoft YaHei"

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
PAGE = [0]

def _set_font(run, size, bold=False, color=DARK, italic=False):
    f = run.font; f.size = Pt(size); f.bold = bold; f.italic = italic
    f.color.rgb = color; f.name = FONT
    rPr = run._r.get_or_add_rPr()
    from pptx.oxml.ns import qn
    for tag in ("a:ea", "a:cs"):
        e = rPr.find(qn(tag))
        if e is None:
            e = rPr.makeelement(qn(tag), {}); rPr.append(e)
        e.set("typeface", FONT)

def rect(slide, x, y, w, h, fill, line=None, lw=1.0, shadow=False, round_=False):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if round_ else MSO_SHAPE.RECTANGLE,
                                 Inches(x), Inches(y), Inches(w), Inches(h))
    if round_:
        try: shp.adjustments[0] = 0.06
        except Exception: pass
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else: shp.line.color.rgb = line; shp.line.width = Pt(lw)
    shp.shadow.inherit = False
    return shp

def text(slide, x, y, w, h, lines, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT, space_after=2):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Pt(2); tf.margin_top = tf.margin_bottom = Pt(1)
    first = True
    for ln in lines:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = align; p.space_after = Pt(space_after)
        runs = ln if isinstance(ln, list) else [ln]
        for (t, size, bold, color) in runs:
            r = p.add_run(); r.text = t; _set_font(r, size, bold, color)
    return tb

def bullet_block(slide, x, y, w, h, items, size=15, color=DARK, gap=6, mark_color=ORANGE):
    lines = []
    for it in items:
        if isinstance(it, tuple):
            lines.append([("▪ ", size, True, mark_color), (it[0], size, True, NAVY), (it[1], size, False, color)])
        else:
            lines.append([("▪ ", size, True, mark_color), (it, size, False, color)])
    return text(slide, x, y, w, h, lines, space_after=gap)

def header(slide, title, sub=None):
    rect(slide, 0, 0, 13.333, 0.92, NAVY)
    rect(slide, 0, 0.92, 13.333, 0.045, ORANGE)
    text(slide, 0.55, 0.12, 11.5, 0.7, [(title, 27, True, WHITE)])
    if sub:
        text(slide, 9.2, 0.30, 3.6, 0.5, [(sub, 12, False, RGBColor(0xBF,0xD7,0xEA))], align=PP_ALIGN.RIGHT)
    PAGE[0] += 1
    rect(slide, 0, 7.18, 13.333, 0.32, LIGHT)
    text(slide, 0.55, 7.19, 9.5, 0.3,
         [("可重复使用运载火箭 AI 协同设计暑期课程 · Day 7 AI辅助优化与设计迭代 · 2026-07-17", 10.5, False, GRAY)])
    text(slide, 12.2, 7.19, 0.7, 0.3, [(str(PAGE[0]), 10.5, False, GRAY)], align=PP_ALIGN.RIGHT)

def style_cell(cell, txt, size=12.5, bold=False, color=DARK, fill=None, align=PP_ALIGN.LEFT,
               anchor=MSO_ANCHOR.MIDDLE):
    cell.margin_left = Pt(5); cell.margin_right = Pt(4)
    cell.margin_top = Pt(1.5); cell.margin_bottom = Pt(1.5)
    cell.vertical_anchor = anchor
    if fill is not None:
        cell.fill.solid(); cell.fill.fore_color.rgb = fill
    tf = cell.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = align
    for i, (t, b, c) in enumerate(txt):
        r = p.add_run(); r.text = t; _set_font(r, size, b, c)

def make_table(slide, x, y, w, h, data, col_w=None, header_fill=NAVY, body_size=12.5,
               head_size=13, band=True, first_col_bold=False):
    rows, cols = len(data), len(data[0])
    gfx = slide.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(h))
    tbl = gfx.table
    tbl.first_row = False; tbl.horz_banding = False
    if col_w:
        total = sum(col_w)
        for i, cw in enumerate(col_w):
            tbl.columns[i].width = Emu(int(Inches(w) * cw / total))
    for ri, row in enumerate(data):
        for ci, val in enumerate(row):
            cell = tbl.cell(ri, ci)
            if ri == 0:
                style_cell(cell, [(val, True, WHITE)], size=head_size, fill=header_fill,
                           align=PP_ALIGN.CENTER)
            else:
                fill = WHITE
                if band and ri % 2 == 0: fill = CARD
                bold = first_col_bold and ci == 0
                col = NAVY if bold else DARK
                if isinstance(val, tuple):
                    bold, col = val[1], val[2]
                    style_cell(cell, [(val[0], bold, col)], size=body_size, fill=fill)
                else:
                    style_cell(cell, [(val, bold, col)], size=body_size, fill=fill)
    return tbl

# ============================================================ SLIDE 1 — TITLE
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 13.333, 7.5, NAVY)
rect(s, 0, 4.62, 13.333, 0.05, ORANGE)
text(s, 0.9, 1.05, 11.5, 0.5, [("可重复使用运载火箭 AI 协同设计暑期课程（11–20 July 2026）", 15, False, RGBColor(0xBF,0xD7,0xEA))])
text(s, 0.9, 1.75, 11.6, 1.6, [("AI辅助轨迹优化与设计迭代", 44, True, WHITE), ("（AI-Assisted Trajectory Optimization & Design Iteration）", 24, False, RGBColor(0xE8,0xF2,0xEC))])
text(s, 0.9, 3.55, 11.5, 0.8, [("物理校核修复 · 敏感度分析(LHS) · 全局差分进化(DE) · 蒙特卡洛(MC)鲁棒性验证 · 闭合设计梯队", 17, False, RGBColor(0xBF,0xD7,0xEA))])
rect(s, 0.9, 4.95, 4.9, 1.5, RGBColor(0x1F,0x45,0x6E), round_=True)
text(s, 1.12, 5.12, 4.5, 1.2, [("Day 7 / 10 · 2026年7月17日", 16, True, WHITE),
                               ("交付物：设计迭代与优化报告（Design Iteration）", 12.5, False, RGBColor(0xBF,0xD7,0xEA))])
rect(s, 6.0, 4.95, 6.4, 1.5, RGBColor(0x1F,0x45,0x6E), round_=True)
text(s, 6.22, 5.12, 6.1, 1.3, [("技术突破：全面废除 Day 5 物理失效数据，重建 3-DOF 上升与 2-DOF 回收模型", 12.5, False, RGBColor(0xBF,0xD7,0xEA)),
                               ("量化结论：18 t 储备不足，回收需 ≥34.5 t；20 t SSO 闭合强制 802 t GLOM 架构", 12.5, False, RGBColor(0xBF,0xD7,0xEA))])

# ============================================================ SLIDE 2 — PHYSICS AUDIT
s = prs.slides.add_slide(BLANK); header(s, "痛点反思：对 Day 5 仿真数据的物理校核与纠偏", "Physics Audit")
bullet_block(s, 0.55, 1.25, 6.1, 4.5, [
 ("能量不守恒（CR-1 幻影能量）：", "原数据中 S1 隐式有效 Isp 达 364 s（超真空 limit 311 s），S2 更达 427 s（超 vacuum limit 348 s），产生 1.5 km/s 的物理溢出。"),
 ("轨道未闭合（CR-2）：", "原数据终止于 245.5 km、7,610 m/s、γ=0°，其实际对应的近地点为 −248 km，即属于亚轨道（suborbital），在 1 圈内必将重返大气层，并未入轨。"),
 ("Max-Q 读数矛盾（CR-3）：", "报告文本称 Max-Q 约 28 kPa @ 12 km；但原 master data 导出的阻力峰值对应 dynamic pressure 实为 40.4 kPa @ 9.3 km，已超 25–35 kPa 限制设计。"),
 ("公式未渲染：", "原 Day 5 报告中第 2.5 节等数个公式留白或未渲染；且在 staging loss 等数据表处存留大量“未完待续”字样。"),
], size=13.5, gap=8)

rect(s, 6.95, 1.25, 5.8, 5.5, CARD, round_=True)
text(s, 7.2, 1.45, 5.3, 0.4, [("物理修复对策与 G1–G8 审计通过栏", 16, True, NAVY)])
data_audit = [
 ["审计项目", "检查规则", "结论"],
 ["G1 质量对账", "终值质量对账精准至 ±0.1 kg", "PASS ✓"],
 ["G2 动压边界", "Max-Q 位于 50–90 s、25–45 kPa 内", "PASS ✓"],
 ["G3 分离状态", "MECO 位于 50–90 km, M5.0–7.0", "PASS ✓"],
 ["G4 二级点火", "Stage 2 起飞 T/W ≥ 0.60 满足物理", "PASS ✓"],
 ["G5 比冲积分", "∫mdot dt = Δm_prop 物理严格限制", "PASS ✓"],
 ["G6 能量残差", "动能变化 = 动力功 − 阻力 − 重力（残差≤3 m/s）", "PASS ✓"],
 ["G7 大气校验", "密度/压力分布符合 USSA76 标准表", "PASS ✓"]
]
make_table(s, 7.05, 2.05, 5.6, 4.5, data_audit, col_w=[2.2,3.5,1.2], body_size=11, head_size=11.5)

# ============================================================ SLIDE 3 — REPAIRED INTEGRATOR
s = prs.slides.add_slide(BLANK); header(s, "重建上升模拟器（Arc A）与 honest 状态值", "Ascent Repair")
if os.path.exists("day7_sim/results/fig1_profile.png"):
    s.shapes.add_picture("day7_sim/results/fig1_profile.png", Inches(6.35), Inches(1.22), width=Inches(6.45))
bullet_block(s, 0.55, 1.25, 5.6, 5.6, [
 ("数学内核：", "3-DOF 平面质点（x-downrange, h-alt），球形地球引力，RK4（dt=0.1 s）严格动力学显式积分。"),
 ("大气与比冲：", "USSA76 分层指数大气；Isp 动态压力插值（Isp = 282 + 29*(1-p/p0)），严格在真空极限 311 s (S1) / 348 s (S2) 处封顶。"),
 ("精确分离点（V-1 交付值）：", "T+142 s, 66.5 km  altitude, 1,892 m/s, γ=40.7°, Mach 5.7, downrange 51 km —— 一级燃尽，释出 58 t 干重（含 18 t 储备）。"),
 ("客观性能缺口：", "用 honest 物理复算 600 t 起飞/20 t 载荷，到 500 km SSO 产生 2,088 m/s 的巨大速度缺口。"),
 ("损失分解：", "重力损失 1,810 m/s（S1 1,217 + S2 593）；空气阻力损失 18–26 m/s；制导偏置损失 82–108 m/s。"),
], size=13.5, gap=8)

# ============================================================ SLIDE 4 — SENSITIVITY LHS
s = prs.slides.add_slide(BLANK); header(s, "敏感度与崩溃边界：1,200 次拉丁超立方抽样", "DOE & Sensitivity")
if os.path.exists("day7_sim/results/fig10_lhs_drivers.png"):
    s.shapes.add_picture("day7_sim/results/fig10_lhs_drivers.png", Inches(6.35), Inches(1.22), width=Inches(6.45))
bullet_block(s, 0.55, 1.25, 5.6, 5.6, [
 ("崩溃边界（Crash Boundary）：", "在开放制导空间下，Config A（1x MVac）由于二级推重比过低（T/W_ign ≈ 0.66），在 9.0% 的 LHS 组合中会发生“重力坠毁”（arc-sag）。失败主因是过早 Pitch kick 或 S1 推进剂不足。Config B（2x MVac）无一坠毁。"),
 ("制导敏感度（Spearman 秩相关）：", "影响轨道速度缺口（Deficit）的绝对主力为制导时间常数。"),
 ("时间常数 t_kick0 (ρ ≈ +0.48 / +0.54)：", "正相关。越晚 pitch kick，弹道越陡，重力损失飙升，轨道缺口越大。"),
 ("S1 煤油 m_prop (ρ ≈ −0.42 / −0.45)：", "强负相关。多载一分煤油，多给一分级间速度，降低二级压力。"),
 ("气动阻力 C_D 比例 (ρ ≤ 0.05)：", "影响极微。对于 3.9 m 细长箭体，阻力能量损失仅占总能 0.3%，非主要矛盾。"),
], size=13, gap=6)

# ============================================================ SLIDE 5 — OPTIMIZATION DE
s = prs.slides.add_slide(BLANK); header(s, "差分进化（DE）全局优化与制导极限", "Trajectory Optimization")
if os.path.exists("day7_sim/results/fig11_de_convergence.png"):
    s.shapes.add_picture("day7_sim/results/fig11_de_convergence.png", Inches(6.35), Inches(1.22), width=Inches(6.45))
bullet_block(s, 0.55, 1.25, 5.6, 5.6, [
 ("Scipy 全局优化：", "基于 4 制导自由度（kick angle, t_kick0, loft bias, hold duration），罚约束 Max-Q ≤ 35 kPa, MECO alt ≥ 50 km, g ≤ 5 g。"),
 ("手调栅格已达极限：", "DE 优化对 Config A 仅抠出 40 m/s 增量（Deficit 1,467 → 1,427 m/s），对 Config B 抠出 1 m/s 增量（872 → 871 m/s）。"),
 ("制导调优无法逆天改命：", "这在数学上证明：2,088 m/s 的轨道缺口是由于整箭湿重/比冲参数决定的物理铁壁，指望制导算法优化无法实现闭合。"),
 ("Max-Q 节流桶：", "引入 Max-Q 处 60% 节流虽然可以把 Max-Q 从 40 kPa 压入 31 kPa，但代价是 MECO 速度下降，轨道缺口增加 +21 m/s。"),
], size=13, gap=6)

# ============================================================ SLIDE 6 — ACCELERATION OVERLOAD
s = prs.slides.add_slide(BLANK); header(s, "发现结构超载：Config B 的 6.2 g 加速度红线", "Structural Overload")
if os.path.exists("day7_sim/results/fig4_split_tw.png"):
    s.shapes.add_picture("day7_sim/results/fig4_split_tw.png", Inches(6.35), Inches(1.22), width=Inches(6.45))
bullet_block(s, 0.55, 1.25, 5.6, 5.6, [
 ("发现致命超限（CR-D7-07）：", "在差分进化所得的最佳弹道中，双 MVac 构型（Config B）在 burn-out 阶段（SECO 瞬间）轴向加速度达到 6.2–6.4 g，严重超出 5.0 g 的载荷红线。"),
 ("物理成因：", "二级发动机推力过剩。SECO 时储箱烧空，二级干重(5.5t)＋ payload(20 t) 仅重约 25.5 t，两台 MVac 提供 1,962 kN，即便双发 40% 深度节流依然会发生过载。"),
 ("制导约束失效：", "将“轴向限制 5 g”作为惩罚项重新运行 DE，算法无法找到任何可闭合解，证明此超限是纯结构物性的超载，而非制导时间所致。"),
 ("Day 8 决议路径：", "① 赋予二级发动机动态单发停机（engine-out）或无极更低节流能力；② 将载荷抗过载指标向上修正至 6.5 g；③ 接受一个欠推力的亚优解（Deficit 扩大）。"),
], size=13, gap=6)

# ============================================================ SLIDE 7 — RECOVERY CHAIN
s = prs.slides.add_slide(BLANK); header(s, "回收子问题（Arc B4）：2-DOF 下行链模拟", "Descent Recovery Chain")
if os.path.exists("day7_sim/results/fig7_recovery_profile.png"):
    s.shapes.add_picture("day7_sim/results/fig7_recovery_profile.png", Inches(6.35), Inches(1.22), width=Inches(6.45))
bullet_block(s, 0.55, 1.25, 5.6, 5.6, [
 ("模型架构：", "2-DOF planar 显式积分，始于 MECO 抛离态（66.5 km, 1,892 m/s, γ=41°），顶点 135 km，重返 70 km 入口速度 1,806 m/s, γ=−42°。"),
 ("3机再入点火 70→40 km：", "移除大量动能以防烧毁，扫描不同点火时长，得出对应的 40 km 走廊状态。"),
 ("气动栅格翼滑翔：", "L/D = 0.25 控制，将升力系数在 10 km 降至 2 km 归零以实现终点弹道垂直化。"),
 ("末段 2 km 终点速度：", "滑翔终点下落至 2 km 时，下行垂直速度约 176–217 m/s。原 Day 6 粗估的“≈100 m/s 亚音速气动平衡”被高空低气压物理推翻。"),
], size=13, gap=6)

# ============================================================ SLIDE 8 — HOVER SLAM VERIFY
s = prs.slides.add_slide(BLANK); header(s, "悬停猛击校核与相对制导（V-2 / V-4）", "Hover Slam & Guidance")
if os.path.exists("day7_sim/results/fig8_terminal_window.png"):
    s.shapes.add_picture("day7_sim/results/fig8_terminal_window.png", Inches(6.35), Inches(1.22), width=Inches(6.45))
bullet_block(s, 0.55, 1.25, 5.6, 5.6, [
 ("单台末段点火物理（V-2）：", "采用单台 M1D（节流下限 40%），末段重量 412–441 kN，悬停所需节流落于 49–52%（不确定区间），必须采用“悬停猛击”（Hover-slam）。"),
 ("末段点火自适应（Bisection）：", "自适应算法二分逼近，确定在 1,500–2,000 m 高度起动单发，燃时 12–21 s，消耗 4.6–4.8 t 煤油，落于捕获接口。"),
 ("船位精度控制（V-4）：", "由分离点（x=51 km）弹道落点及滑翔积分，计算出标称捕获船位应设于 489 km 下程处（含 L/D 偏置 481–496 km），位于 Day 6 预测范围内。"),
 ("避船偏置（Miss Bias）：", "终端轨迹默认保持 10–15 m 偏置，直至末段点火成功再行拉回，以防点火失败直击甲板。"),
], size=13, gap=6)

# ============================================================ SLIDE 9 — RESERVE INSUFFICIENCY
s = prs.slides.add_slide(BLANK); header(s, "原 18 t 储备不足：下行推进剂固定点闭合", "Reserve Closure")
if os.path.exists("day7_sim/results/fig9_reserve_closure.png"):
    s.shapes.add_picture("day7_sim/results/fig9_reserve_closure.png", Inches(6.35), Inches(1.22), width=Inches(6.45))
bullet_block(s, 0.55, 1.25, 5.6, 5.6, [
 ("原 18 t 储备下限（M2.89 走廊）：", "18 t 储备在刨除 residuals 与 2 t aux 冗余后，仅够维持 Mach 2.89 的极高温度走廊（燃耗 17.9 t）。"),
 ("一类动力学固定点（Fixed Point）：", "为了闭合回收需求，燃耗 Need(R) 必须小于等于 R 储备值。经对再入走廊扫描求交："),
 ("再入 M2.7 Corridor：", "需储备 R* = 29.6 t"),
 ("再入 M2.3 Corridor：", "需储备 R* = 32.4 t （推荐基准点）"),
 ("再入 M2.0 Corridor：", "需储备 R* = 35.0 t"),
 ("Day 6 幻想破灭（CR-D7-06）：", "原 Day 6 报告中因选定“捕获环”而宣称比着陆腿节省 6,000 kg 储备（18 t vs 24 t）的结论是不合物理的，回收储备由下行热力载荷支配，两方案均严重短缺推进剂，储备应拓宽至 ≥34.5 t。"),
], size=12.5, gap=5)

# ============================================================ SLIDE 10 — MONTE CARLO
s = prs.slides.add_slide(BLANK); header(s, "双项蒙特卡洛验证（Arc B5）：分散与鲁棒性", "Monte-Carlo Robustness")
if os.path.exists("day7_sim/results/fig12_mc_ascent.png"):
    s.shapes.add_picture("day7_sim/results/fig12_mc_ascent.png", Inches(6.35), Inches(1.22), width=Inches(6.45))
bullet_block(s, 0.55, 1.25, 5.6, 5.6, [
 ("上升分散 MC (400 样, 2σ 偏差)：", "偏差包括 Isp ±1.5 s, C_D ±10%, 干重 ±1%, kick ±0.15°, timing ±1 s。在开环优化制导下："),
 ("Config A (1x MVac)：", "P(及格 SECO) = 82%，P(q_max ≤ 35 kPa) = 45%。生存点缺口 1,496 ± 54 m/s。"),
 ("失败机理：", "极推比（T/W_ign ≈ 0.66）造成“悬崖式失败”。只要 Isp 偏差 -1.5 s，二级就会迅速发生重力沉降下坠，MECO alt 跌穿 50 km 坠毁。真实产品必须引入闭合 PEG 指导以防坠毁。"),
 ("Config B (2x MVac)：", "P(SECO) = 94%，P(q ≤ 35) = 38%，P(q ≤ 35 ∧ g ≤ 5) = 0.00%（超载 100% 出现）。"),
], size=12.5, gap=5)

# ============================================================ SLIDE 11 — RECOVERY MC
s = prs.slides.add_slide(BLANK); header(s, "回收蒙特卡洛（500 样）：为什么 34.5 t 是死线", "Recovery Monte-Carlo")
if os.path.exists("day7_sim/results/fig13_mc_recovery.png"):
    s.shapes.add_picture("day7_sim/results/fig13_mc_recovery.png", Inches(6.35), Inches(1.22), width=Inches(6.45))
bullet_block(s, 0.55, 1.25, 5.6, 5.6, [
 ("回收环境超大发散 (500 样)：", "包括 drag Area U(12, 32) m^2 (涵盖极高迎角晃动), L/D ±20%, entry 节流误差 ±2.5%。末端配置自适应计算机。"),
 ("原 18 t 预案运行：", "P(成功捕获) = 0.00%！在所有样本中，18 t 均在中途烧空坠毁，平均提早 14 s 熄火撞海。"),
 ("M2.3 (32.4 t) 标称闭合运行：", "P(成功捕获) = 45.0%（中值闭合，但未涵盖极端大风高阻样本，在差偏差时由于提前点火，会在最后几米耗尽推进剂）。"),
 ("95% 完好寿命阈值 (p95)：", "要达到 95% 的回收成功率，全箭储备推进剂必须拓宽至 34.5–36.0 t。"),
 ("⇒ 移交 Day 8：", "锁定以 34.5 t（M2.3 走廊）作为最终一级的回收燃油配置标准。"),
], size=12.5, gap=5)

# ============================================================ SLIDE 12 — ITERATION LADDER
s = prs.slides.add_slide(BLANK); header(s, "设计迭代梯队：从 L0 到 L5 的闭合路径", "Iteration Ladder")
if os.path.exists("day7_sim/results/fig6_ladder.png"):
    s.shapes.add_picture("day7_sim/results/fig6_ladder.png", Inches(6.35), Inches(1.22), width=Inches(6.45))
bullet_block(s, 0.55, 1.25, 5.6, 5.6, [
 ("L0 文档化：", "1x MVac, 600 t. Deficit = 2,088 m/s. (物理不成立)"),
 ("L1 裕度转推进：", "通过将 Day 4 预留的 7 t 增长裕度吃掉并加满二级推进剂，获得 621 m/s 的“无痛提升”，Deficit 降至 1,467 m/s。"),
 ("L2 二级双发（T/W 修复）：", "增加第 2 台 MVac（干重+0.55t），极大地改善重力 losses，Deficit 降至 872 m/s。但产生 6.2 g 轴向过载（CR-D7-07）。"),
 "二级煤油单向追加会触碰 T/W 0.62–0.66 阻碍边界，导致重力沉降坠毁。GLOM 级增长若不加一级发动机推力亦无法闭合。",
], size=13, gap=6)

# ============================================================ SLIDE 13 — CLOSURE OPT
s = prs.slides.add_slide(BLANK); header(s, "闭合决策矩阵（交付 Day 8 可靠性与经济性）", "Closure Trades")
data_opt = [
 ["闭合路径", "起飞 GLOM", "S1/S2 发动机", "回收储备", "SSO 载荷", "技术判定/移交优势"],
 ["L2 限制载荷版 (Path B)", "600 t", "9× M1D / 2× MVac", "34.5 t (MC p95)", "12.0 t", "不改变既定吨位；载荷缩水；二级需单发停机控 g"],
 ["L1 极限载荷版", "600 t", "9× M1D / 1× MVac", "34.5 t (MC p95)", "6.6 t", "二级 T/W 过低，极易在 Isp 下偏差时坠毁（P=0.82）"],
 ["L5 增重闭合版 (Path A)", "802 t (+34%)", "12× M1D / 4× MVac", "34.5 t (MC p95)", "20.0 t", "完全闭合原 20 t SSO 载荷；发动机增至 12 台"],
]
make_table(s, 0.55, 1.30, 12.25, 2.5, data_opt, col_w=[2.6,1.4,2.4,1.8,1.4,2.9], body_size=11, head_size=12)

rect(s, 0.55, 4.0, 12.25, 2.9, PEACH, round_=True)
text(s, 0.8, 4.15, 11.8, 0.4, [("决策交接给 Day 8 的重大经济性课题：", 15, True, RED)])
bullet_block(s, 0.85, 4.6, 11.6, 2.1, [
 ("20 t 载荷坚守代价高昂：", "若要坚守 20 t 载荷（Path A），全箭 GLOM 必须充水 34.2%（至 802 t）。不仅新造价大幅上扬，12 台发动机的并联也增加了动力失效概率（Day 8 重点评估 FMEA）。"),
 ("600 t 吨位坚守性价突出：", "若限制 GLOM=600 t（Path B），虽载荷调整为 12 t（比原计划-40%），但整箭由于采用标准 2 台 MVac，技术极其简单，可利用成套流水线（Day 8 舰队模型评估其对 $30M 发射成本的降维打击）。"),
], size=13.5, gap=5)

# ============================================================ SLIDE 14 — CONSISTENCY REGISTER
s = prs.slides.add_slide(BLANK); header(s, "跨文档一致性登记（Cross-Document Register）", "Consistency Register")
data_cr = [
 ["编号", "所在位置", "原条目", "校勘修正项（Day 7 Repaired）", "驱动原因"],
 ["CR-D7-02", "Day 2 §1 / §2", "轨道速度要求“11.0 km/s to SSO”", "修正为“约 9,500 m/s 理论理想 Δv”（包含约 1,900 m/s 损失项）", "原理想 Δv 把 circular speed 与损失项叠加错误，虚增了 1.5 km/s 需求。"],
 ["CR-D7-06", "Day 6 §6", "“捕获兼容型相比着陆腿式可以节省 6 t 回收储备”（18 t vs 24 t）", "废除节省 6 t 储备说法；两者下行气动重返路径一致，均必须扩容至 ≥34.5 t", "18 t 储备在 Monte-Carlo 下由于过早烧空，捕获完好率 P=0.00%。"],
 ["CR-D7-07", "Day 3 §2.1", "二级发动机配置单台 MVac（Config A）", "引入双 MVac 配置（Config B），并新增 S2 burn-out 瞬间单发停机/节流要求", "2x MVac 终点产生 6.2g 超载红线，需动态控制节流减 g。"],
]
make_table(s, 0.55, 1.25, 12.25, 4.3, data_cr, col_w=[1.2,1.8,3.2,3.8,2.5], body_size=11, head_size=12, first_col_bold=True)
rect(s, 0.55, 5.75, 12.25, 1.0, LIGHT, round_=True)
text(s, 0.8, 5.86, 12.0, 0.85, [
 [("集成声明：", 13, True, NAVY), ("上述一致性纠偏在 Day 7 优化中已获物理闭合，将在 Day 9 全系统集成汇总中一并对 Day 1–6 原档进行追溯注释。这种“在迭代中发现矛盾、通过物理计算纠正前序指标”的过程，正是 multidisciplinary design optimization 的精髓所在。", 11.5, False, DARK)],
], space_after=2)

# ============================================================ SLIDE 15 — FINAL VERDICT
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, 13.333, 7.5, NAVY)
rect(s, 0, 1.55, 13.333, 0.05, ORANGE)
text(s, 0.7, 0.45, 12.0, 0.9, [("设计迭代大闭合：在物理真实、诚实校对中实现轨道闭合", 26, True, WHITE)])
items_opt = [
 ("废除幻影能量", "完全重写了 Day 5 OpenRocket 仿真；基于 RK4 USSA76 与 100% 诚实 Isp (SL 282 / Vac 311 / S2 348 s) 建立了 8/8 全审计通过的上升与回收下行模拟。"),
 ("锁定制导天花板", "差分进化（DE）优化表明，在当前整机干湿比约束下，手调基准点已贴近轨道制导极限，优化增量 ≤40 m/s，证明轨道缺口是硬性结构缺口，而非制导时间调优问题。"),
 ("回收储备闭合", "证明 18 t 储备必坠毁（P=0.00%）。采用一类动力学固定点方法与蒙特卡洛 500 样物理寻优，确定了 34.5 t（M2.3 走廊，MC p95 保证）作为复用储备新基线。"),
 ("交接闭合 baselines", "向上闭合 (Path A): GLOM=802 t / 20 t 载荷 / 12× S1 / 4× S2 闭合；向下闭合 (Path B): GLOM=600 t / 12 t 载荷 / 9× S1 / 2× S2 闭合。"),
 ("结构过载警报", "Config B 产生 6.2g 超载（CR-D7-07），作为重大高维风险和缓释条件，与 Path A / Path B 的商业回报分析一道正式交接给 Day 8 可靠性与经济性工包。"),
]
y = 1.95
for t_, d_ in items_opt:
    rect(s, 0.7, y, 0.16, 0.80, ORANGE)
    text(s, 1.05, y, 3.0, 0.8, [(t_, 16, True, RGBColor(0xF2,0xA3,0x3C))])
    text(s, 3.9, y + 0.02, 8.9, 0.9, [(d_, 13.5, False, WHITE)])
    y += 1.02

rect(s, 0.7, 6.28, 12.0, 1.0, RGBColor(0x1F,0x45,0x6E), round_=True)
text(s, 0.95, 6.38, 11.6, 0.85, [
 [("AI协同设计大本营宣言：", 12, True, RGBColor(0xF2,0xA3,0x3C)),
  ("本日修复标志着课程中最重大的“物理对账”战役取得圆满成功，我们的数据链现在具备了轨道级的诚实性、追溯性与极端发散工况下的生存保证，为后续 Day 8–10 决战铺平道路。", 11.5, False, RGBColor(0xBF,0xD7,0xEA))],
], space_after=3)

prs.save("Day7_AI_辅助优化_设计迭代.pptx")
print("Saved Day7_AI_辅助优化_设计迭代.pptx, slides:", len(prs.slides._sldIdLst))
