cd ../vad
python training/train.py --data-set test-clean --data-dir ../LibriSpeech/
python training/train.py --data-set test-clean-db-160 --data-dir ../LibriSpeech/
python training/train.py --data-set test-clean-db-80 --data-dir ../LibriSpeech/
python training/train.py --data-set test-clean-db-40 --data-dir ../LibriSpeech/
python training/train.py --data-set test-clean-db-20 --data-dir ../LibriSpeech/
python training/train.py --data-set test-clean-db-10 --data-dir ../LibriSpeech/
python training/train.py --data-set test-clean-db-5 --data-dir ../LibriSpeech/
python training/train.py --data-set test-clean-db0 --data-dir ../LibriSpeech/
python training/train.py --data-set test-clean-db5 --data-dir ../LibriSpeech/
cd ../scripts

