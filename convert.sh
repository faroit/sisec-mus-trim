cd media/SISEC

for i in *.wav;
  do name=`echo $i | cut -d'.' -f1`;
  echo $name;
  afconvert $i $name.caf -d 0 -f caff --soundcheck-generate
  afconvert $name.caf -d aac -f m4af -u pgcm 2 --soundcheck-read -b 128000 -q 127 -s 2 $name.m4a
done
