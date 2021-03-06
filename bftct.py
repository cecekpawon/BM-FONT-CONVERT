#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# BM-FONT-CONVERT | @cecekpawon - Fri Mar  5 2021
#
# Port of blackosx - ocFontFileGenerator
# https://www.insanelymac.com/forum/topic/344251-opencanopy-icons/?do=findComment&comment=2752057
#

#
# X:.
# ├─── Resources ........................................................ # Required tools asset directory
# │    ├─── dpfb/dpfb(.exe)
# │    ├─── Fontbm/Fontbm(.exe) (opt)
# │    ├─── fonverter/fonverter(.exe)
# │    └─── FNTTools/FNTTools(.exe) (opt)
# ├─── Fonts ............................................................ # Source font asset directory
# └─── BmFonts .......................................................... # Converted bitmap font asset directory
#

#
# NOTE:
#   Added fontbm as dpfontbaker (preferred) alternative.
#   Noticed here dpfontbaker is way faster compared to fontbm.
#   Added fonverter (preferred) as FNTTools alternative.
#   Noticed here fonverter is slightly faster compared to FNTTools, even though they used the same lib.
#   I dont see dpfontbaker '-font-index (x)' will work with font collection.
#   Change / simplify asset directory name.
#

import os, platform, re, shutil, subprocess, sys, time

font_extensions       = (".otf", ".otc", ".ttf", ".ttc")                  # Supported extensions
initial_line_height   = 12                                                # Initial line-height, overridden by args
initial_font_size     = 10                                                # Initial font-size
initial_font_index    = 0                                                 # (useless) initial font-index for font collection
initial_texture_px    = 80                                                # Initial texture width + height

dpfb_exists           = False
fontbm_exists         = False
fonverter_exists      = False
fnttools_exists       = False

font_directory        = "Fonts"       # "TrueTypeFontToProcess"           # Source font asset directory
bmfont_directory      = "BmFonts"     # "ProcessedFonts"                  # Converted bitmap font asset directory
resources_directory   = "Resources"                                       # Required tools asset directory
tmp_directory         = "Tmp"                                             # Temporary asset directory

dpfb_filepath         = "dpfb"                                            # Dpfontbaker bin
dpfb_url              = "https://github.com/danpla/dpfontbaker"           # Dpfontbaker url
fontbm_filepath       = "fontbm"                                          # Fontbm bin (Dpfontbaker replacement | opt)
fontbm_url            = "https://github.com/vladimirgamalyan/fontbm"      # Fontbm url (Dpfontbaker replacement | opt)
fonverter_filepath    = "fonverter"                                       # Fonverter bin
fonverter_url         = "https://github.com/usr-sse2/fonverter"           # Fonverter url
fnttools_filepath     = "FNTTools"                                        # FNTTools bin (fonverter replacement | opt)
fnttools_url          = "https://github.com/AuroraBertaOldham/FNTTools"   # FNTTools url (fonverter replacement | opt)

#
# Ovr fl4666
#
banner = """\
+----------------------------------------------------------+
|          Port of blackosx - ocFontFileGenerator
+----------------------------------------------------------+
| // BM ////////////////////////////////////////////////////
| /////// FONT ///////////////// | @cecekpawon - Mar 2021 //
| ////////////// CONVERT ///////////////////////////////////
+----------------------------------------------------------+
| Usage: {} [opt: line-height]
+----------------------------------------------------------+
"""

print(banner.format(sys.argv[0]))
