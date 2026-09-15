import { type FormEvent, useState } from "react";
import type { Aluno, Nota } from "../tipos";

interface PropsFormularioNota {
  alunos: Aluno[];
  aoSalvar: (dados: { aluno: string; P1: number; P2: number }) => void;
}

export default function FormularioNota({ alunos, aoSalvar }: PropsFormularioNota) {
  const [idAluno, setIdAluno] = useState("");
  const [p1, setP1] = useState("");
  const [p2, setP2] = useState("");

  function lidarComEnvio(evento: FormEvent) {
    evento.preventDefault();
    aoSalvar({ aluno: idAluno, P1: Number(p1), P2: Number(p2) });
    setIdAluno("");
    setP1("");
    setP2("");
  }

  return (
    <form onSubmit={lidarComEnvio} className="flex flex-wrap items-end gap-2 mb-4">
      <label className="flex flex-col text-sm">
        Aluno
        <select
          className="border p-1 text-sm"
          required
          value={idAluno}
          onChange={(e) => setIdAluno(e.target.value)}
        >
          <option value="">selecione</option>
          {alunos.map((aluno) => (
            <option key={aluno._id} value={aluno._id}>
              {aluno.nome} (RA {aluno.RA})
            </option>
          ))}
        </select>
      </label>
      <label className="flex flex-col text-sm">
        P1
        <input
          className="border p-1 text-sm"
          type="number"
          min={0}
          max={10}
          step={0.1}
          required
          value={p1}
          onChange={(e) => setP1(e.target.value)}
        />
      </label>
      <label className="flex flex-col text-sm">
        P2
        <input
          className="border p-1 text-sm"
          type="number"
          min={0}
          max={10}
          step={0.1}
          required
          value={p2}
          onChange={(e) => setP2(e.target.value)}
        />
      </label>
      <button type="submit" className="bg-blue-600 text-white px-3 py-1 rounded">
        Salvar notas
      </button>
    </form>
  );
}
