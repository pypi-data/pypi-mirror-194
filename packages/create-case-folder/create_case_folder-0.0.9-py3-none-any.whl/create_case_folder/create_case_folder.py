import os
import argparse
import datetime

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--case', nargs='?', type=str, help='Name of the case folder')
    parser.add_argument('-e', '--evidence', nargs='+', type=str, help='Name of the evidence folder(s)')
    args = parser.parse_args()

    parent_folder = args.case
    if not parent_folder:
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        parent_folder = f'{timestamp}_NEWCASE'

    evidence_folders = args.evidence
    if not evidence_folders:
        evidence_folders = ['EVIDENCE']

    try:
        if not os.path.exists(parent_folder):
            os.makedirs(parent_folder)

        folders = ['Documents', 'Extracts', 'Pictures', 'Videos', 'Reports']
        for folder in folders:
            folder_path = os.path.join(parent_folder, folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            for evidence_folder in evidence_folders:
                evidence_folder_path = os.path.join(folder_path, evidence_folder)
                if not os.path.exists(evidence_folder_path):
                    os.makedirs(evidence_folder_path)

    except Exception as e:
        print(f'Error: {e}')
    else:
        print(f'Successfully created case folder "{parent_folder}" with evidence "{evidence_folders}" and sub-folders.')

if __name__ == '__main__':
    main()
