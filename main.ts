// THE WORLD TODAY — news-image-20261123 r1.
// Copies the pre-rendered front page (entry.png, drawn at build time with
// PIL) into the grader's output directory. Node 22, stdlib only, no network,
// fully deterministic: the same bytes out on every run.
import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";

mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
copyFileSync(join(here, "entry.png"), target);
// Guard: never hand the grader an empty image.
if (statSync(target).size === 0) {
  throw new Error("entry.png copied but empty");
}
