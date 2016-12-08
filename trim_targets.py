import argparse
import dsdtools
import os
import os.path as op
import glob
import soundfile as sf
import csv
import sys


def csv_to_dict(csv_path="data/previews.csv"):
    previews = {}
    with open(csv_path, 'r') as csvfile:
        preview_reader = csv.reader(csvfile, delimiter=',')
        for row in preview_reader:
            previews[int(row[0])] = (int(row[1]), int(row[2]))

    return previews


def trim_estimates(dsd, output_path):
    previews = csv_to_dict()

    for track in dsd.load_dsd_tracks():
        sys.stdout.write("Trim Target Track: %d\b" % track.id)
        sys.stdout.write("\r")
        sys.stdout.flush()

        estimates_to_cut = {}
        # Read all target estimates for given track

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # write out tracks to disk
        # define route
        # trackid_estimatename_target.wav
        delimiter = '_'
        start = previews[track.id][0]
        end = previews[track.id][1]
        for target_name, target_track in track.targets.iteritems():
            estimates_to_cut['REF_' + target_name] = \
                target_track.audio[start:end, :]

        for target, estimate in list(estimates_to_cut.items()):
            filename = delimiter.join((
                str(track.id),
                target
            ))
            target_path = op.join(output_path, filename + '.wav')
            sf.write(target_path, estimate, track.rate)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Parse DSD100 Targets and crop files')

    parser.add_argument(
        'trimmed_estimates_dir',
        type=str,
        help='Folder to SISEC MUS Estimates'
    )

    args = parser.parse_args()
    dsd = dsdtools.DB(root_dir=None)  # replace None with dir to dsd100 dataset
    trim_estimates(dsd, args.trimmed_estimates_dir)
