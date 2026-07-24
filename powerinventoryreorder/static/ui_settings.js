export function renderPluginSettings(target, data) {

    let rows = "";

    data.context.reorder_list.forEach(item => {

        let color = "white";

        if (item.stock === 0) {
            color = "#ffe5e5";
        }
        else if (item.missing >= 5) {
            color = "#fff4d6";
        }

        rows += `
        <tr style="background:${color}">
            <td>${item.ipn}</td>
            <td>${item.name}</td>
            <td>${item.stock}</td>
            <td>${item.threshold}</td>
            <td>${item.missing}</td>
            <td>${item.qty_to_order}</td>
        </tr>
        `;
    });

    target.innerHTML = `
    <div style="padding:20px">

        <h2>Power Inventory Reorder</h2>

        <p><b>Status:</b> ${data.context.status}</p>

        <hr>

        <p><b>Total Parts:</b> ${data.context.total_parts}</p>

        <p><b>Reorder Candidates:</b> ${data.context.reorder_parts}</p>

        <p><b>Stock Zero:</b> ${data.context.stock_zero}</p>

        <p><b>Critical:</b> ${data.context.critical}</p>

        <hr>

        <p>
            inventoryreorder/export/" target="_blank">
                Download CSV
            </a>
        </p>

        <hr>

        <h3>Reorder List</h3>

        <table style="width:100%; border-collapse:collapse;">

            <thead>
                <tr>
                    <th>IPN</th>
                    <th>Name</th>
                    <th>Stock</th>
                    <th>Threshold</th>
                    <th>Missing</th>
                    <th>Qty To Order</th>
                </tr>
            </thead>

            <tbody>
                ${rows}
            </tbody>

        </table>

    </div>
    `;
}
