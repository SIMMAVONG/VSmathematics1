import numpy as np
import plotly.graph_objects as go
from engine.common import dec


def _layout(fig, h=460):
    fig.update_layout(height=h, margin=dict(l=10, r=10, t=30, b=10), xaxis_title="x", yaxis_title="y",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0))
    return fig


def _pt(fig, x, y, name, color, label=None, size=10):
    fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text" if label else "markers", name=name,
                             text=[label] if label else None, textposition="top right",
                             marker=dict(size=size, color=color)))


def parabola_fig(r):
    a, b, c = float(r["a"]), float(r["b"]), float(r["c"])
    h, k = float(r["h"]), float(r["k"])
    fx, fy = float(r["focus"][0]), float(r["focus"][1])
    d = float(r["directrix"])
    xs_key = [h, 0.0, fx] + r["roots_f"]
    span = max(xs_key) - min(xs_key)
    pad = max(span * 0.5, 4)
    x = np.linspace(min(xs_key) - pad, max(xs_key) + pad, 500)
    y = a * x ** 2 + b * x + c
    ys_key = [k, c, d, fy] + [0.0] * len(r["roots_f"])
    ylo, yhi = min(ys_key), max(ys_key)
    ypad = max((yhi - ylo) * 0.6, 4)
    yr = [ylo - ypad, yhi + 2 * ypad] if r["opens_up"] else [ylo - 2 * ypad, yhi + ypad]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="parabola", line=dict(width=3)))
    fig.add_vline(x=h, line_dash="dot", line_color="gray", annotation_text="axis")
    fig.add_hline(y=d, line_dash="dash", line_color="orange", annotation_text="directrix")
    _pt(fig, h, k, "Vertex", "red", "V")
    _pt(fig, fx, fy, "Focus", "green", "F")
    _pt(fig, 0, c, "y-intercept", "purple")
    for i, rt in enumerate(r["roots_f"]):
        _pt(fig, rt, 0, "root" if i == 0 else "root ", "blue", dec(rt, 3))
    fig.update_yaxes(range=yr)
    return _layout(fig)


def ellipse_fig(r):
    a, b, h, k = float(r["a"]), float(r["b"]), float(r["h"]), float(r["k"])
    t = np.linspace(0, 2 * np.pi, 400)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=h + a * np.cos(t), y=k + b * np.sin(t), mode="lines", name="ellipse",
                             line=dict(width=3)))
    _pt(fig, h, k, "Center", "black", "C")
    for i, (px, py) in enumerate(r["foci_f"]):
        _pt(fig, px, py, "Focus" if i == 0 else "Focus ", "green", f"F{i + 1}")
    for i, (px, py) in enumerate(r["vertices_f"]):
        _pt(fig, px, py, "Vertex" if i == 0 else "Vertex ", "red")
    for i, (px, py) in enumerate(r["cov_f"]):
        _pt(fig, px, py, "Co-vertex" if i == 0 else "Co-vertex ", "purple")
    fig.add_hline(y=k, line_dash="dot", line_color="gray")
    fig.add_vline(x=h, line_dash="dot", line_color="gray")
    m = max(a, b) + 1.5
    fig.update_xaxes(range=[h - m, h + m])
    fig.update_yaxes(range=[k - m, k + m], scaleanchor="x", scaleratio=1)
    return _layout(fig, 480)


def point_on_ellipse(fig, x0, y0, status):
    color = {"on": "green", "inside": "orange", "outside": "red"}[status]
    _pt(fig, x0, y0, "P", color, "P", 12)
    return fig


def number_line_fig(values):
    vals = [float(v) for v in values.values()]
    lo, hi = min(vals + [0.0]) - 1, max(vals + [0.0]) + 1
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[lo, hi], y=[0, 0], mode="lines", line=dict(color="gray"), showlegend=False))
    for (name, v) in values.items():
        fig.add_trace(go.Scatter(x=[float(v)], y=[0], mode="markers+text", name=name,
                                 text=[f"{name} = {dec(v)}"], textposition="top center",
                                 marker=dict(size=13)))
    fig.update_yaxes(visible=False, range=[-1, 1])
    fig.update_layout(height=170, margin=dict(l=10, r=10, t=10, b=10), showlegend=False, xaxis_title="")
    return fig
