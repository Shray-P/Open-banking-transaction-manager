import axios from 'axios'
import { AccessToken, ItemCreateRequest, ItemCreateResponse, LoginRequest, LoginResponse, User, UserCreateRequest, UserCreateResponse, UserLoginRequest, UserLoginResponse } from "./schemas";

const SERVER_ADDR = "http://localhost:8000/api";

export const client = axios.create({
  baseURL: SERVER_ADDR,
  headers: {
    "Content-Type": "application/json",
  },
});

async function get<T, T2 = null>(
  path: string,
  params: T2 | null = null,
): Promise<T> {
  try {
    const response = await client.get<T>(path, {
      params: params,
      headers: {
        Authorization: localStorage.getItem("access_token"),
      },

    });

    return response.data;
  } catch (error) {
    console.error(`GET ${path} failed`, error);
    throw error;
  }
}

async function post<TRequest = null, TResponse = null>(
  path: string,
  request: TRequest,
): Promise<TResponse> {
  try {
    const response = await client.post<TResponse>(path, request, {
      headers: {
        Authorization: localStorage.getItem("access_token"),
      },
    });
    return response.data;
  } catch (error) {
    console.error(`POST ${path} failed`, error);
    throw error;
  }
}

export async function getRoot() {
  return get<string>("")
}

export async function getMe() {
  return get<User>("/user/me")
}

export async function createUser(request: UserCreateRequest) {
  return post<UserCreateRequest, UserCreateResponse>("/user/create", request)
}

export async function loginUser(request: UserLoginRequest) {
  let response = await post<UserLoginRequest, UserLoginResponse>("/user/login", request)
  localStorage.setItem("access_token", `${response.access_token.token_type} ${response.access_token.access_token}`)
  return response.user
}

export async function loginUserWithGoogle() {
  return get<any>("/auth/google")
}

export async function exchangeLoginCode(request: LoginRequest) {
  let response = await post<LoginRequest, LoginResponse>("/auth/exchange-login-code", request)
  if (response === null || response.token === null)
    return

  localStorage.setItem("access_token", `${response.token.token_type} ${response.token.access_token}`)
}

export async function requestLinkToken() {
  return get<string>("/link/request-token")
}

export async function createItem(reuqest: ItemCreateRequest) {
  return post<ItemCreateRequest, ItemCreateResponse>("/items/create", reuqest)
}

