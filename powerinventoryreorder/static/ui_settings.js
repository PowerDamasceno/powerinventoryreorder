export function renderPluginSettings(target, data) {

    let rows = "";

    data.context.reorder_list.forEach(item => {

        const color =
            item.missing >= 10 ? "#ffe5e5" :
            item.missing >= 5 ? "#fff4d6" :
            "white";

        rows += `
            <tr style="background:${color}">
                <td>${item.ipn}</td>
                <td>${item.name}</td>
                <td>${item.stock}</td>
                <td>${item.threshold}</td>
                <td>${item.missing}</td>
            </tr>
        `;
    });

    target.innerHTML = `
        <div style="padding:20px">

            <h3>Power Inventory Reorder</h3>

            <p>
                <strong>Status:</strong>
                ${data.context.status}
            </p>

            <p>
                <strong>Parts with IPN:</strong>
                ${data.context.total_parts}
            </p>

            <p>
                <strong>Reorder candidates:</strong>
                ${data.context.reorder_parts}
            </p>

            <hr>

            <h4>Top 100 Reorder Candidates</h4>

            <table style="width:100%; border-collapse:collapse;">
                <thead>
                    <tr>
                        <th>IPN</th>
                        <th>Name</th>
                        <th>Stock</th>
                        <th>Threshold</th>
                        <th>Missing Qty</th>
                    </tr>
                </thead>

                <tbody>
                    ${rows}
                </tbody>
            </table>

        </div>
    `;
}
