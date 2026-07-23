export function renderPluginSettings({ context }) {

    const root = document.createElement('div');

    root.innerHTML = `
        <div style="padding:20px">

            <h2>Power Inventory Reorder</h2>

            <hr>

            <p>
                <strong>Status:</strong>
                ${context.status}
            </p>

            <p>
                <strong>Parts with IPN:</strong>
                ${context.total_parts}
            </p>

            <p>
                <strong>Reorder candidates:</strong>
                ${context.reorder_parts}
            </p>

        </div>
    `;

    return root;
}
