# Trades homepage mockups

When a prospect says yes to a free mockup:

1. Write `briefs/<business>.json` using `example-brief.json` as the shape. Only use facts from their own site or Google listing. Reviews must be real and quoted word for word.
2. Run `python3 mockups/build.py mockups/briefs/<business>.json out/`
3. Send the desktop and phone PNGs. Never publish a mockup to a public URL. It carries their business name.
