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
# NOTE, CHANGES and ADDITIONS:
#   Added fontbm as dpfontbaker (aka dpfb, preferred) alternative.
#   Noticed here dpfontbaker is way faster compared to fontbm.
#   I dont see dpfontbaker '-font-index (x)' will work with font collection.
#   Added fonverter (preferred) as FNTTools alternative.
#   Noticed here fonverter is slightly faster compared to FNTTools, even though they used the same lib.
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

#
# Manage args
#
if len(sys.argv) == 2:
  line_height = int(sys.argv[1])
  if line_height != initial_line_height:
    initial_line_height = line_height

#
# Manage assets
#
working_directory     = os.path.dirname(os.path.abspath(__file__))
font_directory        = os.path.join(working_directory, font_directory)
bmfont_directory      = os.path.join(working_directory, bmfont_directory)
resources_directory   = os.path.join(working_directory, resources_directory)
tmp_directory         = os.path.join(working_directory, tmp_directory)

dpfb_filepath         = os.path.join(resources_directory, dpfb_filepath, dpfb_filepath)
fontbm_filepath       = os.path.join(resources_directory, fontbm_filepath, fontbm_filepath)
fnttools_filepath     = os.path.join(resources_directory, fnttools_filepath, fnttools_filepath)
fonverter_filepath    = os.path.join(resources_directory, fonverter_filepath, fonverter_filepath)

if (platform.system() == "Windows"):
  dpfb_filepath       += ".exe"
  fontbm_filepath     += ".exe"
  fnttools_filepath   += ".exe"
  fonverter_filepath  += ".exe"

#
# Assets directory
#
#if not os.path.exists(font_directory):
#  os.makedirs(font_directory)
if not os.path.exists(font_directory):
  print("{} directory ({}) not exists".format(os.path.basename(font_directory), font_directory))
  sys.exit()

if not os.path.exists(bmfont_directory):
  os.makedirs(bmfont_directory)
if not os.path.exists(bmfont_directory):
  print("{} directory ({}) not exists".format(os.path.basename(bmfont_directory), bmfont_directory))
  sys.exit()

#if not os.path.exists(resources_directory):
#  os.makedirs(resources_directory)
#if not os.path.exists(resources_directory):
#  print("{} directory ({}) not exists".format(os.path.basename(resources_directory), resources_directory))
#  sys.exit()

if not os.path.exists(tmp_directory):
  os.makedirs(tmp_directory)
if not os.path.exists(tmp_directory):
  print("{} directory ({}) not exists".format(os.path.basename(tmp_directory), tmp_directory))
  sys.exit()

#
# Assets tools
#
dpfb_exists = os.path.exists(dpfb_filepath)
if not dpfb_exists:
  print("{} ({}) not exists".format(os.path.basename(dpfb_filepath), dpfb_filepath))
  print(" - Source ({})".format(dpfb_url))
  fontbm_exists = os.path.exists(fontbm_filepath)
  if not fontbm_exists:
    print("{} ({} | opt) not exists".format(os.path.basename(fontbm_filepath), fontbm_filepath))
    print(" - Source ({})".format(fontbm_url))

fonverter_exists = os.path.exists(fonverter_filepath)
if not fonverter_exists:
  print("{} ({}) not exists".format(os.path.basename(fonverter_filepath), fonverter_filepath))
  print(" - Source ({})".format(fonverter_url))
  fnttools_exists = os.path.exists(fnttools_filepath)
  if not fnttools_exists:
    print("{} ({} | opt) not exists".format(os.path.basename(fnttools_filepath), fnttools_filepath))
    print(" - Source ({})".format(fnttools_url))

print("Required tools: dpfb ({}) fontbm ({} | opt) fonverter ({}) FNTTools ({} | opt)" \
  .format(dpfb_exists, fontbm_exists, fonverter_exists, fnttools_exists))

if (not dpfb_exists and not fontbm_exists) or (not fonverter_exists and not fnttools_exists):
  sys.exit()

#
# Start prog
#
os.chdir(tmp_directory)

#
# Scan fonts directory
#
for file in os.listdir(font_directory):
  #
  # Matches extension
  #
  if not file.startswith(".") and file.lower().endswith(font_extensions):
    #
    # Init local scope vars
    #
    this_font_filepath          = os.path.realpath(os.path.join(font_directory, file))
    this_font_name              = os.path.splitext(file)[0]
    this_bmfont_base_directory  = file.replace(".", "-")
    this_bmfont_directory       = os.path.join(bmfont_directory, this_bmfont_base_directory)
    this_font_fnt               = this_font_name + ".fnt"
    this_font_binary            = this_font_name + ".bin"
    this_font_png               = this_font_name + "_0.png"

    if not os.path.isfile(this_font_filepath) or os.stat(this_font_filepath).st_size < 4:
      continue

    #
    # Font signature check
    #
    this_font_signature = open(this_font_filepath, "rb").read(4)
    if this_font_signature != b'\x00\x01\x00\x00' and this_font_signature != b'OTTO' and this_font_signature != b'ttcf':
      continue

    print("Processing font: {}".format(this_font_name))

    #
    # Remove old built BmFont directory
    #
    if os.path.exists(this_bmfont_directory):
      shutil.rmtree(this_bmfont_directory)
    time.sleep(.100)
    os.makedirs(this_bmfont_directory)
    if not os.path.exists(this_bmfont_directory):
      print("{} directory ({}) not exists".format(this_bmfont_base_directory, this_bmfont_directory))
      break

    last_line_height_found = 0
    last_font_size = initial_font_size

    #
    # Start converting by size
    #
    for this_line_size in range(1, 3):
      font_size_tmp = last_font_size
      this_line_height = initial_line_height * this_line_size
      this_prefix = "Font_{}x".format(this_line_size)
      success = False

      print(" - {}:".format(this_prefix))

      while True:
        #
        # Font convert, find exact line height
        #

        #
        # Exec dpfontbaker
        #
        if dpfb_exists:
          subprocess.call([dpfb_filepath, \
            "-font-size", str(font_size_tmp), \
            "-font-index", str(initial_font_index), \
            "-hinting", "light", \
            "-kerning", "none", \
            "-font-export-format", "bmfont", \
            this_font_filepath])
        #
        # Exec fontbm
        #
        elif fontbm_exists:
          subprocess.call([fontbm_filepath, \
            "--font-size", str(font_size_tmp), \
            "--texture-width", str(initial_texture_px * this_line_size), \
            "--texture-height", str(initial_texture_px * this_line_size), \
            "--background-color", "0,0,0", \
            "--output", this_font_name, \
            "--font-file", this_font_filepath])

        #
        # Check produced .fnt + .png
        #
        if os.path.exists(this_font_fnt) and os.path.exists(this_font_png):
          pattern = re.compile("lineHeight=(\d+)")
          line_height_found = 0
          for i, line in enumerate(open(this_font_fnt)):
            for match in re.finditer(pattern, line):
              line_height_found = int(match.group(1))
              break
          if line_height_found != 0:
            #
            # Matched current line height
            #
            if line_height_found == this_line_height:
              success = True
              break
            #
            # Continue scanning
            #
            elif line_height_found >= last_line_height_found:
              if line_height_found < this_line_height:
                font_size_tmp += 1
              elif line_height_found > this_line_height:
                font_size_tmp -= 1
            else:
              break
            last_line_height_found = line_height_found
          else:
            break
        else:
          break

        if font_size_tmp == 0:
          break

        #
        # Use last font size for next size scan to speedup processes
        #
        if font_size_tmp > last_font_size:
          last_font_size = font_size_tmp

      print("  - Font convert succeed: {} | size ({}) height ({})".format(success, font_size_tmp, line_height_found))

      if success:
        #
        # Font convert succeed, do Bin convert .fnt to .bin
        #
        success = False
        #
        # Exec fonverter
        #
        if fonverter_exists:
          subprocess.call([fonverter_filepath, this_font_fnt, this_font_binary])
          success = os.path.exists(this_font_binary)
          if success:
            this_binary = this_font_binary
        #
        # Exec FNTTools
        #
        elif fnttools_exists:
          subprocess.call([fnttools_filepath, "convert", "Binary", "--overwrite", this_font_fnt])
          success = os.path.exists(this_font_fnt)
          if success:
            this_binary = this_font_fnt

        if success:
          success = False
          #
          # Bin convert succeed, do BmFont signature check
          #
          if os.stat(this_binary).st_size >= 3:
            this_bmf_signature = open(this_binary, "rb").read(3)
            success = this_bmf_signature == b'BMF'
          if success:
            #
            # Copy .png + .bin to BmFont directory
            #
            shutil.copyfile(this_font_png, os.path.join(this_bmfont_directory, this_prefix + ".png"))
            shutil.copyfile(this_binary, os.path.join(this_bmfont_directory, this_prefix + ".bin"))

      print("  - Bin convert succeed: {}".format(success))

      #
      # Remove tmp files
      #
      if os.path.exists(this_font_fnt):
        os.remove(this_font_fnt)
      if os.path.exists(this_font_binary):
        os.remove(this_font_binary)
      if os.path.exists(this_font_png):
        os.remove(this_font_png)

      #
      # Remove BmFont directory if failed
      #
      if not success:
        if os.path.exists(this_bmfont_directory):
          shutil.rmtree(this_bmfont_directory)
        break

os.chdir(working_directory)

#
# Remove Tmp directory
#
if os.path.exists(tmp_directory):
  time.sleep(.100)
  shutil.rmtree(tmp_directory)
