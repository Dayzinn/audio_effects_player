![Python 3.8-3.12](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)



print(banner)

# Audio Effects Player
Real-time Python audio processor for 432/528 Hz tuning + Melda & TDR effects (VB-Cable + Voicemeeter)
A real-time Python audio processing application that:Takes system audio via VB-Cable (or any virtual input)
Applies pitch shifting to 432 Hz or 528 Hz tuning
Chains multiple free/professional-grade effects (MeldaProduction free bundle + TDR Nova)
Routes processed audio to Voicemeeter VAIO3 (or any virtual/physical output)
Allows instant mode switching with keyboard hotkeys (1 = Normal, 2 = 432 Hz, 3 = 528 Hz)

Perfect for creating "healing frequency" listening experiences, live tuning experiments, or creative audio processing.FeaturesSeamless real-time pitch shifting (± semitones for 432/528 Hz)
Full Melda free effects chain (when detected):MAutoPitch (auto-tune/correction)
MSaturator (warmth & distortion)
MCompressor (dynamics control)
MCharmVerb (reverb/ambience)
MStereoExpander (stereo widening)
MEqualizer / MEqualizerLP (parametric EQ)

TDR Nova (dynamic EQ – excellent for mastering-style processing)
Non-blocking keyboard controls (no audio interruption)
Plugin GUI attempts (limited success in streaming mode)
Voicemeeter integration for flexible routing & monitoring

RequirementsPython VersionPython 3.8 – 3.12 (tested on 3.10/3.11)

Required Python PackagesInstall via pip:bash

pip install pedalboard sounddevice numpy keyboard

pedalboard – Core audio processing & VST3 plugin hosting
sounddevice – Real-time audio I/O
numpy – Required by pedalboard/sounddevice
keyboard – Global hotkey detection (may need admin on Windows)

System / Hardware RequirementsWindows (tested on Win 10/11 – 64-bit)
VB-Audio Virtual Cable (free) – https://vb-audio.com/Cable/Used to route audio from apps (YouTube, Spotify, browser…) into the script

Voicemeeter (Banana or Potato recommended – free) – https://vb-audio.com/Voicemeeter/Receives processed audio on VAIO3 input → routes to speakers/headphones

At least 8 GB RAM recommended (more plugins = higher CPU/RAM usage)
Decent CPU (i5/i7 or equivalent) for real-time processing with multiple plugins

Required VST3 Plugins (All Free)Install these and let them scan into C:\Program Files\Common Files\VST3\MeldaProduction\...TDR Nova (Tokyo Dawn Labs – dynamic EQ)Download: https://www.tokyodawn.net/tdr-nova/
Install VST3 64-bit

MFreeFXBundle (MeldaProduction – includes all the following):Download: https://www.meldaproduction.com/MFreeFXBundle
Install via MPluginManager → select VST3 64-bit
Included plugins used:MAutoPitch
MSaturator
MCharmVerb
MStereoExpander
MCompressor
MEqualizer (preferred) or MEqualizerLP (linear-phase fallback)

Installation & SetupInstall Python (if not already installed)
Create virtual environment (optional but recommended):bash

python -m venv venv
venv\Scripts\activate

Install dependencies:bash

pip install pedalboard sounddevice numpy keyboard

Install VB-Cable and Voicemeeter (links above)
Install TDR Nova and MFreeFXBundle (links above)
Save the script as e.g. audio_effects_player.py
Run:bash

python audio_effects_player.py

UsageAudio Routing Setup
This script requires a virtual audio bridge to capture and output system sound.
Input: Set your system output (or browser/media player) to CABLE Input (VB-Audio Virtual Cable).
Output: The script will send processed audio to Voicemeeter VAIO3. Ensure your headphones/speakers are monitoring that channel.
Running the Processor
Clone this repository:

bash

git clone https://github.com
cd your-repo-name

Run the script:bash

python main.py

Live Controls
Use these global hotkeys to switch modes instantly without stopping the audio:
1: Normal Mode (440 Hz) - Bypasses all effects.
2: 432 Hz Mode - Applies -0.3177 semitone shift + full Melda/TDR chain.
3: 528 Hz Mode - Applies +0.1567 semitone shift + full Melda/TDR chain.
Esc: Stop - Safely closes the audio stream and exits.

TroubleshootingPlugins Not Found: Ensure MeldaProduction and TDR Nova VST3 files are installed in the default C:\Program Files\Common Files\VST3 directory.
GUI Issues: Due to limitations in real-time AudioStream processing, plugin windows may not appear or may stay "frozen." All processing happens in the background.
Latency: If you experience "crackling," try closing high-CPU applications or adjusting the buffer size in the AudioStream settings within the code.
No Sound: Double-check routing, device names, and run the script to see printed available devices. Update INPUT_DEVICE_NAME and OUTPUT_DEVICE_NAME if they don't match.DisclaimerThis script is for educational/experimental use. It does not include or distribute the VST plugins — users must download and install them legally from the official sites. Always respect developer terms of use.Made with  by  I/o 7 @Dayzinn

