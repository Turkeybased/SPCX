/*
 * DotPattern and BorderBeam adapted for this static React runtime from Magic UI.
 * https://magicui.design/r/dot-pattern.json
 * https://magicui.design/r/border-beam.json
 * Copyright (c) Magic UI. MIT license: see THIRD-PARTY-NOTICES.txt.
 * SVG repetition and CSS animation replace Motion/Tailwind dependencies.
 */
window.IPOVisuals = (() => {
  function DotPattern({ id, spacing = 24 }) {
    const h = React.createElement;
    return h('svg', { className: 'ipo-dot-pattern', 'aria-hidden': true, focusable: false, width: '100%', height: '100%' },
      h('defs', null, h('pattern', { id, width: spacing, height: spacing, patternUnits: 'userSpaceOnUse' },
        h('circle', { cx: 1, cy: 1, r: 1, fill: 'currentColor' }))),
      h('rect', { width: '100%', height: '100%', fill: 'url(#' + id + ')' }));
  }
  function BorderBeam() {
    return React.createElement('div', { className: 'ipo-border-beam', 'aria-hidden': true },
      React.createElement('div', { className: 'ipo-border-light' }));
  }
  // A conceptual coverage illustration, with no quantitative axes or price marks.
  function CoverageArt() {
    const h = React.createElement;
    const names = [
      { name: 'SpaceX', x: 95, y: 91, color: '#ffa568', symbol: 'X' },
      { name: 'Anthropic', x: 284, y: 125, color: '#a7cdff', symbol: 'A' },
      { name: 'OpenAI', x: 175, y: 247, color: '#c6b4f2', symbol: 'O' },
    ];
    return h('div', { className: 'ipo-coverage-art', 'aria-hidden': true },
      h('svg', { viewBox: '0 0 380 315', focusable: false },
        h('defs', null,
          h('radialGradient', { id: 'ipo-orbit-glow' }, h('stop', { offset: '0%', stopColor: '#4d7bc2', stopOpacity: 0.2 }), h('stop', { offset: '100%', stopColor: '#4d7bc2', stopOpacity: 0 })),
          h('linearGradient', { id: 'ipo-orbit-line', x1: '0%', x2: '100%', y1: '0%', y2: '100%' }, h('stop', { stopColor: '#ff9d61' }), h('stop', { offset: '55%', stopColor: '#8bbdff' }), h('stop', { offset: '100%', stopColor: '#bd98e8' }))),
        h('circle', { cx: 190, cy: 157, r: 151, fill: 'url(#ipo-orbit-glow)' }),
        ...[66, 104, 142].map((r, i) => h('circle', { key: r, cx: 190, cy: 157, r, fill: 'none', stroke: i === 1 ? 'url(#ipo-orbit-line)' : '#527399', strokeOpacity: i === 1 ? 0.5 : 0.2, strokeWidth: 1, strokeDasharray: i === 2 ? '2 7' : undefined })),
        h('path', { className: 'ipo-orbit-arc', d: 'M 48 157 A 142 142 0 0 1 190 15', fill: 'none', stroke: '#b0cfff', strokeWidth: 2, strokeLinecap: 'round' }),
        h('line', { x1: 190, y1: 43, x2: 190, y2: 272, stroke: '#6587af', strokeOpacity: 0.18 }),
        h('line', { x1: 75, y1: 157, x2: 305, y2: 157, stroke: '#6587af', strokeOpacity: 0.18 }),
        h('circle', { cx: 190, cy: 157, r: 40, fill: '#101b2c', stroke: '#57718c' }),
        h('text', { x: 190, y: 152, textAnchor: 'middle', fill: '#e7edf5', fontSize: 12, letterSpacing: 2 }, 'PRICE'),
        h('text', { x: 190, y: 170, textAnchor: 'middle', fill: '#7c9abd', fontSize: 9, letterSpacing: 1 }, '× EVIDENCE'),
        ...names.map(n => h('g', { key: n.name },
          h('circle', { cx: n.x, cy: n.y, r: 24, fill: '#0b1422', stroke: n.color, strokeOpacity: 0.65 }),
          h('circle', { cx: n.x, cy: n.y, r: 29, fill: 'none', stroke: n.color, strokeOpacity: 0.1, strokeWidth: 6 }),
          h('text', { x: n.x, y: n.y + 5, textAnchor: 'middle', fill: n.color, fontSize: 15, fontWeight: 600 }, n.symbol),
          h('text', { x: n.x, y: n.y + 43, textAnchor: 'middle', fill: n.color, fontSize: 10, letterSpacing: 1 }, n.name))),
        h('text', { x: 355, y: 31, textAnchor: 'end', fill: '#6d88a8', fontSize: 8, letterSpacing: 1.5 }, 'COVERAGE / 03')));
  }
  return { DotPattern, BorderBeam, CoverageArt };
})();
