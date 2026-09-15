export interface Aluno {
  _id: string;
  RA: string;
  nome: string;
  email: string;
  curso: string;
  semestre: number;
}

export interface Nota {
  _id: string;
  aluno: Aluno;
  P1: number;
  P2: number;
  media?: number;
  situacao?: string;
}


export interface RespostaPaginada<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}
