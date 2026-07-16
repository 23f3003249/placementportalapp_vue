<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-5">
                <div class="card">
                    <div class="card-body">
                        <h4 class="text-center mb-3">Register</h4>

                        <form @submit.prevent="Register">
                            <input class="form-control mb-3" placeholder="Full Name" v-model="name" required>
                            <input class="form-control mb-3" placeholder="Email" v-model="email" required>
                            <input type="password" class="form-control mb-3" placeholder="Password" v-model="password"
                                required>
                            <select class="form-select mb-3" v-model="role">
                                <option value="Student">Student</option>
                                <option value="Company">Company</option>
                            </select>
                            <div v-if="role == 'Student'" class="mb-3">
                                <label class="form-label">
                                    Branch
                                </label>

                                <div class="d-flex flex-wrap gap-3">

                                    <div v-for="b in branches" :key="b.id" class="form-check">
                                        <input class="form-check-input" type="radio" name="studentBranch"
                                            :id="'student-branch-' + b.id" :value="b.name" v-model="branch">

                                        <label class="form-check-label" :for="'student-branch-' + b.id">
                                            {{ b.name }}
                                        </label>
                                    </div>
                                </div>
                            </div>

                            <input type="number" v-if="role == 'Student'" v-model="cgpa" class="form-control mb-2"
                                placeholder="CGPA" steps="0.00" min="0" max="10" required>

                            <label v-if="role == 'Student'" class="mb-2">Your current accademic year . If you are in 1st
                                year write
                                1.
                                <input type="number" v-if="role == 'Student'" v-model="year" class="form-control mb-1"
                                    placeholder="Year" min="1" max="5" required>
                            </label>
                            <input type="email" v-if="role == 'Company'" v-model="hr_email" class="form-control mb-2"
                                placeholder="Your Company Email" required>
                            <input v-if="role == 'Company'" v-model="website" class="form-control mb-2"
                                placeholder="www.xyz.com">
                            <button class="btn btn-primary w-100">
                                Register </button>
                        </form>
                        <div class="text-center mt-3">Already have an account? <router-link
                                to="/login">Login</router-link></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script setup>
import { ref, onMounted } from "vue"
import api from "../api/axios"
import { useRouter } from "vue-router"

const router = useRouter()

const role = ref("Student")
const name = ref("")
const email = ref("")
const password = ref("")
const branch = ref("")
const cgpa = ref("")
const hr_email = ref("")
const year = ref("")
const website = ref("")

const branches = ref([])

async function Register() {
    try {
        if (role.value == "Student") {
            await api.post("/auth/register/student", {
                name: name.value,
                email: email.value,
                password: password.value,
                branch: branch.value,
                cgpa: cgpa.value,
                year: year.value

            })
        }
        if (role.value == "Company") {
            await api.post("/auth/register/company", {
                company_name: name.value,
                email: email.value,
                password: password.value,
                website: website.value,
                hr_email: hr_email.value.trim()
            })
        }
        alert("Registered Successfully")
        router.push("/login")
    }
    catch (error) {
        console.log(error)
        alert(error.response?.data?.message || "Error in registration")
    }
}

async function loadBranches() {
    try {
        const res = await api.get('/auth/branches')
        branches.value = res.data
    } catch (error) {
        console.error("Error loading branches:", error)
    }
}

onMounted(loadBranches)

</script>
