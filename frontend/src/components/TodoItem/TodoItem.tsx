import { useState, useEffect, type ChangeEvent } from "react";
import { type Todo, type UpdateTodoInput } from "../../types";

interface TodoItemProps {
  todo: Todo;
  isEditing: boolean;
  onEdit: (todo: Todo) => void;
  onDelete: (id: number) => void;
  onSave: (id: number, updates: UpdateTodoInput) => void;
  onCancel: () => void;
}

export default function TodoItem({
  todo,
  isEditing,
  onEdit,
  onDelete,
  onSave,
  onCancel,
}: TodoItemProps) {
  const [editForm, setEditForm] = useState<UpdateTodoInput>({
    titulo: todo.titulo,
    descricao: todo.descricao,
    status: todo.status,
  });

  useEffect(() => {
    if (isEditing) {
      setEditForm({
        titulo: todo.titulo,
        descricao: todo.descricao,
        status: todo.status,
      });
    }
  }, [isEditing, todo]);

  const handleChange = (
    e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value, type } = e.target;
    const checked = (e.target as HTMLInputElement).checked;

    setEditForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? (checked ? "concluida" : "pendente") : value,
    }));
  };

  if (isEditing) {
    return (
      <div className="todo-item editing">
        <div className="todo-form">
          <input
            type="text"
            name="titulo"
            value={editForm.titulo}
            onChange={handleChange}
            placeholder="Título"
          />
          <textarea
            name="descricao"
            value={editForm.descricao}
            onChange={handleChange}
            placeholder="Descrição"
            rows={3}
          />
          <label className="checkbox-label">
            <input
              type="checkbox"
              name="status"
              checked={editForm.status === "concluida"}
              onChange={handleChange}
            />
            Concluída
          </label>
        </div>

        <div className="todo-actions">
          <button
            className="btn btn-primary"
            onClick={() => onSave(todo.id, editForm)}
          >
            Salvar
          </button>
          <button className="btn btn-secondary" onClick={onCancel}>
            Cancelar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="todo-item">
      <div className="todo-content">
        <h3 className="todo-title">{todo.titulo}</h3>
        <p className="todo-description">{todo.descricao}</p>
        <span className={`todo-status ${todo.status}`}>
          {todo.status === "pendente" ? "Pendente" : "Concluída"}
        </span>
      </div>

      <div className="todo-actions">
        <button className="btn btn-edit" onClick={() => onEdit(todo)}>
          Editar
        </button>
        <button className="btn btn-delete" onClick={() => onDelete(todo.id)}>
          Excluir
        </button>
      </div>
    </div>
  );
}
