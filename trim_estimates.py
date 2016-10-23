import argparse
import dsdtools
import os.path as op
import glob
import soundfile as sf
import csv


def csv_to_dict(csv_path="data/previews.csv"):
    previews = {}
    with open(csv_path, 'r') as csvfile:
        preview_reader = csv.reader(csvfile, delimiter=',')
        for row in preview_reader:
            previews[int(row[0])] = (int(row[1]), int(row[2]))

    return previews


def trim_estimates(dsd, estimates_dir, output_path):
    previews = csv_to_dict()
    for track in dsd.load_dsd_tracks():
        print(track.id)
        track_estimate_dir = op.join(
            estimates_dir,
            track.subset,
            track.filename
        )

        estimates_to_cut = {}
        # Read all target estimates for given track
        for target_path in glob.glob(track_estimate_dir + '/*.wav'):
            target_name = op.splitext(
                op.basename(target_path)
            )[0]
            try:
                target_audio, rate = sf.read(
                    target_path,
                    always_2d=True
                )
                start = previews[track.id][0]
                end = previews[track.id][1]
                estimates_to_cut[target_name] = target_audio[start:end, :]
            except RuntimeError:
                pass

        dsd._save_estimates(
            estimates_to_cut,
            track,
            estimates_dir=output_path
        )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Parse DSD100 Estimates and crop files')

    parser.add_argument(
        'estimates_dir',
        type=str,
        help='Folder to SISEC MUS Estimates'
    )

    parser.add_argument(
        'trimmed_estimates_dir',
        type=str,
        help='Folder to SISEC MUS Estimates'
    )

    args = parser.parse_args()
    dsd = dsdtools.DB(root_dir=None)  # replace None with dir to dsd100 dataset
    trim_estimates(dsd, args.estimates_dir, args.trimmed_estimates_dir)
