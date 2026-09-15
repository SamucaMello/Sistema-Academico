import type { Mensagem as TipoMensagem } from "../hooks/useMensagem";

export default function Mensagem({ mensagem }: { mensagem: TipoMensagem }) {
  if (!mensagem) return null;
  return (
    <div
      className={`my-2 font-bold ${
        mensagem.tipo === "sucesso" ? "text-green-600" : "text-red-600"
      }`}
    >
      {mensagem.texto}
    </div>
  );
}
