export interface User {
  id: string
  name: string
}

export interface UserCreateRequest {
  name: string
}

export interface UserCreateResponse {
  user: User
}

export interface ItemCreateRequest {
  public_token: string
}

export interface ItemCreateResponse {
  id: string
  institution_name: string
}
