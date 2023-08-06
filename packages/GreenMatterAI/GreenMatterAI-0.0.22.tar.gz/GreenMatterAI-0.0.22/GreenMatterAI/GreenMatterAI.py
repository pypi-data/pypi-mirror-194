import requests
import json
import boto3
import os
import pathlib
import random
from uuid import uuid4
from aws_requests_auth.aws_auth import AWSRequestsAuth
from .BatchLogger import BatchLogger
from pathlib import Path
from .Utils import Utils


class GMAI:
    def __init__(self, task, access_key_id, secret_access_key):
        if task in ['alfalfa']:
            self.task = task
        else:
            raise Exception('Wrong initialization, task name not supported. Possible values: alfalfa')
        self._bucket = 'web-rendering'
        self._region = 'eu-west-1'
        self._api_service = 'execute-api'

        self._api_host = 'y9wnplxtq2.execute-api.eu-west-1.amazonaws.com'
        self._invoke_url = 'https://' + self._api_host
        self._folder = 'alfalfa'
        self._alfalfa_rendering_endpoint = '/dev/start_rendering'
        self._parameters_extraction_endpoint = '/dev/parameters_extraction'

        self._auth = AWSRequestsAuth(aws_access_key=access_key_id,
                                     aws_secret_access_key=secret_access_key,
                                     aws_host=self._api_host,
                                     aws_region=self._region,
                                     aws_service=self._api_service)
        self._s3_client = boto3.client('s3', region_name=self._region, aws_access_key_id=access_key_id,
                                       aws_secret_access_key=secret_access_key)
        self._batch_client = boto3.client(service_name='batch', region_name=self._region,
                                          endpoint_url='https://batch.' + self._region + '.amazonaws.com')
        self._cloudwatch_client = boto3.client(service_name='logs', region_name=self._region,
                                               endpoint_url='https://logs.' + self._region + '.amazonaws.com')
        self._sf_client = boto3.client('stepfunctions', region_name=self._region, aws_access_key_id=access_key_id,
                                       aws_secret_access_key=secret_access_key)
        self._utils = Utils(self._s3_client, self._bucket, self._folder)

    '''def query(self, image_path):
        folder_path, file_name = os.path.split(image_path)
        s3_path = self._folder + '/data/' + file_name
        self._s3_client.upload_file(image_path, self._bucket, s3_path)

        test_dict = {"image_path": s3_path, "file_name": file_name, "bucket": self._bucket}

        response = requests.post(self._url, auth=self._auth, json=json.dumps(test_dict))

        if folder_path == "":
            output_file_name = "output.jpg"
        else:
            output_file_name = "\\output.jpg"
        output_file_path = folder_path + output_file_name
        self._s3_client.download_file(self._bucket, json.loads(response.text)["s3_path"], output_file_path)

        return output_file_path'''

    def get_params(self):
        if self.task == 'alfalfa':
            print(f"Possible parameters to change for {self.task}:")
            params = {'min_distance': 0.15,
                      'min_density': 0.4,
                      'max_density': 1.0,
                      'min_num_branches': 3,
                      'max_num_branches': 20
                      }
            print(json.dumps(params, indent=4))
            print(f"Possible labels for {self.task}:")
            labels = ['bounding_boxes_per_plant', 'bounding_boxes_per_branch', 'segmentation_masks']
            print(labels)
        else:
            print('Wrong initialization,task name not supported. Possible values: alfalfa')

    def upload_blend_file(self, blend_file_path, folder_path=None):
        if folder_path is None and pathlib.PurePath(blend_file_path).suffix.lower() != '.blend':
            raise Exception("Wrong extention, this is not a blender file")

        uuid = str(uuid4())
        folder = uuid + '/blender_file/'
        bucket, folder_on_s3, blender_file_name = self._utils.upload_file_to_s3(blend_file_path, folder)
        if folder_path is not None:
            self._utils.upload_folder_to_s3(folder_path, folder)

        params = {
            'bucket': bucket,
            'folder': folder_on_s3,
            'blender_file_name': blender_file_name
        }
        '''params = {
            'bucket': 'web-rendering',
            'folder': 'blender_files/alfalfa/',
            'blender_file_name': 'alfalfa.blend'
        }'''
        print("All files uploaded, extracting parameters")
        response = requests.post(self._invoke_url + self._parameters_extraction_endpoint, auth=self._auth,
                                 json=json.dumps(params))

        if response.ok:
            response_body = response.json()
            print('Available parameters:')
            print(json.dumps(response_body, indent=2))
        else:
            print(response.text)
            print(response)
            print('Error while sending request')
            print(response.json())

    def render(self, nr_imgs_to_render, nr_return_imgs, parameters, labels, generate_random_scenes=True, custom_dataset_uri=None):
        # min_distance=0.15, min_density=0.4, max_density=1.0, min_num_branches=3, max_num_branches=20):
        params = {'parameters': parameters,
                  'generate_random_scenes': generate_random_scenes,
                  'custom_dataset_uri': custom_dataset_uri}
        params['parameters']['start_scene'] = 0
        params['parameters']['end_scene'] = nr_imgs_to_render - 1

        params['parameters']['bounding_boxes_plants'] = 'bounding_boxes_per_plant' in labels
        params['parameters']['bounding_boxes_branches'] = 'bounding_boxes_per_branch' in labels
        params['parameters']['segmentation_masks'] = 'segmentation_masks' in labels

        if self.task == 'alfalfa':
            response = requests.post(self._invoke_url + self._alfalfa_rendering_endpoint, auth=self._auth,
                                     json=json.dumps(params))
        else:
            raise Exception('Wrong initialization, task name not supported. Possible values: alfalfa')

        if response.ok:
            response_body = response.json()
            job_s3_bucket = response_body['s3Bucket']
            s3_prefix = response_body['s3Prefix']
            job_name = response_body['jobName']
            job_uuid = response_body['uuid']
            execution_arn = response_body['executionArn']
            zip_name = response_body['zip_name']

            batch_logger = BatchLogger(self._cloudwatch_client, self._batch_client, self._sf_client)

            status = batch_logger.print_step_func_status(execution_arn)
            if status == 'SUCCEEDED':
                self._download_results(s3_prefix=s3_prefix, zip_name=zip_name, nr_return_imgs=nr_return_imgs)

        else:
            print(response.text)
            print(response)
            print('Error while sending request')
            print(response.json())

    '''def render(self, config):
        params = {
            'parameters': config
        }
        response = requests.post(self._url, auth=self._auth, json=json.dumps(params))

        if response.ok:
            response_body = response.json()
            # print(response_body)
            job_id = response_body['jobId']
            job_name = response_body['jobName']
            job_uuid = response_body['uuid']

            batch_logger = BatchLogger(self._cloudwatch_client, self._batch_client)

            status = batch_logger.print_status(job_name, job_id)
            if status == 'SUCCEEDED':
                # TODO change folder name to job_id
                self._download_results(folder=job_uuid)

        else:
            print('Error while sending request')
            print(response.json())

        # print(response)
        # print(response.text)'''

    def _list_files_in_s3(self, s3_prefix=''):
        params = {
            "Bucket": self._bucket,
            "Prefix": s3_prefix
        }

        result = self._s3_client.list_objects_v2(**params)

        if 'Contents' not in result:
            print(result)
            return []

        file_list = []
        for key in result['Contents']:
            file_list.append(key['Key'])

        while result['IsTruncated']:
            continuation_key = result['NextContinuationToken']
            result = self._s3_client.list_objects_v2(ContinuationToken=continuation_key, **params)
            for key in result['Contents']:
                file_list.append(key['Key'])
        return file_list

    def _generate_download_url(self, s3_prefix):
        timeout = 604800  # max value - one week
        url = self._s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': self._bucket,
                'Key': s3_prefix
            },
            ExpiresIn=timeout  # seconds
        )
        return url

    def _download_results(self, nr_return_imgs, zip_name, folder=None, s3_prefix=None):
        files_names_list = self._list_files_in_s3(s3_prefix)
        zip_path = next(filter(lambda file_name: zip_name in file_name, files_names_list))

        rendered_images = list(filter(lambda file_name: 'frames/' in file_name, files_names_list))
        labels_images = list(filter(lambda file_name: 'labels/' in file_name, files_names_list))
        analytics_images = list(filter(lambda file_name: 'analytics/' in file_name, files_names_list))

        imgs_to_download = random.sample(rendered_images, nr_return_imgs)
        # files_to_display = map(lambda x: Image(filename=str(Path(Path.cwd(), x))), rendered_images + analytics_images)
        imgs_to_display = imgs_to_download + analytics_images

        labels_to_download = []
        for img_path in imgs_to_download:
            # file name without extension
            img_name = Path(img_path).stem
            labels = list(filter(lambda file_name: img_name in file_name, labels_images))
            labels_to_download += labels

        imgs_to_download += labels_to_download
        imgs_to_download += analytics_images

        files_count = len(imgs_to_download)

        for idx, file in enumerate(imgs_to_download):
            print(f'Downloading file {idx+1}/{files_count}')
            # skip folders
            if file[-1] == "/":
                continue

            # create nested directory structure
            obj_path = os.path.dirname(file)
            Path(obj_path).mkdir(parents=True, exist_ok=True)

            # save file with full path locally
            self._s3_client.download_file(self._bucket, file, file)

        print(f"Download url for whole generated dataset, valid one week: {self._generate_download_url(zip_path)}")
        if imgs_to_download:
            print(f"Files downloaded to folder: {Path(obj_path).parent}")
        else:
            print("No images selected for display")

        self._utils.display_images_in_grid(imgs_to_display, imgs_in_row=5)
