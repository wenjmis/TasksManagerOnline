<template>
  <div class="todo-item" :class="{ completed: todo.completed }">
    <div class="todo-content">
      <div class="todo-header">
        <h3 class="todo-title">{{ todo.title }}</h3>
        <div class="todo-actions">
          <button @click="$emit('toggle')" class="btn btn-toggle">
            {{ todo.completed ? '取消完成' : '標記完成' }}
          </button>
          <button @click="$emit('delete')" class="btn btn-delete">
            刪除
          </button>
        </div>
      </div>
      <p v-if="todo.description" class="todo-description">
        {{ todo.description }}
      </p>
      <small class="todo-date">
        建立時間: {{ formatDate(todo.created_at) }}
      </small>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TodoItem',
  props: {
    todo: {
      type: Object,
      required: true
    }
  },
  emits: ['toggle', 'delete'],
  methods: {
    formatDate(dateString) {
      return new Date(dateString).toLocaleString('zh-TW')
    }
  }
}
</script>

<style scoped>
.todo-item {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 10px;
  transition: all 0.3s ease;
}

.todo-item:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.todo-item.completed {
  background-color: #f0f8f0;
  border-color: #42b983;
}

.todo-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.todo-title {
  margin: 0;
  color: #333;
  flex-grow: 1;
}

.todo-item.completed .todo-title {
  text-decoration: line-through;
  color: #666;
}

.todo-actions {
  display: flex;
  gap: 10px;
}

.todo-description {
  margin: 10px 0;
  color: #666;
  line-height: 1.4;
}

.todo-date {
  color: #999;
  font-size: 0.9em;
}

.btn {
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
}

.btn-toggle {
  background-color: #42b983;
  color: white;
}

.btn-toggle:hover {
  background-color: #369970;
}

.btn-delete {
  background-color: #e74c3c;
  color: white;
}

.btn-delete:hover {
  background-color: #c0392b;
}
</style>