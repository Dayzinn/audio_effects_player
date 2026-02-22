import keyboard
import sounddevice as sd
from pedalboard import Pedalboard, PitchShift, load_plugin
from pedalboard.io import AudioStream
import os
import time
import threading

# ==================== USER CONFIGURATION ====================
# Change these if your plugins or devices are named/installed differently

# === Audio Devices ===
# Run the script once → look at printed list → copy exact names here if needed
INPUT_DEVICE_NAME  = "CABLE Output (VB-Audio Virtual Cable)"
OUTPUT_DEVICE_NAME = "Voicemeeter VAIO3 Input (VB-Audio Voicemeeter VAIO)"

# === Plugin paths (auto-detected in most cases) ===
# Override manually only if auto-detection fails
MELDA_ROOT = r"C:\Program Files\Common Files\VST3\MeldaProduction"
TDR_NOVA_OVERRIDE = None  # e.g. r"C:\Custom\Path\TDR Nova.vst3" or None

BUFFER_SIZE = 256           # Increase to 512/1024 if crackles/dropouts

SHIFT_432_SEMITONES = -0.3177
SHIFT_528_SEMITONES = +0.1567

# ==================== MELDA PLUGIN DETECTION ====================
def find_melda_plugin(plugin_name):
    """Search in MeldaProduction VST3 subfolders for exact filename match"""
    print(f"Searching for {plugin_name}.vst3...")
    melda_root = MELDA_ROOT
    
    if not os.path.exists(melda_root):
        print("   MeldaProduction folder not found.")
        return None
    
    for dirpath, _, filenames in os.walk(melda_root):
        for f in filenames:
            if f.lower() == f"{plugin_name.lower()}.vst3":
                full_path = os.path.join(dirpath, f)
                print(f"   Found: {full_path}")
                return full_path
    
    print(f"   {plugin_name}.vst3 not found.")
    return None

# Detect plugins – prefer regular MEqualizer
nova_path             = TDR_NOVA_OVERRIDE or (find_melda_plugin("TDR Nova") if os.path.exists(r"C:\Program Files\Common Files\VST3\TDR Nova.vst3") else None)
mequalizer_path       = find_melda_plugin("MEqualizer") or find_melda_plugin("MEqualizerLP")
mautopitch_path       = find_melda_plugin("MAutoPitch")
msaturator_path       = find_melda_plugin("MSaturator")
mcharmverb_path       = find_melda_plugin("MCharmVerb")
mstereoexpander_path  = find_melda_plugin("MStereoExpander")
mcompressor_path      = find_melda_plugin("MCompressor")

# ==================== INITIALIZATION ====================
print("\nInitializing pitch shifter...")
pitch_shifter = PitchShift(semitones=0.0)

# Load plugins
plugins = {
    "TDR Nova": None,
    "MEqualizer": None,
    "MAutoPitch": None,
    "MSaturator": None,
    "MCharmVerb": None,
    "MStereoExpander": None,
    "MCompressor": None
}

paths = {
    "TDR Nova": nova_path,
    "MEqualizer": mequalizer_path,
    "MAutoPitch": mautopitch_path,
    "MSaturator": msaturator_path,
    "MCharmVerb": mcharmverb_path,
    "MStereoExpander": mstereoexpander_path,
    "MCompressor": mcompressor_path
}

for name, path in paths.items():
    if path:
        try:
            plugin = load_plugin(path)
            plugins[name] = plugin
            print(f"✓ {name} loaded successfully!")
        except Exception as e:
            print(f"✗ Failed to load {name}: {e}")
    else:
        print(f"✗ {name} not found")

# Build chain: correction → shift → saturation → compression → reverb → stereo → EQ → dynamic EQ
effects_chain = []
if plugins["MAutoPitch"]:       effects_chain.append(plugins["MAutoPitch"])
effects_chain.append(pitch_shifter)
if plugins["MSaturator"]:       effects_chain.append(plugins["MSaturator"])
if plugins["MCompressor"]:      effects_chain.append(plugins["MCompressor"])
if plugins["MCharmVerb"]:       effects_chain.append(plugins["MCharmVerb"])
if plugins["MStereoExpander"]:  effects_chain.append(plugins["MStereoExpander"])
if plugins["MEqualizer"]:       effects_chain.append(plugins["MEqualizer"])
if plugins["TDR Nova"]:         effects_chain.append(plugins["TDR Nova"])

board = Pedalboard(effects_chain)

# ==================== GUI ATTEMPTS ====================
def try_open_gui(plugin, name):
    if not plugin:
        return
    try:
        print(f"Trying to open {name} GUI...")
        plugin.show_editor()
        print(f"→ {name} GUI attempt sent")
    except Exception as e:
        print(f"GUI failed for {name}: {e}")
        def threaded():
            try:
                time.sleep(0.5)
                plugin.show_editor()
            except Exception as te:
                print(f"Threaded GUI failed for {name}: {te}")
        threading.Thread(target=threaded, daemon=True).start()

# ==================== MODE CONTROL ====================
def set_normal():
    pitch_shifter.semitones = 0.0
    for p in plugins.values():
        if p: p.is_enabled = False
    print(">>> MODE: NORMAL (440 Hz – all effects bypassed)")

def set_432():
    pitch_shifter.semitones = SHIFT_432_SEMITONES
    for p in plugins.values():
        if p: p.is_enabled = True
    print(">>> MODE: 432 Hz ACTIVE (full chain)")

def set_528():
    pitch_shifter.semitones = SHIFT_528_SEMITONES
    for p in plugins.values():
        if p: p.is_enabled = True
    print(">>> MODE: 528 Hz ACTIVE (full chain)")

keyboard.add_hotkey('1', set_normal)
keyboard.add_hotkey('2', set_432)
keyboard.add_hotkey('3', set_528)
set_normal()

# ==================== START ====================
print("\n" + "="*60)
print("     LIVE 432/528 Hz + MELDA FX PROCESSOR")
print("="*60)
print("Routing instructions:")
print("  1. Set music player / browser output → CABLE Input (VB-Audio Virtual Cable)")
print("  2. In Voicemeeter: Enable VAIO3 strip → route to speakers/headphones")
print("\nControls:")
print("  1 → Normal (original pitch, effects off)")
print("  2 → 432 Hz tuning + full effects chain")
print("  3 → 528 Hz tuning + full effects chain")
print("  ESC → Quit")
print("\nNote: If no sound → check routing or device names below.")

# Debug: Show available devices so user can fix names if needed
print("\nAvailable audio devices (copy exact names if yours differ):")
print(sd.query_devices())

try:
    print(f"\nUsing INPUT:  {INPUT_DEVICE_NAME}")
    print(f"Using OUTPUT: {OUTPUT_DEVICE_NAME}\n")

    with AudioStream(
        input_device_name=INPUT_DEVICE_NAME,
        output_device_name=OUTPUT_DEVICE_NAME,
        buffer_size=BUFFER_SIZE
    ) as stream:
        stream.plugins = board

        print("🔊 Processing live!")
        print("Attempting to open plugin GUIs...\n")

        time.sleep(1.5)

        for name, plugin in plugins.items():
            try_open_gui(plugin, name)

        print("\nGUI attempts finished. Audio is processing regardless.")
        print("If GUIs don't appear → known limitation in real-time streaming mode.")
        keyboard.wait('esc')

finally:
    print("\nStopped. Goodbye!")
