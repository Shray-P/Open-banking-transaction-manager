import { useEffect, } from 'react';
import { Navigate, useSearchParams } from 'react-router-dom';
import { exchangeLoginCode } from '../serverConnect/api';

export function AuthCallbackPage() {
  const [searchParams, _] = useSearchParams()
  useEffect(() => {
    let code = searchParams.get("code")
    if (code === null)
      return
    exchangeLoginCode({ code })
  }, [searchParams])
  return <Navigate to="/" ></Navigate>
}
