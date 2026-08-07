import { SyntheticEvent, useState } from "react";
import { Navigate } from 'react-router-dom';
import { Link } from "react-router-dom";
import { createUser, loginUser } from "../serverConnect/api";
import "./LoginPage.css"

export function LoginPage() {
  const alt_auth_methods = ["google", "microsoft"]

  const [createAccount, setCreateAccount] = useState(false)
  const [success, setSuccess] = useState<boolean>(false)


  function LoginForm() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    return (
      <form
        onSubmit={
          async (e: SyntheticEvent) => {
            e.preventDefault()
            await loginUser({ name: username, password: password })
            setSuccess(true)
          }}>
        <div>
          <label>User name</label>
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div>
          <label>Password</label>
          <input
            value={password}
            type={"password"}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <button type="submit">login</button>
      </form>
    )
  }



  function CreateAccountForm() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    return (
      <form
        onSubmit={
          async (e: SyntheticEvent) => {
            e.preventDefault()
            await createUser({ name: username, password: password })
            await loginUser({ name: username, password: password })
            setSuccess(true)
          }}>
        <div>
          <label>User name</label>
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div>
          <label>Password</label>
          <input
            value={password}
            type={"password"}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit">login</button>
      </form>
    )
  }

  return (success) ? <Navigate to="/" /> :
    <div className="login-page">
      <div className="login-card">
        <h1>{createAccount ? "Create account" : "Sign in"}</h1>
        {createAccount ? <CreateAccountForm /> : <LoginForm />}
        <button
          onClick={() => setCreateAccount(!createAccount)}
        >
          {createAccount ? "Sign in" : "Create account"}
        </button>
        <ul className="alt-auth-methods">
          {alt_auth_methods.map((method, i) =>
            <li key={method}>
              <Link to={`http://localhost:8000/api/auth/${method}`}>
                Continue with {method}
              </Link>
            </li>
          )}
        </ul>
      </div>
    </div >
}
