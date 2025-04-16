const baseURL = "http://localhost:8000";

/**
 * Renders the user list in the UI
 * @param {Array} users - List of user objects
 */
function renderUsers(users) {
  const list = document.getElementById("userList");
  list.innerHTML = "";
  
  document.getElementById("userCount").textContent = `Total users: ${users.length}`;
  
  users.forEach(user => {
    const li = document.createElement("li");
    li.textContent = `${user.username}: ${user.bio}`;

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete";
    deleteBtn.onclick = async () => {
      try {
        const response = await fetch(`${baseURL}/users/${user._id}`, { method: "DELETE" });
        if (!response.ok) {
          throw new Error(`Failed to delete user: ${response.status}`);
        }
        loadUsers();
      } catch (error) {
        console.error("Error deleting user:", error);
      }
    };

    li.appendChild(deleteBtn);
    list.appendChild(li);
  });
}

/**
 * Fetches users from the API and updates the UI
 */
async function loadUsers() {
  try {
    const response = await fetch(`${baseURL}/users`);
    if (!response.ok) {
      throw new Error(`Failed to fetch users: ${response.status}`);
    }
    const users = await response.json();
    renderUsers(users);
  } catch (error) {
    console.error("Error loading users:", error);
    document.getElementById("userCount").textContent = "Failed to load users";
  }
}

/**
 * Filter users based on search term
 */
async function searchUsers(searchTerm) {
  try {
    const response = await fetch(`${baseURL}/users`);
    if (!response.ok) {
      throw new Error(`Failed to fetch users: ${response.status}`);
    }
    const users = await response.json();
    
    const filteredUsers = users.filter(user => 
      user.username.toLowerCase().includes(searchTerm.toLowerCase())
    );
    
    renderUsers(filteredUsers);
  } catch (error) {
    console.error("Error searching users:", error);
    document.getElementById("userCount").textContent = "Failed to search users";
  }
}

/**
 * Add a new user
 */
async function addUser(username, bio) {
  try {
    const response = await fetch(`${baseURL}/users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, bio })
    });
    
    if (!response.ok) {
      throw new Error(`Failed to add user: ${response.status}`);
    }
    
    loadUsers();
  } catch (error) {
    console.error("Error adding user:", error);
  }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
  // Load users when page loads
  loadUsers();
  
  // Set up search functionality
  document.getElementById("search").addEventListener("input", (e) => {
    searchUsers(e.target.value);
  });
  
  // Set up form submission
  document.getElementById("userForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = document.getElementById("username").value;
    const bio = document.getElementById("bio").value;
    
    await addUser(username, bio);
    e.target.reset();
  });
});