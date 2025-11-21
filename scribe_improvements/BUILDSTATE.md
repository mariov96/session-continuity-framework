# Scribe Improvements - Microphone Selection Enhancement

## 🎯 Mission
Enhance the microphone selection settings page to provide users with real-time audio visualization and quality metrics, enabling them to easily identify the best recording channel.

## 🚀 Core Features
1.  **Device Enumeration**: Automatically detect all available audio input devices.
2.  **Real-Time Visualization**: For each device, display a real-time waveform or frequency spectrum visualization to show that the microphone is actively capturing audio.
3.  **Input Volume Meter**: Show a live decibel (dB) meter for each device to quantify input volume.
4.  **Signal-to-Noise Ratio (SNR)**: Implement a simple SNR calculation to provide a quantitative measure of microphone quality. A higher SNR indicates a cleaner signal.
5.  **"Test Recording" Feature**: Allow the user to make a short test recording from any device and play it back to hear the quality for themselves.
6.  **Clear Labeling**: Ensure devices are clearly and descriptively labeled (e.g., "MacBook Pro Microphone," "Logitech USB Headset").

## 📋 Implementation Plan

### Phase 1: Scaffolding and Basic UI (This Session)
- **Task 1**: Create the basic HTML structure for the new settings page (`microphone_settings.html`).
- **Task 2**: Add basic CSS for layout and styling (`microphone_settings.css`).
- **Task 3**: Create the main JavaScript file (`microphone_settings.js`) to handle device enumeration and UI updates.

### Phase 2: Real-Time Audio Processing
- **Task 4**: Implement device enumeration using the `navigator.mediaDevices.enumerateDevices()` API.
- **Task 5**: For each device, use `getUserMedia()` to access the audio stream.
- **Task 6**: Implement real-time waveform visualization using the Web Audio API and HTML5 Canvas.
- **Task 7**: Implement the input volume meter using an `AnalyserNode`.

### Phase 3: Advanced Features & Polish
- **Task 8**: Implement the "Test Recording" feature using the `MediaRecorder` API.
- **Task 9**: Research and implement a simplified SNR calculation.
- **Task 10**: Refine the UI and add instructional text to guide the user.

## 🛠️ Tech Stack
- **HTML5**: For the structure of the settings page.
- **CSS3**: For styling and layout.
- **JavaScript (ES6+)**: For all client-side logic.
- **Web Audio API**: For real-time audio processing and visualization.
- **MediaRecorder API**: For the test recording feature.

This plan breaks down the feature into manageable phases, starting with the foundational UI elements.