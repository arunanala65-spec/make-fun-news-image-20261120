// make.fun news-image-20261120: "The World in One Day — 20 November 2026".
//
// What this program does: it takes the finished front page that
// render.py drew (entry.png, sitting next to this file) and places a
// copy at the path the grader reads, $MAKEFUN_OUTPUT_DIR/entry.png
// (or /output/entry.png when that variable is unset).
//
// The image itself never changes while this program runs: no network,
// no randomness, no drawing here. Both grader runs therefore write
// byte-identical files, which is what the competition requires.
//
// Node 22, standard library only:
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { join } from "node:path";

function copyEntry() {
  const here = new URL(".", import.meta.url).pathname;
  const from = join(here, "entry.png");
  const info = statSync(from);
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  const to = join(outDir, "entry.png");
  mkdirSync(outDir, { recursive: true });
  writeFileSync(to, readFileSync(from));
  return { to, bytes: info.size };
}

const { to, bytes } = copyEntry();
console.log(`entry.png -> ${to} (${bytes} bytes)`);
