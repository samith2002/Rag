document.getElementById("queryButton").addEventListener("click", async () => {
    const queryInput = document.getElementById("queryInput").value;
    const responseText = document.getElementById("responseText");

    responseText.innerText = "Loading...";

    try {
        const response = await fetch("/query", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: queryInput })
        });

        const data = await response.json();
        responseText.innerText = data.answer || "No response received";
    } catch (error) {
        responseText.innerText = "An error occurred. Please try again.";
    }
});
