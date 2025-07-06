<template>
  <div class="todo-list">
    <h2>待辦事項列表</h2>
    <div v-if="todos.length === 0" class="empty-state">
      <p>目前沒有待辦事項</p>
    </div>
    <div v-else>
      <TodoItem
        v-for="todo in todos"
        :key="todo.id"
        :todo="todo"
        @toggle="$emit('toggle-todo', todo)"
        @delete="$emit('delete-todo', todo.id)"
      />
    </div>
  </div>
</template>

<script>
import TodoItem from './TodoItem.vue'

export default {
  name: 'TodoList',
  components: {
    TodoItem
  },
  props: {
    todos: {
      type: Array,
      required: true
    }
  },
  emits: ['toggle-todo', 'delete-todo']
}
</script>

<style scoped>
.todo-list {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.todo-list h2 {
  margin-top: 0;
  color: #42b983;
}

.empty-state {
  text-align: center;
  color: #666;
  padding: 40px;
}
</style>