import { useEffect, useState } from "react";
import { logout } from "../util/auth";
import { useNavigate } from "react-router-dom";
import "../style/dashboard.css";

function AdminDashboard() {
    const [masterView, setMasterView] = useState("issue");
    const [issueView, setIssueView] = useState("active");
    const [bookView, setBookView] = useState("all");
    const [issues, setIssues] = useState([]);
    const [logs, setLogs] = useState([]);
    const [returned, setReturned] = useState([]);
    const [users, setUsers] = useState([]);
    const [books, setBooks] = useState([]);
    const [searchResults, setSearchResults] = useState([]);
    const [editingBook, setEditingBook] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        getActiveIssue();
    }, []);

    async function getActiveIssue() {
        try {
            const token = localStorage.getItem("token");
            const response = await fetch("http://localhost:8080/issue/active", {
                headers: { Authorization: `Bearer ${token}` },
            });
            const data = await response.json();
            setIssues(Array.isArray(data) ? data : []);
        } catch (error) {
            console.log(error);
        }
    }

    async function getLogs() {
        try {
            const token = localStorage.getItem("token");
            const response = await fetch("http://localhost:8080/issue/", {
                headers: { Authorization: `Bearer ${token}` },
            });
            const data = await response.json();
            setLogs(Array.isArray(data) ? data : []);
        } catch (error) {
            console.log(error);
        }
    }

    async function getReturnedIssue() {
        try {
            const token = localStorage.getItem("token");
            const response = await fetch("http://localhost:8080/issue/returned", {
                headers: { Authorization: `Bearer ${token}` },
            });
            const data = await response.json();
            setReturned(Array.isArray(data) ? data : []);
        } catch (error) {
            console.log(error);
        }
    }

    async function getUsers() {
        try {
            const token = localStorage.getItem("token");
            const response = await fetch("http://localhost:8080/users/", {
                headers: { Authorization: `Bearer ${token}` },
            });
            const data = await response.json();
            setUsers(Array.isArray(data) ? data : []);
        } catch (error) {
            console.log(error);
        }
    }

    async function deleteUser(email) {
        if (!window.confirm("Delete this user?")) return;
        try {
            const token = localStorage.getItem("token");
            await fetch(`http://localhost:8080/users/?email=${email}`, {
                method: "DELETE",
                headers: { Authorization: `Bearer ${token}` },
            });
            getUsers();
        } catch (error) {
            console.log(error);
        }
    }

    async function makeAdmin(email) {
        try {
            const token = localStorage.getItem("token");
            await fetch(`http://localhost:8080/users/${email}/role`, {
                method: "PUT",
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ role: "admin" }),
            });
            getUsers();
        } catch (error) {
            console.log(error);
        }
    }

    async function getBooks() {
        try {
            const response = await fetch("http://localhost:8080/books/");
            const data = await response.json();
            setBooks(Array.isArray(data) ? data : []);
        } catch (error) {
            console.log(error);
        }
    }

    async function createBook(name, author, isbn) {
        try {
            const token = localStorage.getItem("token");
            await fetch("http://localhost:8080/books/", {
                method: "POST",
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ name, author, isbn }),
            });
            getBooks();
            setBookView("all");
        } catch (error) {
            console.log(error);
        }
    }

    async function updateBook(id, name, author) {
        try {
            const token = localStorage.getItem("token");
            await fetch(`http://localhost:8080/books/${id}`, {
                method: "PATCH",
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ name, author }),
            });
            getBooks();
            setBookView("all");
            setEditingBook(null);
        } catch (error) {
            console.log(error);
        }
    }

    async function deleteBook(id) {
        if (!window.confirm("Delete this book?")) return;
        try {
            const token = localStorage.getItem("token");
            await fetch(`http://localhost:8080/books/${id}`, {
                method: "DELETE",
                headers: { Authorization: `Bearer ${token}` },
            });
            getBooks();
        } catch (error) {
            console.log(error);
        }
    }

    async function searchBook(query) {
        try {
            const response = await fetch(`http://localhost:8080/books/search?query=${encodeURIComponent(query)}`);
            const data = await response.json();
            setSearchResults(Array.isArray(data) ? data : []);
        } catch (error) {
            console.log(error);
        }
    }

    return (
        <div>
            <h1>Admin Dashboard</h1>
            <div className="top-controls">
                <button onClick={() => setMasterView("issue")}>Issues</button>
                <button onClick={() => { setMasterView("user"); getUsers(); }}>Users</button>
                <button onClick={() => { setMasterView("book"); getBooks(); }}>Books</button>
                <button onClick={() => logout(navigate)}>Logout</button>
            </div>

            {masterView === "issue" && (
                <>
                    <div className="top-controls">
                        <button onClick={() => { setIssueView("active"); getActiveIssue(); }}>Active</button>
                        <button onClick={() => { setIssueView("all"); getLogs(); }}>All Issues</button>
                        <button onClick={() => { setIssueView("returned"); getReturnedIssue(); }}>Returned</button>
                    </div>
                    <div className="grid-layout">
                        {(issueView === "active" ? issues : issueView === "all" ? logs : returned).map((issue) => (
                            <div key={issue.id} className="data-card">
                                <h3>Issue Date: {issue.issue_date}</h3>
                                {/* <p>Issue ID: {issue.id}</p> */}
                                <p>User: {issue.user}</p>
                                {/* <p>UserID: {issue.user_id}</p> */}
                                <p>Book: {issue.book_name}</p>
                                {/* <p>BookID: {issue.book_id}</p> */}
                                <p>Status: {issue.status}</p>
                            </div>
                        ))}
                    </div>
                </>
            )}

            {masterView === "user" && (
                <div className="grid-layout">
                    {users.map((user) => (
                        <div key={user.id} className="data-card">
                            <h3>{user.name}</h3>
                            <p>ID: {user.id}</p>
                            <p>Email: {user.email}</p>
                            <p>Role: {user.role}</p>
                            {user.role === "student" && (
                                <button className="primary-btn" onClick={() => makeAdmin(user.email)}>Make Admin</button>
                            )}
                            <button onClick={() => deleteUser(user.email)}>Delete</button>
                        </div>
                    ))}
                </div>
            )}

            {masterView === "book" && (
                <div>
                    <h2 style={{ textAlign: "center" }}>Manage Books</h2>
                    <div className="top-controls">
                        <button onClick={() => { setBookView("all"); setEditingBook(null); }}>All Books</button>
                        <button onClick={() => { setBookView("create"); setEditingBook(null); }}>Create Book</button>
                    </div>

                    {bookView === "all" && (
                        <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
                            <input type="text" placeholder="Search books..." onChange={(e) => searchBook(e.target.value)} />
                            <div className="grid-layout" style={{ width: "100%" }}>
                                {(searchResults.length > 0 ? searchResults : books).map((book) => (
                                    <div key={book.id} className="data-card">
                                        <h3>{book.name}</h3>
                                        <p>Author: {book.author}</p>
                                        <p>ISBN: {book.isbn}</p>
                                        <button 
                                            className="primary-btn" 
                                            onClick={() => {
                                                setEditingBook(book);
                                                setBookView("update");
                                            }}
                                        >
                                            Update
                                        </button>
                                        <button onClick={() => deleteBook(book.id)}>Delete</button>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {bookView === "create" && (
                        <form
                            className="form-panel"
                            onSubmit={(e) => {
                                e.preventDefault();
                                const formData = new FormData(e.target);
                                createBook(formData.get("name"), formData.get("author"), formData.get("isbn"));
                            }}
                        >
                            <h3>Add New Book</h3>
                            <input name="name" placeholder="Book Name" required />
                            <input name="author" placeholder="Author Name" required />
                            <input name="isbn" placeholder="ISBN" required />
                            <button className="primary-btn" type="submit" style={{ width: "100%" }}>Submit</button>
                        </form>
                    )}

                    {bookView === "update" && editingBook && (
                        <form
                            className="form-panel"
                            onSubmit={(e) => {
                                e.preventDefault();
                                const formData = new FormData(e.target);
                                updateBook(editingBook.id, formData.get("name"), formData.get("author"));
                            }}
                        >
                            <h3>Update Book</h3>
                            <input name="name" defaultValue={editingBook.name} placeholder="Book Name" required />
                            <input name="author" defaultValue={editingBook.author} placeholder="Author Name" required />
                            <input name="isbn" defaultValue={editingBook.isbn} disabled placeholder="ISBN (Cannot be changed)" />
                            <button className="primary-btn" type="submit" style={{ width: "100%" }}>Save Changes</button>
                            <button 
                                type="button" 
                                onClick={() => { setBookView("all"); setEditingBook(null); }} 
                                style={{ width: "100%", marginTop: "10px" }}
                            >
                                Cancel
                            </button>
                        </form>
                    )}
                </div>
            )}
        </div>
    );
}

export default AdminDashboard;