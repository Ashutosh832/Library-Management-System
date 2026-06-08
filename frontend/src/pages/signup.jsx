import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../style/auth.css";
function SignUp(){
    const [name,setName] = useState("");
    const [email,setEmail] = useState("");
    const [password,setPassword] = useState("");
    const navigate = useNavigate();
    async function handleSignup(){
        try {
            const response = await fetch("http://localhost:8080/auth/signup",
            {
                method : "POST",
                headers : {
                    "Content-Type" : "application/json"
                },
                body : JSON.stringify({
                    "name" : name,
                    "email" : email,
                    "password" : password,
                    "role" : "student"
                })
            });
            const data = await response.json();
            console.log(data);
            if (response.ok){
                alert("Registration Successful");
                navigate("/");
            }
            else{
                alert(data.detail);
            }
            
        }
        catch(error){
            console.log(error)
        }
    }
    return (
        <div className="Auth_Container">
            <h1>Registration</h1>
            <h3>Name:</h3>
            <input type="text" value={name} onChange={(e)=>setName(e.target.value)}/>
            <h3>Email:</h3>
            <input type="email" value={email} onChange={(e)=>setEmail(e.target.value)}/>
            <h3>Password:</h3>
            <input type="password" value={password} onChange={(e)=>setPassword(e.target.value)}/>
            <button onClick={handleSignup}>Register</button>
            <p>Already have an account?</p>
            <button onClick={() =>navigate("/")}>Login</button>
        </div>
    )
}
export default SignUp;