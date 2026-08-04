import { Routes, Route, BrowserRouter } from "react-router";
import './App.css';
import { HomePage } from './pages/HomePage';
import { Layout } from './Layout';
import { AuthCallbackPage } from "./pages/AuthCallbackPage";
import { LoginPage } from "./pages/LoginPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/auth/callback" element={<AuthCallbackPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
