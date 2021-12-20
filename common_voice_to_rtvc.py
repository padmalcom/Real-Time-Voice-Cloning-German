import csv
import os
from tqdm import tqdm
from pydub import AudioSegment
from pydub.silence import detect_leading_silence

trim_leading_silence: AudioSegment = lambda x: x[detect_leading_silence(x) :]
trim_trailing_silence: AudioSegment = lambda x: trim_leading_silence(x.reverse()).reverse()
strip_silence: AudioSegment = lambda x: trim_trailing_silence(trim_leading_silence(x))

if __name__ == '__main__':

	common_voice_folder = u"E:\Datasets\cv-corpus-7.0-2021-07-21-de.tar\cv-corpus-7.0-2021-07-21\de"
	target_folder = u"E:\Datasets\cv-converted"
	
	if not os.path.exists(target_folder):
		os.mkdir(target_folder)
		
	if not os.path.exists(os.path.join(target_folder, "wavs")):
		os.mkdir(os.path.join(target_folder, "wavs"))
	
	with open(os.path.join(target_folder, 'metadata.csv'), 'w', newline='', encoding='utf-8') as metadata_csv:
		metadata_writer = csv.writer(metadata_csv, delimiter='|')
							
		with open(os.path.join(common_voice_folder, 'validated.tsv'), newline='', encoding="utf8") as cv_file:
			cv_reader = csv.reader(cv_file, delimiter='\t')
			next(cv_reader, None) # skip header
			for row in tqdm(cv_reader):
				mp3path = row[1]
				sentence = row[2]
				
				# convert mp3 to wav
				mp3FullPath = os.path.join(common_voice_folder, "clips", mp3path)
				filename, file_extension =os.path.splitext(os.path.basename(mp3FullPath))
				sound = AudioSegment.from_mp3(mp3FullPath)
				
				# strip silence
				sound = strip_silence(sound)
				if sound.duration_seconds > 0:
					sound = sound.set_frame_rate(16000)
					sound = sound.set_channels(1)
					sound.export(os.path.join(target_folder, "wavs", filename + ".wav"), format="wav")
					
					# Write metadata.csv		
					metadata_writer.writerow([filename, sentence])
