import { useRef, useState } from "react";

export type Mensagem = { texto: string; tipo: "sucesso" | "erro" } | null;

export function useMensagem() {
  const [mensagem, setMensagem] = useState<Mensagem>(null);
  const referenciaTimeout = useRef<ReturnType<typeof setTimeout>>();

  function exibirMensagem(texto: string, tipo: "sucesso" | "erro") {
    setMensagem({ texto, tipo });
    clearTimeout(referenciaTimeout.current);
    referenciaTimeout.current = setTimeout(() => setMensagem(null), 4000);
  }

  return { mensagem, exibirMensagem };
}
