'''*************************************************
content     generate_report

version     2.0.0
date        12-04-2026

author      Harry Shaper <harryshaper@gmail.com>

*************************************************'''

import os
import getpass

from datetime import date, datetime


# *********************************************************************
# HELPERS
def get_folder_size(folder_path):
	total_bytes = 0

	for root, dirs, files in os.walk(folder_path):
		for file in files:
			file_path = os.path.join(root, file)
			if os.path.isfile(file_path):
				total_bytes += os.path.getsize(file_path)

	return total_bytes


def get_child_dirs(folder_path):
	if not os.path.isdir(folder_path):
		return []

	return sorted([
		item for item in os.listdir(folder_path)
		if os.path.isdir(os.path.join(folder_path, item))
	], key=str.lower)


def collect_slate_summary(shoot_path):
	"""
	Reads:
		slates / SLATE / DATA_TYPE / CAPTURE_FOLDER
	Case-insensitive for the top-level slates folder.
	"""
	slate_summary = {}

	slates_root = None
	for item in get_child_dirs(shoot_path):
		if item.lower() == "slates":
			slates_root = os.path.join(shoot_path, item)
			break

	if not slates_root or not os.path.isdir(slates_root):
		return slate_summary

	for slate in get_child_dirs(slates_root):
		slate_path = os.path.join(slates_root, slate)
		slate_summary[slate] = {}

		for data_type in get_child_dirs(slate_path):
			data_type_path = os.path.join(slate_path, data_type)

			capture_count = len(get_child_dirs(data_type_path))
			slate_summary[slate][data_type] = capture_count

	return slate_summary


def collect_asset_summary(shoot_path):
	"""
	Reads:
		assets / ASSET_TYPE / ASSET_NAME / DATA_TYPE / ...
	Case-insensitive for the top-level assets folder.
	"""
	asset_summary = {}

	assets_root = None
	for item in get_child_dirs(shoot_path):
		if item.lower() == "assets":
			assets_root = os.path.join(shoot_path, item)
			break

	if not assets_root or not os.path.isdir(assets_root):
		return asset_summary

	for asset_type in get_child_dirs(assets_root):
		asset_type_path = os.path.join(assets_root, asset_type)
		asset_summary[asset_type] = {}

		for asset_name in get_child_dirs(asset_type_path):
			asset_name_path = os.path.join(asset_type_path, asset_name)
			data_types = get_child_dirs(asset_name_path)

			asset_summary[asset_type][asset_name] = data_types

	return asset_summary

def collect_keep_structure_summary(shoot_path):
	"""
	Reads folders that remained in place and were not sorted into:
		slates
		assets
		.showtools
	Case-insensitive.

	Returns:
		{
			"photogrammetry": {
				"item_count": 2,
				"items": ["chr_steven_costume_006", "prp_bedroom_coffee_table"]
			}
		}
	"""
	excluded = {"slates", "assets", ".showtools"}
	keep_summary = {}

	for item in get_child_dirs(shoot_path):
		if item.lower() in excluded:
			continue

		item_path = os.path.join(shoot_path, item)
		child_items = get_child_dirs(item_path)

		keep_summary[item] = {
			"item_count": len(child_items),
			"items": child_items,
		}

	return keep_summary

# *********************************************************************
# Create report
def generate_report(shoot_path, settings_data=None):
	"""Creates a readable report detailing slate, asset, and kept-structure data."""

	settings_data = settings_data or {}
	project_details = settings_data.get("project_details", {})

	project_alias = project_details.get("project_name", "CODENAME") or "CODENAME"
	unit = project_details.get("unit", "MU") or "MU"

	shoot_date_raw = project_details.get("shoot_date", "")
	if shoot_date_raw:
		try:
			shoot_date = datetime.strptime(str(shoot_date_raw), "%Y-%m-%d").date()
		except ValueError:
			shoot_date = date.today()
	else:
		shoot_date = date.today()

	user = project_details.get("wrangler", "").strip() or getpass.getuser()
	shoot_day = os.path.basename(shoot_path)

	report_file_name = shoot_day + "_report.yaml"
	report_path = os.path.join(shoot_path, report_file_name)

	total_bytes = get_folder_size(shoot_path)
	total_mb = total_bytes / (1024 * 1024)
	total_gb = total_mb / 1024

	timestamp = datetime.now().strftime("%Y-%m-%d @ %H:%M")

	slate_summary = collect_slate_summary(shoot_path)
	asset_summary = collect_asset_summary(shoot_path)
	keep_summary = collect_keep_structure_summary(shoot_path)

	slate_count = len(slate_summary)
	asset_type_count = len(asset_summary)
	asset_count = sum(len(asset_summary[asset_type]) for asset_type in asset_summary)

	with open(report_path, "w", encoding="utf-8") as f:
		# ------------------------------------------------
		# HEADER
		# ------------------------------------------------
		f.write(f"{project_alias}:\n")
		f.write(f"{unit} - {shoot_day}:\n")
		f.write(f"DATE - {shoot_date}:\n")
		f.write(f"  report_generated_by: {user}\n")
		f.write(f"  report_generated_at: {timestamp}\n")
		f.write(f"  total_captured_size_gb: {total_gb:.2f}\n")
		f.write(f"  total_captured_size_mb: {total_mb:.1f}\n")
		f.write(f"  #------------------------------------------------#\n\n")

		# ------------------------------------------------
		# SLATES
		# ------------------------------------------------
		f.write("slates_summary:\n")
		f.write(f"  slate_count: {slate_count}\n")

		if slate_summary:
			for slate, data_types in slate_summary.items():
				f.write(f"  {slate}:\n")

				if data_types:
					for data_type, count in data_types.items():
						f.write(f"    {data_type}: {count}\n")
				else:
					f.write("    empty: 0\n")
		else:
			f.write("  none: true\n")

		f.write("\n")

		# ------------------------------------------------
		# ASSETS
		# ------------------------------------------------
		f.write("assets_summary:\n")
		f.write(f"  asset_type_count: {asset_type_count}\n")
		f.write(f"  asset_count: {asset_count}\n")

		if asset_summary:
			for asset_type, assets in asset_summary.items():
				f.write(f"  {asset_type}:\n")

				if assets:
					for asset_name, data_types in assets.items():
						f.write(f"    {asset_name}:\n")

						if data_types:
							for data_type in data_types:
								f.write(f"      - {data_type}\n")
						else:
							f.write("      - empty\n")
				else:
					f.write("    none: true\n")
		else:
			f.write("  none: true\n")

		f.write("\n")

		# ------------------------------------------------
		# KEPT STRUCTURE
		# ------------------------------------------------
		f.write("kept_structure_summary:\n")
		f.write(f"  folder_count: {len(keep_summary)}\n")

		if keep_summary:
			for folder_name, data in keep_summary.items():
				f.write(f"  {folder_name}:\n")
				f.write(f"    item_count: {data['item_count']}\n")

				if data["items"]:
					f.write("    items:\n")
					for child_name in data["items"]:
						f.write(f"      - {child_name}\n")
				else:
					f.write("    items: []\n")
		else:
			f.write("  none: true\n")

	return report_path