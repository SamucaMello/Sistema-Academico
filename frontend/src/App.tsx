import { useState } from "react";
import { obterMensagemErro } from "./services/api";
import * as alunoService from "./services/alunoService";
import * as notaService from "./services/notaService";
import type { Aluno } from "./tipos";
import { useListaPaginada } from "./hooks/useListaPaginada";
import { useMensagem } from "./hooks/useMensagem";

import Mensagem from "./components/Mensagem";
import Paginacao from "./components/Paginacao";
import FormularioAluno from "./components/FormularioAluno";
import TabelaAlunos from "./components/TabelaAlunos";
import FormularioNota from "./components/FormularioNota";
import TabelaNotas from "./components/TabelaNotas";


export default function App() {
  const { mensagem, exibirMensagem } = useMensagem();

  const alunos = useListaPaginada(alunoService.listarAlunos);
  const notas = useListaPaginada(notaService.listarNotas);

  const [alunoEmEdicao, setAlunoEmEdicao] = useState<Aluno | null>(null);

  async function salvarAluno(dados: Aluno) {
    try {
      if (alunoEmEdicao) {
        await alunoService.atualizarAluno(alunoEmEdicao._id, dados);
        exibirMensagem("Aluno atualizado com sucesso.", "sucesso");
      } else {
        await alunoService.criarAluno(dados);
        exibirMensagem("Aluno cadastrado com sucesso.", "sucesso");
      }
      setAlunoEmEdicao(null);
      alunos.recarregar();
    } catch (erro) {
      exibirMensagem("Erro ao salvar aluno: " + obterMensagemErro(erro), "erro");
    }
  }

  async function editarAluno(id: string) {
    try {
      const aluno = await alunoService.buscarAluno(id);
      setAlunoEmEdicao(aluno);
    } catch (erro) {
      exibirMensagem("Erro ao carregar aluno: " + obterMensagemErro(erro), "erro");
    }
  }

  async function excluirAluno(id: string) {
    if (!confirm("Excluir este aluno?")) return;
    try {
      await alunoService.excluirAluno(id);
      exibirMensagem("Aluno excluído.", "sucesso");
      alunos.recarregar();
    } catch (erro) {
      exibirMensagem("Erro ao excluir aluno: " + obterMensagemErro(erro), "erro");
    }
  }

  async function salvarNota(dados: { aluno: string; P1: number; P2: number }) {
    if (!dados.aluno) {
      exibirMensagem("Selecione um aluno.", "erro");
      return;
    }
    try {
      await notaService.criarNota(dados);
      exibirMensagem("Notas lançadas com sucesso.", "sucesso");
      notas.recarregar();
    } catch (erro) {
      exibirMensagem("Erro ao lançar notas: " + obterMensagemErro(erro), "erro");
      
    }
  }

  async function excluirNota(id: string) {
    if (!confirm("Excluir esta nota?")) return;
    try {
      await notaService.excluirNota(id);
      exibirMensagem("Nota excluída.", "sucesso");
      notas.recarregar();
    } catch (erro) {
      exibirMensagem("Erro ao excluir nota: " + obterMensagemErro(erro), "erro");
    }
  }

  return (
    <div className="max-w-3xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-2">Sistema Acadêmico</h1>

      <Mensagem mensagem={mensagem} />

      {/* CADASTRO DE ALUNO */}
      <h2 className="text-lg font-semibold mt-8 mb-2">Cadastrar aluno</h2>
      <FormularioAluno
        alunoEmEdicao={alunoEmEdicao}
        aoSalvar={salvarAluno}
        aoCancelarEdicao={() => setAlunoEmEdicao(null)}
      />

      {/* LISTA DE ALUNOS */}
      <h2 className="text-lg font-semibold mt-8 mb-2">Alunos</h2>
      <TabelaAlunos alunos={alunos.items} aoEditar={editarAluno} aoExcluir={excluirAluno} />
      <Paginacao
        pagina={alunos.pagina}
        totalPaginas={alunos.totalPaginas}
        total={alunos.total}
        tamanho={alunos.tamanho}
        aoMudarPagina={alunos.setPagina}
        aoMudarTamanho={alunos.setTamanho}
      />


      {/* CADASTRO DE NOTAS */}
      <h2 className="text-lg font-semibold mt-8 mb-2">Lançar notas</h2>
      <FormularioNota alunos={alunos.items} aoSalvar={salvarNota} />

      {/* LISTA DE NOTAS */}
      <h2 className="text-lg font-semibold mt-8 mb-2">Notas lançadas</h2>
      <TabelaNotas notas={notas.items} aoExcluir={excluirNota} />
      <Paginacao
        pagina={notas.pagina}
        totalPaginas={notas.totalPaginas}
        total={notas.total}
        tamanho={notas.tamanho}
        aoMudarPagina={notas.setPagina}
        aoMudarTamanho={notas.setTamanho}
      />
    </div>
  );
}
