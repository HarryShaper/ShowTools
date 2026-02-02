
# a) Changed this section into into a single line 

# Old
if SCRIPT_DIR not in sys.path:
sys.path.append(SCRIPT_DIR)

# New
sys.path.append(SCRIPT_DIR) if SCRIPT_DIR not in sys.path else None






















