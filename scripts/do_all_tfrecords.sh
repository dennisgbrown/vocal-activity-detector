cd ../vad
python data_processing/data_to_tfrecords.py --data_set test-clean --data_dir ../LibriSpeech/
python data_processing/data_to_tfrecords.py --data_set test-clean-db-160 --data_dir ../LibriSpeech/
python data_processing/data_to_tfrecords.py --data_set test-clean-db-80 --data_dir ../LibriSpeech/
python data_processing/data_to_tfrecords.py --data_set test-clean-db-40 --data_dir ../LibriSpeech/
python data_processing/data_to_tfrecords.py --data_set test-clean-db-20 --data_dir ../LibriSpeech/
python data_processing/data_to_tfrecords.py --data_set test-clean-db-10 --data_dir ../LibriSpeech/
python data_processing/data_to_tfrecords.py --data_set test-clean-db-5 --data_dir ../LibriSpeech/
python data_processing/data_to_tfrecords.py --data_set test-clean-db0 --data_dir ../LibriSpeech/
python data_processing/data_to_tfrecords.py --data_set test-clean-db5 --data_dir ../LibriSpeech/
cd ../scripts


