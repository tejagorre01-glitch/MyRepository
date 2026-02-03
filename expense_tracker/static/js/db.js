let db;

const request = indexedDB.open("ExpenseTrackerDB", 2);

request.onupgradeneeded = e => {
  db = e.target.result;

  if (!db.objectStoreNames.contains("expenses")) {
    db.createObjectStore("expenses", { keyPath: "id", autoIncrement: true });
  }

  if (!db.objectStoreNames.contains("monthly_expenses")) {
    db.createObjectStore("monthly_expenses", { keyPath: "id", autoIncrement: true });
  }
};

request.onsuccess = e => {
  db = e.target.result;
};
