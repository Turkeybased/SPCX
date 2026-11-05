/* Price/news alignment is descriptive. It is not an estimate of causal impact. */
window.SpaceXContext = (() => {
  const colors = { Deals: '#85c4ff', 'M&A': '#c2a3f4', 'War & policy': '#efb57c', Earnings: '#88d6b1', Launches: '#84c8cb', Capital: '#d6c28f', Market: '#f1919c' };
  const pct = (base, end) => base > 0 && Number.isFinite(end) ? (end / base - 1) * 100 : null;
  const displayPct = n => n == null ? 'Unavailable' : (n > 0 ? '+' : '') + n.toFixed(2) + '%';
  const dollars = n => n == null ? 'Unavailable' : '$' + n.toFixed(2);
  const nextDate = date => new Date(Date.parse(date + 'T12:00:00Z') + 86400000).toISOString().slice(0, 10);
  function eventWindow(event, series, benchmark = [], length = 1) {
    const target = event.timing === 'after_close' ? nextDate(event.date) : event.date;
    const index = series.findIndex(p => p.date >= target);
    if (index < 0) return { status: 'pending', session: null };
    const session = series[index].date;
    if (index === 0) return { status: 'no_prior_close', session };
    const last = series[index + length - 1];
    if (!last) return { status: 'pending', session };
    const previous = series[index - 1];
    const stock = pct(previous.close, last.close);
    const bm = new Map(benchmark.map(p => [p.date, p.close]));
    const benchmarkReturn = pct(bm.get(previous.date), bm.get(last.date));
    const priorVolume = series.slice(Math.max(0, index - 20), index).map(p => p.volume).filter(v => v > 0);
    const mean = priorVolume.length ? priorVolume.reduce((sum, n) => sum + n, 0) / priorVolume.length : null;
    return { status: 'ok', session, from: previous.date, to: last.date, stock, benchmark: benchmarkReturn,
      difference: benchmarkReturn == null ? null : stock - benchmarkReturn,
      volumeRatio: mean ? series[index].volume / mean : null, volumeSample: priorVolume.length };
  }
  function render({ market, archive, state = {}, onChange, retry }) {
    const h = React.createElement;
    const el = (tag, cls, ...children) => h(tag, cls ? { className: cls } : null, ...children);
    const small = text => el('p', 'ipo-small', text);
    const source = s => h('a', { key: s.url, className: 'ipo-source', href: s.url, target: '_blank', rel: 'noopener noreferrer' }, s.publisher + ' ↗');
    const button = (label, active, onClick) => h('button', { type: 'button', className: 'scx-toggle', 'aria-pressed': active, onClick }, label);
    const series = market?.stock?.series || [];
    if (!series.length) return el('section', 'ipo-section', el('div', 'ipo-eyebrow', '03 / SPACEX'),
      el('h2', '', 'SpaceX price history is unavailable.'), small('The retained IPO research is available below.'), h('button', { className: 'ipo-button', onClick: retry }, 'Retry loading'));
    const newest = series[series.length - 1];
    const checkedAt = new Intl.DateTimeFormat('en-US', { dateStyle: 'medium', timeStyle: 'short', timeZone: 'America/New_York' }).format(new Date(market.generated_at));
    const benchmarkName = state.benchmark || 'SPY';
    const benchmark = market.benchmarks?.[benchmarkName]?.series || [];
    const events = (archive?.events || []).map((e, i) => ({ ...e, number: i + 1, window: eventWindow(e, series, benchmark) }));
    const cutoff = state.range === '30' || state.range === '90' ?
      new Date(Date.parse(newest.date + 'T12:00:00Z') - Number(state.range) * 86400000).toISOString().slice(0, 10) : series[0].date;
    const shown = series.filter(p => p.date >= cutoff);
    const query = (state.search || '').trim().toLowerCase();
    const filtered = events.filter(e => (!state.category || e.category === state.category) &&
      (!state.confirmed || e.evidence === 'Confirmed') &&
      (!query || [e.title, e.summary, e.channel, e.evidence, ...e.sources.map(s => s.publisher)].join(' ').toLowerCase().includes(query)) &&
      (!state.range || e.date >= cutoff || e.window.session >= cutoff));
    const selected = state.selectedDay ? null : filtered.find(e => e.id === state.selectedEvent) || filtered[filtered.length - 1];
    const selectedDay = state.selectedDay || selected?.window.session;
    const selectedBar = series.find(p => p.date === selectedDay);
    const selectEvent = id => onChange({ selectedEvent: id, selectedDay: null });
    const statusText = w => w.status === 'pending' ? 'Pending sessions' : 'No prior public close';
    const previous = series[series.length - 2];
    const stat = (label, value, note) => el('div', 'ipo-stat', el('div', 'ipo-label', label), el('strong', '', value), small(note));
    const controls = el('div', 'scx-controls',
      el('div', 'scx-toggle-group', ...[['', 'Since IPO'], ['90', '90 days'], ['30', '30 days']].map(([v, label]) => button(label, (state.range || '') === v, () => onChange({ range: v, selectedDay: null })))),
      el('div', 'scx-toggle-group', button('Price', state.mode !== 'returns', () => onChange({ mode: 'price' })), button('Relative returns', state.mode === 'returns', () => onChange({ mode: 'returns' }))),
      h('label', { className: 'scx-select-label' }, 'Benchmark ', h('select', { value: benchmarkName, onChange: e => onChange({ benchmark: e.target.value }) },
        h('option', { value: 'SPY' }, 'SPY · broad US market'), h('option', { value: 'QQQ' }, 'QQQ · Nasdaq-100'))));

    // A calendar-date x-axis leaves weekends visible; all event mapping uses actual sessions.
    const L = 62, R = 1068, T = 83, B = 307, V = 367;
    const t0 = Date.parse(shown[0].date), t1 = Date.parse(shown[shown.length - 1].date);
    const x = day => L + (Date.parse(day) - t0) / Math.max(86400000, t1 - t0) * (R - L);
    const relative = state.mode === 'returns';
    const first = shown[0].close;
    const bmMap = new Map(benchmark.map(p => [p.date, p]));
    const bmFirst = bmMap.get(shown[0].date)?.close;
    const value = p => relative ? pct(first, p.close) : p.close;
    const bmShown = relative && bmFirst ? shown.filter(p => bmMap.has(p.date)).map(p => ({ date: p.date, value: pct(bmFirst, bmMap.get(p.date).close) })) : [];
    const values = [...shown.map(value), ...bmShown.map(p => p.value), ...(relative ? [0] : [market.offer_price_usd])];
    const minimum = Math.min(...values), maximum = Math.max(...values);
    const pad = Math.max(4, (maximum - minimum) * 0.12);
    const lo = minimum - pad, hi = maximum + pad;
    const y = n => B - (n - lo) / (hi - lo) * (B - T);
    const line = shown.map(p => x(p.date).toFixed(1) + ',' + y(value(p)).toFixed(1)).join(' ');
    const volumeMax = Math.max(1, ...shown.map(p => p.volume || 0));
    const markerEvents = filtered.filter(e => e.window.session && e.window.session >= shown[0].date && e.window.session <= newest.date);
    const chart = h('svg', { className: 'scx-chart', viewBox: '0 0 1120 407', role: 'group', 'aria-label': 'SPCX daily closing prices, volume and numbered news markers. Select a marker or its matching archive entry to inspect the window.' },
      h('title', null, 'SpaceX prices and dated news; association does not establish causation'),
      h('defs', null, h('linearGradient', { id: 'scx-price-fill', x1: '0%', x2: '0%', y1: '0%', y2: '100%' },
        h('stop', { stopColor: '#eaa36d', stopOpacity: 0.2 }), h('stop', { offset: '100%', stopColor: '#eaa36d', stopOpacity: 0 }))),
      ...[0, 1, 2, 3, 4].map(n => { const v = lo + (hi - lo) * n / 4; return h('g', { key: 'axis' + n },
        h('line', { x1: L, y1: y(v), x2: R, y2: y(v), stroke: '#2b3b50', strokeDasharray: '2 5' }),
        h('text', { x: L - 9, y: y(v) + 4, textAnchor: 'end', fill: '#9aaec8', fontSize: 11 }, relative ? v.toFixed(0) + '%' : '$' + v.toFixed(0))); }),
      !relative && h('g', null, h('line', { x1: L, y1: y(market.offer_price_usd), x2: R, y2: y(market.offer_price_usd), stroke: '#d1bb93', strokeDasharray: '5 6', opacity: 0.7 }),
        h('text', { x: R - 4, y: y(market.offer_price_usd) - 7, textAnchor: 'end', fill: '#d1bb93', fontSize: 10 }, '$135 IPO offer')),
      h('path', { d: 'M ' + x(shown[0].date) + ' ' + B + ' L ' + line.replaceAll(',', ' ') + ' L ' + x(newest.date) + ' ' + B + ' Z', fill: 'url(#scx-price-fill)' }),
      bmShown.length > 0 && h('polyline', { points: bmShown.map(p => x(p.date) + ',' + y(p.value)).join(' '), fill: 'none', stroke: '#8db9e9', strokeWidth: 1.6, strokeDasharray: '5 4' }),
      h('polyline', { points: line, fill: 'none', stroke: '#f2ae7d', strokeWidth: 2.3, strokeLinejoin: 'round' }),
      state.selectedDay && selectedBar && selectedBar.date >= shown[0].date && h('g', null,
        h('line', { x1: x(selectedBar.date), x2: x(selectedBar.date), y1: T, y2: V, stroke: '#e0e8f6', strokeDasharray: '3 4', opacity: 0.65 }),
        h('circle', { cx: x(selectedBar.date), cy: y(value(selectedBar)), r: 5, fill: '#f2ae7d', stroke: '#f3f5f8', strokeWidth: 2 })),
      ...shown.map((p, i) => h('g', { key: p.date },
        h('rect', { x: x(p.date) - 2, y: V - (p.volume || 0) / volumeMax * 36, width: 4, height: (p.volume || 0) / volumeMax * 36, fill: i && p.close < shown[i - 1].close ? '#8e5363' : '#4b7c78', opacity: 0.6 }),
        h('circle', { cx: x(p.date), cy: y(value(p)), r: 6, fill: 'transparent' }, h('title', null, p.date + ' · ' + dollars(p.close) + ' · volume ' + (p.volume || 0).toLocaleString())))),
      ...markerEvents.map((e, i) => {
        const p = series.find(p => p.date === e.window.session), active = e.id === selected?.id;
        const markerY = 16 + (i % 3) * 21;
        return h('g', { key: e.id },
          h('line', { x1: x(p.date), y1: markerY + 8, x2: x(p.date), y2: y(value(p)), stroke: colors[e.category], opacity: active ? 0.8 : 0.17, strokeDasharray: '2 4', pointerEvents: 'none' }),
          h('g', { className: 'scx-marker', role: 'button', tabIndex: 0, transform: 'translate(' + x(p.date) + ',' + markerY + ')', 'aria-label': 'Event ' + e.number + ': ' + e.title,
            onClick: () => selectEvent(e.id), onKeyDown: key => { if (key.key === 'Enter' || key.key === ' ') { key.preventDefault(); selectEvent(e.id); } } },
            h('title', null, e.date + ' · ' + e.title + ' · ' + e.evidence),
            h('rect', { x: -11, y: -10, width: 22, height: 20, fill: 'transparent' }),
            h('circle', { cx: 0, cy: 0, r: active ? 10 : 8, fill: active ? colors[e.category] : '#101a2b', stroke: colors[e.category], strokeWidth: active ? 2 : 1, strokeDasharray: e.evidence === 'Confirmed' ? undefined : '2 2' }),
            h('text', { x: 0, y: 3, fill: active ? '#0a111c' : colors[e.category], textAnchor: 'middle', fontSize: 8, fontWeight: 700 }, e.number)),
          active && h('circle', { cx: x(p.date), cy: y(value(p)), r: 5, fill: colors[e.category], stroke: '#0b1220', strokeWidth: 2 }));
      }),
      ...shown.filter((p, i) => i === 0 || (p.date.slice(0, 7) !== shown[i - 1].date.slice(0, 7) && R - x(p.date) > 60)).map(p =>
        h('text', { key: 'date' + p.date, x: x(p.date), y: 392, textAnchor: 'middle', fill: '#91a6c2', fontSize: 10 }, p.date.slice(5))),
      h('text', { x: L, y: 329, fill: '#6e86a3', fontSize: 9 }, 'VOLUME · relative bar heights'),
      h('text', { x: R, y: 392, textAnchor: 'end', fill: '#91a6c2', fontSize: 10 }, newest.date.slice(5)));

    const event = selected || (selectedDay ? { date: selectedDay, timing: 'intraday', title: 'Trading session · ' + selectedDay } : null);
    let detail = small('No event matches these filters. The price series remains visible.');
    if (event) {
      const windows = [1, 3, 5].map(n => ({ n, ...eventWindow(event, series, benchmark, n) }));
      const overlaps = events.filter(e => e.window.session && e.window.session === windows[0].session);
      detail = h('div', { className: 'scx-detail', id: 'spacex-event-detail' }, el('div', 'ipo-eyebrow', selected ? 'SELECTED EVENT / ' + selected.number : 'SELECTED SESSION'),
        el('h3', '', event.title), selected && small(event.summary),
        selected && el('div', 'scx-evidence-line', el('span', 'scx-evidence', event.evidence), el('span', '', 'Public report: ' + event.date), el('span', '', 'Mapped session: ' + (windows[0].session || 'Pending'))),
        selected?.event_date && small('Underlying event reported from ' + selected.event_date + '; not backdated into the price chart.'),
        selected?.timing === 'unknown' && el('p', 'scx-timing-note', 'Publication time is unverified. This daily window can include trading before the news; it is not a post-announcement return.'),
        selected?.timing === 'after_close' && small('After-close publication: measurement starts with the next available trading session.'),
        el('div', 'ipo-table-wrap', el('table', 'ipo-table scx-window-table',
          el('thead', '', el('tr', '', ...['Window', 'SPCX', benchmarkName, 'Difference'].map(t => el('th', '', t)))),
          el('tbody', '', ...windows.map(w => h('tr', { key: w.n }, el('td', '', 'Through session ' + w.n),
            el('td', '', w.status === 'ok' ? displayPct(w.stock) : statusText(w)),
            el('td', '', w.status === 'ok' ? displayPct(w.benchmark) : '—'),
            el('td', '', w.difference == null ? '—' : (w.difference >= 0 ? '+' : '') + w.difference.toFixed(2) + ' pp')))))),
        small(windows[0].status === 'ok' ? 'One-session window: ' + windows[0].from + ' close → ' + windows[0].to + ' close.' : statusText(windows[0]) + '; no value is substituted.'),
        windows[0].volumeRatio != null && small('Session volume: ' + windows[0].volumeRatio.toFixed(2) + '× the prior ' + windows[0].volumeSample + '-session average.'),
        overlaps.length > 1 && small(overlaps.length + ' archive entries share this session. Longer windows may include additional news.'),
        selected && el('div', 'scx-channel', el('div', 'ipo-label', 'Potential business channel · interpretation'), small(selected.channel)),
        selected && el('div', 'scx-sources', ...selected.sources.map(source)),
        !selected && small(overlaps.length ? 'Archive items on this session: ' + overlaps.map(e => e.title).join('; ') : 'No researched item is linked to this session. The archive does not explain this price move.'));
    }
    const filters = el('div', 'scx-filters',
      h('label', null, el('span', 'ipo-label', 'Search the archive'), h('input', { type: 'search', placeholder: 'Deals, Ukraine, Cursor…', value: state.search || '', onChange: e => onChange({ search: e.target.value, selectedDay: null }) })),
      h('label', null, el('span', 'ipo-label', 'Category'), h('select', { value: state.category || '', onChange: e => onChange({ category: e.target.value, selectedDay: null }) },
        h('option', { value: '' }, 'All categories'), ...Object.keys(colors).map(k => h('option', { key: k, value: k }, k)))),
      h('label', { className: 'scx-checkbox' }, h('input', { type: 'checkbox', checked: !!state.confirmed, onChange: e => onChange({ confirmed: e.target.checked, selectedDay: null }) }), 'Confirmed items only'));
    const cards = filtered.length ? [...filtered].reverse().map(e => h('article', {
      className: 'scx-event' + (selected?.id === e.id ? ' scx-event-active' : ''), key: e.id, style: { '--event-color': colors[e.category] } },
      el('div', 'scx-event-meta', el('span', '', String(e.number).padStart(2, '0') + ' / ' + e.date), el('span', '', e.category), el('span', 'scx-evidence', e.evidence)),
      h('button', { className: 'scx-event-title', type: 'button', onClick: () => selectEvent(e.id), 'aria-pressed': selected?.id === e.id }, e.title),
      small(e.summary), el('div', 'scx-event-footer', el('span', '', '1 session: ' + (e.window.status === 'ok' ? displayPct(e.window.stock) : statusText(e.window))),
        el('span', '', e.window.difference == null ? '' : 'vs ' + benchmarkName + ': ' + (e.window.difference >= 0 ? '+' : '') + e.window.difference.toFixed(2) + ' pp')),
      el('div', 'scx-sources', ...e.sources.map(source)))) : el('div', 'scx-empty', 'No archive entries match. Try clearing the search or choosing another category.');
    const moves = series.map((p, i) => ({ ...p, move: i ? pct(series[i - 1].close, p.close) : null }))
      .filter(p => p.date >= shown[0].date && p.move != null).sort((a, b) => Math.abs(b.move) - Math.abs(a.move)).slice(0, 5);
    return el('section', 'ipo-section scx-context', el('div', 'ipo-eyebrow', '03 / SPACEX · PRICE & NEWS'),
      el('h2', '', 'The price. The news. The wider market.'),
      el('p', 'ipo-intro', 'Explore the trading history alongside dated deals, earnings, launch milestones, war-related developments and reported acquisition talks.'),
      el('div', 'ipo-stats', stat('Last completed close', dollars(newest.close), newest.date + ' · ' + series.length + ' sessions'),
        stat('Latest session', displayPct(pct(previous?.close, newest.close)), 'Previous public close → latest close'),
        stat('Since $135 offer', displayPct(pct(market.offer_price_usd, newest.close)), 'IPO allocation-price basis'),
        stat('Since first close', displayPct(pct(series[0].close, newest.close)), 'June 12 close: ' + dollars(series[0].close))),
      el('div', 'ipo-panel scx-chart-panel', controls, el('p', 'scx-pan-hint', 'Swipe the chart sideways to explore the full timeline →'), chart,
        el('div', 'scx-chart-legend', el('span', '', '━━ SPCX'), relative && el('span', '', '┄ ' + benchmarkName), el('span', '', 'Numbered markers = filtered archive items'),
          el('span', '', relative ? 'Both lines rebased to the first shown close; excludes dividends.' : 'Daily closes in USD · select a numbered marker')),
        selected && h('button', { type: 'button', className: 'scx-selection-caption', onClick: () => document.getElementById('spacex-event-detail')?.scrollIntoView({ block: 'start' }) },
          selected.date + ' / ' + selected.title, el('span', '', 'Inspect window ↓')),
        el('div', 'scx-sources', source({ publisher: 'SPCX prices · Yahoo Finance', url: market.stock.source_url }), source({ publisher: benchmarkName + ' history', url: market.benchmarks?.[benchmarkName]?.source_url || 'https://finance.yahoo.com/' })),
        small('Prices checked ' + checkedAt + ' ET. ' + market.session_policy)),
      el('div', 'scx-causality', 'Observed moves around news are associations. Broad-market changes, overlapping reports, anticipation and unobserved information can all affect the same window.'),
      el('div', 'scx-workspace', el('div', 'ipo-panel', detail), el('div', 'ipo-panel',
        el('div', 'ipo-eyebrow', 'CHECK THE OTHER DAYS'), el('h3', '', 'Largest sessions in this range'),
        small('Sorted by absolute close-to-close move, regardless of whether a news item is in the archive.'),
        el('div', 'scx-moves', ...moves.map(p => h('button', { key: p.date, className: 'scx-move', onClick: () => onChange({ selectedDay: p.date }), type: 'button' },
          el('span', '', p.date), el('strong', '', displayPct(p.move)), el('span', '', dollars(p.close))))),
        small('Select a session to inspect its market comparison and any researched items on that date.'))),
      el('div', 'scx-archive-heading', el('div', '', el('div', 'ipo-eyebrow', 'THE COMPENDIUM'), el('h3', '', filtered.length + ' of ' + events.length + ' researched items')), small('Source review: ' + (archive?.reviewed_at || 'Unavailable'))),
      !archive && small('The news archive could not load; the price history is still available.'),
      filters, el('div', 'scx-archive-list', ...[].concat(cards)),
      h('details', { className: 'scx-methodology' }, h('summary', null, 'Coverage, timing and return methodology'), small(archive?.coverage_note || ''), small(archive?.methodology || ''),
        small('SPY and QQQ are ETF price-return benchmarks, not estimates of SpaceX-specific risk. Percentage-point differences do not control for beta. Confirmed marks refer to the described announcement or milestone; plans and reviews are not completed projects or transactions.')),
      h('details', { className: 'scx-methodology' }, h('summary', null, 'Inspect the daily prices and volume'),
        el('div', 'ipo-table-wrap', el('table', 'ipo-table', el('thead', '', el('tr', '', ...['Session', 'Open', 'High', 'Low', 'Close', 'Volume'].map(t => el('th', '', t)))),
          el('tbody', '', ...[...shown].reverse().map(p => h('tr', { key: p.date }, ...[p.date, dollars(p.open), dollars(p.high), dollars(p.low), dollars(p.close), p.volume.toLocaleString()].map((v, i) => h('td', { key: i }, v)))))))));
  }
  return { render, eventWindow, displayPct };
})();
