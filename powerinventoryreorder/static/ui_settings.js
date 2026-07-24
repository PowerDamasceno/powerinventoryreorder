export function renderPluginSettings(target, data) {

    let rows = "";

    data.context.reorder_list.forEach(item => {

        rows += `
            <tr>
                <td>${item.ipn}</td>
                <td>${item.name}</td>
                <td>${item.stock}</td>
                <td>${item.threshold}</td>
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

            <h4>Top 50 Reorder Candidates</h4>

            <table style="width:100%; border-collapse:collapse;">
                <thead>
                    <tr>
                        <th style="text-align:left;">IPN</th>
                        <th style="text-align:left;">Name</th>
                        <th style="text-align:left;">Stock</th>
                        <th style="text-align:left;">Threshold</th>
                    </tr>
                </thead>

                <tbody>
                    ${rows}
                </tbody>
            </table>

        </div>
    `;
}
