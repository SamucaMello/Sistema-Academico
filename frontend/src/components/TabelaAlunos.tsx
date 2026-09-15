import { type Aluno } from "../tipos";

interface PropsTabelaAlunos {
  alunos: Aluno[];
  aoEditar: (id: string) => void;
  aoExcluir: (id: string) => void;
}

export default function TabelaAlunos({ alunos, aoEditar, aoExcluir }: PropsTabelaAlunos) {
  return (
    <table className="border-collapse w-full text-sm mb-2">
      <thead>
        <tr>
          <th className="border p-1 text-left">RA</th>
          <th className="border p-1 text-left">Nome</th>
          <th className="border p-1 text-left">E-mail</th>
          <th className="border p-1 text-left">Curso</th>
          <th className="border p-1 text-left">Semestre</th>
          <th className="border p-1 text-left">Ações</th>
        </tr>
      </thead>
      <tbody>
        {alunos.map((aluno) => (
          
          <tr key={aluno._id}>
            <td className="border p-1">{aluno.RA}</td>
            <td className="border p-1">{aluno.nome}</td>
            <td className="border p-1">{aluno.email}</td>
            <td className="border p-1">{aluno.curso}</td>
            <td className="border p-1">{aluno.semestre}</td>
            <td className="border p-1 space-x-2">
              <button className="underline" onClick={() => aoEditar(aluno._id)}>
                Editar
              </button>
              <button className="underline" onClick={() => aoExcluir(aluno._id)}>
                Excluir
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
