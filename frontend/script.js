const API_BASE = "http://127.0.0.1:8000";

// =========================
// SINGLE FILE VERIFICATION
// =========================
async function verifySingle() {
    const fileInput = document.getElementById("singleFile");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file first.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    showLoading("singleResult");

    try {
        const res = await fetch(`${API_BASE}/verify`, {
            method: "POST",
            body: formData
        });

        const data = await res.json();
        renderSingleResult(data);

    } catch (err) {
        console.error(err);
        document.getElementById("singleResult").innerHTML =
            "<p class='fail'>Error processing file</p>";
    }
}

// =========================
// BATCH VERIFICATION
// =========================
async function verifyBatch() {
    const fileInput = document.getElementById("batchFile");
    const files = fileInput.files;

    if (!files.length) {
        alert("Please select files first.");
        return;
    }

    const formData = new FormData();

    for (let file of files) {
        formData.append("files", file);
    }

    showLoading("batchResult");

    try {
        const res = await fetch(`${API_BASE}/verify/batch`, {
            method: "POST",
            body: formData
        });

        const data = await res.json();
        renderBatchResult(data);

    } catch (err) {
        console.error(err);
        document.getElementById("batchResult").innerHTML =
            "<p class='fail'>Batch processing failed</p>";
    }
}

// =========================
// LOADING STATE
// =========================
function showLoading(id) {
    document.getElementById(id).innerHTML =
        "<p>Processing...</p>";
}

// =========================
// SINGLE RESULT RENDER
// =========================
function renderSingleResult(data) {
    const el = document.getElementById("singleResult");

    if (!data || data.status !== "success") {
        el.innerHTML = "<p class='fail'>Error processing file</p>";
        return;
    }

    const result = data.data.validation;
    const status = result.is_valid ? "PASS" : "FAIL";

    el.innerHTML = `
        <h3 class="${status.toLowerCase()}">
            Result: ${status}
        </h3>

        <p><strong>Confidence:</strong> ${result.confidence}</p>

        <p><strong>Extracted Text:</strong></p>
        <pre>${data.data.extracted_text}</pre>

        <p><strong>Issues:</strong></p>
        <ul>
            ${result.issues.length > 0
                ? result.issues.map(i => `<li>${i}</li>`).join("")
                : "<li>No issues found</li>"
            }
        </ul>
    `;
}

// =========================
// BATCH RESULT RENDER
// =========================
function renderBatchResult(data) {
    const el = document.getElementById("batchResult");

    if (!data || !data.results) {
        el.innerHTML = "<p class='fail'>Invalid batch response</p>";
        return;
    }

    let passCount = 0;
    let failCount = 0;

    data.results.forEach(item => {
        if (item.status === "success") {
            if (item.data.validation.is_valid) passCount++;
            else failCount++;
        } else {
            failCount++;
        }
    });

    el.innerHTML = `
        <h3>Batch Results</h3>

        <div class="summary">
            <p><strong>Total:</strong> ${data.total_files}</p>
            <p class="pass"><strong>PASS:</strong> ${passCount}</p>
            <p class="fail"><strong>FAIL:</strong> ${failCount}</p>
        </div>

        <div class="results-grid">
            ${data.results.map(item => {

                if (item.status === "failed") {
                    return `
                        <div class="card fail">
                            <h4>${item.filename}</h4>
                            <p class="fail">FAIL</p>
                            <p>${item.error || "Error processing file"}</p>
                        </div>
                    `;
                }

                const result = item.data.validation;
                const status = result.is_valid ? "PASS" : "FAIL";

                return `
                    <div class="card ${status.toLowerCase()}">
                        <h4>${item.filename}</h4>
                        <p class="${status.toLowerCase()}">${status}</p>
                        <p>Confidence: ${result.confidence}</p>
                    </div>
                `;
            }).join("")}
        </div>
    `;
}