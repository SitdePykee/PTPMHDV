hostname = window.location.hostname;

function fetchMaterials() {
    fetch("http://" + hostname + ":5000/api/material_management/material")
        .then(response => response.json())
        .then(data => {
            let list = document.getElementById("material-list");
            list.innerHTML = "";
            data.forEach(material => {
                let item = document.createElement("li");
                item.className = "excel-item";
                item.innerHTML = `<strong>📦 ${material.name}</strong><br>Số lượng: ${material.quantity} | Nhà cung cấp: ${material.supplier_id}`;
                list.appendChild(item);
            });
        })
        .catch(error => console.error("❌ Lỗi khi lấy dữ liệu:", error));
}

function addMaterial() {
    let name = document.getElementById("material_name").value;
    let quantity = document.getElementById("material_quantity").value;
    let supplier_id = document.getElementById("supplier_id").value;

    fetch("http://" + hostname + ":5000/api/material_management/material", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, quantity, supplier_id })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchMaterials();
    })
    .catch(error => console.error("❌ Lỗi khi thêm nguyên vật liệu:", error));
}

function fetchStockTransactions() {
    fetch("http://" + hostname + ":5000/api/material_management/stock_transaction")
        .then(response => response.json())
        .then(data => {
            let list = document.getElementById("stock-list");
            list.innerHTML = "";
            data.forEach(transaction => {
                let item = document.createElement("li");
                item.className = "item";
                item.innerHTML = `📦 Nguyên liệu ${transaction.material_id} - ${transaction.type} ${transaction.quantity} cái vào ngày ${transaction.date}`;
                list.appendChild(item);
            });
        })
        .catch(error => console.error("❌ Lỗi khi lấy dữ liệu giao dịch kho:", error));
}

function addStockTransaction() {
    let material_id = document.getElementById("transaction_material_id").value;
    let type = document.getElementById("transaction_type").value;
    let quantity = document.getElementById("transaction_quantity").value;
    let date = document.getElementById("transaction_date").value;

    fetch("http://" + hostname + ":5000/api/material_management/stock_transaction", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ material_id, type, quantity, date })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchStockTransactions();
    })
    .catch(error => console.error("❌ Lỗi khi thêm giao dịch kho:", error));
}

function readExcelData() {
    let filePath = document.getElementById("excel_path").value;

    fetch("http://" + hostname + ":5000/api/material_management/read_excel_data", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ file_path: filePath })
    })
    .then(response => response.json())
    .then(data => {
        let list = document.getElementById("excel-data");
        list.innerHTML = "";
        data.forEach(material => {
            let item = document.createElement("li");
            item.className = "item";
            item.innerHTML = `📄 ${material.name} - Số lượng: ${material.quantity} | Nhà cung cấp: ${material.supplier_id}`;
            list.appendChild(item);
        });
    })
    .catch(error => console.error("❌ Lỗi khi đọc file Excel:", error));
}

function requestExcelData() {
    let filePath = document.getElementById("excel_file_path").value.trim();
    let remoteServer = document.getElementById("remote_server").value.trim();

    if (!filePath) {
        alert("⚠ Vui lòng nhập đường dẫn file Excel trên máy chủ!");
        return;
    }

    let apiUrl = "http://" + hostname + ":5000/api/material_management/fetch_excel_data";

    fetch(apiUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ file_path: filePath, remote_server: remoteServer })
    })
    .then(response => response.json())
    .then(data => {
        let list = document.getElementById("excel-data");
        list.innerHTML = "";
        if (data.data) {
            data.data.forEach(material => {
                let item = document.createElement("li");
                item.className = "item";
                item.innerHTML = `📄 ${material.name} - Số lượng: ${material.quantity} | Nhà cung cấp: ${material.supplier_id}`;
                list.appendChild(item);
            });
            alert("✅ Dữ liệu đã được tải từ máy chủ DCOM!");
        } else {
            list.innerHTML = `<li class='item'>❌ ${data.error || "Không thể đọc dữ liệu từ file Excel"}</li>`;
        }
    })
    .catch(error => {
        console.error("❌ Lỗi khi yêu cầu dữ liệu từ API backend:", error);
        alert("❌ Lỗi khi lấy dữ liệu từ API backend! Kiểm tra console để biết thêm chi tiết.");
    });
}

