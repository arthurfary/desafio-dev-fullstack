
export type TodoStatus = "pendente" | "concluida";

export interface Todo {
  id: number;
  titulo: string;
  descricao: string;
  status: TodoStatus;
  dataCriacao: string;
}

export interface CreateTodoInput {
  titulo: string;
  descricao: string;
  status: TodoStatus;
}

export interface UpdateTodoInput {
  titulo: string;
  descricao: string;
  status: TodoStatus;
}
