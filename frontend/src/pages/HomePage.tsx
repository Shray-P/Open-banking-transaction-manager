import { useEffect, useState } from 'react';
import { usePlaidLink } from 'react-plaid-link';
import { createItem, createUser, getRoot, requestLinkToken } from "../serverConnect/api"
import { User } from '../serverConnect/schemas';

export function HomePage() {
  const [serverMessage, setServerMessage] = useState<string>("");
  const [publicToken, setPublicToken] = useState<string | null>(null);
  const [institutions, setInstitutions] = useState<Array<string>>([]);

  const [userName, setUserName] = useState("");

  const [user, setUser] = useState<User>();

  const { open, ready } = usePlaidLink({
    token: publicToken,
    onSuccess: (publicToken, metadata) => {
      createItem({ public_token: publicToken }).then(
        (res) => {
          setInstitutions([...institutions, res.institution_name])
        }
      )
    },
  });

  useEffect(() => {
    getRoot()
      .then(
        (res) =>
          setServerMessage(res)
      )

    requestLinkToken().then(
      res => {
        setPublicToken(res)
      }
    )
  }, [])


  return <>
    <h1>
      Home Page
    </h1>

    {serverMessage}

    <div>
      <div>{user?.id}</div>
      <div>{user?.name}</div>
    </div>

    <div>

      <input onChange={(e) => setUserName(e.target.value)} />

      <button onClick={() => {
        createUser(
          {
            name: userName
          }
        ).then(res => setUser(res.user))
      }}>sign up</button>
    </div>

    <button onClick={() => open()} disabled={!ready}>
      Connect a bank account
    </button>


    {
      institutions.map((name, i) => <div key={i}>{name}</div>)
    }
  </>

}
