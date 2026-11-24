// news-image-20261124 entry (Node 22, standard library only).
//
// The image is the entry.png beside this file: it was drawn by draw.py
// (original vector-style artwork with PIL + DejaVu fonts) and committed
// here. This program checks it is a whole PNG inside the competition's
// limits and copies it to the grader's output directory. It writes the
// same bytes on every run.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
const MAX_FILE_BYTES = 1024 * 1024;
const MAX_SIDE_PX = 1024;

function checkPng(bytes: Buffer): { width: number; height: number } {
  if (bytes.length > MAX_FILE_BYTES) {
    throw new Error(
      `entry.png is ${bytes.length} bytes, over the 1 MiB limit`,
    );
  }
  if (bytes.length < 24 || !bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
    throw new Error('entry.png does not start with the PNG signature');
  }
  // The IHDR chunk holds width and height at bytes 16..24, big-endian.
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width > MAX_SIDE_PX || height > MAX_SIDE_PX) {
    throw new Error(
      `entry.png is ${width}x${height}, over the 1024x1024 limit`,
    );
  }
  return { width, height };
}

const here = new URL('./entry.png', import.meta.url);
const png = readFileSync(here);
const { width, height } = checkPng(png);

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(here, join(outDir, 'entry.png'));
console.log(`wrote entry.png (${width}x${height}, ${png.length} bytes)`);
