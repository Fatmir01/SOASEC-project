import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

plt.rcParams.update({
    "font.family": "serif",
    "pdf.fonttype": 42,
})

# palette
C_PREP   = ("#E1F5EE", "#0F6E56")  # teal  (shared preprocessing)
C_LEG    = ("#EEEDFE", "#3C3489")  # purple (legends branch)
C_REG    = ("#FAECE7", "#993C1D")  # coral  (regulation branch)
C_SHARED = ("#F1EFE8", "#444441")  # gray   (shared stages on both branches)
C_FT     = ("#E6F1FB", "#0C447C")  # blue   (fine-tuning / models)
C_EVAL   = ("#FAEEDA", "#854F0B")  # amber  (evaluation)
C_CIP    = ("#FBEAF0", "#72243E")  # pink   (CIP)

fig, ax = plt.subplots(figsize=(11.0, 6.6))
ax.set_xlim(0, 100)
ax.set_ylim(0, 66)
ax.axis("off")

def box(x, y, w, h, title, sub, colors, fs=9.5, subfs=7.8):
    fc, ec = colors
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle="round,pad=0.02,rounding_size=1.2",
                       linewidth=1.1, edgecolor=ec, facecolor=fc, zorder=3)
    ax.add_patch(p)
    cy = y + h/2
    if sub:
        ax.text(x+w/2, cy+h*0.16, title, ha="center", va="center",
                fontsize=fs, color=ec, zorder=4)
        ax.text(x+w/2, cy-h*0.22, sub, ha="center", va="center",
                fontsize=subfs, color=ec, alpha=0.85, zorder=4, style="italic")
    else:
        ax.text(x+w/2, cy, title, ha="center", va="center",
                fontsize=fs, color=ec, zorder=4)
    return (x, y, w, h)

def arrow(p1, p2, color="#444441", ls="-", lw=1.3):
    a = FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=12,
                        linewidth=lw, color=color, linestyle=ls,
                        shrinkA=2, shrinkB=2, zorder=2)
    ax.add_patch(a)

def right(b):  return (b[0]+b[2], b[1]+b[3]/2)
def left(b):   return (b[0], b[1]+b[3]/2)
def top(b):    return (b[0]+b[2]/2, b[1]+b[3])
def bottom(b): return (b[0]+b[2]/2, b[1])

# ---- Row 1: shared preprocessing (teal) -----------------------------------
yR1 = 54
bw, bh = 15, 8
b_pdf  = box(2,  yR1, bw, bh, "PDF input",      "regulation + 4 CEB docs", C_PREP)
b_md   = box(21, yR1, bw, bh, "Markdown",        "Marker + regex clean",    C_PREP)
b_seg  = box(40, yR1, bw, bh, "Segmentation",    "5 thematic parts",        C_PREP)
arrow(right(b_pdf), left(b_md))
arrow(right(b_md), left(b_seg))

# fork point from segmentation down to the two branches
fork_x = b_seg[0] + b_seg[2]/2

# ---- Row 2: two parallel branches -----------------------------------------
yLEG = 39   # legends branch (upper)
yREG = 27   # regulation branch (lower)

# branch entry boxes
b_leg_gen = box(2,  yLEG, 17, 8, "Legends generation", "3 LLMs x 5 pillars", C_LEG)
b_reg_src = box(2,  yREG, 17, 8, "Regulation text",    "cleaned passages",   C_REG)

# shared stages (gray) applied to BOTH branches -- drawn once per branch
b_leg_cls  = box(22, yLEG, 15, 8, "Classification", "6-class pillar", C_SHARED)
b_reg_cls  = box(22, yREG, 15, 8, "Classification", "6-class pillar", C_SHARED)

b_leg_span = box(40, yLEG, 14, 8, "Span extract", "2-stage", C_SHARED)
b_reg_span = box(40, yREG, 14, 8, "Span extract", "2-stage", C_SHARED)

b_leg_qa = box(57, yLEG, 16, 8, "Q&A generation", "factoid + non-factoid", C_SHARED, subfs=7.2)
b_reg_qa = box(57, yREG, 16, 8, "Q&A generation", "factoid + non-factoid", C_SHARED, subfs=7.2)

b_leg_js = box(76, yLEG, 14, 8, "JSONL", "327 lines", C_LEG)
b_reg_js = box(76, yREG, 14, 8, "JSONL", "293 lines", C_REG)

# segmentation fork into the two branch-entry boxes
arrow((fork_x, b_seg[1]), top(b_leg_gen), color=C_LEG[1])
arrow((fork_x, b_seg[1]), top(b_reg_src), color=C_REG[1])

# legends branch chain
for a, b in [(b_leg_gen,b_leg_cls),(b_leg_cls,b_leg_span),(b_leg_span,b_leg_qa),(b_leg_qa,b_leg_js)]:
    arrow(right(a), left(b), color=C_LEG[1])
# regulation branch chain
for a, b in [(b_reg_src,b_reg_cls),(b_reg_cls,b_reg_span),(b_reg_span,b_reg_qa),(b_reg_qa,b_reg_js)]:
    arrow(right(a), left(b), color=C_REG[1])

# closed-book annotation between QA and JSONL
ax.text(74.7, (yLEG+yREG)/2+4, "closed-book\nJSON $\\to$ JSONL", ha="center",
        va="center", fontsize=7.2, color="#444441", style="italic")

# ---- converge on fine-tuning (blue) ---------------------------------------
yFT = 33
b_ft = box(92.5, yFT+0.0, 6.5, 8, "FT", "", C_FT, fs=10)
ax.text(b_ft[0]+b_ft[2]/2, b_ft[1]-2.4, "FineTuneDB", ha="center", va="top",
        fontsize=7.0, color=C_FT[1], style="italic")
ax.text(b_ft[0]+b_ft[2]/2, b_ft[1]-4.4, "gpt-4o", ha="center", va="top",
        fontsize=7.0, color=C_FT[1], style="italic")

# branches converge into FT
arrow(right(b_leg_js), (b_ft[0], b_ft[1]+b_ft[3]*0.72), color=C_LEG[1])
arrow(right(b_reg_js), (b_ft[0], b_ft[1]+b_ft[3]*0.28), color=C_REG[1])

# ---- Row 3: diverge into evaluation + CIP ---------------------------------
yEVAL = 11
# three model chips produced by FT
ax.text(50, 20.5, "three models:  base  ·  tuned-legends  ·  tuned-regulation",
        ha="center", va="center", fontsize=8.6, color="#0C447C",
        bbox=dict(boxstyle="round,pad=0.4", fc=C_FT[0], ec=C_FT[1], lw=1.0))

# arrow FT down to the model strip
arrow(bottom(b_ft), (b_ft[0]+b_ft[2]/2, 22.2), color=C_FT[1])
arrow((75, 20.5), (75, 17.0), color="#444441")  # strip -> eval header line

# five GenderEqGLUE tasks
tasks = ["GE-CLS", "GE-NLI", "GE-QA", "GE-WSC", "GE-NEXT"]
tw, th, gap = 11.2, 6.5, 1.0
total = len(tasks)*tw + (len(tasks)-1)*gap
startx = 6
for i, t in enumerate(tasks):
    bx = startx + i*(tw+gap)
    bb = box(bx, yEVAL, tw, th, t, "", C_EVAL, fs=8.6)
    arrow((bx+tw/2, yEVAL+th+2.0), (bx+tw/2, yEVAL+th), color=C_EVAL[1])

# GenderEqGLUE bracket label
ax.annotate("", xy=(startx, yEVAL+th+2.0), xytext=(startx+total, yEVAL+th+2.0),
            arrowprops=dict(arrowstyle="-", color=C_EVAL[1], lw=1.1))
ax.text(startx+total/2, yEVAL+th+3.4, "GenderEqGLUE evaluation",
        ha="center", va="bottom", fontsize=9, color=C_EVAL[1])

# connect model strip down to the bracket
arrow((50, 18.2), (startx+total/2, yEVAL+th+2.1), color="#444441")

# CIP box on the right
b_cip = box(76, yEVAL, 18, th, "Counterfactual", "Input Probing (CIP)", C_CIP, fs=8.8, subfs=7.4)
arrow((85, 18.2), top(b_cip), color=C_CIP[1])

# ---- legend ----------------------------------------------------------------
handles = [
    Line2D([0],[0], marker='s', color='none', markerfacecolor=C_PREP[0],   markeredgecolor=C_PREP[1],   markersize=11, label="shared preprocessing"),
    Line2D([0],[0], marker='s', color='none', markerfacecolor=C_LEG[0],    markeredgecolor=C_LEG[1],    markersize=11, label="legends branch"),
    Line2D([0],[0], marker='s', color='none', markerfacecolor=C_REG[0],    markeredgecolor=C_REG[1],    markersize=11, label="regulation branch"),
    Line2D([0],[0], marker='s', color='none', markerfacecolor=C_SHARED[0], markeredgecolor=C_SHARED[1], markersize=11, label="shared stages (both branches)"),
    Line2D([0],[0], marker='s', color='none', markerfacecolor=C_FT[0],     markeredgecolor=C_FT[1],     markersize=11, label="fine-tuning / models"),
    Line2D([0],[0], marker='s', color='none', markerfacecolor=C_EVAL[0],   markeredgecolor=C_EVAL[1],   markersize=11, label="evaluation"),
    Line2D([0],[0], marker='s', color='none', markerfacecolor=C_CIP[0],    markeredgecolor=C_CIP[1],    markersize=11, label="explainability"),
]
ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.04),
          ncol=4, frameon=False, fontsize=7.8, handletextpad=0.4,
          columnspacing=1.4)

fig.tight_layout()
fig.savefig("fig2_pipeline.pdf", bbox_inches="tight")
fig.savefig("fig2_pipeline.png", dpi=180, bbox_inches="tight")
print("saved fig2_pipeline.pdf and .png")


