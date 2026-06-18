import { Routes, Route, BrowserRouter } from "react-router";
import './App.css';
import { HomePage } from './pages/HomePage';
import { Layout } from './Layout';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<HomePage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
