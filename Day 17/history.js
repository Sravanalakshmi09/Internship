// ==========================
// Load History
// ==========================

window.onload = loadHistory;

async function loadHistory() {

    try {

        const response = await fetch("/api/history");

        const result = await response.json();

        const tbody = document.getElementById("historyBody");

        tbody.innerHTML = "";

        if (!result.success) {

            tbody.innerHTML =
                "<tr><td colspan='6'>No history found.</td></tr>";

            return;

        }

        result.history.forEach(item => {

            let color =
                item.prediction === "Normal"
                ? "#22c55e"
                : "#ef4444";

            tbody.innerHTML += `

            <tr>

                <td>${item.id}</td>

                <td>${item.device_id}</td>

                <td style="color:${color};font-weight:bold;">

                    ${item.prediction}

                </td>

                <td>${item.confidence}%</td>

                <td>${item.created_at}</td>

                <td>

                    <button
                        onclick="deleteRecord(${item.id})"
                        style="
                            background:#dc2626;
                            color:white;
                            border:none;
                            padding:8px 12px;
                            border-radius:8px;
                            cursor:pointer;
                        ">

                        Delete

                    </button>

                </td>

            </tr>

            `;

        });

    }

    catch(error){

        console.log(error);

    }

}

// ==========================
// Delete One Record
// ==========================

async function deleteRecord(id){

    if(!confirm("Delete this prediction?")) return;

    await fetch(`/api/history/delete/${id}`,{

        method:"DELETE"

    });

    loadHistory();

}

// ==========================
// Delete All
// ==========================

async function deleteAllHistory(){

    if(!confirm("Delete all history?")) return;

    await fetch("/api/history/delete-all",{

        method:"DELETE"

    });

    loadHistory();

}

// ==========================
// Search
// ==========================

document.getElementById("search").addEventListener("keyup",function(){

    let value=this.value.toLowerCase();

    let rows=document.querySelectorAll("#historyBody tr");

    rows.forEach(row=>{

        let text=row.innerText.toLowerCase();

        row.style.display=text.includes(value)?"":"none";

    });

});

// ==========================
// Export CSV
// ==========================

function exportCSV(){

    let csv=[];

    let rows=document.querySelectorAll("table tr");

    rows.forEach(row=>{

        let cols=row.querySelectorAll("td,th");

        let data=[];

        cols.forEach(col=>{

            data.push(col.innerText);

        });

        csv.push(data.join(","));

    });

    let csvFile=new Blob([csv.join("\n")],{

        type:"text/csv"

    });

    let downloadLink=document.createElement("a");

    downloadLink.download="Prediction_History.csv";

    downloadLink.href=window.URL.createObjectURL(csvFile);

    downloadLink.click();

}