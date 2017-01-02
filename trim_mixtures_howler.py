import argparse
import dsdtools
import os
import os.path as op
import soundfile as sf
import sys
import utils
import numpy as np
import json


def trim_estimates(dsd, output_path):
    previews = utils.csv_to_dict()

    samples = []
    samples_pos = []

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for track in dsd.load_dsd_tracks():
        sys.stdout.write("Trim Target Track: %d\b" % track.id)
        sys.stdout.write("\r")
        sys.stdout.flush()

        start = previews[track.id][0]
        samples.append(track.audio[start:start+44100*3, :])
        samples_pos.append({
            'id': track.id,
            'pos': [start, start+44100*3]
        })

    samples = np.concatenate(samples)
    target_path = op.join(output_path, 'howler.wav')
    sf.write(target_path, samples, 44100)

    with open(op.join(output_path, "howler.json"), 'w') as f:
        json.dump(samples_pos, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Parse DSD100 Targets and crop files')

    parser.add_argument(
        'trimmed_mix_dir',
        type=str,
        help='Folder to SISEC MUS Estimates'
    )

    args = parser.parse_args()
    dsd = dsdtools.DB(root_dir=None)
    trim_estimates(dsd, args.trimmed_mix_dir)
