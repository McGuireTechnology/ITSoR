<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { signupUser } from '../lib/api'
import { setToken } from '../lib/auth'

const router = useRouter()

const username = ref('')
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleSubmit() {
  loading.value = true
  error.value = ''
  try {
    const response = await signupUser({
      username: username.value,
      email: email.value,
      password: password.value,
    })
    setToken(response.access_token)
    await router.push('/users')
  } catch (submitError) {
    error.value = submitError.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="container min-vh-100 d-flex align-items-center justify-content-center py-5 px-3">
    <div class="card shadow-sm border-0 w-100 max-w-md rounded-4 bg-brand-surface/70">
      <div class="card-body p-4 p-md-5">
        <h2 class="h3 fw-bold mb-4 text-brand-deep">Signup</h2>
        <form class="d-flex flex-column gap-3" @submit.prevent="handleSubmit">
          <div>
            <label class="form-label" for="signup-username">Username</label>
            <input
              id="signup-username"
              v-model="username"
              class="form-control"
              type="text"
              required
              autocomplete="username"
            />
          </div>

          <div>
            <label class="form-label" for="signup-email">Email</label>
            <input
              id="signup-email"
              v-model="email"
              class="form-control"
              type="email"
              required
              autocomplete="email"
            />
          </div>

          <div>
            <label class="form-label" for="signup-password">Password</label>
            <input
              id="signup-password"
              v-model="password"
              class="form-control"
              type="password"
              required
              autocomplete="new-password"
            />
          </div>

          <button class="btn btn-primary mt-2 bg-primary hover:bg-accent border-0" type="submit" :disabled="loading">
            {{ loading ? 'Creating...' : 'Signup' }}
          </button>

          <div v-if="error" class="alert alert-danger py-2 mb-0" role="alert">{{ error }}</div>
        </form>

        <p class="text-body-secondary mt-4 mb-0">
          Already have an account?
          <RouterLink class="link-primary fw-semibold text-brand-purple hover:text-brand-pink" to="/login">Login</RouterLink>
        </p>
      </div>
    </div>
  </section>
</template>
