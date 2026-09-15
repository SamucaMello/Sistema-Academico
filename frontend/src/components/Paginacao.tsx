interface PropsPaginacao {
  pagina: number;
  totalPaginas: number;
  total: number;
  tamanho: number;
  aoMudarPagina: (pagina: number) => void;
  aoMudarTamanho: (tamanho: number) => void;
  opcoesTamanho?: number[];
}

export default function Paginacao({
  pagina,
  totalPaginas,
  total,
  tamanho,
  aoMudarPagina,
  aoMudarTamanho,
  opcoesTamanho = [5, 10, 20],
}: PropsPaginacao) {
  return (
    <div className="flex flex-wrap items-center gap-2 text-sm mb-4">
      <button
        className="border px-2 py-1 rounded disabled:opacity-40"
        disabled={pagina <= 1}
        onClick={() => aoMudarPagina(pagina - 1)}
      >
        Anterior
      </button>

      <span>
        Página {pagina} de {totalPaginas} ({total} registros)
      </span>

      <button
        className="border px-2 py-1 rounded disabled:opacity-40"
        disabled={pagina >= totalPaginas}
        onClick={() => aoMudarPagina(pagina + 1)}
      >
        Próxima
      </button>

      <label className="flex items-center gap-1 ml-auto">
        Por página
        <select
          className="border p-1"
          value={tamanho}
          onChange={(e) => aoMudarTamanho(Number(e.target.value))}
        >
          {opcoesTamanho.map((opcao) => (
            <option key={opcao} value={opcao}>
              {opcao}
            </option>
          ))}
        </select>
      </label>
    </div>
  );
}
