import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../style/auth.css";
function Login(){
    const [email,setEmail] = useState("");
    const [password,setPassword] = useState("");
    const navigate = useNavigate();
    async function HandleLogin(){
        try{
            const response = await fetch("http://localhost:8080/auth/login",
                {
                    method : "POST",
                    headers : {
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body : new URLSearchParams({
                        username : email,
                        password : password 
                    })
                }
            );
            const data = await response.json();
            console.log(data);
            if (response.ok){
                localStorage.setItem(
                    "token",data.access_token
                );
                localStorage.setItem(
                    "email",data.email
                );
                localStorage.setItem(
                    "name",data.name
                )
            }
            if(data.role === "admin"){
                navigate("/admin");

            }
            else if(data.role === "student"){
                navigate("/student");
            }
            else{
                alert(data.detail);
            }
        }
        catch(error){
            console.log(error)  ;
        }
    }
    return (
        <div className="Auth_Container">
            <h1>Login</h1>
            <h3>Email:</h3>
            <input type="email" value={email} onChange={(e) =>setEmail(e.target.value)}/>
            <h3>Password:</h3>
            <input type="password" value={password} onChange={(e) =>setPassword(e.target.value)}/>
            <button onClick={HandleLogin}>Login</button>
            <p>Don't have an account?</p>
            <button onClick={()=>navigate("/signup")}>Signup</button>
        </div>
    );
}
export default Login;