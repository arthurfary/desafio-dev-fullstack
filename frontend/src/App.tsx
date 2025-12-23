import { useState, useEffect } from 'react'
import './App.css'

function App() {
  //const [count, setCount] = useState(0)
  const [todos, setTodos] = useState({})

  useEffect(() => {
    fetch("http://127.0.0.1:5000/tasks")
      .then(response => response.json())
      .then(data => console.log(data))
  }, [])



  return (
    <>
      hello
    </>
  )
}

export default App
