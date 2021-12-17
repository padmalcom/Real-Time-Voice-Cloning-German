import argparse
import os
import csv
import sys
from glob import glob
import codecs

if __name__ == "__main__":    
	parser = argparse.ArgumentParser(
		description="Create normlized text files for each audio file in mailabs datasets.",
		formatter_class=argparse.ArgumentDefaultsHelpFormatter
	)
	parser.add_argument("--datasets_root", type=str, help="Path to the mailabs root directory (e.g. '/training_data/fr_FR').")
	# overwrite
	# male, female, mix
	# audio format
	args = parser.parse_args()
	print(args.datasets_root)
	
	wav_folders = []
	
	print("Searching speakers...")

	# list female speakers
	speaker_search_dir_female = os.path.join(args.datasets_root, "female\\*\\")
	female_speaker_dirs = glob(speaker_search_dir_female)
	
	# list male speakers
	speaker_search_dir_male = os.path.join(args.datasets_root, "male\\*\\")
	male_speaker_dirs = glob(speaker_search_dir_male)
	
	# list mixed speakers
	speaker_search_dir_mix = os.path.join(args.datasets_root, "mix\\*\\")
	mix_speaker_dirs = glob(speaker_search_dir_mix)
	
	all_speakers = female_speaker_dirs + male_speaker_dirs + mix_speaker_dirs
	print(all_speakers)
	
	# Check if speaker dirs have subfoders
	print("Checking subfolders...")
	for speaker in all_speakers:
		# get subfolders
		speaker_subfolders_search_dir = os.path.join(speaker, "*\\")
		#print(speaker_subfolders_search_dir)
		speaker_subfolders = glob(speaker_subfolders_search_dir)
		#print(speaker_subfolders)
		
		# is subfolder a wavs dir?
		for speaker_subfolder in speaker_subfolders:
			last_folder = os.path.basename(os.path.normpath(speaker_subfolder))
			if last_folder == 'wavs':
				#print(speaker_subfolder + " is a wav folder")
				wav_folders.append(speaker_subfolder)
			else:
				# traverse further dirs
				speaker_subfolders_books_search_dir = os.path.join(speaker_subfolder, "*\\")
				speaker_subfolders_books_dirs = glob(speaker_subfolders_books_search_dir)
				#print(speaker_subfolders_books_dirs)
				for speaker_subfolders_book in speaker_subfolders_books_dirs:
					last_folder = os.path.basename(os.path.normpath(speaker_subfolders_book))
					if last_folder == 'wavs':
						#print(speaker_subfolders_book + " is a wav folder")
						wav_folders.append(speaker_subfolders_book)					
						
	print("Found " + str(len(wav_folders)) + " wav folders")
	print(wav_folders)
	
	# read metadata.csv
	file_count = 0
	maxInt = sys.maxsize
	while True:
		# decrease the maxInt value by factor 10 
		# as long as the OverflowError occurs.
		try:
			csv.field_size_limit(maxInt)
			break
		except OverflowError:
			maxInt = int(maxInt/10)
	for wav_folder in wav_folders:
		wav_folder_parent = os.path.dirname(os.path.dirname(wav_folder))
		metadata_path = os.path.join(wav_folder_parent, "metadata.csv")
		if os.path.exists(metadata_path):
			with open(metadata_path, newline='', encoding='utf-8') as csvfile:
				csv.field_size_limit(maxInt)
				csv_reader = csv.reader(csvfile, delimiter='|')
				for row in csv_reader:
					txt_file_to_create = os.path.join(wav_folder, row[0] + ".txt")
					if os.path.exists(txt_file_to_create):
						print(txt_file_to_create + " already exists.")
					else:
						expected_wav_file = os.path.join(wav_folder, row[0] + ".wav")
						if os.path.exists(expected_wav_file):
							if len(row) > 1:
								print("All good. Creating " + txt_file_to_create)
								f = codecs.open(txt_file_to_create, "w", "utf-8")
								f.write(row[1])
								f.close()
								file_count +=1
							else:
								print("Metadat is corrupt" + str(row))
						else:
							print("Corresponding wav file " + expected_wav_file + " was not found.")
		else:
			print("Expected file to exist: " + metadata_path)
	
	print("Wrote " + str(file_count) + " files.")
