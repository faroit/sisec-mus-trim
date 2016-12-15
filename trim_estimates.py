import argparse
import dsdtools
import os
import os.path as op
import glob
import soundfile as sf
import sys
import utils


def trim_estimates(dsd, estimates_dirs, output_path):
    previews = utils.csv_to_dict()

    # cut references
    # for target_name, target_track in track.targets.iteritems():
    #     if target_name in estimates_to_cut.keys():
    #         estimates_to_cut['ref_' + target_name] = \
    #             target_track.audio[start:end, :]

    for estimates_dir in estimates_dirs:
        for track in dsd.load_dsd_tracks():
            sys.stdout.write("Trim Track: %d\b" % track.id)
            sys.stdout.write("\r")
            sys.stdout.flush()
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

            if not os.path.exists(output_path):
                os.makedirs(output_path)

            # write out tracks to disk
            # define route
            # trackid_estimatename_target.wav
            delimiter = '_'
            for target, estimate in list(estimates_to_cut.items()):
                filename = delimiter.join((
                    str(track.id),
                    op.basename(estimates_dir),
                    target
                ))
                target_path = op.join(output_path, filename + '.wav')
                sf.write(target_path, estimate, track.rate)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Parse DSD100 Estimates and crop files')

    parser.add_argument(
        'estimates_dirs',
        type=str,
        nargs='+',
        help='Folder to SISEC MUS Estimates'
    )

    parser.add_argument(
        'trimmed_estimates_dir',
        type=str,
        help='Folder to SISEC MUS Estimates'
    )

    args = parser.parse_args()
    dsd = dsdtools.DB(root_dir=None)  # replace None with dir to dsd100 dataset
    trim_estimates(dsd, args.estimates_dirs, args.trimmed_estimates_dir)
