document.addEventListener("DOMContentLoaded", () => {
    const dropZone = document.getElementById("dropZone");
    const fileInput = document.getElementById("fileInput");
    const selectedFile = document.getElementById("selectedFile");
    const fileName = document.getElementById("fileName");
    const removeFileBtn = document.getElementById("removeFile");
    const summarizeBtn = document.getElementById("summarizeBtn");
    const loadingState = document.getElementById("loadingState");
    const loadingStatus = document.getElementById("loadingStatus");
    const progressBar = document.getElementById("progressBar");
    const resultsSection = document.getElementById("resultsSection");
    
    // Results Elements
    const keyPointsList = document.getElementById("keyPointsList");
    const summaryText = document.getElementById("summaryText");
    const transcriptText = document.getElementById("transcriptText");

    let currentFile = null;

    // File Drag and Drop logic
    dropZone.addEventListener("click", () => fileInput.click());

    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.classList.add("dragover");
    });

    dropZone.addEventListener("dragleave", () => {
        dropZone.classList.remove("dragover");
    });

    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.classList.remove("dragover");
        if (e.dataTransfer.files.length) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener("change", (e) => {
        if (e.target.files.length) {
            handleFileSelect(e.target.files[0]);
        }
    });

    function handleFileSelect(file) {
        if (!file.name.match(/\.(wav|mp3)$/i)) {
            alert("Please select a .wav or .mp3 file.");
            return;
        }
        currentFile = file;
        fileName.textContent = file.name;
        dropZone.style.display = "none";
        selectedFile.style.display = "flex";
        summarizeBtn.disabled = false;
        
        // Hide results if showing a previous run
        resultsSection.style.display = "none";
    }

    removeFileBtn.addEventListener("click", () => {
        currentFile = null;
        fileInput.value = "";
        dropZone.style.display = "flex";
        selectedFile.style.display = "none";
        summarizeBtn.disabled = true;
    });

    // API Interaction
    summarizeBtn.addEventListener("click", async () => {
        if (!currentFile) return;

        // UI Transition to Loading state
        summarizeBtn.style.display = "none";
        loadingState.style.display = "block";
        loadingStatus.textContent = "Uploading audio... (~1-3 seconds)";
        progressBar.style.width = "20%";
        resultsSection.style.display = "none";

        const formData = new FormData();
        formData.append("file", currentFile);

        try {
            // Fake progression for user experience while we await the backend
            let transcriptionTimeout = setTimeout(() => { 
                loadingStatus.textContent = "Transcribing voice to text... (This can take a moment)"; 
                progressBar.style.width = "50%"; 
            }, 3000);
            
            let summaryTimeout = setTimeout(() => { 
                loadingStatus.textContent = "Running AI NLP text summarization... (Heavy lifting)"; 
                progressBar.style.width = "85%"; 
            }, 8000);

            // Using the local python FastAPI server
            const response = await fetch("http://127.0.0.1:8000/api/summarize", {
                method: "POST",
                body: formData,
            });

            clearTimeout(transcriptionTimeout);
            clearTimeout(summaryTimeout);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || "Server error occurred");
            }

            const data = await response.json();

            // Populate the DOM
            populateResults(data);
            
            progressBar.style.width = "100%";
            loadingStatus.textContent = "Complete!";
            
            // Show results
            setTimeout(() => {
                loadingState.style.display = "none";
                summarizeBtn.style.display = "flex";
                resultsSection.style.display = "flex";
            }, 800);

        } catch (error) {
            console.error("Error:", error);
            alert("Failed to process audio:\n" + error.message);
            loadingState.style.display = "none";
            summarizeBtn.style.display = "flex";
        }
    });

    function populateResults(data) {
        // Transcript
        transcriptText.textContent = data.transcript || "No transcript returned.";

        // General Summary
        summaryText.textContent = data.summary || "No summary was generated.";

        // Key Points
        keyPointsList.innerHTML = "";
        if (data.key_points && data.key_points.length > 0) {
            data.key_points.forEach(point => {
                if(point && point.trim()) {
                    const li = document.createElement("li");
                    const txt = point.trim();
                    li.textContent = txt + (txt.endsWith('.') ? '' : '.');
                    keyPointsList.appendChild(li);
                }
            });
        }
        
        // Edge case fallback
        if (keyPointsList.children.length === 0) {
            const li = document.createElement("li");
            li.textContent = "No distinct key points could be identified.";
            keyPointsList.appendChild(li);
        }
    }

    // Tabs Navigation Logic
    const tabBtns = document.querySelectorAll(".tab-btn");
    const tabContents = document.querySelectorAll(".tab-content");

    tabBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            // Remove active state
            tabBtns.forEach(b => b.classList.remove("active"));
            tabContents.forEach(c => c.classList.remove("active"));

            // Add active state to clicked tab
            btn.classList.add("active");
            document.getElementById(btn.dataset.target).classList.add("active");
        });
    });
});
