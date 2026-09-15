import axios from "axios";


export const URL_BASE_API = "http://localhost:8000";

export const api = axios.create({
  baseURL: URL_BASE_API,
  headers: { "Content-Type": "application/json" },
});

export function obterMensagemErro(erro: unknown): string {
  if (axios.isAxiosError(erro)) {
    return erro.response?.data?.detail ?? erro.message;
  }
  return "Erro desconhecido";
}
