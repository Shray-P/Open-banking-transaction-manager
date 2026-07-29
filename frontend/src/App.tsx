import { Routes, Route, BrowserRouter } from "react-router";
import './App.css';
import { HomePage } from './pages/HomePage';
import { Layout } from './Layout';
import { AuthCallbackPage } from "./pages/AuthCallbackPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/auth/callback" element={<AuthCallbackPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
