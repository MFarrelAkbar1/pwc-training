// Draws chart blocks from the test JSON with Chart.js
// (loaded as a global from vendor/chart.umd.min.js).
import { fmt } from "./dom.js";

const COLORS = ["#3b6fd8", "#e07b39", "#2e9e6a", "#9b59d0", "#d9485f", "#7d8590", "#c9a227"];
const active = []; // charts on screen, destroyed when the screen changes

export function destroyCharts() {
  while (active.length) active.pop().destroy();
}

function cssVar(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

// Prints each value on its bar / point / slice, like the source charts do,
// so you never have to read values off the axis.
const valueLabels = {
  id: "valueLabels",
  afterDatasetsDraw(chart, _args, options) {
    const { ctx } = chart;
    const { kind, unit } = options;
    ctx.save();
    ctx.font = "600 11px system-ui, sans-serif";
    ctx.textBaseline = "middle";
    chart.data.datasets.forEach((dataset, i) => {
      const meta = chart.getDatasetMeta(i);
      if (meta.hidden) return;
      meta.data.forEach((point, j) => {
        const value = dataset.data[j];
        if (value == null || (kind === "stackedBar" && value === 0)) return;
        const text = fmt(value) + (unit === "%" ? "%" : "");
        let { x, y } = point.tooltipPosition();
        ctx.textAlign = "center";
        ctx.fillStyle = cssVar("--text");
        if (kind === "pie" || kind === "stackedBar") {
          ctx.fillStyle = "#fff";
          if (kind === "stackedBar") y = (point.y + point.base) / 2;
        } else if (kind === "hbar") {
          ctx.textAlign = value < 0 ? "right" : "left";
          x = point.x + (value < 0 ? -4 : 4);
          y = point.y;
        } else {
          y = value < 0 ? point.y + 10 : point.y - 10;
        }
        ctx.fillText(text, x, y);
      });
    });
    ctx.restore();
  },
};

export function chartHeight(block) {
  if (block.kind === "hbar") return Math.max(220, block.labels.length * block.series.length * 20 + 90);
  if (block.kind === "pie") return 280;
  return 300;
}

export function drawChart(canvas, block) {
  if (!window.Chart) throw new Error("Chart library failed to load");
  const { kind } = block;
  const text = cssVar("--text-muted");
  const grid = cssVar("--border");
  const isPie = kind === "pie";

  const datasets = block.series.map((s, i) => ({
    label: s.name,
    data: s.values,
    backgroundColor: isPie ? s.values.map((_, j) => COLORS[j % COLORS.length]) : COLORS[i % COLORS.length],
    borderColor: isPie ? cssVar("--surface") : COLORS[i % COLORS.length],
    borderWidth: kind === "line" ? 2 : 1,
    pointRadius: 4,
  }));

  const valueAxisTitle = block.axisLabel || block.unit || "";
  const axis = (title) => ({
    stacked: kind === "stackedBar",
    ticks: { color: text },
    grid: { color: grid },
    title: { display: Boolean(title), text: title, color: text },
    grace: "8%", // headroom for the value labels
  });

  const chart = new window.Chart(canvas, {
    type: isPie ? "pie" : kind === "line" ? "line" : "bar",
    data: { labels: block.labels, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      indexAxis: kind === "hbar" ? "y" : "x",
      layout: { padding: { right: kind === "hbar" ? 36 : 8, top: 4 } },
      scales: isPie ? {} : kind === "hbar"
        ? { x: axis(valueAxisTitle), y: { ...axis(""), grace: 0 } }
        : { x: { ...axis(""), grace: 0 }, y: axis(valueAxisTitle) },
      plugins: {
        legend: { display: isPie || block.series.length > 1, labels: { color: text } },
        valueLabels: { kind, unit: block.unit },
      },
    },
    plugins: [valueLabels],
  });
  active.push(chart);
}

// Text alternative for screen readers: every value in the chart.
export function describeChart(block) {
  return block.series
    .map((s) => `${s.name}: ` + block.labels.map((label, i) => `${label} ${fmt(s.values[i])}`).join(", "))
    .join("; ");
}
