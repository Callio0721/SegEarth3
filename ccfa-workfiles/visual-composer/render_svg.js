const fs = require('fs');
const path = require('path');
const sharp = require('sharp');
const dir = 'D:/论文/9.27论文/author-kit-main/fig';
const names = ['intro_teaser','method_overview','method_detail','category_gain','qualitative_placeholder'];
(async () => {
  for (const name of names) {
    const svg = fs.readFileSync(path.join(dir, name + '.svg'));
    await sharp(svg, { density: 300 }).png({ compressionLevel: 9 }).toFile(path.join(dir, name + '.png'));
    console.log('wrote', name + '.png');
  }
})();
