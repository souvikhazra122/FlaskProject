function addEmployee() {
    let name = document.getElementById("name").value;
    let salary = document.getElementById("salary").value;

    if (!name || !salary) {
        alert("Please enter both Name and Salary.");
        return;
    }

    fetch("/add_employee", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: name, salary: salary })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || data.error);
        fetchEmployees();
    });
}

function fetchEmployees() {
    fetch("/get_employees")
    .then(response => response.json())
    .then(data => {
        let tableBody = document.getElementById("employeeTable");
        tableBody.innerHTML = "";
        data.forEach(emp => {
            tableBody.innerHTML += `
                <tr>
                    <td>${emp.id}</td>
                    <td>${emp.employee_name}</td>
                    <td>${emp.salary}</td>
                    <td>
                        <button class="btn yellow" onclick="editEmployee(${emp.id}, '${emp.employee_name}', ${emp.salary})">Edit</button>
                        <button class="btn red" onclick="deleteEmployee(${emp.id})">Delete</button>
                    </td>
                </tr>`;
        });
    });
}

function editEmployee(id, name, salary) {
    let newName = prompt("Enter new name", name);
    let newSalary = prompt("Enter new salary", salary);
    if (newName && newSalary) {
        fetch("/update_employee", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: id, name: newName, salary: newSalary })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
            fetchEmployees();
        });
    }
}

function deleteEmployee(id) {
    if (confirm("Are you sure you want to delete this employee?")) {
        fetch("/delete_employee", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id: id })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || data.error);
            fetchEmployees();
        });
    }
}
