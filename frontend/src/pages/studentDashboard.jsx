import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../style/dashboard.css";
import { logout } from "../util/auth.js";

function StudentDashboard() {
    const [Activeview, setActiveview] = useState("");
    const [books, setBooks] = useState([]);
    const [myissue, setmyIssue] = useState([]);
    const [updateName, setUpdateName] = useState("");
    const [student_name, setStudentName] = useState(localStorage.getItem("name") || "");
    const [searchBook, setSearchBook] = useState("");
    const [searchResults, setSearchResults] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        getAllBooks();
        setActiveview("All");
    }, []);

    async function getAllBooks() {
        try {
            const token = localStorage.getItem("token");
            const response = await fetch("http://localhost:8080/books/", {
                method: "GET",
                headers: { Authorization: `Bearer ${token}` }
            });
            const data = await response.json();
            setBooks(data);
        } catch (error) {
            console.log(error);
        }
    }

    async function IssueBook(book_id) {
        try {
            const token = localStorage.getItem("token");
            await fetch("http://localhost:8080/issue/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({ book_id: book_id })
            });
        } catch (error) {
            console.log(error);
        }
    }

    async function returnBook(issue_id) {
        try {
            const token = localStorage.getItem("token");
            await fetch(`http://localhost:8080/issue/${issue_id}/return`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                }
            });
            await Get_all_my_issue();
        } catch (error) {
            console.log(error);
        }
    }

    async function Get_all_my_issue() {
        try {
            const token = localStorage.getItem("token");
            const response = await fetch("http://localhost:8080/issue/me", {
                method: "GET",
                headers: { Authorization: `Bearer ${token}` }
            });
            const data = await response.json();
            setmyIssue(Array.isArray(data) ? data : []);
        } catch (error) {
            console.log(error);
        }
    }

    async function update_profile(updateName) {
        try {
            const token = localStorage.getItem("token");
            const email = localStorage.getItem("email");
            const response = await fetch(`http://localhost:8080/users/?email=${email}`, {
                method: "PATCH",
                headers: {
                    Authorization: `Bearer ${token}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ name: updateName })
            });
            const data = await response.json();
            if (response.ok) {
                localStorage.setItem("name", updateName);
                setStudentName(updateName);
                alert("Updated");
            } else {
                alert(data.error);
            }
        } catch (error) {
            console.log(error);
        }
    }

    async function search_book(query) {
        try {
            const response = await fetch(`http://localhost:8080/books/search?query=${query}`);
            const data = await response.json();
            setSearchResults(Array.isArray(data) ? data : []);
        } catch (error) {
            console.log(error);
        }
    }

    return (
        <div>
            <h1>Hello, {student_name}</h1>
            <div className="top-controls">
                <button onClick={() => { setActiveview("MyIssue"); Get_all_my_issue(); }}>My Issues</button>
                <button onClick={() => { setActiveview("All"); getAllBooks(); }}>All Books</button>
                <button onClick={() => setActiveview("update")}>Update Profile</button>
                <button onClick={() => logout(navigate)}>Logout</button>
            </div>

            <div className="top-controls">
                <input 
                    type="text" 
                    placeholder="Search books..." 
                    value={searchBook} 
                    onChange={(e) => setSearchBook(e.target.value)} 
                    style={{ marginBottom: 0 }}
                />
                <button className="primary-btn" onClick={() => { setActiveview("searchresult"); search_book(searchBook); }}>
                    Search
                </button>
            </div>

            {Activeview === "All" && (
                <div className="grid-layout">
                    {books.map((book) => (
                        <div key={book.id} className="data-card">
                            <h3>{book.name}</h3>
                            <p>Author: {book.author}</p>
                            <button className="primary-btn" onClick={() => IssueBook(book.id)}>Issue</button>
                        </div>
                    ))}
                </div>
            )}

            {Activeview === "MyIssue" && (
                <div className="grid-layout">
                    {myissue.map((issue) => (
                        <div key={issue.id} className="data-card">
                            <p>Book: {issue.book_name}</p>
                            <p>Issue Date: {issue.issue_date}</p>
                            <p>Status: {issue.status}</p>
                            <button className="primary-btn" onClick={() => returnBook(issue.id)}>Return</button>
                        </div>
                    ))}
                </div>
            )}

            {Activeview === "update" && (
                <div className="form-panel">
                    <h3 style={{ textAlign: "center", borderBottom: "none" }}>Update Profile</h3>
                    <label>Name</label>
                    <input value={updateName} onChange={(e) => setUpdateName(e.target.value)} />
                    <button className="primary-btn" style={{ width: "100%" }} onClick={() => update_profile(updateName)}>
                        Update
                    </button>
                </div>
            )}

            {Activeview === "searchresult" && (
                <div className="grid-layout">
                    {searchResults.map((book) => (
                        <div key={book.id} className="data-card">
                            <h3>{book.name}</h3>
                            <p>Author: {book.author}</p>
                            <button className="primary-btn" onClick={() => IssueBook(book.id)}>Issue</button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

export default StudentDashboard;