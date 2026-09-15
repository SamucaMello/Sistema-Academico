import { api } from "./api";
import type { Aluno, RespostaPaginada } from "../tipos";

export function listarAlunos(pagina: number, tamanho: number) {
  return api
    .get<RespostaPaginada<Aluno>>("/aluno/", { params: { page: pagina, size: tamanho } })
    .then((resposta) => resposta.data);
}

export function buscarAluno(id: string) {
  return api.get<Aluno>(`/aluno/${id}`).then((resposta) => resposta.data);
}

export function criarAluno(dados: Omit<Aluno, "id">) {
  return api.post<Aluno>("/aluno/", dados).then((resposta) => resposta.data);
}

export function atualizarAluno(id: string, dados: Omit<Aluno, "_id">) {
  return api.put<Aluno>(`/aluno/${id}`, dados).then((resposta) => resposta.data);
}

export function excluirAluno(id: string) {
  return api.delete(`/aluno/${id}`);
}
