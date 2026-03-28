import os
import sys
import shutil
import time

from functools import wraps

import generate_report

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

from FileSplitter.file_splitter import file_split


def timer_function(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		start_time = time.time()
		result = func(*args, **kwargs)
		end_time = time.time()
		print(f"{func.__name__} took {end_time - start_time:.4f} seconds.")
		return result
	return wrapper


def define_shoot_data(shoot_folder):
	return [
		os.path.join(shoot_folder, folder)
		for folder in os.listdir(shoot_folder)
		if os.path.isdir(os.path.join(shoot_folder, folder))
	]


def update_slate_list(folder, slate_list):
	data_set_folder = os.listdir(folder)

	for item in data_set_folder:
		unique_slate = item.split("_")
		if unique_slate[0] not in slate_list:
			slate_list.append(unique_slate[0])


def get_slates(shoot_folder):
	slate_list = []

	for folder in define_shoot_data(shoot_folder):
		update_slate_list(folder, slate_list)

	return slate_list


def make_slate_folders(shoot_folder, slate_list):
	for slate in slate_list:
		slate_path = os.path.join(shoot_folder, slate.upper())
		os.makedirs(slate_path, exist_ok=True)


#*********************************************************************#
# HELPERS
def folder_contains_images(folder_path):
	image_extensions = {
		".jpg", ".jpeg", ".png", ".tif", ".tiff", ".exr",
		".dng", ".cr2", ".cr3", ".nef", ".arw", ".raf"
	}

	if not os.path.isdir(folder_path):
		return False

	for root, dirs, files in os.walk(folder_path):
		for file_name in files:
			ext = os.path.splitext(file_name)[1].lower()
			if ext in image_extensions:
				return True

	return False


def find_empty_data_folders(shoot_folder):
	empty_folders = []

	for slate in os.listdir(shoot_folder):
		slate_path = os.path.join(shoot_folder, slate)
		if not os.path.isdir(slate_path):
			continue

		for data_type in os.listdir(slate_path):
			data_type_path = os.path.join(slate_path, data_type)
			if not os.path.isdir(data_type_path):
				continue

			for capture_folder in os.listdir(data_type_path):
				capture_path = os.path.join(data_type_path, capture_folder)
				if not os.path.isdir(capture_path):
					continue

				if not folder_contains_images(capture_path):
					empty_folders.append(capture_path)

	return empty_folders


def tag_empty_folders(empty_folders):
	renamed_paths = []

	for folder_path in empty_folders:
		parent = os.path.dirname(folder_path)
		name = os.path.basename(folder_path)

		if name.endswith("_MISSING"):
			renamed_paths.append(folder_path)
			continue

		new_name = f"{name}_MISSING"
		new_name = new_name.replace("__", "_").strip("_")
		
		new_path = os.path.join(parent, new_name)

		if not os.path.exists(new_path):
			os.rename(folder_path, new_path)
			renamed_paths.append(new_path)
		else:
			renamed_paths.append(folder_path)

	return renamed_paths


#*********************************************************************#


@timer_function
def sort_data(shoot_folder, subfolder_check=False):
	moves = []
	source_folders = set(define_shoot_data(shoot_folder))

	for data_type_folder in define_shoot_data(shoot_folder):
		data_type = os.path.basename(data_type_folder)

		for item in os.listdir(data_type_folder):
			src_path = os.path.join(data_type_folder, item)

			if not os.path.isdir(src_path):
				continue

			slate = item.split("_")[0].upper()

			dst_path = os.path.join(
				shoot_folder,
				slate,
				data_type,
				item
			)

			moves.append((src_path, dst_path))

	for src, dst in moves:
		os.makedirs(os.path.dirname(dst), exist_ok=True)
		shutil.move(src, dst)

	for folder in source_folders:
		if os.path.exists(folder) and not os.listdir(folder):
			os.rmdir(folder)

	if subfolder_check:
		for _, dst in moves:
			if os.path.isdir(dst):
				if any(os.path.isfile(os.path.join(dst, f)) for f in os.listdir(dst)):
					file_split(dst)
					


def rename_shoot_folder(shoot_folder, rename_remove="", rename_prefix="", rename_suffix=""):
	parent_folder = os.path.dirname(shoot_folder)
	original_name = os.path.basename(shoot_folder)

	# Remove requested text first
	cleaned_name = original_name
	if rename_remove:
		cleaned_name = cleaned_name.replace(rename_remove, "")

	# Optional small cleanup for repeated underscores
	cleaned_name = cleaned_name.replace("__", "_").strip("_")

	# Build new name using cleaned name
	new_shoot_name = f"{rename_prefix}{cleaned_name}{rename_suffix}"

	# Optional cleanup again after prefix/suffix
	new_shoot_name = new_shoot_name.replace("__", "_").strip("_")

	new_shoot_path = os.path.join(parent_folder, new_shoot_name)

	if original_name == new_shoot_name:
		print("Folder name unchanged (remove/prefix/suffix result identical).")
		return shoot_folder

	if os.path.exists(new_shoot_path):
		print(f"Cannot rename. Destination already exists: {new_shoot_path}")
		return shoot_folder

	os.rename(shoot_folder, new_shoot_path)
	print(f"Folder renamed to: {new_shoot_path}")
	return new_shoot_path


def run_slate_sorter(shoot_folder, settings_data):
	if not shoot_folder or not os.path.isdir(shoot_folder):
		raise ValueError(f"'{shoot_folder}' is not a valid folder.")

	package_settings = settings_data.get("package_settings", {})

	subfolder_check = package_settings.get("subfolder_images", False)
	generate_yaml = package_settings.get("generate_yaml", False)
	flag_empty_folders = package_settings.get("flag_empty_folders", False)

	slate_list = get_slates(shoot_folder)
	make_slate_folders(shoot_folder, slate_list)
	sort_data(shoot_folder, subfolder_check=subfolder_check)

	empty_folders = []
	if flag_empty_folders:
		empty_folders = find_empty_data_folders(shoot_folder)

	if generate_yaml:
		print("Generating report...")
		generate_report.generate_report(shoot_folder, settings_data)
		print("Report generation finished.")

	print("\nProcessing complete.")
	return {
		"final_path": shoot_folder,
		"empty_folders": empty_folders
	}


def main():
	if len(sys.argv) < 2:
		print("Usage: python slate_sorter.py <shoot_folder_path>")
		sys.exit(1)

	shoot_folder = sys.argv[1]

	settings_data = {
		"package_settings": {
			"rename_package": True,
			"prefix": "",
			"suffix": "_sorted",
			"subfolder_images": False,
			"generate_yaml": False,
		}
	}

	try:
		run_slate_sorter(shoot_folder, settings_data)
	except Exception as error:
		print(f"Error: {error}")
		sys.exit(1)


if __name__ == "__main__":
	main()