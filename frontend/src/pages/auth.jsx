import { useState }
from "react";

import Login from "./login";
import Signup from "./signup";


function Auth(){
    const [isLogin, setIsLogin]
        = useState(true);
    return (

        <div>

            <button
                onClick={() =>
                    setIsLogin(true)
                }
            >
                Login
            </button>

            <button
                onClick={() =>
                    setIsLogin(false)
                }
            >
                Signup
            </button>

            {
                isLogin
                ? <Login />
                : <Signup />
            }

        </div>
    );
}

export default Auth;