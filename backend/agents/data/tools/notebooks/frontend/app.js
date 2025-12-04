// OBOS Frontend JavaScript
// This connects your frontend to the backend API on Replit

const API_BASE = "https://5629101d-c8d0-45c5-bdde-65e132223b2c-00-26z867wwgf554.worf.replit.dev/"; 
// Example: "https://obos-intelligence--michaeloscar747.replit.app"
// Replace this after you finish creating the backend public URL

// --- Handle Query Submission ---
async function sendQuery() {
  const query = document.getElementById("queryInput").value;
  const resultBox = document.getElementById("responseBox");

  if (!query.trim()) {
    resultBox.innerText = "Please type something first.";
    return;
  }

  resultBox.innerText = "Processing... ⏳";

  try {
    const response = await fetch(`${API_BASE}/reason`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: query })
    });

    const data = await response.json();
    resultBox.innerText = data.response || JSON.stringify(data);
  } 
  catch (error) {
    resultBox.innerText = "Error connecting to backend 🚫";
  }
}

// --- Handle File Upload ---
async function uploadFile() {
  const fileInput = document.getElementById("fileInput");
  const resultBox = document.getElementById("uploadResult");

  if (!fileInput.files.length) {
    resultBox.innerText = "Please select a PDF.";
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  resultBox.innerText = "Uploading PDF... ⏳";

  try {
    const response = await fetch(`${API_BASE}/upload`, {
      method: "POST",
      body: formData
    });

    const data = await response.json();
    resultBox.innerText = data.message || JSON.stringify(data);
  }
  catch (error) {
    resultBox.innerText = "Upload failed 🚫";
  }
}
