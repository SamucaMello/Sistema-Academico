import type { Nota } from "../tipos";

function calcularSituacao(media: number) {
  if (media >= 6) return "Aprovado";
  if (media >= 4) return "Exame";
  return "Reprovado";
}

interface PropsTabelaNotas {
  notas: Nota[];
  aoExcluir: (id: string) => void;
}

export default function TabelaNotas({ notas, aoExcluir }: PropsTabelaNotas) {
  return (
    <table className="border-collapse w-full text-sm mb-2">
      <thead>
        <tr>
          <th className="border p-1 text-left">Aluno</th>
          <th className="border p-1 text-left">P1</th>
          <th className="border p-1 text-left">P2</th>
          <th className="border p-1 text-left">Média</th>
          <th className="border p-1 text-left">Situação</th>
          <th className="border p-1 text-left">Ações</th>
        </tr>
      </thead>
      <tbody>
        {notas.map((nota) => {
          const media = nota.media ?? (nota.P1 + nota.P2) / 2;
          const situacao = nota.situacao ?? calcularSituacao(media);
          return (
            <tr key={nota._id}>
              <td className="border p-1">{nota.aluno.nome}</td>
              <td className="border p-1">{nota.P1}</td>
              <td className="border p-1">{nota.P2}</td>
              <td className="border p-1">{media.toFixed(1)}</td>
              <td className="border p-1">{situacao}</td>
              <td className="border p-1">
                <button className="underline" onClick={() => aoExcluir(nota._id)}>
                  Excluir
                </button>
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}
