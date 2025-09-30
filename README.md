## First things first
- Trained on female and male German voices from m-ailabs
- Tests show that the vocoder training is not neccessary, so focus on encoder and synthesizer
- I had to edit some parts of the implementation to make it work with m-ailabs
- m-ailabs requires a lot of cleaning (at least for German voices). I added a script to do most of the work.
	- mailab_normalize_text.py: Creates text files besides each wav file of the m-ailabs dataset which apparently is required.
	
- Works with the following commit of Real-Time-Voice-Cloning: https://github.com/CorentinJ/Real-Time-Voice-Cloning/commit/95adc699c1deb637f485e85a5107d40da0ad94fc

## Support me
Training models and creating tutorials takes time. I'd be happy to get your support [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/Y8Y11M25J7)

## Learn on Udemy
The issue tracker here told me that the framework and models are not as easy to use as I first thought so I created a Udemy course to exactly teach step by step how to get everything up and running (get German training data, train encoder, synthesizer and vocoder, inference using UI and code):

https://www.udemy.com/course/voice-cloning/learn/

## How to run?
Please note that all changes I did were made for windows. You might want to adapt it for linux.

# Dependencies
- Install all dependencies from the environment.yml (conda env update -n [MYENV] --file environment.yml
- If you don't use anaconda, copy all dependencies under -pip to a file requirements.txt and do a pip install -r requirements.txt
- Install pytorch 1.7.1 with/without cuda, for cuda 10.1 it would be: pip install torch==1.7.1+cu101 torchvision==0.8.2+cu101 torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html

# Encoder
- python encoder_preprocess.py E:\Datasets\
- python encoder_train.py my_run E:\Datasets\SV2TTS\encoder --no_visdom

# Synthesizer
- Make sure you updated synthesizer/utils/symbols.py for your language
- python synthesizer_preprocess_audio.py E:\Datasets\ --subfolders de_DE\by_book\female\,de_DE\by_book\male\,de_DE\by_book\mix --dataset "" --no_alignments --wav_dir
- python synthesizer_preprocess_embeds.py E:\Datasets\SV2TTS\synthesizer --encoder_model_fpath encoder/saved_models/my_run.pt
- python synthesizer_train.py my_run E:\Datasets\SV2TTS\synthesizer

# Vocoder
- You really do not need to train the vocoder, it works well as the pretrained model is - at least for German
- Create a folder E:\Datasets\SV2TTS\vocoder
- python vocoder_preprocess.py E:\Datasets\ --model_dir=synthesizer/saved_models/my_run/
- python vocoder_train.py my_run E:\Datasets\

# Toolbox
- python demo_toolbox.py -d E:\Datasets\

## Todos and Learnings
- Application for a specific voice needs fine tuning for the specific voice.
