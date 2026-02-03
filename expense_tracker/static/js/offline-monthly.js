function saveMonthlyOffline(data) {
  data.synced = false;
  const tx = db.transaction("monthly_expenses", "readwrite");
  tx.objectStore("monthly_expenses").add(data);
}

function calculateMonthlyOffline() {
  const tx = db.transaction("monthly_expenses", "readonly");
  const store = tx.objectStore("monthly_expenses");

  store.getAll().onsuccess = e => {
    const data = e.target.result;
    const total = data.reduce((s, x) => s + Number(x.amount), 0);
    document.getElementById("monthlyTotal").innerText = total;
  };
}
