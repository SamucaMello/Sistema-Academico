import { useCallback, useEffect, useState } from "react";
import { obterMensagemErro } from "../services/api";
import type { RespostaPaginada } from "../tipos";

type FuncaoListagem<T> = (pagina: number, tamanho: number) => Promise<RespostaPaginada<T>>;

export function useListaPaginada<T>(listar: FuncaoListagem<T>, tamanhoInicial = 10) {
  const [items, setItems] = useState<T[]>([]);
  const [pagina, setPagina] = useState(1);
  const [tamanho, setTamanho] = useState(tamanhoInicial);
  const [total, setTotal] = useState(0);
  const [totalPaginas, setTotalPaginas] = useState(1);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState<string | null>(null);

  const recarregar = useCallback(async () => {
    setCarregando(true);
    setErro(null);
    try {
      const resposta = await listar(pagina, tamanho);
      setItems(resposta.items);
      setTotal(resposta.total);
      setTotalPaginas(resposta.pages || 1);
    } catch (erroRequisicao) {
      setErro(obterMensagemErro(erroRequisicao));
    } finally {
      setCarregando(false);
    }
  }, [listar, pagina, tamanho]);

  useEffect(() => {
    recarregar();
  }, [recarregar]);

  // volta para a página 1 sempre que o tamanho de página muda
  function alterarTamanho(novoTamanho: number) {
    setTamanho(novoTamanho);
    setPagina(1);
  }

  return {
    items,
    pagina,
    setPagina,
    tamanho,
    setTamanho: alterarTamanho,
    total,
    totalPaginas,
    carregando,
    erro,
    recarregar,
  };
}
