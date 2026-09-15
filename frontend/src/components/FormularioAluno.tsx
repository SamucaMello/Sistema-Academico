import {type FormEvent, useEffect, useState } from "react";
import type { Aluno } from "../tipos";

const formularioVazio = { RA: "", nome: "", email: "", curso: "", semestre: "", _id: "" };

interface PropsFormularioAluno {
  alunoEmEdicao: Aluno | null;
  aoSalvar: (dados: Aluno) => void;
  aoCancelarEdicao: () => void;
}

export default function FormularioAluno({
  alunoEmEdicao,
  aoSalvar,
  aoCancelarEdicao,
}: PropsFormularioAluno) {
  console.log()
  const [dados, setDados] = useState(alunoEmEdicao ?? formularioVazio);

  useEffect(() => {
    if (alunoEmEdicao) {
      setDados({
        RA: alunoEmEdicao.RA,
        nome: alunoEmEdicao.nome,
        email: alunoEmEdicao.email,
        curso: alunoEmEdicao.curso,
        semestre: String(alunoEmEdicao.semestre),
        _id: alunoEmEdicao._id
      });
    } else {
      setDados(formularioVazio);
    }
  }, [alunoEmEdicao]);

  function lidarComEnvio(evento: FormEvent) {
    evento.preventDefault();
    aoSalvar({
      RA: dados.RA,
      nome: dados.nome,
      email: dados.email,
      curso: dados.curso,
      semestre: Number(dados.semestre),
      _id: dados._id
    });
    setDados(formularioVazio);
  }

  return (
    <form onSubmit={lidarComEnvio} className="flex flex-wrap items-end gap-2 mb-4">
      <label className="flex flex-col text-sm">
        RA
        <input
          className="border p-1 text-sm"
          required
          value={dados.RA}
          onChange={(e) => setDados({ ...dados, RA: e.target.value })}
        />
      </label>
      <label className="flex flex-col text-sm">
        Nome
        <input
          className="border p-1 text-sm"
          required
          value={dados.nome}
          onChange={(e) => setDados({ ...dados, nome: e.target.value })}
        />
      </label>
      <label className="flex flex-col text-sm">
        E-mail
        <input
          className="border p-1 text-sm"
          type="email"
          required
          value={dados.email}
          onChange={(e) => setDados({ ...dados, email: e.target.value })}
        />
      </label>
      <label className="flex flex-col text-sm">
        Curso
        <input
          className="border p-1 text-sm"
          required
          value={dados.curso}
          onChange={(e) => setDados({ ...dados, curso: e.target.value })}
        />
      </label>
      <label className="flex flex-col text-sm">
        Semestre
        <input
          className="border p-1 text-sm"
          type="number"
          min={1}
          required
          value={dados.semestre}
          onChange={(e) => setDados({ ...dados, semestre: e.target.value })}
        />
      </label>
      <button type="submit" className="bg-blue-600 text-white px-3 py-1 rounded">
        Salvar
      </button>
      {alunoEmEdicao && (
        <button
          type="button"
          onClick={aoCancelarEdicao}
          className="bg-gray-300 px-3 py-1 rounded"
        >
          Cancelar edição
        </button>
      )}
    </form>
  );
}
