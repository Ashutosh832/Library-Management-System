import Login from "./pages/login";
import {BrowserRouter,Routes,Route} from "react-router-dom";
import AdminDashboard from "./pages/AdminDashboard";
import StudentDashboard from "./pages/studentDashboard";
import SignUp from "./pages/signup";
function App() {
  return (
    <BrowserRouter>
    <Routes>
      <Route path="/" element={<Login />}/>
      <Route path="/signup" element={<SignUp/>}/>
      <Route path="/admin" element={<AdminDashboard />}/>
      <Route path="/student" element={<StudentDashboard />}/>
    </Routes>
    </BrowserRouter>
  );
}

export default App;
