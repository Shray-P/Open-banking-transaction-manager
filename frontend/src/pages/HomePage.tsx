import { useEffect, useState } from 'react';
import axios from 'axios';

export function HomePage() {
  const [serverMessage, setServerMessage] = useState<String>("");

  useEffect(() => {
    axios.get<String>("http://localhost:8000")
      .then(
        (res) =>
          setServerMessage(res.data)
      )
  })

  return <>
    <h1>
      Home Page
    </h1>

    {serverMessage}
  </>

}
