import argparse
from pathlib import Path
import shutil
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch


PALETTE = {
    "bg": "#F8FAFC",
    "panel_bg": "#FFFFFF",
    "panel_border": "#CBD5E1",
    "navy_fill": "#1E293B",
    "navy_text": "#FFFFFF",
    "blue_fill": "#EFF6FF",
    "blue_edge": "#2563EB",
    "teal_fill": "#ECFEFF",
    "teal_edge": "#0891B2",
    "green_fill": "#ECFDF5",
    "green_edge": "#059669",
    "amber_fill": "#FFFBEB",
    "amber_edge": "#D97706",
    "red_fill": "#FEF2F2",
    "red_edge": "#DC2626",
    "slate_fill": "#F1F5F9",
    "slate_edge": "#475569",
    "ink": "#0F172A",
    "muted": "#475569",
    "arrow": "#334155",
}


def new_canvas(figsize, title, subtitle):
    fig, ax = plt.subplots(figsize=figsize, dpi=220)
    fig.patch.set_facecolor(PALETTE["bg"])
    ax.set_facecolor(PALETTE["bg"])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    ax.text(3, 96.8, title, fontsize=15.5, fontweight="bold", color=PALETTE["ink"], va="top")
    ax.text(3, 93.0, subtitle, fontsize=9.8, color=PALETTE["muted"], va="top")
    return fig, ax


def draw_section(ax, x, y, w, h, title, accent=PALETTE["slate_edge"], fill=PALETTE["panel_bg"]):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.25,rounding_size=1.1",
        facecolor=fill, edgecolor=PALETTE["panel_border"], linewidth=1.3, zorder=1
    )
    ax.add_patch(box)
    ax.text(
        x + 1.4, y + h - 1.1, title, fontsize=9.4, fontweight="bold",
        color=accent, va="top", ha="left", zorder=5,
        bbox=dict(boxstyle="round,pad=0.2", facecolor=fill, edgecolor="none", alpha=0.95)
    )


def draw_box(ax, cx, cy, w, h, text, fill=PALETTE["blue_fill"], edge=PALETTE["blue_edge"],
             title=None, fontsize=8.6, code=False):
    x, y = cx - w / 2, cy - h / 2
    family = "DejaVu Sans Mono" if code else "DejaVu Sans"
    if title:
        outer = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.15,rounding_size=0.8",
            facecolor="#FFFFFF", edgecolor=edge, linewidth=1.55, zorder=3
        )
        ax.add_patch(outer)
        hdr_h = min(3.3, h * 0.34)
        hdr = FancyBboxPatch(
            (x, y + h - hdr_h), w, hdr_h,
            boxstyle="round,pad=0.15,rounding_size=0.8",
            facecolor=fill, edgecolor=edge, linewidth=1.35, zorder=3
        )
        ax.add_patch(hdr)
        ax.text(cx, y + h - hdr_h / 2, title, fontsize=fontsize + 0.1, fontweight="bold",
                color=edge, ha="center", va="center", zorder=4)
        body_cy = y + (h - hdr_h) / 2
        ax.text(cx, body_cy, text, fontsize=fontsize - 0.4, family=family, fontweight="normal",
                color=PALETTE["ink"], ha="center", va="center", zorder=4, linespacing=1.3)
    else:
        box = FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.2,rounding_size=0.8",
            facecolor=fill, edgecolor=edge, linewidth=1.55, zorder=3
        )
        ax.add_patch(box)
        ax.text(cx, cy, text, fontsize=fontsize, family=family, fontweight="normal",
                color=PALETTE["ink"], ha="center", va="center", zorder=4, linespacing=1.3)


def draw_pill(ax, cx, cy, w, h, text, fill=PALETTE["navy_fill"], text_color="#FFFFFF",
              edge=None, fontsize=9.0):
    x, y = cx - w / 2, cy - h / 2
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0.1,rounding_size={h * 0.48}",
        facecolor=fill, edgecolor=edge or fill, linewidth=1.55, zorder=3
    )
    ax.add_patch(box)
    ax.text(cx, cy, text, fontsize=fontsize, fontweight="bold",
            color=text_color, ha="center", va="center", zorder=4)


def draw_diamond(ax, cx, cy, w, h, text, fill=PALETTE["amber_fill"], edge=PALETTE["amber_edge"], fontsize=8.3):
    pts = [(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)]
    poly = Polygon(pts, closed=True, facecolor=fill, edgecolor=edge, linewidth=1.55, zorder=3)
    ax.add_patch(poly)
    ax.text(cx, cy, text, fontsize=fontsize, family="DejaVu Sans Mono", fontweight="bold",
            color=PALETTE["ink"], ha="center", va="center", zorder=4, linespacing=1.22)


def draw_arrow(ax, p1, p2, label=None, label_pos=(0, 0), color=PALETTE["arrow"],
               rad=0.0, dashed=False, label_color=None):
    style = "--" if dashed else "-"
    arrow = FancyArrowPatch(
        p1, p2,
        arrowstyle="-|>,head_width=0.35,head_length=0.55",
        connectionstyle=f"arc3,rad={rad}",
        color=color, linewidth=1.45, linestyle=style, zorder=2
    )
    ax.add_patch(arrow)
    if label:
        lx = (p1[0] + p2[0]) / 2 + label_pos[0]
        ly = (p1[1] + p2[1]) / 2 + label_pos[1]
        ax.text(
            lx, ly, label, fontsize=7.9, fontweight="bold",
            color=label_color or color, ha="center", va="center", zorder=5,
            bbox=dict(boxstyle="round,pad=0.18", facecolor=PALETTE["panel_bg"], edgecolor="none", alpha=0.94)
        )


def draw_polyline(ax, pts, label=None, label_xy=None, color=PALETTE["arrow"], dashed=False, label_color=None):
    style = "--" if dashed else "-"
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    if len(pts) > 2:
        ax.plot(xs[:-1], ys[:-1], color=color, linewidth=1.45, linestyle=style, zorder=2, solid_capstyle="round")
    arrow = FancyArrowPatch(
        pts[-2], pts[-1],
        arrowstyle="-|>,head_width=0.35,head_length=0.55",
        color=color, linewidth=1.45, linestyle=style, zorder=2
    )
    ax.add_patch(arrow)
    if label and label_xy:
        ax.text(
            label_xy[0], label_xy[1], label, fontsize=7.9, fontweight="bold",
            color=label_color or color, ha="center", va="center", zorder=5,
            bbox=dict(boxstyle="round,pad=0.18", facecolor=PALETTE["panel_bg"], edgecolor="none", alpha=0.94)
        )


def save_diagram(fig, out_dir: Path, filename: str, sodo_dir: Path = None):
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / filename
    fig.savefig(target, dpi=220, bbox_inches="tight", pad_inches=0.2, facecolor=PALETTE["bg"])
    if sodo_dir is not None:
        sodo_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(target, sodo_dir / filename)
    plt.close(fig)
    print(f"Generated {target}")


# ---------------------------------------------------------------------------
# 1. DLL Deletion Algorithm (src/BrowserHistory.cpp::deleteByUrl)
# ---------------------------------------------------------------------------
def build_dll_deletion(out_dir: Path, sodo_dir: Path = None):
    fig, ax = new_canvas(
        (15, 9.2),
        "1. Doubly Linked List Deletion Algorithm  —  BrowserHistory::deleteByUrl(url)",
        "Exact control flow from src/BrowserHistory.cpp: O(N) case-insensitive scan + O(1) bidirectional relink"
    )

    draw_section(ax, 3, 28, 41, 61, "PHASE A  |  CASE-INSENSITIVE LINEAR TRAVERSAL", PALETTE["blue_edge"])
    draw_pill(ax, 23.5, 81.5, 22, 5.0, "START: deleteByUrl(url)")
    draw_box(ax, 23.5, 72.2, 31, 6.0,
             "urlLower = toLower(url)\nDLLNode* node = head",
             fill=PALETTE["blue_fill"], edge=PALETTE["blue_edge"], code=True)
    draw_diamond(ax, 23.5, 59.5, 22, 9.2, "node != nullptr ?")
    draw_diamond(ax, 23.5, 44.5, 29, 9.8, "toLower(node->data.url)\n== urlLower ?")
    draw_box(ax, 14.0, 32.5, 16.5, 4.8, "node = node->next",
             fill=PALETTE["slate_fill"], edge=PALETTE["slate_edge"], code=True)
    draw_pill(ax, 34.5, 32.5, 14.5, 4.8, "return false",
              fill=PALETTE["red_fill"], text_color=PALETTE["red_edge"], edge=PALETTE["red_edge"])

    draw_arrow(ax, (23.5, 79.0), (23.5, 75.2))
    draw_arrow(ax, (23.5, 69.2), (23.5, 64.1))
    draw_arrow(ax, (23.5, 54.9), (23.5, 49.4), label="Yes", label_pos=(2.2, 0), label_color=PALETTE["green_edge"])
    draw_polyline(ax, [(34.5, 59.5), (39.0, 59.5), (39.0, 34.9), (34.5, 34.9)],
                  label="No (Exhausted)", label_xy=(38.8, 48.0), label_color=PALETTE["red_edge"])
    draw_polyline(ax, [(14.0, 39.6), (14.0, 34.9)], label="No", label_xy=(11.8, 37.8), label_color=PALETTE["slate_edge"])
    draw_polyline(ax, [(5.75, 32.5), (4.6, 32.5), (4.6, 59.5), (12.5, 59.5)], color=PALETTE["slate_edge"])

    draw_section(ax, 47, 28, 50, 61, "PHASE B  |  SAFE RELINKING & DEALLOCATION  O(1)", PALETTE["green_edge"])
    draw_box(ax, 72.0, 77.2, 45, 14.4,
             "if (node == current) {\n"
             "  if (node->prev)      current = node->prev;\n"
             "  else if (node->next) current = node->next;\n"
             "  else                 current = nullptr;\n}",
             title="Stage 1: Preserve Active current Cursor",
             fill=PALETTE["amber_fill"], edge=PALETTE["amber_edge"], fontsize=8.0, code=True)

    draw_box(ax, 72.0, 58.6, 45, 13.0,
             "if (node->prev) node->prev->next = node->next;\n"
             "else            head = node->next;\n"
             "if (node->next) node->next->prev = node->prev;",
             title="Stage 2: Bypass Target (Head / Middle / Tail)",
             fill=PALETTE["teal_fill"], edge=PALETTE["teal_edge"], fontsize=8.1, code=True)

    draw_box(ax, 72.0, 42.8, 30, 8.8,
             "delete node;\nsize--;",
             title="Stage 3: Free Heap Memory",
             fill=PALETTE["green_fill"], edge=PALETTE["green_edge"], fontsize=8.3, code=True)

    draw_pill(ax, 72.0, 32.0, 18, 4.8, "return true",
              fill=PALETTE["green_edge"], text_color="#FFFFFF")

    draw_polyline(ax, [(38.0, 44.5), (45.2, 44.5), (45.2, 77.2), (49.5, 77.2)],
                  label="Yes (Match)", label_xy=(44.8, 61.5), color=PALETTE["green_edge"])
    draw_arrow(ax, (72.0, 70.0), (72.0, 65.1))
    draw_arrow(ax, (72.0, 52.1), (72.0, 47.2))
    draw_arrow(ax, (72.0, 38.4), (72.0, 34.4))

    draw_section(ax, 3, 3.5, 94, 21.5, "MEMORY STATE  |  POINTER RELINK VISUALIZATION (MIDDLE NODE CASE)", PALETTE["teal_edge"])
    draw_box(ax, 17.5, 12.2, 24.5, 10.5,
             "prev == nullptr -> head = node->next\nnext == nullptr -> new tail",
             title="Edge Boundary Rules", fill=PALETTE["slate_fill"], edge=PALETTE["slate_edge"], fontsize=7.8, code=True)
    draw_box(ax, 43.5, 12.2, 14, 7.8, "[ prev ]\ndata | prev | next", fill=PALETTE["blue_fill"], edge=PALETTE["blue_edge"], fontsize=8.0, code=True)
    draw_box(ax, 64.0, 12.2, 14.5, 7.8, "[ target node ]\n(delete)", fill=PALETTE["red_fill"], edge=PALETTE["red_edge"], fontsize=8.0, code=True)
    draw_box(ax, 84.5, 12.2, 14, 7.8, "[ next ]\ndata | prev | next", fill=PALETTE["blue_fill"], edge=PALETTE["blue_edge"], fontsize=8.0, code=True)

    draw_polyline(ax, [(43.5, 16.1), (43.5, 19.6), (84.5, 19.6), (84.5, 16.1)],
                  label="prev->next = node->next", label_xy=(64.0, 20.6), color=PALETTE["green_edge"])
    draw_polyline(ax, [(84.5, 8.3), (84.5, 5.4), (43.5, 5.4), (43.5, 8.3)],
                  label="next->prev = node->prev", label_xy=(64.0, 6.4), color=PALETTE["teal_edge"])
    draw_arrow(ax, (50.5, 12.2), (56.75, 12.2), color=PALETTE["slate_edge"], dashed=True)
    draw_arrow(ax, (71.25, 12.2), (77.5, 12.2), color=PALETTE["slate_edge"], dashed=True)

    save_diagram(fig, out_dir, "1_DLL_Deletion_Algorithm.png", sodo_dir)


# ---------------------------------------------------------------------------
# 2. Two-Stack Navigation & Reconstruction Overhead (benchmarks/Benchmark.cpp)
# ---------------------------------------------------------------------------
def build_twostack_navigation(out_dir: Path, sodo_dir: Path = None):
    fig, ax = new_canvas(
        (15, 9.2),
        "2. Two-Stack Simulator Architecture  —  TwoStackSimulator (Benchmark Baseline)",
        "Three O(1) navigation lanes vs O(N) stack-rebuild overhead documented in benchmarks/Benchmark.cpp"
    )

    draw_section(ax, 3, 66, 94, 22.5, "LANE 1  |  visit(Page p)  —  Push Current & Truncate Forward Branch", PALETTE["blue_edge"])
    draw_box(ax, 16, 75.5, 21, 9.5, "if (current != nullptr)\n  backStack.push(*current);\n  delete current;", fill=PALETTE["blue_fill"], edge=PALETTE["blue_edge"], code=True, fontsize=8.0)
    draw_box(ax, 42, 75.5, 20, 9.5, "current = new Page(p);\n(Active Session Pointer)", fill=PALETTE["green_fill"], edge=PALETTE["green_edge"], code=True, fontsize=8.2)
    draw_box(ax, 69, 75.5, 22, 9.5, "while (!forwardStack.empty())\n  forwardStack.pop();", fill=PALETTE["red_fill"], edge=PALETTE["red_edge"], code=True, fontsize=8.0)
    draw_pill(ax, 90, 75.5, 11, 5.2, "O(k) Trunc.", fill=PALETTE["amber_fill"], text_color=PALETTE["amber_edge"], edge=PALETTE["amber_edge"], fontsize=8.3)
    draw_arrow(ax, (26.5, 75.5), (32.0, 75.5))
    draw_arrow(ax, (52.0, 75.5), (58.0, 75.5))
    draw_arrow(ax, (80.0, 75.5), (84.5, 75.5))

    draw_section(ax, 3, 45, 45.5, 18.5, "LANE 2  |  back()  —  O(1)", PALETTE["teal_edge"])
    draw_diamond(ax, 12.5, 53.0, 14.5, 8.2, "backStack\nempty?", fontsize=8.0)
    draw_box(ax, 34.5, 53.0, 23, 9.8,
             "if (current) forwardStack.push(*current);\ncurrent = new Page(backStack.top());\nbackStack.pop(); return true;",
             fill=PALETTE["teal_fill"], edge=PALETTE["teal_edge"], code=True, fontsize=7.8)
    draw_arrow(ax, (19.75, 53.0), (23.0, 53.0), label="No", label_pos=(0, 2.2), color=PALETTE["green_edge"])
    ax.text(12.5, 46.8, "Yes -> return false", fontsize=7.8, fontweight="bold", color=PALETTE["red_edge"], ha="center")

    draw_section(ax, 51.5, 45, 45.5, 18.5, "LANE 3  |  forward()  —  O(1)", PALETTE["green_edge"])
    draw_diamond(ax, 61.0, 53.0, 15.0, 8.2, "forwardStack\nempty?", fontsize=8.0)
    draw_box(ax, 83.0, 53.0, 23, 9.8,
             "if (current) backStack.push(*current);\ncurrent = new Page(forwardStack.top());\nforwardStack.pop(); return true;",
             fill=PALETTE["green_fill"], edge=PALETTE["green_edge"], code=True, fontsize=7.8)
    draw_arrow(ax, (68.5, 53.0), (71.5, 53.0), label="No", label_pos=(0, 2.2), color=PALETTE["green_edge"])
    ax.text(61.0, 46.8, "Yes -> return false", fontsize=7.8, fontweight="bold", color=PALETTE["red_edge"], ha="center")

    draw_section(ax, 3, 4, 94, 38, "SEARCH & DELETE PENALTY  |  Two-Stack Temporary Stack Rebuild Loop  O(N) with 2x Copy", PALETTE["red_edge"])
    draw_box(ax, 15.5, 29, 20, 8.2, "1. Check current Page\nif (current && url == key)\n  return / delete!",
             fill=PALETTE["amber_fill"], edge=PALETTE["amber_edge"], code=True, fontsize=8.0)
    draw_box(ax, 42, 29, 25, 9.0, "2. Drain backStack -> temp\nwhile (!backStack.empty()) {\n  check/skip top; temp.push(...);\n}",
             fill=PALETTE["blue_fill"], edge=PALETTE["blue_edge"], code=True, fontsize=7.8)
    draw_box(ax, 72, 29, 24, 9.0, "3. Restore temp -> backStack\nwhile (!temp.empty()) {\n  backStack.push(temp.top()); temp.pop();\n}",
             fill=PALETTE["slate_fill"], edge=PALETTE["slate_edge"], code=True, fontsize=7.8)

    draw_box(ax, 42, 13.5, 25, 9.0, "4. Drain forwardStack -> temp\nwhile (!forwardStack.empty()) {\n  check/skip top; temp.push(...);\n}",
             fill=PALETTE["teal_fill"], edge=PALETTE["teal_edge"], code=True, fontsize=7.8)
    draw_box(ax, 72, 13.5, 24, 9.0, "5. Restore temp -> forwardStack\nwhile (!temp.empty()) {\n  forwardStack.push(temp.top());\n}",
             fill=PALETTE["slate_fill"], edge=PALETTE["slate_edge"], code=True, fontsize=7.8)
    draw_box(ax, 15.5, 13.5, 20, 9.0,
             "Contrast with DLL:\nBrowserHistory scans\nhead -> next in-place\nwith ZERO allocations!",
             fill=PALETTE["green_fill"], edge=PALETTE["green_edge"], fontsize=8.2)

    draw_arrow(ax, (25.5, 29), (29.5, 29))
    draw_arrow(ax, (54.5, 29), (60.0, 29))
    draw_polyline(ax, [(84, 29), (93.5, 29), (93.5, 21.5), (27.5, 21.5), (27.5, 13.5), (29.5, 13.5)])
    draw_arrow(ax, (54.5, 13.5), (60.0, 13.5))

    save_diagram(fig, out_dir, "2_Two-Stack_Navigation.png", sodo_dir)


# ---------------------------------------------------------------------------
# 3. Cache Stack Bounded Insertion & Bottom Eviction (src/CacheStack.cpp::push)
# ---------------------------------------------------------------------------
def build_cache_limit(out_dir: Path, sodo_dir: Path = None):
    fig, ax = new_canvas(
        (15, 9.2),
        "3. Bounded LIFO Cache Insertion & Bottom Eviction  —  CacheStack::push(Page p)",
        "Exact control flow from src/CacheStack.cpp: deduplication guard, size == 1 edge case, and O(N) tail eviction"
    )

    draw_section(ax, 3, 4.5, 60, 84.5, "CONTROL FLOW  |  CacheStack::push(Page p)   (maxSize = 100)", PALETTE["teal_edge"])
    draw_pill(ax, 21.5, 81.5, 22, 4.8, "START: push(Page p)")
    draw_diamond(ax, 21.5, 70.0, 23, 8.8, "urlExists(p.url) ?")
    draw_pill(ax, 48.0, 70.0, 19, 5.0, "return (Skip Dup)",
              fill=PALETTE["amber_fill"], text_color=PALETTE["amber_edge"], edge=PALETTE["amber_edge"], fontsize=8.3)
    draw_diamond(ax, 21.5, 55.0, 23, 8.8, "size >= maxSize ?")

    draw_diamond(ax, 46.0, 55.0, 17, 8.4, "size == 1 ?")
    draw_box(ax, 46.0, 42.0, 22, 7.6, "delete top;\ntop = nullptr;\nsize = 0;",
             fill=PALETTE["red_fill"], edge=PALETTE["red_edge"], code=True, fontsize=7.9)
    draw_box(ax, 46.0, 27.5, 27.5, 12.2,
             "node = top;\nwhile (node->next->next != nullptr)\n  node = node->next;\ndelete node->next;\nnode->next = nullptr;  size--;",
             title="Evict Bottom Node (size > 1)", fill=PALETTE["red_fill"], edge=PALETTE["red_edge"], code=True, fontsize=7.4)

    draw_box(ax, 21.5, 12.5, 29, 10.5,
             "newNode = new StackNode(p);\nnewNode->next = top;\ntop = newNode;  size++;",
             title="LIFO Top Push", fill=PALETTE["green_fill"], edge=PALETTE["green_edge"], code=True, fontsize=8.0)
    draw_pill(ax, 48.0, 12.5, 14, 4.8, "DONE", fill=PALETTE["green_edge"], text_color="#FFFFFF")

    draw_arrow(ax, (21.5, 79.1), (21.5, 74.4))
    draw_arrow(ax, (33.0, 70.0), (38.5, 70.0), label="Yes", label_pos=(0, 2.1), color=PALETTE["amber_edge"])
    draw_arrow(ax, (21.5, 65.6), (21.5, 59.4), label="No", label_pos=(2.0, 0), color=PALETTE["green_edge"])
    draw_arrow(ax, (33.0, 55.0), (37.5, 55.0), label="Yes", label_pos=(0, 2.1), color=PALETTE["red_edge"])
    draw_arrow(ax, (21.5, 50.6), (21.5, 17.75), label="No (Has Capacity)", label_pos=(-6.2, 0), color=PALETTE["green_edge"])
    draw_arrow(ax, (46.0, 50.8), (46.0, 45.8), label="Yes", label_pos=(2.2, 0), color=PALETTE["red_edge"])
    draw_polyline(ax, [(54.5, 55.0), (61.2, 55.0), (61.2, 27.5), (59.75, 27.5)],
                  label="No", label_xy=(61.2, 41.5), color=PALETTE["slate_edge"])
    draw_polyline(ax, [(35.0, 42.0), (28.5, 42.0), (28.5, 17.75)], color=PALETTE["slate_edge"])
    draw_polyline(ax, [(32.25, 27.5), (28.5, 27.5), (28.5, 17.75)], color=PALETTE["slate_edge"])
    draw_arrow(ax, (36.0, 12.5), (41.0, 12.5))

    draw_section(ax, 65.5, 4.5, 31.5, 84.5, "LINKED STACK MEMORY LAYOUT", PALETTE["navy_fill"])
    ax.text(81.25, 81.5, "Before Push (Full: size == 100)", fontsize=9.1, fontweight="bold", color=PALETTE["ink"], ha="center")
    draw_box(ax, 81.25, 73.5, 25, 5.8, "top -> [ URL #100 ] (Newest)", fill=PALETTE["blue_fill"], edge=PALETTE["blue_edge"], code=True, fontsize=7.9)
    draw_box(ax, 81.25, 64.5, 25, 5.8, "...    [ URL #2..#99 ]", fill=PALETTE["slate_fill"], edge=PALETTE["slate_edge"], code=True, fontsize=7.9)
    draw_box(ax, 81.25, 55.5, 25, 5.8, "tail -> [ URL #1 ] (Evict!)", fill=PALETTE["red_fill"], edge=PALETTE["red_edge"], code=True, fontsize=7.9)
    draw_arrow(ax, (81.25, 70.6), (81.25, 67.4))
    draw_arrow(ax, (81.25, 61.6), (81.25, 58.4))

    ax.text(81.25, 44.5, "After Bottom Eviction + Top Push", fontsize=9.1, fontweight="bold", color=PALETTE["green_edge"], ha="center")
    draw_box(ax, 81.25, 36.5, 25, 5.8, "top -> [ New Page ] (Node #101)", fill=PALETTE["green_fill"], edge=PALETTE["green_edge"], code=True, fontsize=7.9)
    draw_box(ax, 81.25, 27.5, 25, 5.8, "next -> [ URL #100 .. #2 ]", fill=PALETTE["blue_fill"], edge=PALETTE["blue_edge"], code=True, fontsize=7.9)
    draw_box(ax, 81.25, 18.5, 25, 5.8, "node->next = nullptr (size=100)", fill=PALETTE["slate_fill"], edge=PALETTE["slate_edge"], code=True, fontsize=7.9)
    draw_arrow(ax, (81.25, 33.6), (81.25, 30.4))
    draw_arrow(ax, (81.25, 24.6), (81.25, 21.4))

    draw_box(ax, 81.25, 9.5, 27, 5.8, "Invariants: size <= maxSize & unique URLs\nCopy/Assign deleted (Rule of Three)",
             fill=PALETTE["amber_fill"], edge=PALETTE["amber_edge"], fontsize=7.8)

    save_diagram(fig, out_dir, "3_Cache_Limit_Algorithm.png", sodo_dir)


# ---------------------------------------------------------------------------
# 4. QPC Benchmark Harness Architecture (benchmarks/Benchmark.cpp)
# ---------------------------------------------------------------------------
def build_benchmark_harness(out_dir: Path, sodo_dir: Path = None):
    fig, ax = new_canvas(
        (15, 9.0),
        "4. High-Resolution QPC Benchmark & RAM Probe  —  benchmarks/Benchmark.cpp",
        "Automated scaling sweep (N = 10..10000) measuring sub-microsecond latency via QueryPerformanceCounter & PSAPI"
    )

    draw_section(ax, 3, 47.5, 94, 41.5, "TIER 1  |  SCALING HARNESS: runPerformanceBenchmark()   (N in {10, 100, 1000, 5000, 10000})", PALETTE["blue_edge"])
    draw_box(ax, 15, 73.0, 20.5, 13.5,
             "dll_before = PSAPI()\npopulate N pages\ndll_after  = PSAPI()\nDelta = after - before",
             title="1A. Build BrowserHistory", fill=PALETTE["blue_fill"], edge=PALETTE["blue_edge"], code=True, fontsize=7.8)
    draw_box(ax, 39.5, 73.0, 21.5, 13.5,
             "ts_before = PSAPI()\npopulate N pages\nts_after  = PSAPI()\nDelta = after - before",
             title="1B. Build TwoStackSimulator", fill=PALETTE["teal_fill"], edge=PALETTE["teal_edge"], code=True, fontsize=7.8)
    draw_box(ax, 64.5, 73.0, 21.5, 13.5,
             "target = \"url_\" +\n  to_string(N / 2) + \".com\"\n(Mid-history stress key)",
             title="2. Mid-List Target Key", fill=PALETTE["amber_fill"], edge=PALETTE["amber_edge"], code=True, fontsize=7.8)
    draw_box(ax, 86.5, 73.0, 16.5, 13.5,
             "Search(target)\nDelete(target)\nBack()\nForward()",
             title="3. Dispatch Ops", fill=PALETTE["green_fill"], edge=PALETTE["green_edge"], code=True, fontsize=7.9)

    draw_arrow(ax, (25.25, 73.0), (28.75, 73.0))
    draw_arrow(ax, (50.25, 73.0), (53.75, 73.0))
    draw_arrow(ax, (75.25, 73.0), (78.25, 73.0))

    draw_box(ax, 45.5, 55.0, 77, 9.0,
             "Loop Next Milestone N   |   Outputs: Operation | DLL Time (us) | TS Time (us) | DLL Ops/sec\n"
             "Observed at N=10,000: DLL Search & Delete are ~2.8x-3.0x faster; Back & Forward stay sub-microsecond O(1)",
             fill=PALETTE["slate_fill"], edge=PALETTE["slate_edge"], fontsize=8.4)

    draw_section(ax, 3, 4.5, 94, 38.5, "TIER 2  |  TEMPLATE PROBE: measureExecutionTime<Func>(iterations = 1000, func)", PALETTE["green_edge"])
    draw_box(ax, 14, 24.5, 18, 12.0, "QueryPerformance\nFrequency(&freq)\n\n(Hardware TSC Hz)", fill=PALETTE["blue_fill"], edge=PALETTE["blue_edge"], code=True, fontsize=8.0)
    draw_box(ax, 33, 24.5, 15, 12.0, "QueryPerformance\nCounter(&start)", fill=PALETTE["teal_fill"], edge=PALETTE["teal_edge"], code=True, fontsize=8.0)
    draw_box(ax, 51, 24.5, 17, 12.0, "for i = 0 .. 999:\n  func();\n(Amortizes jitter)", fill=PALETTE["amber_fill"], edge=PALETTE["amber_edge"], code=True, fontsize=7.9)
    draw_box(ax, 69, 24.5, 15, 12.0, "QueryPerformance\nCounter(&end)", fill=PALETTE["teal_fill"], edge=PALETTE["teal_edge"], code=True, fontsize=8.0)
    draw_box(ax, 87, 24.5, 16.5, 12.0,
             "total = dTicks*1e6/freq\navg = total / 1000\nformatTime / Ops",
             fill=PALETTE["green_fill"], edge=PALETTE["green_edge"], code=True, fontsize=7.6)

    draw_arrow(ax, (23.0, 24.5), (25.5, 24.5))
    draw_arrow(ax, (40.5, 24.5), (42.5, 24.5))
    draw_arrow(ax, (59.5, 24.5), (61.5, 24.5))
    draw_arrow(ax, (76.5, 24.5), (78.75, 24.5))

    # Route Tier 1 Dispatch -> Tier 2 cleanly at x=91.0
    draw_polyline(ax, [(91.0, 66.25), (91.0, 30.5)],
                  label="Measure 1,000x", label_xy=(91.0, 45.2), color=PALETTE["green_edge"])
    # Return avg_us through the clean gap at x=77.5 (past Tier 2 title, between End Tick & Format boxes)
    draw_polyline(ax, [(87.0, 18.5), (87.0, 10.5), (77.5, 10.5), (77.5, 50.5)],
                  label="Return avg_us", label_xy=(82.3, 12.2), color=PALETTE["navy_fill"])

    ax.text(32.0, 10.5, "formatTime(): scientific (< 0.01 us) | fixed (>= 0.01 us)", fontsize=8.4,
            fontweight="bold", color=PALETTE["muted"], ha="center", va="center")

    save_diagram(fig, out_dir, "4_Benchmark_QPC_Algorithm.png", sodo_dir)


# ---------------------------------------------------------------------------
# 5. 4-Layer System Architecture (Full Repo Pipeline)
# ---------------------------------------------------------------------------
def draw_layer_band(ax, y, h, tag, sublabel, accent):
    panel = FancyBboxPatch(
        (13.5, y), 83.5, h,
        boxstyle="round,pad=0.2,rounding_size=1.0",
        facecolor=PALETTE["panel_bg"], edgecolor=PALETTE["panel_border"], linewidth=1.3, zorder=1
    )
    ax.add_patch(panel)
    rail = FancyBboxPatch(
        (3.0, y), 9.6, h,
        boxstyle="round,pad=0.2,rounding_size=1.0",
        facecolor=accent, edgecolor=accent, linewidth=1.3, zorder=2
    )
    ax.add_patch(rail)
    ax.text(7.8, y + h * 0.57, tag, fontsize=9.2, fontweight="bold", color="#FFFFFF", ha="center", va="center", zorder=4)
    ax.text(7.8, y + h * 0.34, sublabel, fontsize=7.4, color="#E2E8F0", ha="center", va="center", zorder=4, linespacing=1.2)


def build_system_architecture(out_dir: Path, sodo_dir: Path = None):
    fig, ax = new_canvas(
        (15, 9.2),
        "5. System Architecture & End-to-End Execution Pipeline",
        "Layered decomposition separating CLI control, data structures, OS probes, datasets, tests, and plotting"
    )

    draw_layer_band(ax, 72.5, 15.5, "LAYER 1", "CLI Menu\nsrc/main.cpp", PALETTE["navy_fill"])
    draw_box(ax, 27.5, 80.25, 25, 8.8, "Interactive Options 1-9\nvisit, back, forward, search, delete, cache", fill=PALETTE["blue_fill"], edge=PALETTE["blue_edge"], fontsize=8.1)
    draw_box(ax, 55.5, 80.25, 25, 8.8, "Option 10: QPC Benchmark\nRuns N=10..10000 Latency & RAM Sweep", fill=PALETTE["amber_fill"], edge=PALETTE["amber_edge"], fontsize=8.1)
    draw_box(ax, 83.0, 80.25, 24, 8.8, "Option 11: Dataset Loader\nParses datasets/data_<N>.txt", fill=PALETTE["teal_fill"], edge=PALETTE["teal_edge"], fontsize=8.1)

    draw_layer_band(ax, 49.0, 18.5, "LAYER 2", "Core Engines\n& Tests", PALETTE["blue_edge"])
    draw_box(ax, 27.5, 58.25, 25, 11.4,
             "Doubly Linked List (head, current)\nO(1) back/forward; O(N) scan/delete",
             title="BrowserHistory", fill=PALETTE["blue_fill"], edge=PALETTE["blue_edge"], fontsize=8.0)
    draw_box(ax, 55.5, 58.25, 25, 11.4,
             "Bounded Singly-Linked Stack (max 100)\nDuplicate URL guard + bottom eviction",
             title="CacheStack", fill=PALETTE["teal_fill"], edge=PALETTE["teal_edge"], fontsize=8.0)
    draw_box(ax, 83.0, 58.25, 24, 11.4,
             "Reference std::stack<Page> Model\nOption 10 baseline & UT-01..UT-05",
             title="TwoStack & Tests", fill=PALETTE["green_fill"], edge=PALETTE["green_edge"], fontsize=8.0)

    draw_layer_band(ax, 26.5, 17.5, "LAYER 3", "Models &\nOS Probes", PALETTE["slate_edge"])
    draw_box(ax, 27.5, 35.25, 25, 10.2,
             "Page {url, title, visitTime}\nDLLNode & CacheStack::StackNode",
             title="Structs & Records (include/)", fill=PALETTE["slate_fill"], edge=PALETTE["slate_edge"], fontsize=7.9)
    draw_box(ax, 55.5, 35.25, 25, 10.2,
             "QueryPerformanceCounter / Frequency\nstd::chrono high-resolution timing",
             title="Sub-Microsecond Timer", fill=PALETTE["amber_fill"], edge=PALETTE["amber_edge"], fontsize=7.9)
    draw_box(ax, 83.0, 35.25, 24, 10.2,
             "psapi.dll -> GetProcessMemoryInfo\nWorkingSetSize KB Probe",
             title="PSAPI Memory Probe", fill=PALETTE["red_fill"], edge=PALETTE["red_edge"], fontsize=7.9)

    draw_layer_band(ax, 4.5, 16.5, "LAYER 4", "Data & Plot\nPipeline", PALETTE["green_edge"])
    draw_box(ax, 27.5, 12.75, 24, 8.8, "datasets/generate_datasets.py\n-> data_{10..10000}.txt", fill=PALETTE["blue_fill"], edge=PALETTE["blue_edge"], fontsize=8.1)
    draw_box(ax, 55.5, 12.75, 24, 8.8, "Compiled C++ Binary\nLive Option 10 + Option 11 Run", fill=PALETTE["amber_fill"], edge=PALETTE["amber_edge"], fontsize=8.1)
    draw_box(ax, 83.0, 12.75, 23, 8.8, "results/*.csv + *.txt\n-> plot_*.py -> *.png", fill=PALETTE["green_fill"], edge=PALETTE["green_edge"], fontsize=8.1)

    # Exact logical C++ call graph connectors across layer gutters:
    # Options 1-9 -> BrowserHistory & CacheStack
    draw_arrow(ax, (25.0, 75.85), (25.0, 63.95))
    draw_polyline(ax, [(33.5, 75.85), (33.5, 70.6), (51.0, 70.6), (51.0, 63.95)])
    # Option 10 -> BrowserHistory & TwoStackSimulator
    draw_polyline(ax, [(48.0, 75.85), (48.0, 69.2), (29.5, 69.2), (29.5, 63.95)])
    draw_polyline(ax, [(62.5, 75.85), (62.5, 69.2), (76.0, 69.2), (76.0, 63.95)])
    # Option 11 -> BrowserHistory & CacheStack
    draw_polyline(ax, [(79.0, 75.85), (79.0, 71.2), (59.5, 71.2), (59.5, 63.95)])

    # Layer 2 -> Layer 3 dependencies
    draw_arrow(ax, (25.0, 52.55), (25.0, 40.35))
    draw_polyline(ax, [(55.5, 52.55), (55.5, 46.5), (32.5, 46.5), (32.5, 40.35)])
    draw_polyline(ax, [(78.5, 52.55), (78.5, 46.5), (55.5, 46.5), (55.5, 40.35)])
    draw_arrow(ax, (84.5, 52.55), (84.5, 40.35))

    # Layer 3 -> Layer 4 pipeline handoff + Stage-4 left-to-right data flow
    draw_arrow(ax, (55.5, 30.15), (55.5, 17.15))
    draw_arrow(ax, (83.0, 30.15), (63.0, 17.15))
    draw_arrow(ax, (39.5, 12.75), (43.5, 12.75))
    draw_arrow(ax, (67.5, 12.75), (71.5, 12.75))

    save_diagram(fig, out_dir, "5_System_Architecture.png", sodo_dir)


# ---------------------------------------------------------------------------
# 6. C++11 UML Class & Module Diagram (include/*.h)
# ---------------------------------------------------------------------------
def draw_uml_box(ax, cx, top_y, w, header, attrs, methods, stereotype=None, edge=PALETTE["blue_edge"], fill_head="#EFF6FF"):
    line_h = 2.05
    head_h = 5.4 if stereotype else 3.8
    attr_h = max(2.8, len(attrs) * line_h + 1.4)
    meth_h = max(2.8, len(methods) * line_h + 1.4)
    total_h = head_h + attr_h + meth_h
    x = cx - w / 2
    y = top_y - total_h

    outer = FancyBboxPatch((x, y), w, total_h, boxstyle="round,pad=0,rounding_size=0.6",
                           facecolor="#FFFFFF", edgecolor=edge, linewidth=1.6, zorder=3)
    ax.add_patch(outer)
    hdr = FancyBboxPatch((x, top_y - head_h), w, head_h, boxstyle="round,pad=0,rounding_size=0.6",
                         facecolor=fill_head, edgecolor=edge, linewidth=1.4, zorder=3)
    ax.add_patch(hdr)

    if stereotype:
        ax.text(cx, top_y - 1.5, stereotype, fontsize=7.6, style="italic", color=edge, ha="center", va="center", zorder=4)
        ax.text(cx, top_y - 3.6, header, fontsize=9.8, fontweight="bold", color=PALETTE["ink"], ha="center", va="center", zorder=4)
    else:
        ax.text(cx, top_y - head_h / 2, header, fontsize=9.8, fontweight="bold", color=PALETTE["ink"], ha="center", va="center", zorder=4)

    y_sep = top_y - head_h - attr_h
    ax.plot([x, x + w], [y_sep, y_sep], color=edge, linewidth=1.1, zorder=4)

    for i, a in enumerate(attrs):
        ax.text(x + 1.1, top_y - head_h - 1.5 - i * line_h, a, fontsize=7.6,
                family="DejaVu Sans Mono", color=PALETTE["ink"], ha="left", va="center", zorder=4)
    for j, m in enumerate(methods):
        ax.text(x + 1.1, y_sep - 1.5 - j * line_h, m, fontsize=7.6,
                family="DejaVu Sans Mono", color=PALETTE["ink"], ha="left", va="center", zorder=4)

    return {"cx": cx, "top": top_y, "bottom": y, "left": x, "right": x + w}


def build_uml_class_diagram(out_dir: Path, sodo_dir: Path = None):
    fig, ax = new_canvas(
        (16, 9.6),
        "6. C++11 UML Class & Struct Diagram  —  include/*.h",
        "Exact member types, deleted Rule-of-Three copy operators, and ownership relations verified against headers"
    )

    bh = draw_uml_box(
        ax, 19, 88, 31, "BrowserHistory",
        ["- head : DLLNode*", "- current : DLLNode*", "- size : int"],
        [
            "+ BrowserHistory() / ~BrowserHistory()",
            "+ visit(p : Page) : void",
            "+ back() : bool",
            "+ forward() : bool",
            "+ searchHistory(kw : string) const : void",
            "+ searchHistorySilent(kw : string) const : bool",
            "+ deleteByUrl(url : string) : bool",
            "+ clearHistory() : void",
            "+ getCurrentPage() const : Page*",
            "+ canGoBack() / canGoForward() const : bool",
            "+ getSize() const : int / isEmpty() const : bool",
        ],
        edge=PALETTE["blue_edge"], fill_head=PALETTE["blue_fill"]
    )

    cs = draw_uml_box(
        ax, 53, 88, 30, "CacheStack",
        [
            "- top : StackNode*",
            "- size : int",
            "- maxSize : int  (default 5 / CLI 100)",
            "- StackNode (private nested struct)",
            "~ deleted: CacheStack(const CacheStack&)",
            "~ deleted: operator=(const CacheStack&)",
        ],
        [
            "+ CacheStack(maxSize : int = 5)",
            "+ ~CacheStack()",
            "+ push(p : Page) : void",
            "+ pop() : Page",
            "+ peek() const : Page*",
            "+ displayCache() const / clearCache() : void",
            "+ isEmpty() const : bool / getSize() const : int",
        ],
        edge=PALETTE["teal_edge"], fill_head=PALETTE["teal_fill"]
    )

    ts = draw_uml_box(
        ax, 84, 88, 26, "TwoStackSimulator",
        [
            "- backStack : std::stack<Page>",
            "- forwardStack : std::stack<Page>",
            "- current : Page*",
        ],
        [
            "+ TwoStackSimulator() / ~TwoStackSimulator()",
            "+ visit(p : Page) : void",
            "+ back() : bool",
            "+ forward() : bool",
            "+ searchHistory(kw : string) : bool",
            "+ deleteByUrl(url : string) : bool",
        ],
        edge=PALETTE["green_edge"], fill_head=PALETTE["green_fill"]
    )

    dll = draw_uml_box(
        ax, 19, 36, 27, "DLLNode",
        ["+ data : Page", "+ prev : DLLNode*", "+ next : DLLNode*"],
        ["+ DLLNode(p : Page)"],
        stereotype="<<struct>>", edge=PALETTE["slate_edge"], fill_head=PALETTE["slate_fill"]
    )

    sn = draw_uml_box(
        ax, 53, 36, 27, "CacheStack::StackNode",
        ["+ data : Page", "+ next : StackNode*"],
        ["+ StackNode(p : Page)"],
        stereotype="<<private struct>>", edge=PALETTE["teal_edge"], fill_head=PALETTE["slate_fill"]
    )

    pg = draw_uml_box(
        ax, 84, 46, 26, "Page",
        ["+ url : std::string", "+ title : std::string", "+ visitTime : std::string"],
        ["+ Page()", "+ Page(url, title, visitTime)"],
        stereotype="<<struct>>", edge=PALETTE["amber_edge"], fill_head=PALETTE["amber_fill"]
    )

    draw_uml_box(
        ax, 84, 21, 26, "Utils & Benchmark",
        ["Windows API: QueryPerformanceCounter", "PSAPI: GetProcessMemoryInfo"],
        [
            "+ getCurrentTime() : string",
            "+ getIntInput(prompt) : int",
            "+ getActualRAMUsageKB() : double",
            "+ runPerformanceBenchmark() : void",
        ],
        stereotype="<<module>>", edge=PALETTE["slate_edge"], fill_head=PALETTE["slate_fill"]
    )

    draw_arrow(ax, (19, bh["bottom"]), (19, dll["top"]), label="1  *--  0..* owns", label_pos=(6.5, 0), color=PALETTE["blue_edge"])
    draw_arrow(ax, (53, cs["bottom"]), (53, sn["top"]), label="1  *--  0..maxSize", label_pos=(7.2, 0), color=PALETTE["teal_edge"])
    draw_arrow(ax, (84, ts["bottom"]), (84, pg["top"]), label="holds Page values", label_pos=(7.0, 0), color=PALETTE["green_edge"])

    # Route Page composition from DLLNode cleanly beneath StackNode (y=15.0) with no box crossings
    draw_polyline(ax, [(19, dll["bottom"]), (19, 15.0), (70.0, 15.0), (70.0, 35.0), (pg["left"], 35.0)],
                  label="holds Page (1:1)", label_xy=(44.5, 15.0), color=PALETTE["slate_edge"])
    draw_polyline(ax, [(53, sn["bottom"]), (53, 15.0)], color=PALETTE["teal_edge"])

    save_diagram(fig, out_dir, "6_System_Design_UML.png", sodo_dir)


def main():
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Generate engineering diagrams for docs/diagrams/.")
    parser.add_argument("--out-dir", type=Path, default=repo_root / "docs" / "diagrams")
    parser.add_argument("--sodo-dir", type=Path, default=None, help="Optional secondary folder copy (e.g. so do/)")
    args = parser.parse_args()

    build_dll_deletion(args.out_dir, args.sodo_dir)
    build_twostack_navigation(args.out_dir, args.sodo_dir)
    build_cache_limit(args.out_dir, args.sodo_dir)
    build_benchmark_harness(args.out_dir, args.sodo_dir)
    build_system_architecture(args.out_dir, args.sodo_dir)
    build_uml_class_diagram(args.out_dir, args.sodo_dir)


if __name__ == "__main__":
    main()
