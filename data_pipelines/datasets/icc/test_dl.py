from download import TTSClusterDownloader

ttscdl = TTSClusterDownloader(metadata_path='data_pipelines/datasets/icc/test_metadata.json', output_dir='./download_examples')
files = ttscdl.upload_to_share()
print(files)