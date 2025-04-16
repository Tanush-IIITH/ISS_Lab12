const baseURL = "http://localhost:8000";

async function loadItems(searchTerm = "") {
  try {
    const res = await fetch(`${baseURL}/items`);
    const data = await res.json();
    const list = document.getElementById("itemList");
    list.innerHTML = "";

    const filteredItems = data.filter(item =>
      item.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    document.getElementById("itemCount").textContent = `Total items: ${filteredItems.length}`;

    filteredItems.forEach(item => {
      const li = document.createElement("li");
      li.className = "item-card";
      
      const header = document.createElement("div");
      header.className = "item-header";
      header.innerHTML = `<strong>${item.name}</strong>`;
      
      const body = document.createElement("div");
      body.className = "item-body";
      body.textContent = item.description;
      
      const footer = document.createElement("div");
      footer.className = "item-footer";
      
      const del = document.createElement("button");
      del.textContent = "Delete";
      del.className = "delete-btn";
      del.onclick = () => deleteItem(item._id);
      
      footer.appendChild(del);
      li.appendChild(header);
      li.appendChild(body);
      li.appendChild(footer);
      list.appendChild(li);
    });
  } catch (error) {
    console.error("Error loading items:", error);
    document.getElementById("itemList").innerHTML = "<p>Error loading items. Please try again later.</p>";
  }
}

async function deleteItem(id) {
  try {
    await fetch(`${baseURL}/items/${id}`, { method: "DELETE" });
    loadItems(document.getElementById("search").value);
  } catch (error) {
    console.error("Error deleting item:", error);
    alert("Failed to delete item. Please try again.");
  }
}

document.getElementById("search").addEventListener("input", (e) => {
  loadItems(e.target.value); 
});

document.getElementById("itemForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const name = document.getElementById("name").value;
  const description = document.getElementById("description").value;
  
  try {
    await fetch(`${baseURL}/items`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, description })
    });
    e.target.reset();
    loadItems(document.getElementById("search").value);
  } catch (error) {
    console.error("Error adding item:", error);
    alert("Failed to add item. Please try again.");
  }
});

// Load items when the page loads
window.addEventListener("DOMContentLoaded", () => {
  loadItems();
});
