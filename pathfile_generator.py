import argparse
import os
import re
if __name__ == '__main__':
    files = os.listdir()
    with open('./input.txt', 'w') as w:
        for file in os.listdir('.'):
            if file.endswith('.jpg'):
                img_path = os.path.abspath(file)
                w.writelines("{}\n".format(img_path))


