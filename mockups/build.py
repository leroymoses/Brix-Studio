"""Fill template.html from a JSON brief and screenshot it.
Usage: python3 build.py brief.json out_dir
Brief keys: name, name_short, trade, city, area_short, phone, license, rating, review_count,
headline_a, headline_b, subhead, services[{title,desc}], trust[{big,small}], reviews[{text,who}],
areas[], services_title, services_sub, area_sub, cta_title, cta_sub, address, color.
Only use facts from the business's own site or Google listing. Reviews must be real, quoted verbatim."""
import json, sys, re, html, datetime, subprocess, pathlib
b = json.load(open(sys.argv[1])); out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
e = html.escape
f = {k: e(str(v)) for k, v in b.items() if not isinstance(v, (list, dict))}
f['phone_raw'] = re.sub(r'\D', '', b['phone'])
f['year'] = str(datetime.date.today().year)
f.setdefault('color', '#C2410C')
f['service_options'] = ''.join(f'<option>{e(s["title"])}</option>' for s in b['services'])
f['service_cards'] = ''.join(f'<div class="svc"><i></i><h3>{e(s["title"])}</h3><p>{e(s["desc"])}</p></div>' for s in b['services'][:6])
f['trust_items'] = ''.join(f'<div><strong>{e(t["big"])}</strong>{e(t["small"])}</div>' for t in b['trust'][:4])
f['review_cards'] = ''.join(f'<div class="rev"><b>&#9733;&#9733;&#9733;&#9733;&#9733;</b><p>&ldquo;{e(r["text"])}&rdquo;</p><small>{e(r["who"])}, Google review</small></div>' for r in b['reviews'][:3])
f['area_chips'] = ''.join(f'<span>{e(a)}</span>' for a in b['areas'])
t = open(pathlib.Path(__file__).with_name('template.html')).read()
page = re.sub(r'{{(\w+)}}', lambda m: f.get(m.group(1), ''), t)
slug = re.sub(r'[^a-z0-9]+', '-', b['name'].lower()).strip('-')
p = out / f'{slug}.html'; p.write_text(page)
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();
for (const [w,n] of [[1280,'desktop'],[390,'phone']]){{const pg=await b.newPage({{viewport:{{width:w,height:900}},deviceScaleFactor:2}});
await pg.goto('file://{p.resolve()}',{{waitUntil:'networkidle'}});await pg.screenshot({{path:'{out.resolve()}/{slug}-'+n+'.png',fullPage:true}});}}
await b.close();}})();"""
subprocess.run(['node', '-e', js], check=True)
print(p)
