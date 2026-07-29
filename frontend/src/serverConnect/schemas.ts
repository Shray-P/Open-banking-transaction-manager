export interface AccessToken {
  access_token: string
  token_type: string
}

export interface LoginRequest {
  code: string
}

export interface LoginResponse {
  token: AccessToken
}

export interface User {
  id: string
  name: string
}

export interface UserCreateRequest {
  name: string
  password: string
}

export interface UserCreateResponse {
  user: User
}

export interface UserLoginRequest {
  name: string
  password: string
}


export interface UserLoginResponse {
  user: User
  access_token: AccessToken
}

export interface ItemCreateRequest {
  public_token: string
}

export interface ItemCreateResponse {
  id: string
  institution_name: string
}
