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

const addStockTransaction = () => {
    const materialId = document.getElementById("transaction_material_id").value;
    const transactionType = document.getElementById("transaction_type").value;
    const quantity = document.getElementById("transaction_quantity").value;
    const date = document.getElementById("transaction_date").value;
    let apiUrl = "http://" + hostname + ":5000/api/material_management/stock_transaction";
    fetch(apiUrl, {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            material_id: materialId,
            type: transactionType,
            quantity: quantity,
            date: date
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Lỗi từ server: ${response.statusText}`);
        }
        return response.json();  // Dữ liệu phải là JSON
    })
    .then(data => {
        alert('Giao dịch kho đã được ghi nhận');
        console.log(data);  // Xử lý kết quả
    })
    .catch(error => {
        console.error('Lỗi:', error);
        alert(`Có lỗi xảy ra: ${error.message}`);
    });
};



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
            data.data.forEach((material, index) => {
                let row = document.createElement("div");
                row.className = "excel-row";
                row.innerHTML = `
                    <input type="text" class="excel-input" value="${material.name}" data-index="${index}" data-field="name">
                    <input type="number" class="excel-input" value="${material.quantity}" data-index="${index}" data-field="quantity">
                    <input type="text" class="excel-input" value="${material.supplier_id}" data-index="${index}" data-field="supplier_id">
                `;
                list.appendChild(row);
            });

            // Hiển thị nút lưu dữ liệu
            document.getElementById("save-button").style.display = "block";

            alert("✅ Dữ liệu đã được tải từ máy chủ DCOM!");
        } else {
            list.innerHTML = `<div class="error-msg">❌ ${data.error || "Không thể đọc dữ liệu từ file Excel"}</div>`;
        }
    })
    .catch(error => {
        console.error("❌ Lỗi khi yêu cầu dữ liệu từ API backend:", error);
        alert("❌ Lỗi khi lấy dữ liệu từ API backend! Kiểm tra console để biết thêm chi tiết.");
    });
}

function saveExcelData() {
    let filePath = document.getElementById("excel_file_path").value.trim();
    let remoteServer = document.getElementById("remote_server").value.trim();
    let inputs = document.querySelectorAll(".excel-input");

    let updatedData = [];

    inputs.forEach(input => {
        let index = input.getAttribute("data-index");
        let field = input.getAttribute("data-field");
        let materialId = input.getAttribute("data-id");

        if (!updatedData[index]) {
            updatedData[index] = { id: materialId };
        }
        updatedData[index][field] = input.value;
    });

    console.log("📌 Data gửi lên server:", updatedData); // Debug dữ liệu trước khi gửi

    let apiUrl = "http://" + hostname + ":5000/api/material_management/update_excel_data";

    fetch(apiUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ file_path: filePath, remote_server: remoteServer, updated_data: updatedData })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("✅ Dữ liệu Excel đã được cập nhật thành công!");
        } else {
            alert("❌ Lỗi khi cập nhật dữ liệu: " + data.error);
        }
    })
    .catch(error => {
        console.error("❌ Lỗi khi cập nhật dữ liệu:", error);
        alert("❌ Lỗi khi cập nhật dữ liệu! Kiểm tra console để biết thêm chi tiết.");
    });
}

function fetchStockTransactions() {
    let apiUrl = "http://" + hostname + ":5000/api/material_management/stock_transaction";

    fetch(apiUrl, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        const stockList = document.getElementById('stock-list');
        stockList.innerHTML = '';  // Clear the list before rendering

        data.forEach(transaction => {
            const li = document.createElement('li');
            li.textContent = `Nguyên vật liệu ID: ${transaction.material_id}, Loại: ${transaction.type}, Số lượng: ${transaction.quantity}, Ngày: ${transaction.date}`;
            stockList.appendChild(li);
        });
    })
    .catch(error => {
        alert("Lỗi: " + error);
    });
}
