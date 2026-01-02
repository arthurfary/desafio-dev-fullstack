import { useState, type FormEvent, type ChangeEvent } from "react";
import { type CreateTodoInput } from "../../types";

interface TodoFormProps {
  onSubmit: (todo: CreateTodoInput) => void;
  onCancel: () => void;
}

export default function TodoForm({ onSubmit, onCancel }: TodoFormProps) {
  const [inputs, setInputs] = useState<CreateTodoInput>({
    titulo: "",
    descricao: "",
    status: "pendente",
  });

  const handleChange = (
    e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value, type } = e.target;
    const checked = (e.target as HTMLInputElement).checked;

    setInputs((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? (checked ? "concluida" : "pendente") : value,
    }));
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    onSubmit(inputs);
    setInputs({ titulo: "", descricao: "", status: "pendente" });
  };

  return (
    <form className="todo-form" onSubmit={handleSubmit}>
      <input
        type="text"
        name="titulo"
        value={inputs.titulo}
        onChange={handleChange}
        placeholder="Título"
        required
      />

      <textarea
        name="descricao"
        value={inputs.descricao}
        onChange={handleChange}
        placeholder="Descrição"
        rows={3}
        required
      />

      <label className="checkbox-label">
        <input
          type="checkbox"
          name="status"
          checked={inputs.status === "concluida"}
          onChange={handleChange}
        />
        Concluída
      </label>

      <div className="form-actions">
        <button type="submit" className="btn btn-primary">
          Adicionar
        </button>
        <button type="button" className="btn btn-secondary" onClick={onCancel}>
          Cancelar
        </button>
      </div>
    </form>
  );
}
