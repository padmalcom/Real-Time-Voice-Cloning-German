## First things first
- Trained on female and male German voices from m-ailabs
- Tests show that the vocoder training is not neccessary, so focus on encoder and synthesizer
- I had to edit some parts of the implementation to make it work with m-ailabs
- m-ailabs requires a lot of cleaning (at least for German voices). I added a script to do most of the work.
	- mailab_normalize_text.py: Creates text files besides each wav file of the m-ailabs dataset which apparently is required.
	
- Works with the following commit of Real-Time-Voice-Cloning: https://github.com/CorentinJ/Real-Time-Voice-Cloning/commit/95adc699c1deb637f485e85a5107d40da0ad94fc

## How to run?
Please note that all changes I did were made for windows. You might want to adapt it for linux.

# Encoder
- python encoder_preprocess.py E:\Datasets\
- python encoder_train.py my_run E:\Datasets\SV2TTS\encoder --no_visdom

# Synthesizer
- Make sure you updated synthesizer/utils/symbols.py for your language
- python synthesizer_preprocess_audio.py E:\Datasets\ --subfolders de_DE\by_book\female\,de_DE\by_book\male\,de_DE\by_book\mix\ --dataset "" --no_alignments --wav_dir
- python synthesizer_preprocess_embeds.py E:\Datasets\SV2TTS\synthesizer --encoder_model_fpath encoder/saved_models/my_run.pt
- python synthesizer_train.py my_run E:\Datasets\SV2TTS\synthesizer

# Vocoder (You really do not need to train the vocoder, it works well as the pretrained model is - at least for German)
- pip install librosa==0.8.1
- installation of correct numba version is no longer neccessary
- python vocoder_preprocess.py E:\Datasets\ --model_dir=synthesizer/saved_models/logs-my_run/
- python vocoder_train.py my_run E:\Datasets\

# Toolbox
- pip install matplotlib==3.2.2 #required for toolbox to work
- python demo_toolbox.py -d E:\Datasets\

## Todos and Learnings
- Application for a specific voice needs fine tuning for the specific voice.