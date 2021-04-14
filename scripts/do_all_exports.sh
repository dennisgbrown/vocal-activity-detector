cd ../vad
python inference/export_model.py --data-set test-clean --model-dir ../LibriSpeech/models/
python inference/export_model.py --data-set test-clean-db-160 --model-dir ../LibriSpeech/models/
python inference/export_model.py --data-set test-clean-db-80 --model-dir ../LibriSpeech/models/
python inference/export_model.py --data-set test-clean-db-40 --model-dir ../LibriSpeech/models/
python inference/export_model.py --data-set test-clean-db-20 --model-dir ../LibriSpeech/models/
python inference/export_model.py --data-set test-clean-db-10 --model-dir ../LibriSpeech/models/
python inference/export_model.py --data-set test-clean-db-5 --model-dir ../LibriSpeech/models/
python inference/export_model.py --data-set test-clean-db0 --model-dir ../LibriSpeech/models/
python inference/export_model.py --data-set test-clean-db5 --model-dir ../LibriSpeech/models/
cd ../scripts

