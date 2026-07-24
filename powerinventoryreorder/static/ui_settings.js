export function renderPluginSettings(target, data) {

    console.log("PowerInventoryReorder", data);

    target.innerHTML = `
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
    `;
}
