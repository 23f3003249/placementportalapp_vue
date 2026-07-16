<template>
  <nav class="navbar navbar-dark bg-dark">
    <div class="container">
      <span class="navbar-brand">
        Placement Portal
      </span>

      <button class="btn btn-danger btn-sm" @click="logout">
        Logout
      </button>
    </div>
  </nav>
</template>

<script setup>
import api from "../api/axios"
import { useRouter } from "vue-router"

const router = useRouter()

async function logout() {
  try {
    await api.post("/auth/logout")
    router.push("/")
  } catch (err) {
    alert(err.response?.data?.message || "Failed logging out")
  }
}
</script>