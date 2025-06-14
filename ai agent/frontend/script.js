document.addEventListener("DOMContentLoaded", () => {
  console.log("Script.js loaded ✅");

  const form = document.getElementById("uploadForm");
  const fileInput = document.getElementById("fileInput");
  const output = document.getElementById("output");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const file = fileInput.files[0];
    if (!file) {
      output.innerHTML = `<span style="color:red;">Please select a file.</span>`;
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    output.textContent = "Uploading and processing...";

    try {
      const response = await fetch("/upload/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Failed to upload file");

      const data = await response.json();
      output.innerHTML = formatResult(data);
    } catch (err) {
      output.innerHTML = `<span style="color:red;">Error: ${err.message}</span>`;
    }
  });

  function formatResult(data) {
    let html = `
      <h5>File: ${data.filename}</h5>
      <p><strong>Format:</strong> ${data.format}</p>
      <p><strong>Intent:</strong> ${data.intent}</p>
      <p><strong>Action:</strong> ${data.action}</p>
    `;

    if (data.format === "pdf" && data.pdf_data) {
      html += `
        <p><strong>Extracted Text:</strong></p>
        <pre>${data.pdf_data.fields?.text || "None"}</pre>
        <p><strong>Compliance Flags:</strong> ${data.pdf_data.fields?.compliance_flags?.join(", ") || "None"}</p>
        <p><strong>Anomalies:</strong> ${data.pdf_data.anomalies?.join(", ") || "None"}</p>
      `;
    } else if (data.format === "email" && data.email_data) {
      html += `
        <p><strong>From:</strong> ${data.email_data.from}</p>
        <p><strong>To:</strong> ${data.email_data.to}</p>
        <p><strong>Subject:</strong> ${data.email_data.subject}</p>
        <p><strong>Body:</strong></p>
        <pre>${data.email_data.body}</pre>
      `;
    } else if (data.format === "json" && data.json_data) {
      html += `
        <p><strong>Validated JSON:</strong></p>
        <pre>${JSON.stringify(data.json_data, null, 2)}</pre>
      `;
    } else if (data.message) {
      html += `<p><strong>Message:</strong> ${data.message}</p>`;
    }

    return html;
  }
});
