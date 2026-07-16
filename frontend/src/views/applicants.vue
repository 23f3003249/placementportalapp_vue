<template>
    <Navbar />
    <div class="alert alert-dismissible" :class="'alert-' + messageType" role="alert">
        {{ message }}
        <button type="button" class="btn btn-close" @click="message = ''"></button>
    </div>
    <div class="container mt-4">
        <button class="btn btn-danger" @click="goback">Back</button>
        <h2>Applicants</h2>
        <div class="table-responsive">
            <table class="table table-bordered align-middle">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>CGPA</th>
                        <th>Branch</th>
                        <th>Resume</th>
                        <th>Status</th>
                        <th>Save Status</th>
                        <th>Interview Date</th>
                        <th>Schedule Interview</th>
                    </tr>
                </thead>
                <tbody>

                    <tr v-for="a in applicants" :key="a.application_id">

                        <td>{{ a.student }}</td>
                        <td>{{ a.email }}</td>
                        <td>{{ a.cgpa }}</td>
                        <td>{{ a.branch }}</td>
                        <td>

                            <a v-if="a.resume" :href="a.resume" target="_blank" class="btn btn-outline-success btn-sm">
                                View Resume
                            </a>
                            <span v-else class="text-muted">
                                Not Uploaded
                            </span>

                        </td>
                        <td>
                            <select v-model="a.status" class="form-select form-select-sm">
                                <option>Applied</option>
                                <option>Shortlisted</option>
                                <option>Selected</option>
                                <option>Rejected</option>
                            </select>
                        </td>

                        <td>
                            <button class="btn btn-success btn-sm" @click="updateStatus(a)">
                                Save
                            </button>
                        </td>
                        <td>
                            <input type="date" v-model="a.newInterviewDate" class="form-control form-control-sm">
                        </td>
                        <td>
                            <button class="btn btn-primary btn-sm" @click="updateInterview(a)">
                                Schedule Interview
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

</template>

<script setup>

import Navbar from "@/components/navbar.vue"
import api from "../api/axios"


import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"

const applicants = ref([])
const route = useRoute()
const router = useRouter()

const message = ref("")
const messageType = ref("success")

async function load() {

    const res = await api.get("/company/applications/" + route.params.id)
    applicants.value = res.data
}


async function updateStatus(a) {
    try {

        const res = await api.post("/company/application/update/" + a.application_id,
            {
                status: a.status
            }
        )
        message.value = res.data.message || "Unable to update status"
        messageType.value = "success"

        message.value = "Status Updated"
        messageType.value = "success"
        await load()
    } catch (error) {
        message.value = error.response?.data?.message || "Unable to update the status"
        messageType.value = "danger"
    }
}
async function updateInterview(a) {
    try {
        if (!a.newInterviewDate) {
            message.value = "Please select interview date"
            messageType.value = "danger"
            console.log("Please select interview date")
            return
        }
        const res = await api.post("/company/application/schedule/" + a.application_id, {
            interview_date: a.newInterviewDate
        })
        message.value = res.data.message
        messageType.value = "success"
        await load()
    }
    catch (err) {
        message.value = err.response?.data?.message || "Unable to schedule a interview "
        messageType.value = "danger"
    }
}

async function goback() {
    router.push("/companydashboard")
}

onMounted(load)


</script>