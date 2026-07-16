<template>

    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-4">
                <div class="card">
                    <div class="card-body">
                        <h4 class="text-center mb-3">Login</h4>

                        <form @submit.prevent="login">
                            <input type="email" class="form-control mb-3" placeholder="xyz@gmail.com" v-model="email">
                            <input type="password" class="form-control mb-3" placeholder="Password" v-model="password">

                            <button class="btn btn-primary w-100"> Login </button>
                        </form>


                        <div class="text-center mt-3">Do not have a account ? <router-link
                                to="/register">Register</router-link></div>

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import api from "../api/axios"


const router = useRouter()

const email = ref("")
const password = ref("")

async function login() {
    try {
        const res = await api.post("/auth/login", {
            email: email.value.trim(),
            password: password.value
        })

        await api.get("/auth/current-user")

        if (res.data.role == "admin") await router.push("/admindashboard")
        else if (res.data.role == "company") await router.push("/companydashboard")
        else if (res.data.role == "student") await router.push("/studentdashboard")

    } catch (error) {
        console.log(error)
        alert(error.response?.data?.message)
    }
}

</script>