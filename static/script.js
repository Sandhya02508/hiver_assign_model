async function processSupportQuery() {
    const message = document.getElementById("queryInput").value;
    if (!message.trim()) {
        alert("Please enter a customer support message.");
        return;
    }

    try {
        const response = await fetch("/v1/support", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });
        const data = await response.json();

        document.getElementById("resIntent").textContent = data.predicted_intent;
        document.getElementById("resConf").textContent = (data.intent_confidence * 100).toFixed(1) + "%";
        document.getElementById("confidenceBar").style.width = Math.round(data.intent_confidence * 100) + "%";

        const escBadge = document.getElementById("resEscalation");
        escBadge.textContent = data.escalate ? "ESCALATE" : "AUTO";
        escBadge.className = "decision-badge " + (data.escalate ? "escalate" : "auto");

        document.getElementById("resReason").textContent = data.escalation_reason;
        document.getElementById("resReply").textContent = data.reply;

        let evidenceHtml = "";
        data.retrieved_evidence.forEach((ev, idx) => {
            evidenceHtml += `<div class="evidence-card"><span class="evidence-intent">#${idx + 1} ${ev.intent}</span><span class="evidence-score">${(ev.similarity_score * 100).toFixed(1)}%</span></div>`;
        });
        document.getElementById("resEvidence").innerHTML = evidenceHtml;

    } catch (err) {
        alert("Error processing query: " + err);
    }
}

async function runEvaluation() {
    try {
        const response = await fetch("/v1/evaluate", { method: "POST" });
        const data = await response.json();

        const prop = data.proposed_system.intent_classification;
        const esc = data.proposed_system.escalation_metrics;

        document.getElementById("metricAccuracy").textContent = (prop.accuracy * 100).toFixed(1) + "%";
        document.getElementById("metricMacroF1").textContent = prop.macro_f1.toFixed(3);
        document.getElementById("metricEscAccuracy").textContent = (esc.accuracy * 100).toFixed(1) + "%";
        document.getElementById("metricFnRate").textContent = (esc.dangerous_false_negative_rate * 100).toFixed(1) + "%";

        document.getElementById("evalJsonOutput").textContent = JSON.stringify(data, null, 2);
    } catch (err) {
        document.getElementById("evalJsonOutput").textContent = "Error running evaluation: " + err;
    }
}

document.getElementById("processButton")?.addEventListener("click", processSupportQuery);
document.getElementById("evaluateButton")?.addEventListener("click", runEvaluation);
document.getElementById("clearButton")?.addEventListener("click", function () {
    document.getElementById("queryInput").value = "";
});
document.getElementById("sampleButton")?.addEventListener("click", function () {
    document.getElementById("queryInput").value = "My card was charged for a trip I never took.";
});
