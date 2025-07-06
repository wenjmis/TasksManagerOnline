<template>
  <div class="home">
    <div class="todo-form">
      <h2>新增待辦事項</h2>
      <form @submit.prevent="addTodo">
        <div class="form-group">
          <input
            v-model="newTodo.title"
            type="text"
            placeholder="待辦事項標題"
            required
            class="form-input"
          />
        </div>
        <div class="form-group">
          <textarea
            v-model="newTodo.description"
            placeholder="詳細描述（可選）"
            class="form-textarea"
            rows="3"
          ></textarea>
        </div>
        <button type="submit" class="btn btn-primary">新增</button>
      </form>
    </div>

    <TodoList
      :todos="todos"
      @toggle-todo="toggleTodo"
      @delete-todo="deleteTodo"
    />
  </div>
</template>

<script>
import TodoList from '../components/TodoList.vue'

export default {
  name: 'Home',
  components: {
    TodoList
  },
  data() {
    return {
      todos: [],
      newTodo: {
        title: '',
        description: ''
      }
    }
  },
  async mounted() {
    await this.fetchTodos()
  },
  methods: {
    async fetchTodos() {
      try {
        const response = await this.$http.get('/api/todos')
        this.todos = response.data
      } catch (error) {
        console.error('取得待辦事項失敗:', error)
      }
    },
    async addTodo() {
      if (!this.newTodo.title.trim()) return

      try {
        const response = await this.$http.post('/api/todos', this.newTodo)
        this.todos.push(response.data)
        this.newTodo = { title: '', description: '' }
      } catch (error) {
        console.error('新增待辦事項失敗:', error)
      }
    },
    async toggleTodo(todo) {
      try {
        const response = await this.$http.put(`/api/todos/${todo.id}`, {
          ...todo,
          completed: !todo.completed
        })
        const index = this.todos.findIndex(t => t.id === todo.id)
        this.todos[index] = response.data
      } catch (error) {
        console.error('更新待辦事項失敗:', error)
      }
    },
    async deleteTodo(todoId) {
      try {
        await this.$http.delete(`/api/todos/${todoId}`)
        this.todos = this.todos.filter(todo => todo.id !== todoId)
      } catch (error) {
        console.error('刪除待辦事項失敗:', error)
      }
    }
  }
}
</script>

<style scoped>
.todo-form {
  background: white;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.todo-form h2 {
  margin-top: 0;
  color: #42b983;
}

.form-group {
  margin-bottom: 15px;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #42b983;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.btn-primary {
  background-color: #42b983;
  color: white;
}

.btn-primary:hover {
  background-color: #369970;
}
</style>