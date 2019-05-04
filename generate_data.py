import json
import requests
import re
import os
import sys
import zipfile
import errno
from glob import glob
from train import Train, TrainStop

TRA_TIMETABLE_JSON_BASE_URL = os.environ.get('TRA_JSON_API_BASE_URL')
TEMP_DIR_PATH = './tmp'
OUTPUT_DIR_PATH = './output'

def create_temp_dir(subdir=''):
    path = os.path.join(TEMP_DIR_PATH, subdir)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def create_output_dir(subdir=''):
    path = os.path.join(OUTPUT_DIR_PATH, subdir)
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def download_data(date_string):
    zip_dir = create_temp_dir('zip')
    zip_filename = '{0}.zip'.format(date_string)
    response = requests.get('{0}/{1}'.format(TRA_TIMETABLE_JSON_BASE_URL, zip_filename))
    zip_file_path = os.path.join(zip_dir, zip_filename)
    with open(zip_file_path, 'wb') as f:
        f.write(response.content)

    json_dir = create_temp_dir('json')
    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        zip_file.extractall(json_dir)

    json_filename = '{0}.json'.format(date_string)
    json_file_path = os.path.join(json_dir, json_filename)

    if os.path.exists(json_file_path) and os.path.isfile(json_file_path):
        with open(json_file_path, encoding='utf-8') as f:
            json_str = f.read()
        return json.loads(json_str)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), json_file_path)

def parse_data(date_string, payload):
    output_trains_dir = create_output_dir('trains')
    output_timetables_dir = create_output_dir('timetables')
    if not 'TrainInfos' in payload:
        raise ValueError('`TrainInfos` not in JSON payload.')

    trains_data = payload['TrainInfos']

    for entry in trains_data:
        train = Train(entry)
        for start_index in range(len(train.stops)):
            for end_index in range(start_index + 1, len(train.stops)):
                begin_stop = train.stops[start_index]
                end_stop = train.stops[end_index]

                timetable_data = {
                    'train_no' : train.number,
                    'has_breastfeeding_rooms' : train.has_breastfeeding_rooms,
                    'carries_packages' : train.carries_packages,
                    'has_dining_rooms' : train.has_dining_rooms,
                    'is_accessible' : train.is_accessible,
                    'has_bike_stands' : train.has_bike_stands,
                    'train_class' : train.train_class,
                    'departs_at' : begin_stop.departure_time[:5],
                    'arrives_at' : end_stop.arrival_time[:5],
                    'direction' : train.direction
                }

                timetable_dir = create_output_dir('timetables/{0}'.format(begin_stop.station))
                timetable_file_path = os.path.join(timetable_dir, '{0}.json'.format(end_stop.station))

                if not os.path.exists(timetable_file_path):
                    # creates file
                     with open(timetable_file_path, 'w') as f:
                         pass

                with open(timetable_file_path, 'a') as timetable_file:
                    timetable_file.write(json.dumps(timetable_data, sort_keys=True))
                    timetable_file.write('\n')

        with open(os.path.join(output_trains_dir, '{0}.json'.format(train.number)), 'w') as train_file:
            def _gen_stops_data(stop):
                return {
                    'station' : stop.station,
                    'departs_at' : stop.departure_time[:5],
                    'arrives_at' : stop.arrival_time[:5]
                }

            train_output_data = {
                'train_no' : train.number,
                'has_breastfeeding_rooms' : train.has_breastfeeding_rooms,
                'carries_packages' : train.carries_packages,
                'has_dining_rooms' : train.has_dining_rooms,
                'is_accessible' : train.is_accessible,
                'has_bike_stands' : train.has_bike_stands,
                'train_class' : train.train_class,
                'stops' : list(map(lambda x: _gen_stops_data(x), train.stops))
            }

            json.dump(train_output_data, train_file)

    timetable_files = glob(os.path.join(output_timetables_dir, '**/*.json'))

    for path in timetable_files:
        with open(path, 'r') as f:
            entries = list(map(lambda x: json.loads(x), f.read().strip().split('\n')))
            entries = sorted(entries, key=lambda x: x['departs_at'])
        with open(path, 'w') as f:
            json.dump(entries, f)

def generate_data(date_string):
    json_data = download_data(date_string)
    parse_data(date_string, json_data)


if __name__ == '__main__':
    date_str = sys.argv[1].strip()
    if date_str == 'None':
        print('No need to download data')
    elif re.match(r'\d{8}', date_str):
        generate_data(date_str)
    else:
        raise ValueError('unsupported input `{0}`'.format(date_str))
