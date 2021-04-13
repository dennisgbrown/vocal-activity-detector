cd ../vad
python data_processing/librispeech_label_data.py --data_set test-clean --data_dir ../LibriSpeech/ --out_dir ../LibriSpeech/labels/ --exported_model ../LibriSpeech/models/pretrainedfg/exported 
cd ../scripts
