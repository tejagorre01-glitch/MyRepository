function saveExpenseOffline(data) {
  data.synced = false;
  const tx = db.transaction("expenses", "readwrite");
  tx.objectStore("expenses").add(data);
}

function calculateOfflineExpenses() {
  const tx = db.transaction("expenses", "readonly");
  const store = tx.objectStore("expenses");
  store.getAll().onsuccess = e => {
    const expenses = e.target.result;
    const total = expenses.reduce((s, x) => s + Number(x.amount), 0);
    document.getElementById("total").innerText = total;
  };
}
function submitExpenseForm() {
    const data = {
        name: document.getElementById("name").value,
        amount: document.getElementById("amount").value,
        category: document.getElementById("category").value,
        date: document.getElementById("date").value,
        member_id: document.getElementById("member_id").value,
        payee: document.getElementById("payee").value,
        description: document.getElementById("description").value,
        mode_of_payment: document.getElementById("mode_of_payment").value
    };

    if (!navigator.onLine) {
        saveExpenseOffline(data);      // 👈 HERE
        alert("Saved offline ✔");
        calculateOfflineExpenses();
    } else {
        document.getElementById("expenseForm").submit();
    }
}
