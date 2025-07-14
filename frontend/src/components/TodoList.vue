<template>
  <div class="todo-list">
    <h2>待辦事項列表</h2>

    <!-- 排序按鈕 -->
    <button @click="toggleSortOrder" class="sort-btn">
      依時間排序：{{ sortOrder === 'asc' ? '最舊優先' : '最新優先' }}
    </button>

    <div v-if="todos.length === 0" class="empty-state">
      <p>目前沒有待辦事項</p>
    </div>

    <div v-else>
      <TodoItem
        v-for="todo in sortedTodos"
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
  data() {
    return {
      sortOrder: 'asc' // 'asc' | 'desc'
    };
  },
  computed: {
    sortedTodos() {
      return [...this.todos].sort((a, b) => {
        const timeA = new Date(a.time || a.createdAt);
        const timeB = new Date(b.time || b.createdAt);
        return this.sortOrder === 'asc' ? timeA - timeB : timeB - timeA;
      });
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