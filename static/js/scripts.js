// Upload Data
document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('file-upload');
    const file = fileInput.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload_train_data', {
            method: 'POST',
            body: formData,
        });
        const data = await response.json();
        document.getElementById('upload-result').textContent = `Uploaded: ${data.message} (Train: ${data.train_records}, Test: ${data.test_records})`;
    } catch (error) {
        document.getElementById('upload-result').textContent = `Error: ${error.message || 'Upload failed'}`;
    }
});

// Prediction Form
const features = [
    { name: 'School', type: 'text', placeholder: 'e.g., MS' },
    { name: 'Mother_Education', type: 'number', placeholder: '0-4 (0=none, 4=higher)' },
    { name: 'Father_Education', type: 'number', placeholder: '0-4 (0=none, 4=higher)' },
    { name: 'Final_Grade', type: 'number', placeholder: '0-20' },
    { name: 'Grade_1', type: 'number', placeholder: '0-20' },
    { name: 'Grade_2', type: 'number', placeholder: '0-20' },
    { name: 'Number_of_Failures', type: 'number', placeholder: '0-4' },
    { name: 'Wants_Higher_Education', type: 'text', placeholder: 'yes/no' },
    { name: 'Study_Time', type: 'number', placeholder: '1-4 (1=<2h, 4=>10h)' },
    { name: 'Weekend_Alcohol_Consumption', type: 'number', placeholder: '1-5 (1=low, 5=high)' },
    { name: 'Weekday_Alcohol_Consumption', type: 'number', placeholder: '1-5 (1=low, 5=high)' },
    { name: 'Address', type: 'text', placeholder: 'U=urban, R=rural' },
    { name: 'Reason_for_Choosing_School', type: 'text', placeholder: 'e.g., course' },
];

const predictionForm = document.getElementById('prediction-form');
features.forEach(feature => {
    const div = document.createElement('div');
    div.innerHTML = `
        <label>${feature.name.replace('_', ' ')}</label>
        <input type="${feature.type}" name="${feature.name}" placeholder="${feature.placeholder}" required>
    `;
    predictionForm.appendChild(div);
});

document.getElementById('predict-button').addEventListener('click', async () => {
    const formData = new FormData(predictionForm);
    const data = Object.fromEntries(formData.entries());

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams(data).toString(),
        });
        const result = await response.json();
        document.getElementById('prediction-result').textContent = `Prediction: ${result.prediction === 1 ? 'Will drop out' : 'Will not drop out'}`;
    } catch (error) {
        document.getElementById('prediction-result').textContent = `Error: ${error.message || 'Prediction failed'}`;
    }
});

// Visualize Features
document.getElementById('visualization-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const featureName = document.getElementById('feature-name').value;
    const imgElement = document.getElementById('visualization-image');
    const textElement = document.getElementById('visualization-text');

    try {
        const response = await fetch(`/visualize/${featureName}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();

        // Set the image source and make it visible
        imgElement.src = `data:image/png;base64,${data.image}`;
        imgElement.classList.add('visible');
        imgElement.style.display = 'block'; // Ensure it’s visible
        textElement.textContent = data.interpretation;
    } catch (error) {
        imgElement.style.display = 'none'; // Hide image on error
        textElement.textContent = `Error: ${error.message || 'Failed to load visualization'}`;
    }
});

// Retrain Model
document.getElementById('retrain-button').addEventListener('click', async () => {
    try {
        const response = await fetch('/retrain', { method: 'POST' });
        const data = await response.json();
        document.getElementById('retrain-result').textContent = data.message;
    } catch (error) {
        document.getElementById('retrain-result').textContent = `Error: ${error.message || 'Retraining failed'}`;
    }
});

// Evaluate Model
document.getElementById('evaluate-button').addEventListener('click', async () => {
    const evalResult = document.getElementById('evaluate-result');
    const classReportDiv = document.getElementById('classification-report');
    const confusionDiv = document.getElementById('confusion-matrix');
    const predSummaryDiv = document.getElementById('prediction-summary');

    try {
        const response = await fetch('/evaluate', { method: 'POST' });
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const data = await response.json();

        // Classification Report
        const report = data.classification_report;
        classReportDiv.innerHTML = `
            <h3>Classification Report</h3>
            <table>
                <thead>
                    <tr>
                        <th>Class</th>
                        <th>Precision</th>
                        <th>Recall</th>
                        <th>F1-Score</th>
                        <th>Support</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>False</td>
                        <td>${report.False.precision.toFixed(2)}</td>
                        <td>${report.False.recall.toFixed(2)}</td>
                        <td>${report.False['f1-score'].toFixed(2)}</td>
                        <td>${report.False.support}</td>
                    </tr>
                    <tr>
                        <td>True</td>
                        <td>${report.True.precision.toFixed(2)}</td>
                        <td>${report.True.recall.toFixed(2)}</td>
                        <td>${report.True['f1-score'].toFixed(2)}</td>
                        <td>${report.True.support}</td>
                    </tr>
                    <tr>
                        <td>Accuracy</td>
                        <td colspan="3">${report.accuracy.toFixed(2)}</td>
                        <td>${report['macro avg'].support}</td>
                    </tr>
                    <tr>
                        <td>Macro Avg</td>
                        <td>${report['macro avg'].precision.toFixed(2)}</td>
                        <td>${report['macro avg'].recall.toFixed(2)}</td>
                        <td>${report['macro avg']['f1-score'].toFixed(2)}</td>
                        <td>${report['macro avg'].support}</td>
                    </tr>
                    <tr>
                        <td>Weighted Avg</td>
                        <td>${report['weighted avg'].precision.toFixed(2)}</td>
                        <td>${report['weighted avg'].recall.toFixed(2)}</td>
                        <td>${report['weighted avg']['f1-score'].toFixed(2)}</td>
                        <td>${report['weighted avg'].support}</td>
                    </tr>
                </tbody>
            </table>
        `;

        // Confusion Matrix
        const cm = data.confusion_matrix;
        confusionDiv.innerHTML = `
            <h3>Confusion Matrix</h3>
            <div class="confusion-matrix">
                <div class="confusion-cell">${cm[0][0]}</div>
                <div class="confusion-cell">${cm[0][1]}</div>
                <div class="confusion-cell">${cm[1][0]}</div>
                <div class="confusion-cell">${cm[1][1]}</div>
            </div>
            <p style="text-align: center; margin-top: 10px;">[True Neg, False Pos] [False Neg, True Pos]</p>
        `;

        // Prediction Summary
        const yPred = data.y_pred;
        const yTest = data.y_test.map(v => v ? 1 : 0); // Convert booleans to 0/1
        const correct = yPred.filter((pred, i) => pred === yTest[i]).length;
        const total = yPred.length;
        predSummaryDiv.innerHTML = `
            <h3>Prediction Summary</h3>
            <p>Total Predictions: ${total}</p>
            <p>Correct Predictions: ${correct}</p>
            <p>Accuracy: ${(correct / total * 100).toFixed(2)}%</p>
        `;

    } catch (error) {
        evalResult.innerHTML = `<p class="error">Error: ${error.message || 'Evaluation failed'}</p>`;
    }
});