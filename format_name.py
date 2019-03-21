import argparse
import os
import re
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process')
    parser.add_argument('-i', '--input_file', default='./input.txt')
    parser.add_argument('-o,' '--output_file', default='./output.txt')
    args = parser.parse_args()
    img_paths_txt = args.input_file
    with open(img_paths_txt) as f, open(img_paths_txt + '_', 'w') as w:
        for line in f.readlines():
            img_path = line.strip()
            img_dir = os.path.dirname(img_path)
            img_name = os.path.basename(img_path)

            lower_name = img_path.lower()
            if lower_name != img_name:
                new_img_name = lower_name
                new_img_path = os.path.join(img_dir, new_img_name)
                os.rename(img_name, new_img_name)
                img_name = new_img_name
                img_path = new_img_path
            w.writelines("{}\n".format(img_path))