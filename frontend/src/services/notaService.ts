import { api } from "./api";
import type { Nota, RespostaPaginada } from "../tipos";

export function listarNotas(pagina: number, tamanho: number) {
  return api
    .get<RespostaPaginada<Nota>>("/notas/", { params: { page: pagina, size: tamanho } })
    .then((resposta) => resposta.data);
}

export function criarNota(dados: { aluno: string; P1: number; P2: number }) {
  return api.post<Nota>("/notas/", dados).then((resposta) => resposta.data);
}

export function excluirNota(id: string) {
  return api.delete(`/notas/${id}`);
}
