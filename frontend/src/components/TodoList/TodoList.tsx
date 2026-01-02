import TodoItem from "../TodoItem/TodoItem";
import { type Todo, type UpdateTodoInput } from "../../types";

interface TodoListProps {
  todos: Todo[];
  editingId: number | null;
  onEdit: (todo: Todo) => void;
  onDelete: (id: number) => void;
  onSave: (id: number, updates: UpdateTodoInput) => void;
  onCancel: () => void;
}

export default function TodoList({
  todos,
  editingId,
  onEdit,
  onDelete,
  onSave,
  onCancel,
}: TodoListProps) {
  if (todos.length === 0) {
    return <p className="empty-message">Nenhuma tarefa encontrada</p>;
  }

  return (
    <div className="todo-list">
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          isEditing={editingId === todo.id}
          onEdit={onEdit}
          onDelete={onDelete}
          onSave={onSave}
          onCancel={onCancel}
        />
      ))}
    </div>
  );
}
