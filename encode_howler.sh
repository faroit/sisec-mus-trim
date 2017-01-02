afconvert howler/howler.wav howler/howler.caf -d 0 -f caff --soundcheck-generate
afconvert howler/howler.caf -d aac -f m4af -u pgcm 2 --soundcheck-read -b 96000 -q 127 -s 2 howler/howler.m4a
