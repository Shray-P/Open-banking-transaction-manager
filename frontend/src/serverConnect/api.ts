import axios from 'axios'
import { ItemCreateRequest, ItemCreateResponse, UserCreateRequest, UserCreateResponse } from './schemas';

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

export async function requestLinkToken() {
  return get<string>("/link/request-token")
}

export async function createItem(reuqest: ItemCreateRequest) {
  return post<ItemCreateRequest, ItemCreateResponse>("/items/create", reuqest)
}

export async function createUser(request: UserCreateRequest) {
  return post<UserCreateRequest, UserCreateResponse>("/user/create", request)
}
