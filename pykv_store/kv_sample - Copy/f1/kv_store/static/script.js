// Utility to show messages
function showResult(id, message, isError = false) {
    const el = document.getElementById(id);
    el.innerText = message;
    el.style.color = isError ? "#ff4b2b" : "#006aff";
}


// ---------------- PUT ----------------
async function putData() {
    console.log("PUT button clicked");   // 👈 ADD THIS

    const key = document.getElementById("putKey").value.trim();
    const value = document.getElementById("putValue").value.trim();
    const ttl = document.getElementById("putTTL")?.value.trim();

    if (!key || !value) {
        showResult("putResult", "Key and Value required!", true);
        return;
    }

    let url = `/put?key=${key}&value=${value}`;
    if (ttl) url += `&ttl=${ttl}`;

    console.log("Calling URL:", url);   // 👈 ADD THIS

    try {
        const response = await fetch(url, {
            method: "PUT"
        });

        console.log("Response status:", response.status);  // 👈 ADD

        const data = await response.json();
        console.log("Response data:", data);  // 👈 ADD

        if (response.ok) {
            showResult("putResult", "Saved Successfully!");
        } else {
            showResult("putResult", data.error, true);
        }

    } catch (error) {
        console.log(error);
        showResult("putResult", "Server Error!", true);
    }
}


// ---------------- GET ----------------
async function getData() {
    const key = document.getElementById("getKey").value.trim();

    if (!key) {
        showResult("getResult", "Key required!", true);
        return;
    }

    try {
        const response = await fetch(`/get?key=${key}`);
        const data = await response.json();

        if (response.ok) {
            showResult("getResult", `Value: ${data.value}`);
        } else {
            showResult("getResult", data.error, true);
        }

    } catch (error) {
        showResult("getResult", "Server Error!", true);
    }
}


async function updateData() {
    const key = document.getElementById("updateKey").value.trim();
    const value = document.getElementById("updateValue").value.trim();

    if (!key || !value) {
        showResult("updateResult", "Key and Value required!", true);
        return;
    }

    try {
        const response = await fetch(`/update?key=${key}&value=${value}`, {
            method: "PUT"
        });

        const data = await response.json();

        if (response.ok) {
            showResult("updateResult", "updated Successfully!");
        } else {
            showResult("updateResult", data.error, true);
        }

    } catch (error) {
        showResult("updateResult", "Server Error!", true);
    }
}


// ---------------- DELETE ----------------
async function deleteData() {
    const key = document.getElementById("deleteKey").value.trim();

    if (!key) {
        showResult("deleteResult", "Key required!", true);
        return;
    }

    try {
        const response = await fetch(`/delete?key=${key}`, {
            method: "DELETE"
        });

        const data = await response.json();

        if (response.ok) {
            showResult("deleteResult", data.message);
        } else {
            showResult("deleteResult", data.error, true);
        }

    } catch (error) {
        showResult("deleteResult", "Server Error!", true);
    }
}
async function getTTL() {
    const key = document.getElementById("ttlKey").value.trim();
    const ttlResult = document.getElementById("ttlResult");

    if (!key) {
        ttlResult.innerText = "Key required!";
        return;
    }

    try {
        const response = await fetch(`/ttl?key=${key}`);
        const data = await response.json();

        if (response.ok) {
            ttlResult.innerText =
                data.ttl_remaining
                ? `TTL Remaining: ${data.ttl_remaining} seconds`
                : data.message;
        } else {
            ttlResult.innerText = data.error;
        }
    } catch {
        ttlResult.innerText = "Server Error!";
    }
}

async function getKeys() {
    try {
        const response = await fetch(`/keys`);
        const data = await response.json();

        keysResult.innerText = JSON.stringify(data.keys, null, 2);
    } catch {
        keysResult.innerText = "Server Error!";
    }
}

async function getLogs() {
    try {
        const response = await fetch(`/logs`);
        const data = await response.json();

        logsResult.innerText = JSON.stringify(data.logs, null, 2);
    } catch {
        logsResult.innerText = "Server Error!";
    }
}