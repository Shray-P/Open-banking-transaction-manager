import { useEffect, useState } from 'react';
import axios from 'axios';
import { usePlaidLink } from 'react-plaid-link';

export function HomePage() {
  const [serverMessage, setServerMessage] = useState<string>("");
  const [publicToken, setPublicToken] = useState<string | null>(null);
  const [institutions, setInstitutions] = useState<Array<string>>([]);

  const { open, ready } = usePlaidLink({
    token: publicToken,
    onSuccess: (publicToken, metadata) => {
      axios.post<{ id: string, institution_name: string }>(`http://localhost:8000/api/items/create`, { public_token: publicToken }).then(
        (res) => {
          setInstitutions([...institutions, res.data.institution_name])
        }
      )
    },
  });

  useEffect(() => {
    axios.get<string>("http://localhost:8000/api")
      .then(
        (res) =>
          setServerMessage(res.data)
      )

    axios.get<string>("http://localhost:8000/api/link/request-token").then(
      res => {
        setPublicToken(res.data)
      }
    )
  }, [])


  return <>
    <h1>
      Home Page
    </h1>

    {serverMessage}

    <button onClick={() => open()} disabled={!ready}>
      Connect a bank account
    </button>


    {
      institutions.map((name, i) => <div key={i}>{name}</div>)
    }
  </>

}
