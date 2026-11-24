import { copyFileSync, mkdirSync } from "node:fs";

// Entry for news-image-20261124: the image is drawn by draw.py in this
// repository (every element drawn from code) and shipped as entry.png.
// This program only copies it to the output directory, deterministically.
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL("./entry.png", import.meta.url), `${outDir}/entry.png`);
