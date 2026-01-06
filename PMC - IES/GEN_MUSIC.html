<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generative Music Creator</title>
    <!-- Use Tailwind CSS for a clean, modern, and responsive design -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
        body {
            font-family: 'Inter', sans-serif;
            background-color: #0d1117;
            color: #c9d1d9;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 1rem;
        }
        .container {
            background-color: #161b22;
            padding: 2.5rem;
            border-radius: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            max-width: 500px;
            width: 100%;
        }
        .control-group {
            margin-bottom: 1.5rem;
        }
        .slider {
            width: 100%;
            -webkit-appearance: none;
            height: 8px;
            background: #30363d;
            outline: none;
            border-radius: 9999px;
            transition: background 0.3s ease;
        }
        .slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 20px;
            height: 20px;
            background: #58a6ff;
            cursor: pointer;
            border-radius: 50%;
            border: 2px solid #58a6ff;
            transition: transform 0.2s ease-in-out;
        }
        .slider::-moz-range-thumb {
            width: 20px;
            height: 20px;
            background: #58a6ff;
            cursor: pointer;
            border-radius: 50%;
            border: 2px solid #58a6ff;
            transition: transform 0.2s ease-in-out;
        }
    </style>
</head>
<body>

    <div id="container" class="container text-center">
        <h1 class="text-3xl font-bold mb-4">Generative Music Creator</h1>
        <p class="text-gray-400 mb-8">
            Click play to generate a unique, evolving ambient soundscape.
            <br>
            You can adjust the parameters in real time.
        </p>

        <div class="control-group">
            <label for="tempoSlider" class="block text-left mb-2 text-gray-400">Tempo (BPM)</label>
            <input type="range" id="tempoSlider" min="60" max="180" value="120" class="slider" oninput="updateParameter('tempo', this.value)">
            <span id="tempoValue" class="block text-right text-gray-400 text-sm">120</span>
        </div>

        <div class="control-group">
            <label for="densitySlider" class="block text-left mb-2 text-gray-400">Note Density</label>
            <input type="range" id="densitySlider" min="0.1" max="1.0" step="0.1" value="0.5" class="slider" oninput="updateParameter('density', this.value)">
            <span id="densityValue" class="block text-right text-gray-400 text-sm">0.5</span>
        </div>

        <div class="control-group">
            <label for="octaveSlider" class="block text-left mb-2 text-gray-400">Octave Range</label>
            <input type="range" id="octaveSlider" min="2" max="6" value="4" class="slider" oninput="updateParameter('octave', this.value)">
            <span id="octaveValue" class="block text-right text-gray-400 text-sm">4</span>
        </div>

        <div class="flex space-x-4 justify-center mt-8">
            <button id="playBtn" class="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-full transition-colors duration-200 focus:outline-none">
                <span id="playText">Play</span>
            </button>
            <button id="randomBtn" class="bg-gray-700 hover:bg-gray-600 text-white font-bold py-3 px-6 rounded-full transition-colors duration-200 focus:outline-none">
                Randomize
            </button>
        </div>

        <div id="messageBox" class="mt-8 text-gray-400 text-sm h-4"></div>
    </div>

    <!-- Tone.js library for audio synthesis -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.js"></script>
    <script>
        // Use a global variable for the synth and the loop
        let synth = null;
        let loop = null;
        let isPlaying = false;
        let noteSequence = [];

        // Global parameters for the generative algorithm
        const params = {
            tempo: 120,
            density: 0.5,
            octave: 4,
            scale: ["C", "D", "E", "F", "G", "A", "B"] // C Major Scale
        };

        const playBtn = document.getElementById('playBtn');
        const playText = document.getElementById('playText');
        const randomBtn = document.getElementById('randomBtn');
        const messageBox = document.getElementById('messageBox');
        
        // Function to handle initial user gesture and start audio context
        async function startAudio() {
            if (Tone.context.state !== 'running') {
                await Tone.start();
                showMessage('Audio context started successfully!');
            }
        }

        // Initialize the synth and its effects
        function setupSynth() {
            synth = new Tone.Synth({
                oscillator: { type: 'sine' },
                envelope: {
                    attack: 0.1,
                    decay: 0.2,
                    sustain: 0.8,
                    release: 0.5
                }
            }).toDestination();
        }

        // Generates a new sequence of notes based on current parameters
        function generateSequence() {
            noteSequence = [];
            const numNotes = 16;
            const noteCount = Math.floor(numNotes * params.density);

            // Create a shuffled list of notes from the scale
            const availableNotes = [];
            for (let i = 0; i < 3; i++) { // Use 3 octaves for variation
                params.scale.forEach(note => {
                    availableNotes.push(note + (parseInt(params.octave) + i - 1));
                });
            }

            // Randomly pick notes from the available set
            for (let i = 0; i < noteCount; i++) {
                const note = availableNotes[Math.floor(Math.random() * availableNotes.length)];
                noteSequence.push(note);
            }
        }

        // Sets up the Tone.Loop to play the generated sequence
        function setupLoop() {
            // Stop and dispose of any existing loop
            if (loop) {
                loop.stop().dispose();
            }

            // Create a new loop with the generated note sequence
            loop = new Tone.Loop(time => {
                // Get a random note from the sequence to add variation
                const note = noteSequence[Math.floor(Math.random() * noteSequence.length)];
                if (note) {
                    synth.triggerAttackRelease(note, "8n", time);
                }
            }, "8n").start(0);
        }

        // Toggles the play/stop state
        playBtn.addEventListener('click', async () => {
            await startAudio();
            
            if (isPlaying) {
                // Stop the music
                Tone.Transport.stop();
                playText.textContent = 'Play';
                isPlaying = false;
                showMessage('Music stopped.');
            } else {
                // Start the music
                Tone.Transport.start();
                playText.textContent = 'Stop';
                isPlaying = true;
                showMessage('Generating music...');
                
                // If it's the first time playing, set up everything
                if (!synth) {
                    setupSynth();
                    generateSequence();
                    setupLoop();
                }
            }
        });

        // Randomize button generates a new sequence and restarts the loop
        randomBtn.addEventListener('click', () => {
            startAudio();
            generateSequence();
            setupLoop();
            if (isPlaying) {
                showMessage('New sequence generated!');
            } else {
                showMessage('New sequence generated (click play to hear it)!');
            }
        });

        // Updates parameters from slider values
        function updateParameter(paramName, value) {
            params[paramName] = parseFloat(value);
            switch (paramName) {
                case 'tempo':
                    Tone.Transport.bpm.value = params.tempo;
                    document.getElementById('tempoValue').textContent = params.tempo;
                    break;
                case 'density':
                    document.getElementById('densityValue').textContent = params.density;
                    generateSequence(); // Re-generate sequence with new density
                    break;
                case 'octave':
                    document.getElementById('octaveValue').textContent = params.octave;
                    generateSequence(); // Re-generate sequence with new octave
                    break;
            }
        }
        
        // Simple message box to give user feedback
        function showMessage(text) {
            messageBox.textContent = text;
        }

        // Initial setup on page load
        window.onload = function() {
            showMessage('Click "Play" to start the audio context.');
            
            // Set up initial slider values
            document.getElementById('tempoSlider').value = params.tempo;
            document.getElementById('densitySlider').value = params.density;
            document.getElementById('octaveSlider').value = params.octave;
        };
    </script>
</body>
</html>
