
import { useState, useEffect } from "react";
import "./App.css";
import type { Todo, CreateTodoInput, UpdateTodoInput } from "./types";
import TodoForm from "./components/todoForm/TodoForm";
import TodoList from "./components/TodoList/TodoList";

const API_URL: string = "http://127.0.0.1:5000/tasks";

export default function App() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [showForm, setShowForm] = useState<boolean>(false);

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      const response: Response = await fetch(API_URL);
      const data: Todo[] = await response.json();
      setTodos(data);
    } catch (error: unknown) {
      console.error("Erro ao carregar tarefas:", error);
    }
  };

  const handleCreate = async (
    input: CreateTodoInput
  ) => {
    try {
      await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(input),
      });

      await fetchTodos();
      setShowForm(false);
    } catch (error: unknown) {
      console.error("Erro ao criar tarefa:", error);
    }
  };

  const handleUpdate = async (
    id: number,
    updates: UpdateTodoInput
  ) => {
    setTodos((prev: Todo[]): Todo[] =>
      prev.map((todo: Todo): Todo =>
        todo.id === id ? { ...todo, ...updates } : todo
      )
    );

    setEditingId(null);

    try {
      await fetch(`${API_URL}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updates),
      });
    } catch (error: unknown) {
      console.error("Erro ao atualizar tarefa:", error);
      await fetchTodos();
    }
  };

  const handleDelete = async (id: number) => {
    setTodos((prev: Todo[]): Todo[] =>
      prev.filter((todo: Todo): boolean => todo.id !== id)
    );

    try {
      await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    } catch (error: unknown) {
      console.error("Erro ao deletar tarefa:", error);
      await fetchTodos();
    }
  };

  const pendingTodos: Todo[] = todos.filter(
    (todo: Todo): boolean => todo.status === "pendente"
  );

  const completedTodos: Todo[] = todos.filter(
    (todo: Todo): boolean => todo.status === "concluida"
  );

  return (
    <div className="app">
      <header>
        <h1>Minhas Tarefas</h1>
        <button
          className="btn btn-primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? "Cancelar" : "Nova Tarefa"}
        </button>
      </header>

      {showForm && (
        <TodoForm
          onSubmit={handleCreate}
          onCancel={() => setShowForm(false)}
        />
      )}

      <section>
        <h2>Pendentes ({pendingTodos.length})</h2>
        <TodoList
          todos={pendingTodos}
          editingId={editingId}
          onEdit={(todo: Todo) => setEditingId(todo.id)}
          onDelete={handleDelete}
          onSave={handleUpdate}
          onCancel={() => setEditingId(null)}
        />
      </section>

      <section>
        <h2>Concluídas ({completedTodos.length})</h2>
        <TodoList
          todos={completedTodos}
          editingId={editingId}
          onEdit={(todo: Todo) => setEditingId(todo.id)}
          onDelete={handleDelete}
          onSave={handleUpdate}
          onCancel={() => setEditingId(null)}
        />
      </section>
    </div>
  );
}

