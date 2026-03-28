'''*************************************************
content     ShowTools

version     0.0.1
date        23-03-2026

author      Harry Shaper <harryshaper@gmail.com>

*************************************************'''

import os
import sys
import webbrowser
import yaml
import urllib.parse
from pathlib import Path

from Qt import QtWidgets, QtGui, QtCore, QtCompat
from Qt.QtCore import QDate
from Qt.QtWidgets import QFileDialog


try:
	from .resources import resources_rc
	from .slate_sorter import run_slate_sorter, tag_empty_folders, rename_shoot_folder
except ImportError:
	from resources import resources_rc
	from slate_sorter import run_slate_sorter, tag_empty_folders, rename_shoot_folder


TITLE = Path(__file__).stem
CURRENT_PATH = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_PATH.parent

ICONS_DIR = ROOT_DIR / "assets" / "Icons"
PIPELINE_PROFILES_PATH = ROOT_DIR / "config" / "Pipeline_profiles"
SHOW_DEFAULTS_DIR = ROOT_DIR / "config" / "Show_defaults"
UI_PATH = CURRENT_PATH / "ui" / "ShowTools.ui"

SELECTED_DEFAULT_SETTINGS = "show_defaults_highlander_2U.yaml"


def icon_path(name):
	return str(ICONS_DIR / f"{name}.png")


# ******************************************************************************
# CLASSES

# CLASS - CUSTOM DIALOG
class CustomMessageDialog(QtWidgets.QDialog):
	def __init__(self, title, heading, detail="", sub_detail="", parent=None):
		super().__init__(parent)

		self.setWindowTitle(title)
		self.setWindowIcon(QtGui.QIcon(icon_path("logo")))
		self.setModal(True)
		self.setFixedSize(430, 165)

		self.setStyleSheet("""
			QDialog {
				background-color: #2f2f2f;
			}

			QLabel {
				background-color: transparent;
			}

			QLabel#headingLabel {
				color: #d8a106;
				font-size: 16px;
				font-weight: 600;
			}

			QLabel#detailLabel {
				color: #f2f2f2;
				font-size: 13px;
				font-weight: 400;
			}

			QLabel#subDetailLabel {
				color: #bfbfbf;
				font-size: 11px;
				font-weight: 400;
			}

			QPushButton {
				background-color: #c99700;
				color: black;
				border: none;
				padding: 5px 14px;
				min-width: 72px;
				min-height: 30px;
				font-size: 12px;
				font-weight: 500;
			}

			QPushButton:hover {
				background-color: #d8a106;
			}

			QPushButton:pressed {
				background-color: #b88705;
			}
		""")

		# SIZING
		main_layout = QtWidgets.QVBoxLayout(self)
		main_layout.setContentsMargins(24, 18, 24, 18)
		main_layout.setSpacing(8)

		# HEADINGS
		self.heading_label = QtWidgets.QLabel(heading)
		self.heading_label.setObjectName("headingLabel")
		self.heading_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
		main_layout.addWidget(self.heading_label)

		if detail:
			self.detail_label = QtWidgets.QLabel(detail)
			self.detail_label.setObjectName("detailLabel")
			self.detail_label.setWordWrap(False)
			self.detail_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
			main_layout.addWidget(self.detail_label)

		if sub_detail:
			self.sub_detail_label = QtWidgets.QLabel(sub_detail)
			self.sub_detail_label.setObjectName("subDetailLabel")
			self.sub_detail_label.setWordWrap(True)
			self.sub_detail_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
			main_layout.addWidget(self.sub_detail_label)

		main_layout.addStretch()

		button_layout = QtWidgets.QHBoxLayout()
		button_layout.addStretch()

		self.ok_button = QtWidgets.QPushButton("OK")
		self.ok_button.clicked.connect(self.accept)
		button_layout.addWidget(self.ok_button)

		main_layout.addLayout(button_layout)


# CLASS - EMPTY FOLDERS DIALOGUE
class EmptyFoldersDialog(QtWidgets.QDialog):
	def __init__(self, empty_folders, parent=None):
		super().__init__(parent)

		self.setWindowTitle("Empty Folders Detected")
		self.setWindowIcon(QtGui.QIcon(icon_path("logo")))
		self.setModal(True)
		self.setFixedSize(520, 320)

		self.setStyleSheet("""
			QDialog {
				background-color: #2f2f2f;
			}
			QLabel {
				color: #ededed;
				background: transparent;
			}
			QLabel#headingLabel {
				color: #d8a106;
				font-size: 16px;
				font-weight: 600;
			}
			QTextEdit {
				background-color: #1f1f1f;
				color: #ededed;
				border: 1px solid #4a4a4a;
				padding: 6px;
			}
			QPushButton {
				background-color: #c99700;
				color: black;
				border: none;
				padding: 5px 14px;
				min-width: 100px;
				min-height: 30px;
				font-size: 12px;
				font-weight: 500;
			}
			QPushButton:hover {
				background-color: #d8a106;
			}
			QPushButton:pressed {
				background-color: #b88705;
			}
		""")

		layout = QtWidgets.QVBoxLayout(self)
		layout.setContentsMargins(24, 18, 24, 18)
		layout.setSpacing(10)

		heading = QtWidgets.QLabel("Empty Folders Detected")
		heading.setObjectName("headingLabel")
		layout.addWidget(heading)

		detail = QtWidgets.QLabel(
			"The following folders contain no image files.\n"
			"Continue export to tag them with _MISSING, or go back to review them."
		)
		detail.setWordWrap(True)
		layout.addWidget(detail)

		folder_list = QtWidgets.QTextEdit()
		folder_list.setReadOnly(True)
		folder_list.setText("\n".join(empty_folders))
		layout.addWidget(folder_list)

		button_row = QtWidgets.QHBoxLayout()
		button_row.addStretch()

		self.back_button = QtWidgets.QPushButton("Go Back")
		self.back_button.clicked.connect(self.reject)
		button_row.addWidget(self.back_button)

		self.continue_button = QtWidgets.QPushButton("Continue Export")
		self.continue_button.clicked.connect(self.accept)
		button_row.addWidget(self.continue_button)

		layout.addLayout(button_row)


# CLASS - ShowTools
class ShowTools:

	def __init__(self):
		self.wgShowTools = QtCompat.loadUi(str(UI_PATH))

		# TABS
		self.wgShowTools.btn_mainSettings.clicked.connect(self.show_main_settings)
		self.wgShowTools.btn_renameSettings.clicked.connect(self.show_rename_settings)

		# WINDOW ICON
		self.wgShowTools.setWindowIcon(QtGui.QIcon(icon_path("logo")))

		# LINK ICONS
		self.wgShowTools.btn_gmail.setIcon(QtGui.QIcon(icon_path("gmail_icon")))
		self.wgShowTools.btn_github.setIcon(QtGui.QIcon(icon_path("github_icon")))
		self.wgShowTools.btn_linkedin.setIcon(QtGui.QIcon(icon_path("linkedin_icon")))
		self.wgShowTools.btn_youtube.setIcon(QtGui.QIcon(icon_path("youtube_icon")))
		self.wgShowTools.btn_website.setIcon(QtGui.QIcon(icon_path("logo")))

		# TOOL ICONS
		self.wgShowTools.btn_browseConfig.setIcon(QtGui.QIcon(icon_path("browse_file_icon")))
		self.wgShowTools.btn_browseTargetFolder.setIcon(QtGui.QIcon(icon_path("browse_file_icon")))

		# SIGNALS
		# ------- Action Buttons
		self.wgShowTools.btn_clearSettings.clicked.connect(self.press_clearSettings)
		self.wgShowTools.btn_browseConfig.clicked.connect(self.press_browseConfig)
		self.wgShowTools.btn_saveSettings.clicked.connect(self.press_saveSettings)
		self.wgShowTools.btn_browseTargetFolder.clicked.connect(self.press_browseTargetFolder)
		self.wgShowTools.btn_export.clicked.connect(self.press_export)

		# ------- Links
		self.wgShowTools.btn_gmail.clicked.connect(self.press_loadGmail)
		self.wgShowTools.btn_github.clicked.connect(self.press_loadGithub)
		self.wgShowTools.btn_linkedin.clicked.connect(self.press_loadLinkedin)
		self.wgShowTools.btn_youtube.clicked.connect(self.press_loadYoutube)
		self.wgShowTools.btn_website.clicked.connect(self.press_loadWebsite)

		# SETUP
		self.wgShowTools.input_shootDate.setDate(QDate.currentDate())
		self.wgShowTools.input_configFile.setPlaceholderText("Select sorting template...")
		self.update_target_folder_state("")
		self.show_main_settings()

		self.load_show_defaults()

		# GET PATH FROM SYS.ARGV - RIGHT CLICK, SEND TO
		if len(sys.argv) > 1:
			startup_path = sys.argv[1]
			if os.path.isdir(startup_path):
				self.set_target_folder(startup_path)

		self.wgShowTools.show()

		self.wgShowTools.chk_renamePackage.stateChanged.connect(self.update_rename_fields_state)

		# SET INITIAL STATE
		self.update_rename_fields_state()

		# FIND PIPELINE PROFILES
		os.makedirs(PIPELINE_PROFILES_PATH, exist_ok=True)

	# ************************************************************************************************
	# TABS
	def show_main_settings(self):
		self.wgShowTools.stackedWidget.setCurrentIndex(0)
		self.update_tab_styles(active="main")

	def show_rename_settings(self):
		self.wgShowTools.stackedWidget.setCurrentIndex(1)
		self.update_tab_styles(active="rename")

	def update_tab_styles(self, active):
		active_style = """
			QPushButton {
				color: #d8a106;
				background: transparent;
				border: none;
			}
		"""

		inactive_style = """
			QPushButton {
				color: #f2f2f2;
				background: transparent;
				border: none;
			}

			QPushButton:hover {
				color: #d8a106;
			}
		"""

		if active == "main":
			self.wgShowTools.btn_mainSettings.setStyleSheet(active_style)
			self.wgShowTools.btn_renameSettings.setStyleSheet(inactive_style)

		elif active == "rename":
			self.wgShowTools.btn_mainSettings.setStyleSheet(inactive_style)
			self.wgShowTools.btn_renameSettings.setStyleSheet(active_style)

	# *********************************************************************#
	# HELPERS
	def open_link(self, url):
		preferred_browser = "default"

		if hasattr(self, "browser_defaults"):
			preferred_browser = self.browser_defaults.get("preferred_browser", "default").lower()

		browser_map = {
			"chrome": [
				"C:/Program Files/Google/Chrome/Application/chrome.exe %s",
				"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s",
			],
			"edge": [
				"C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s",
				"C:/Program Files/Microsoft/Edge/Application/msedge.exe %s",
			],
		}

		if preferred_browser in browser_map:
			for browser_path in browser_map[preferred_browser]:
				if os.path.exists(browser_path.replace(" %s", "")):
					try:
						webbrowser.get(browser_path).open(url)
						return
					except Exception:
						pass

		webbrowser.open(url)

	def open_email_client(self, subject, body, to_list=None, cc_list=None):
		to = ",".join(to_list or [])
		cc = ",".join(cc_list or [])

		preferred_browser = "default"

		if hasattr(self, "browser_defaults"):
			preferred_browser = self.browser_defaults.get("preferred_browser", "default").lower()

		# CASE 1: Use system default email client (mailto)
		if preferred_browser == "default":
			params = {
				"subject": subject,
				"body": body
			}

			if cc:
				params["cc"] = cc

			query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
			url = f"mailto:{to}?{query}"

			webbrowser.open(url)
			return

		# CASE 2: Use Gmail in browser
		params = {
			"view": "cm",
			"to": to,
			"su": subject,
			"body": body
		}

		if cc:
			params["cc"] = cc

		query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
		url = f"https://mail.google.com/mail/?{query}"

		self.open_link(url)

	def format_email_text(self, text, context):
		if not text:
			return ""

		try:
			return text.format(**context)
		except Exception:
			return text

	def load_show_defaults(self):
		data = {}
		defaults_path = SHOW_DEFAULTS_DIR / SELECTED_DEFAULT_SETTINGS

		if not defaults_path.exists():
			return

		try:
			with open(defaults_path, "r", encoding="utf-8") as f:
				data = yaml.safe_load(f) or {}

			show_profile = data.get("show_profile", {})
			project_defaults = data.get("project_defaults", {})
			wrangler_defaults = data.get("wrangler_defaults", {})
			email_defaults = data.get("email_defaults", {})

			# Master toggle
			if not show_profile.get("auto_load_defaults", False):
				return

			# Project Defaults
			if show_profile.get("apply_project_name_on_startup", True):
				if not self.wgShowTools.input_projectName.text().strip():
					self.wgShowTools.input_projectName.setText(
						project_defaults.get("project_name", "")
					)

			if project_defaults.get("unit"):
				unit = project_defaults.get("unit")
				idx = self.wgShowTools.input_unit.findText(unit, QtCore.Qt.MatchExactly)
				if idx >= 0:
					self.wgShowTools.input_unit.setCurrentIndex(idx)

			# Wrangler Defaults
			if show_profile.get("apply_wranglers_on_startup", True):
				wranglers = wrangler_defaults.get("options", [])

				if wranglers:
					self.wgShowTools.input_wrangler.clear()
					self.wgShowTools.input_wrangler.addItems(wranglers)

					default_wrangler = wrangler_defaults.get("default_selection", "")
					idx = self.wgShowTools.input_wrangler.findText(
						default_wrangler, QtCore.Qt.MatchExactly
					)
					if idx >= 0:
						self.wgShowTools.input_wrangler.setCurrentIndex(idx)

			# Email Defaults
			if show_profile.get("apply_email_defaults_on_startup", False):
				enabled = email_defaults.get("enabled_by_default", False)
				self.wgShowTools.chk_notifyByEmail.setChecked(enabled)

			self.email_defaults = email_defaults

		except Exception as error:
			print(f"Failed to load show defaults: {error}")

		self.browser_defaults = data.get("browser_defaults", {})

	def update_rename_fields_state(self):
		enabled = self.wgShowTools.chk_renamePackage.isChecked()

		# Inputs
		self.wgShowTools.input_remove.setEnabled(enabled)
		self.wgShowTools.input_prefix.setEnabled(enabled)
		self.wgShowTools.input_suffix.setEnabled(enabled)

		# Labels
		active_color = "#ffffff"
		disabled_color = "#7a7a7a"

		color = active_color if enabled else disabled_color

		self.wgShowTools.label_remove.setStyleSheet(f"color: {color};")
		self.wgShowTools.label_prefix.setStyleSheet(f"color: {color};")
		self.wgShowTools.label_suffix.setStyleSheet(f"color: {color};")

		if not enabled:
			self.wgShowTools.input_remove.clear()
			self.wgShowTools.input_prefix.clear()
			self.wgShowTools.input_suffix.clear()

	def update_target_folder_state(self, folder_path=""):
		if folder_path and os.path.isdir(folder_path):
			state = "valid"
		else:
			state = "missing"

		widget = self.wgShowTools.input_targetFolder
		widget.setProperty("pathState", state)
		widget.style().unpolish(widget)
		widget.style().polish(widget)

	def set_target_folder(self, folder_path):
		self.wgShowTools.input_targetFolder.setText(folder_path if folder_path else "")
		self.wgShowTools.input_targetFolder.setToolTip(folder_path if folder_path else "")
		self.update_target_folder_state(folder_path)

	def confirm_empty_folders(self, empty_folders):
		dialog = EmptyFoldersDialog(empty_folders, parent=self.wgShowTools)
		return dialog.exec() == QtWidgets.QDialog.Accepted

	def show_message(self, title, heading, detail="", sub_detail=""):
		dialog = CustomMessageDialog(
			title=title,
			heading=heading,
			detail=detail,
			sub_detail=sub_detail,
			parent=self.wgShowTools
		)
		dialog.exec()

	def get_settings_data(self):
		return {
			"project_details": {
				"project_name": self.wgShowTools.input_projectName.text().strip(),
				"shoot_date": self.wgShowTools.input_shootDate.date().toString("yyyy-MM-dd"),
				"wrangler": self.wgShowTools.input_wrangler.currentText().strip(),
				"unit": self.wgShowTools.input_unit.currentText().strip(),
			},
			"package_settings": {
				"rename_package": self.wgShowTools.chk_renamePackage.isChecked(),
				"remove": self.wgShowTools.input_remove.text().strip(),
				"prefix": self.wgShowTools.input_prefix.text().strip(),
				"suffix": self.wgShowTools.input_suffix.text().strip(),
				"subfolder_images": self.wgShowTools.chk_subfolderImages.isChecked(),
				"generate_yaml": self.wgShowTools.chk_generateYAML.isChecked(),
				"notify_by_email": self.wgShowTools.chk_notifyByEmail.isChecked(),
				"flag_empty_folders": self.wgShowTools.chk_flagEmptyFolders.isChecked(),
			}
		}

	def load_settings_from_yaml(self, file_path):
		try:
			with open(file_path, "r", encoding="utf-8") as yaml_file:
				settings_data = yaml.safe_load(yaml_file) or {}

			project_details = settings_data.get("project_details", {})
			package_settings = settings_data.get("package_settings", {})

			# Project Details
			self.wgShowTools.input_projectName.setText(project_details.get("project_name", ""))

			shoot_date = QDate.fromString(project_details.get("shoot_date", ""), "yyyy-MM-dd")
			if shoot_date.isValid():
				self.wgShowTools.input_shootDate.setDate(shoot_date)
			else:
				self.wgShowTools.input_shootDate.setDate(QDate.currentDate())

			wrangler = project_details.get("wrangler", "")
			wrangler_index = self.wgShowTools.input_wrangler.findText(
				wrangler,
				QtCore.Qt.MatchExactly
			)
			if wrangler_index >= 0:
				self.wgShowTools.input_wrangler.setCurrentIndex(wrangler_index)
			else:
				self.wgShowTools.input_wrangler.setCurrentIndex(0)

			unit = project_details.get("unit", "")
			unit_index = self.wgShowTools.input_unit.findText(
				unit,
				QtCore.Qt.MatchExactly
			)
			if unit_index >= 0:
				self.wgShowTools.input_unit.setCurrentIndex(unit_index)
			else:
				self.wgShowTools.input_unit.setCurrentIndex(0)

			# Package Settings
			self.wgShowTools.chk_renamePackage.setChecked(
				package_settings.get("rename_package", False)
			)
			self.wgShowTools.input_remove.setText(package_settings.get("remove", ""))
			self.wgShowTools.input_prefix.setText(package_settings.get("prefix", ""))
			self.wgShowTools.input_suffix.setText(package_settings.get("suffix", ""))
			self.wgShowTools.chk_subfolderImages.setChecked(
				package_settings.get("subfolder_images", False)
			)
			self.wgShowTools.chk_generateYAML.setChecked(
				package_settings.get("generate_yaml", False)
			)
			self.wgShowTools.chk_notifyByEmail.setChecked(
				package_settings.get("notify_by_email", False)
			)
			self.wgShowTools.chk_flagEmptyFolders.setChecked(
				package_settings.get("flag_empty_folders", False)
			)

			self.wgShowTools.input_configFile.setText(file_path)

			profile_name = os.path.basename(file_path)

			self.show_message(
				"Load Successful",
				"Loaded Profile",
				profile_name
			)

		except Exception as error:
			self.show_message(
				"Load Failed",
				"Could not load settings.",
				str(error)
			)

	# *********************************************************************#
	# PRESS
	def press_clearSettings(self):
		self.wgShowTools.input_configFile.clear()
		self.wgShowTools.input_configFile.setPlaceholderText("Select sorting template...")

		self.wgShowTools.input_projectName.setText("")
		self.wgShowTools.input_wrangler.setCurrentIndex(0)
		self.wgShowTools.input_unit.setCurrentIndex(0)
		self.wgShowTools.input_shootDate.setDate(QDate.currentDate())

		self.wgShowTools.chk_renamePackage.setChecked(False)
		self.wgShowTools.input_remove.setText("")
		self.wgShowTools.input_prefix.setText("")
		self.wgShowTools.input_suffix.setText("")
		self.wgShowTools.chk_subfolderImages.setChecked(False)
		self.wgShowTools.chk_generateYAML.setChecked(False)
		self.wgShowTools.chk_notifyByEmail.setChecked(False)
		self.wgShowTools.chk_flagEmptyFolders.setChecked(False)

	def press_saveSettings(self):
		settings_data = self.get_settings_data()

		file_path, _ = QFileDialog.getSaveFileName(
			self.wgShowTools,
			"Save Settings Profile",
			str(PIPELINE_PROFILES_PATH),
			"YAML Files (*.yaml *.yml)"
		)

		if not file_path:
			return

		if not file_path.lower().endswith((".yaml", ".yml")):
			file_path += ".yaml"

		try:
			with open(file_path, "w", encoding="utf-8") as yaml_file:
				yaml.dump(
					settings_data,
					yaml_file,
					default_flow_style=False,
					sort_keys=False
				)

			profile_name = os.path.basename(file_path)

			self.show_message(
				"Save Successful",
				"Settings Saved",
				profile_name,
				file_path
			)

		except Exception as error:
			self.show_message(
				"Save Failed",
				"Could not save settings.",
				str(error)
			)

	def press_export(self):
		folder_path = self.wgShowTools.input_targetFolder.text().strip()

		if not folder_path or not os.path.isdir(folder_path):
			self.show_message(
				"Export Failed",
				"Missing Target Folder",
				"Please select a valid target folder."
			)
			return

		settings_data = self.get_settings_data()
		package_settings = settings_data.get("package_settings", {})

		rename_package = package_settings.get("rename_package", False)
		rename_remove = package_settings.get("remove", "")
		rename_prefix = package_settings.get("prefix", "")
		rename_suffix = package_settings.get("suffix", "")

		try:
			result = run_slate_sorter(folder_path, settings_data)

			working_path = result.get("final_path", folder_path)
			empty_folders = result.get("empty_folders", [])

			flagged_count = 0

			if empty_folders:
				should_continue = self.confirm_empty_folders(empty_folders)

				if not should_continue:
					self.show_message(
						"Export Paused",
						"Empty Folders Found",
						"Export was paused so you can review the empty folders."
					)
					return

				flagged_paths = tag_empty_folders(empty_folders)
				flagged_count = len(flagged_paths)

			final_path = working_path

			if rename_package:
				final_path = rename_shoot_folder(
					working_path,
					rename_remove=rename_remove,
					rename_prefix=rename_prefix,
					rename_suffix=rename_suffix
				)

			self.set_target_folder(final_path)

			package_name = os.path.basename(final_path)
			clean_package_name = package_name

			if rename_suffix:
				clean_package_name = clean_package_name.replace(rename_suffix, "")

			if rename_remove:
				clean_package_name = clean_package_name.replace(rename_remove, "")

			clean_package_name = clean_package_name.replace("__", "_").strip("_")

			context = {
				"package_name": package_name,
				"clean_package_name": clean_package_name,
				"project_name": self.wgShowTools.input_projectName.text().strip(),
				"wrangler": self.wgShowTools.input_wrangler.currentText().strip(),
				"unit": self.wgShowTools.input_unit.currentText().strip(),
				"shoot_date": self.wgShowTools.input_shootDate.date().toString("yyyy-MM-dd"),
			}

			email_subject = ""
			email_body = ""

			if hasattr(self, "email_defaults"):
				email_subject = self.format_email_text(
					self.email_defaults.get("subject", ""),
					context
				)
				email_body = self.format_email_text(
					self.email_defaults.get("body", ""),
					context
				)

				self.email_subject = email_subject
				self.email_body = email_body
				self.email_to = self.email_defaults.get("to", [])
				self.email_cc = self.email_defaults.get("cc", [])

			if flagged_count == 1:
				detail_text = "1 folder was flagged as missing."
			elif flagged_count > 1:
				detail_text = f"{flagged_count} folders were flagged as missing."
			else:
				detail_text = final_path

			self.show_message(
				"Export Successful",
				"Sorting Complete",
				detail_text,
				final_path
			)

			if hasattr(self, "email_defaults") and self.wgShowTools.chk_notifyByEmail.isChecked():
				self.open_email_client(
					subject=self.email_subject,
					body=self.email_body,
					to_list=self.email_to,
					cc_list=self.email_cc
				)

		except Exception as error:
			self.show_message(
				"Export Failed",
				"Could not complete export.",
				str(error)
			)

	# *********************************************************************#
	# PRESS BROWSE FILES
	def press_browseConfig(self):
		file_path, _ = QFileDialog.getOpenFileName(
			self.wgShowTools,
			"Select Pipeline Config",
			str(PIPELINE_PROFILES_PATH),
			"YAML Files (*.yaml *.yml);;All Files (*)"
		)

		if file_path:
			self.load_settings_from_yaml(file_path)

	def press_browseTargetFolder(self):
		current_path = self.wgShowTools.input_targetFolder.text().strip()

		folder = QtWidgets.QFileDialog.getExistingDirectory(
			self.wgShowTools,
			"Select Target Folder",
			current_path if current_path else ""
		)

		if folder:
			self.set_target_folder(folder)

	# *********************************************************************#
	# PRESS LINKS
	def press_loadGmail(self):
		email = "harryshaper@gmail.com"
		subject = urllib.parse.quote("ShowTools Inquiry")
		body = urllib.parse.quote("Hi Harry,\n\n")

		url = (
			f"https://mail.google.com/mail/?view=cm"
			f"&to={email}"
			f"&su={subject}"
			f"&body={body}"
		)

		self.open_link(url)

	def press_loadGithub(self):
		self.open_link("https://github.com/HarryShaper")

	def press_loadLinkedin(self):
		self.open_link("https://www.linkedin.com/in/harry-shaper-vfx/")

	def press_loadYoutube(self):
		self.open_link("https://www.youtube.com/")

	def press_loadWebsite(self):
		self.open_link("https://www.shapervfx.com/")


# *********************************************************************#
# START UI
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    initialize_app = ShowTools()
    app.exec()