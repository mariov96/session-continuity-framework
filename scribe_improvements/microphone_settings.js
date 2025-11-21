document.addEventListener('DOMContentLoaded', () => {
    const deviceList = document.getElementById('device-list');
    const refreshButton = document.getElementById('refresh-devices');
    const deviceTemplate = document.getElementById('device-template');

    let audioStream;

    // Function to get permissions and enumerate devices
    async function getDevices() {
        // Clear the existing list
        deviceList.innerHTML = '';

        try {
            // Get user permission to access microphone
            // This is necessary before we can enumerate the full device list
            if (!audioStream) {
                audioStream = await navigator.mediaDevices.getUserMedia({ audio: true, video: false });
            }

            // Enumerate all media devices
            const devices = await navigator.mediaDevices.enumerateDevices();
            const audioDevices = devices.filter(device => device.kind === 'audioinput');

            if (audioDevices.length === 0) {
                deviceList.innerHTML = '<p>No microphone devices found.</p>';
                return;
            }

            // Populate the list with found devices
            audioDevices.forEach(device => {
                const deviceClone = deviceTemplate.content.cloneNode(true);

                deviceClone.querySelector('.device-name').textContent = device.label || `Microphone ${deviceList.children.length + 1}`;
                deviceClone.querySelector('.device-id').textContent = device.deviceId;

                // TODO: Add event listeners for test and select buttons

                deviceList.appendChild(deviceClone);
            });

        } catch (err) {
            console.error('Error accessing media devices.', err);
            let errorMessage = 'Could not access microphone. Please grant permission in your browser settings.';
            if (err.name === 'NotAllowedError') {
                errorMessage = 'Microphone access was denied. Please grant permission to use this feature.';
            } else if (err.name === 'NotFoundError') {
                errorMessage = 'No microphone was found on your system.';
            }
            deviceList.innerHTML = `<p style="color: red;">${errorMessage}</p>`;
        }
    }

    // Event Listeners
    refreshButton.addEventListener('click', getDevices);

    // Initial device load
    getDevices();
});