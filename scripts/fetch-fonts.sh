#!/usr/bin/env bash
# Download the open-licensed (OFL) Google Fonts the Instagram preset uses into
# skills/video-editor/presets/instagram/assets/fonts/. Safe to re-run.
set -euo pipefail
DEST="$(cd "$(dirname "$0")/.." && pwd)/skills/video-editor/presets/instagram/assets/fonts"
mkdir -p "$DEST"
UA="Mozilla/4.0"   # an old user agent makes the CSS API hand out .ttf instead of .woff2

# file name | Google Fonts family | italic (0/1) | weight
FONTS="
Anton-Regular|Anton|0|400
ArchivoBlack-Regular|Archivo Black|0|400
BebasNeue-Regular|Bebas Neue|0|400
EBGaramond-Medium|EB Garamond|0|500
EBGaramond-MediumItalic|EB Garamond|1|500
InstrumentSerif-Regular|Instrument Serif|0|400
InstrumentSerif-Italic|Instrument Serif|1|400
Inter-Medium|Inter|0|500
Inter-Bold|Inter|0|700
Inter-ExtraBold|Inter|0|800
Inter-Black|Inter|0|900
Montserrat-SemiBold|Montserrat|0|600
Montserrat-ExtraBold|Montserrat|0|800
Montserrat-Black|Montserrat|0|900
Oswald-SemiBold|Oswald|0|600
PlayfairDisplay-Italic|Playfair Display|1|400
PlayfairDisplay-Bold|Playfair Display|0|700
PlayfairDisplay-BoldItalic|Playfair Display|1|700
Poppins-Bold|Poppins|0|700
Poppins-ExtraBold|Poppins|0|800
ReenieBeanie-Regular|Reenie Beanie|0|400
Ultra-Regular|Ultra|0|400
"

echo "$FONTS" | while IFS='|' read -r file family ital wght; do
  [ -z "$file" ] && continue
  out="$DEST/$file.ttf"
  [ -s "$out" ] && { echo "have  $file"; continue; }
  fam="${family// /+}"
  css=$(curl -fsSL -A "$UA" "https://fonts.googleapis.com/css2?family=$fam:ital,wght@$ital,$wght")
  url=$(printf '%s' "$css" | grep -o 'https://fonts.gstatic.com/[^)]*' | head -1)
  [ -z "$url" ] && { echo "FAIL  $file (no URL)"; continue; }
  curl -fsSL "$url" -o "$out" && echo "got   $file"
done
