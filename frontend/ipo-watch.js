/* Company views share the existing dashboard runtime and historical charts. */
window.IPOContext = (() => {
  const number = new Intl.NumberFormat('en-US', { maximumFractionDigits: 2 });
  const usd = value => value == null ? 'Pending' :
    (value < 0 ? '−$' : '$') + (Math.abs(value) >= 1e12 ? number.format(Math.abs(value) / 1e12) + 'T' :
      Math.abs(value) >= 1e9 ? number.format(Math.abs(value) / 1e9) + 'B' : number.format(Math.abs(value) / 1e6) + 'M');
  const ageDays = date => date && Number.isFinite(Date.parse(date)) ?
    Math.floor((Date.now() - Date.parse(date)) / 86400000) : null;
  const views = ['overview', 'anthropic', 'spacex'];
  const viewFromHash = (fallback = 'overview') => views.includes(location.hash.slice(1)) ? location.hash.slice(1) : fallback;
  function render({ comps, prices, filings, anthropic: a, view, valuation, onValuation, retry, spacexMarket, spacexEvents, spaceContext, onSpaceContext }) {
    const h = React.createElement;
    const el = (tag, cls, ...children) => h(tag, cls ? { className: cls } : null, ...children);
    const source = (url, label = 'Source ↗') => h('a', { className: 'ipo-source', href: url, target: '_blank', rel: 'noopener noreferrer' }, label);
    const kicker = text => el('div', 'ipo-eyebrow', text);
    const small = text => el('p', 'ipo-small', text);
    const stat = (label, value, note, color) => el('div', 'ipo-stat',
      el('div', 'ipo-label', label), h('strong', { style: { color } }, value), small(note));
    const row = (label, value) => el('div', 'ipo-row', el('dt', '', label), el('dd', '', value));
    const section = (eyebrow, title, intro, ...content) => el('section', 'ipo-section', kicker(eyebrow), el('h2', '', title), intro && el('p', 'ipo-intro', intro), ...content);
    const priceDate = prices?.prices?.SPCX?.last_close_date;
    const priceAge = ageDays(priceDate);
    const q = a?.quarterly_financials || [];
    const latest = q[q.length - 1];
    const prior = q[q.length - 2];
    const ttm = q.length >= 4 ? q.slice(-4).reduce((sum, p) => sum + p.revenue_usd, 0) : null;
    const annualized = latest ? latest.revenue_usd * 4 : null;
    const basis = a?.last_private_round;
    const nav = el('nav', 'ipo-nav', ...views.map((v, i) => h('a', {
      key: v, href: '#' + v, 'aria-current': view === v ? 'page' : undefined,
    }, el('span', '', '0' + (i + 1)), v === 'spacex' ? 'SpaceX' : v[0].toUpperCase() + v.slice(1))));
    const header = el('header', 'ipo-head',
      h(window.IPOVisuals.DotPattern, { id: 'ipo-hero-dots' }),
      h(window.IPOVisuals.BorderBeam),
      el('div', 'ipo-head-top',
        el('div', 'ipo-brand', el('span', 'ipo-brand-mark', '↗'), kicker('IPO / CONTEXT')),
        el('div', 'ipo-head-issue', 'PERSONAL RESEARCH / 2026')),
      el('div', 'ipo-hero-copy',
        el('div', 'ipo-hero-kicker', 'SPACEX', el('span', '', '/'), 'ANTHROPIC', el('span', '', '/'), 'OPENAI'),
        el('h1', '', 'Big ambitions.', el('br'), el('em', '', 'At what price?')),
        el('p', '', 'Participate, wait, or pass? Weigh the entry price against the business, the risks, and the evidence still missing.'),
        h('a', { href: '#ipo-decision', className: 'ipo-hero-link' }, 'Start with the decision', el('span', '', '↘'))),
      h(window.IPOVisuals.CoverageArt),
      el('div', 'ipo-stamp',
        el('span', '', 'RESEARCH ', el('strong', '', a?.as_of || 'Unavailable')),
        el('span', '', 'PRICE SNAPSHOT ', el('strong', '', priceDate || 'unavailable')),
        el('span', '', 'HISTORICAL SEED ', el('strong', '', comps?._meta?.as_of || 'unavailable'))));
    const stale = priceAge == null || priceAge > 3;
    const notice = stale ? el('div', 'ipo-notice',
      'SpaceX price data ', priceDate ? 'ends ' + priceDate : 'is unavailable',
      '. The SpaceX charts show a saved snapshot. Anthropic research and filing checks carry their own dates.') : null;
    const filing = name => filings?.companies?.find(c => c.name === name);
    const filingNote = name => {
      const f = filing(name);
      return f?.refresh_error ? 'Last filing refresh failed; previous observation retained.' :
        'Filing check: ' + (f?.checked_at?.slice(0, 10) || filings?.generated_at?.slice(0, 10) || 'unavailable');
    };
    const decisionLens = h('section', { className: 'ipo-decision', id: 'ipo-decision', 'aria-label': 'The decision this research supports' },
      el('div', 'ipo-decision-lead', kicker('THE DECISION'), el('h2', '', 'A price you can justify.')),
      ...[
        ['01', 'Participate', 'The price and business case meet your criteria.'],
        ['02', 'Wait', 'Your assessment needs more evidence or firmer terms.'],
        ['03', 'Pass', 'The price requires assumptions you cannot defend.'],
      ].map(([n, title, text]) => h('div', { className: 'ipo-decision-option', key: n },
        el('span', 'ipo-decision-number', n), el('h3', '', title), el('p', '', text))));
    let content;
    if (!comps) {
      content = section('DATA UNAVAILABLE', 'The dashboard could not load its data.', 'Try loading the saved files again.',
        h('button', { className: 'ipo-button', onClick: retry }, 'Retry loading'));
    } else if (view === 'overview') {
      const cards = (comps.deals || []).map(d => {
        const isAnt = d.company === 'Anthropic';
        const isSpace = d.company === 'SpaceX';
        const watch = filing(d.company);
        const publicFiling = watch?.public_s1 || watch?.filings?.[0];
        const value = isAnt ? basis?.valuation_usd : d.target_valuation_usd;
        return h('article', { className: 'ipo-panel ipo-card', key: d.company, style: { '--company-color': isSpace ? '#ffa568' : isAnt ? '#a7cdff' : '#c6b4f2' } },
          el('div', 'ipo-company-heading', el('span', 'ipo-company-mark', isSpace ? 'X' : isAnt ? 'A' : 'O'), el('h3', '', d.company)), el('span', 'ipo-badge', isAnt ? (a?.stage || 'Research unavailable') :
            isSpace ? 'Priced · SPCX' : publicFiling ? 'Public filing found' : 'Filing watch'),
          el('div', 'ipo-big', usd(value)), el('div', 'ipo-label', isAnt ? 'Last private valuation · May 2026' : isSpace ? 'Valuation at offer · June 2026' : 'Private valuation · March 2026 seed'),
          el('dl', '', row('IPO price', isAnt ? usd(a?.offer_price_usd) : d.offer_price_usd ? '$' + d.offer_price_usd : 'Pending'),
            row(isAnt ? 'Q3 ’26 revenue' : 'Revenue basis', isAnt ? usd(latest?.revenue_usd) : isSpace ? 'FY2025 actual' : 'February ’26 ARR'),
            row('IPO proceeds', isAnt ? usd(a?.raise_usd) : usd(d.raise_usd))),
          el('div', 'ipo-card-foot', small(isAnt ? 'IPO valuation and pricing remain undisclosed in the reviewed filing.' :
            isSpace ? 'Price snapshot: ' + (priceDate || 'unavailable') : 'Financial figures remain the June research snapshot.'),
            small(filingNote(d.company)), source(isAnt ? a?.source_url || d.source_url : publicFiling?.url || d.source_url, 'Read filing ↗')),
          isAnt || isSpace ? h('a', { className: 'ipo-button', href: isAnt ? '#anthropic' : '#spacex' }, 'Explore ' + d.company + ' →') : small('Financial detail: not yet expanded'));
      });
      content = section('01 / WATCHLIST', 'Three companies. Different stages.',
        'An IPO valuation, a private funding mark and an annualized run rate answer different questions. The labels matter.',
        el('div', 'ipo-grid', ...cards),
        el('div', 'ipo-panel', el('h3', '', 'What changed for Anthropic?'),
          small(a ? 'The confidential filing is now public. The November 2 amendment includes September-quarter financials; final offering terms are still pending.' : 'Anthropic research could not be loaded.'),
          a && source(a.source_url, 'Read the November 2 S-1/A ↗')));
    } else if (view === 'anthropic' && (!a || !latest || !basis)) {
      content = section('02 / ANTHROPIC', 'Anthropic research is unavailable.', 'The historical charts below are still available.',
        h('button', { className: 'ipo-button', onClick: retry }, 'Retry loading'));
    } else if (view === 'anthropic') {
      const qoQ = prior ? ((latest.revenue_usd / prior.revenue_usd - 1) * 100).toFixed(1) : null;
      const scenario = valuation * 1e9;
      const max = Math.ceil(Math.max(...q.map(p => p.revenue_usd)) / 5e9) * 5;
      const chart = h('svg', { viewBox: '0 0 700 280', className: 'ipo-chart', role: 'img', 'aria-label': 'Quarterly revenue, Q1 2025 through Q3 2026. Exact values in the table below.' },
        h('title', null, 'Anthropic quarterly reported revenue'),
        h('defs', null,
          h('linearGradient', { id: 'ipo-revenue-fill', x1: '0%', x2: '0%', y1: '0%', y2: '100%' },
            h('stop', { stopColor: '#7baceb', stopOpacity: 0.8 }), h('stop', { offset: '100%', stopColor: '#254771', stopOpacity: 0.35 })),
          h('linearGradient', { id: 'ipo-revenue-latest', x1: '0%', x2: '0%', y1: '0%', y2: '100%' },
            h('stop', { stopColor: '#d6e8ff' }), h('stop', { offset: '100%', stopColor: '#6c9edf', stopOpacity: 0.65 }))),
        ...[0, max / 2, max].map(n => h('g', { key: n },
          h('line', { x1: 48, y1: 230 - n / max * 185, x2: 685, y2: 230 - n / max * 185, stroke: '#253047', strokeDasharray: '3 5' }),
          h('text', { x: 40, y: 234 - n / max * 185, fill: '#8a9bb8', fontSize: 11, textAnchor: 'end' }, '$' + n + 'B'))),
        ...q.map((p, i) => {
          const x = 65 + i * 90;
          const height = p.revenue_usd / 1e9 / max * 185;
          return h('g', { key: p.period },
            h('rect', { className: 'ipo-revenue-bar', x, y: 230 - height, width: 51, height, fill: i === q.length - 1 ? 'url(#ipo-revenue-latest)' : 'url(#ipo-revenue-fill)', stroke: i === q.length - 1 ? '#b7d7ff' : '#6d99c9', strokeOpacity: 0.5, rx: 3 },
              h('title', null, p.period + ': ' + usd(p.revenue_usd))),
            h('text', { x: x + 25.5, y: 220 - height, textAnchor: 'middle', fill: '#c7d8ee', fontSize: 11 }, (p.revenue_usd / 1e9).toFixed(2)),
            h('text', { x: x + 25.5, y: 253, textAnchor: 'middle', fill: '#8a9bb8', fontSize: 11 }, p.period));
        }));
      const terms = el('div', 'ipo-panel', el('h3', '', 'The offering is still taking shape.'),
        el('span', 'ipo-badge', a.stage), el('dl', '', row('Proposed symbol', a.proposed_ticker + ' · Nasdaq'),
          row('Offer price', usd(a.offer_price_usd)), row('IPO proceeds', usd(a.raise_usd)),
          row('IPO valuation', usd(a.ipo_valuation_usd)), row('First trading day', a.ipo_date || 'Pending')),
        small(a.terms_note), small('Research checked ' + a.as_of + ' · ' + filingNote('Anthropic')),
        source(a.source_url, 'Read the S-1/A ↗'));
      const results = el('div', 'ipo-panel', el('h3', '', 'Revenue is scaling quickly.'),
        small('Reported quarterly revenue, $ billions. Q3 growth: ' + qoQ + '% over Q2.'), chart,
        source(a.source_url, 'Quarterly results · pp. 161–165 ↗'));
      const comparisonTable = el('div', 'ipo-table-wrap', el('table', 'ipo-table',
        el('thead', '', el('tr', '', ...['Period', 'Revenue', 'GAAP operating', 'Adjusted operating', 'GAAP net'].map(label => el('th', '', label)))),
        el('tbody', '', ...q.map(p => h('tr', { key: p.period },
          ...[p.period, usd(p.revenue_usd), usd(p.operating_income_usd), usd(p.adjusted_operating_income_usd), usd(p.net_income_usd)].map((text, i) => h('td', { key: i }, text)))))));
      const fundamentals = section('02 / ANTHROPIC', 'A public filing. An open price question.',
        'Proposed Nasdaq symbol ANT. The public financials are available; the price investors will be asked to pay is still pending.',
        el('div', 'ipo-stats', stat('Q3 ’26 reported revenue', usd(latest.revenue_usd), '+' + qoQ + '% quarter over quarter'),
          stat('Trailing 12-month revenue', usd(ttm), 'Sum of the latest four reported quarters'),
          stat('Q3 GAAP operating loss', usd(latest.operating_income_usd), 'Adjusted operating income: ' + usd(latest.adjusted_operating_income_usd), '#ff9d9d'),
          stat('Last private valuation', usd(basis.valuation_usd), 'Series H · ' + basis.date)),
        el('div', 'ipo-two', results, terms),
        h('details', null, h('summary', null, 'Inspect the financials and accounting basis'), comparisonTable, small(a.accounting_note), source(a.source_url)));
      const scenarioPanel = h('div', { className: 'ipo-panel ipo-scenario-panel', id: 'ipo-valuation-panel' }, el('h3', '', 'What does a valuation imply?'),
        small('Illustrative equity valuations. The slider is a scenario, not a forecast or a published IPO range.'),
        h('label', { htmlFor: 'ipo-valuation', className: 'ipo-label' }, 'Illustrative valuation · $ billions'),
        h('input', { className: 'ipo-range', id: 'ipo-valuation', type: 'range', min: 500, max: 2500, step: 5, value: valuation,
          'aria-valuetext': usd(scenario), onChange: e => onValuation(Number(e.target.value)) }),
        el('div', 'ipo-range-labels', el('span', '', '$500B'), el('span', '', '$2.5T')),
        el('div', 'ipo-scenario', el('div', '', el('div', 'ipo-label', 'Scenario valuation'), el('strong', '', usd(scenario))),
          el('div', '', el('div', 'ipo-label', 'Valuation / TTM revenue'), el('strong', '', (scenario / ttm).toFixed(1) + '×')),
          el('div', '', el('div', 'ipo-label', 'Valuation / (Q3 × 4)'), el('strong', '', (scenario / annualized).toFixed(1) + '×'))),
        h('button', { className: 'ipo-button', onClick: () => onValuation(basis.valuation_usd / 1e9) }, 'Reset to last private mark'),
        small('TTM: ' + usd(ttm) + '. Q3 × 4: ' + usd(annualized) + ' — a simple annualization, not ARR or a forecast. Equity valuation / revenue is not enterprise value / revenue.'),
        source(basis.source_url, 'Series H funding announcement ↗'));
      // Only compare reported-revenue multiples; never substitute ARR for TTM.
      const compRows = (comps.tech_comps || []).filter(c => ['Google', 'Facebook / Meta', 'Facebook', 'Snowflake', 'Airbnb', 'Arm'].includes(c.company));
      const compScale = Math.max(100, scenario / ttm, ...compRows.map(c => c.ps_multiple || 0));
      const context = el('div', 'ipo-panel', el('h3', '', 'Keep the denominator visible.'),
        small('At the last private valuation, Anthropic is ' + (basis.valuation_usd / ttm).toFixed(1) + '× TTM revenue. That combines a May valuation with September financials; it is not a contemporaneous market quote.'),
        el('div', 'ipo-multiple-list',
          el('div', 'ipo-multiple ipo-multiple-current', el('div', 'ipo-multiple-label', el('span', '', 'Anthropic · scenario'), el('strong', '', (scenario / ttm).toFixed(1) + '×')),
            el('div', 'ipo-multiple-track', h('span', { style: { width: ((scenario / ttm) / compScale * 100) + '%' } }))),
          ...compRows.map(c => h('div', { className: 'ipo-multiple', key: c.company },
            el('div', 'ipo-multiple-label', el('span', '', c.company, ' ', /^https?:/.test(c.source_url || '') ? source(c.source_url, '↗') : null), el('strong', '', c.ps_multiple == null ? 'Unavailable' : c.ps_multiple + '× at IPO')),
            el('div', 'ipo-multiple-track', h('span', { style: { width: ((c.ps_multiple || 0) / compScale * 100) + '%' } }))))),
        small('Historical multiples use the June research seed. Sector, growth, accounting and dates differ.'),
        h('a', { className: 'ipo-source', href: '#ipo-history' }, 'Explore the historical distributions ↓'));
      const watch = el('div', 'ipo-panel', el('h3', '', 'The questions to carry into pricing.'),
        el('div', 'ipo-terms', el('div', 'ipo-label', 'Compute obligations'),
          el('strong', '', usd(a.compute_commitments_usd) + ' committed; ' + usd(a.compute_due_next_12_months_usd) + ' due within 12 months.'), small(a.compute_commitments_note)),
        el('div', 'ipo-terms', el('div', 'ipo-label', 'Governance'), el('strong', '', 'Public shares do not control the board.'),
          small('Class T elects a board majority; the founder Class F holds 50.1% of general voting power.')),
        el('div', 'ipo-terms', el('div', 'ipo-label', 'Earnings quality'),
          el('strong', '', 'GAAP and adjusted results tell different stories.'), small(a.accounting_note)), source(a.source_url, 'Risk factors & governance ↗'));
      const timeline = el('div', 'ipo-panel', el('h3', '', 'From private round to public market.'),
        el('ol', 'ipo-timeline', ...(a.timeline || []).map(t => h('li', { key: t.date },
          el('time', '', t.date), h('a', { href: t.source_url, target: '_blank', rel: 'noopener noreferrer' }, t.event + ' ↗')))));
      content = h(React.Fragment, null, fundamentals,
        section('VALUATION / CONTEXT', 'The multiple changes with the price.', '', el('div', 'ipo-two', scenarioPanel, context)),
        section('FILING / WATCH', 'What to watch next.', '', el('div', 'ipo-two', watch, timeline)));
    } else {
      content = window.SpaceXContext.render({ market: spacexMarket, archive: spacexEvents, state: spaceContext, onChange: onSpaceContext, retry });
    }
    return el('div', 'ipo-watch', header, nav, notice, comps && decisionLens, content);
  }
  return { render, viewFromHash, ageDays };
})();
