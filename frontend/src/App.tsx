import { useEffect, useState } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [serverMessage, setServerMessage] = useState<String>("");

  useEffect(() => {
    axios.get<String>("http://localhost:8000")
      .then(
        (res) =>
          setServerMessage(res.data)
      )

  })

  return (
    <div className="App">
      <header className="App-header">
        Bank transaction tracker
      </header>

      {serverMessage}

    </div>
  );
}

export default App;
