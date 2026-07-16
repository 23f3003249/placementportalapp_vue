<template>
    <Navbar />
    <div v-if="message" class="alert alert-dismissible" :class="'alert-' + messageType" role="alert">{{ message }}
        <button type="button" class="btn-close" @click="message = ''">
        </button>
    </div>
    <div class="container mt-4">
        <h4>Student Dashboard</h4>
        <hr>
        <div class="card mb-4 shadow-sm">
            <div class="class-header">
                <h5>Profile</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <label>Name</label>
                        <input v-model="profile.name" class="form-control">
                    </div>
                    <div class="col-md-6">
                        <label>Email</label>
                        <input v-model="profile.email" class="form-control" disabled>
                    </div>
                    <div class="col-md-4 mt-2">
                        <label class="form-label">
                            Branch
                        </label>
                        <div class="d-flex flex-wrap gap-3">
                            <div v-for="b in branches" :key="b.id" class="form-check">
                                <input class="form-check-input" type="radio" name="profileBranch"
                                    :id="'profile-branch-' + b.id" :value="b.name" v-model="profile.branch">
                                <label class="form-check-label" :for="'profile-branch-' + b.id">
                                    {{ b.name }}
                                </label>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4 mt-2">
                        <label>CGPA</label>
                        <input type="number" step="0.01" min="0" max="10" v-model="profile.cgpa" class="form-control">
                    </div>
                    <div class="col-md-4 mt-2">
                        <label>Year</label>
                        <input type="number" min="1" max="5" v-model="profile.year" class="form-control">
                    </div>
                    <div class="col-md-12 mt-2">
                        <button class="btn btn-primary mt-3" @click="updateprofile">Update profile</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="card mt-3 mb-3">
            <div class="card-header">
                <h5>Resume</h5>
            </div>
            <div class="card-body">
                <div v-if="profile.resume" class="alert alert-light">
                    <strong>Current Resume</strong>
                    <br>

                    <a :href="'http://localhost:5000/uploads/' + profile.resume" target="_blank">
                        {{ profile.resume }}
                    </a>
                </div>
            </div>
            <input type="file" accept=".pdf" class="form-control mb-2" @change="uploadresume" />
        </div>
        <div class="card shadow-sm mb-4">
            <br>
            <div class="card-header bg-primary text-white">Available Drives</div>

            <div class="card-body">
                <h5 class="mb-3">
                    Available Drives
                    <span class="badge bg-primary">
                        {{ drives.length }}
                    </span>
                </h5>
                <div>
                    <button class="btn btn-success mb-1 col-sm-2" @click="Download">Export email CSV Report</button>
                </div>

                <div class="row mb-3">

                    <div class="col-md-5">
                        <input type="text" class="form-control mb-2" placeholder="Search drives..." v-model="search"
                            @input="searchdrives" />
                    </div>
                </div>
                <div class="table-responsive">
                    <table class="table table-bordered align-middle">
                        <thead>
                            <tr>
                                <th>Company</th>
                                <th>Role</th>
                                <th>Deadline</th>
                                <th>Action</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="d in drives" :key="d.id">
                                <td>{{ d.company }}</td>
                                <td>{{ d.title }}</td>
                                <td>{{ d.deadline }}</td>
                                <td>
                                    <router-link :to="'/details/drive/' + d.id" class="btn btn-primary btn-sm">
                                        View Details
                                    </router-link>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <hr>

        <div class="card shadow-sm mb-4">
            <div class="card-header">
                Application History
            </div>
            <div class="card-body">
                <table class="table table-bordered align-middle">
                    <thead>
                        <tr>
                            <th>Company</th>
                            <th>Drive</th>
                            <th>Status</th>
                            <th>Applied Date</th>
                            <th>Interview </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="h in history" :key="h.title + h.company">

                            <td>{{ h.company }}</td>
                            <td>{{ h.title }}</td>
                            <td>
                                <span class="badge" :class="{
                                    'bg-warning': h.status == 'Applied', 'bg-info': h.status == 'Shortlisted',
                                    'bg-success': h.status == 'Selected', 'bg-danger': h.status == 'Rejected',
                                    'bg-primary': h.status == 'Interview Scheduled'
                                }">{{ h.status }}</span>
                            </td>
                            <td>
                                {{ h.date }}
                            </td>
                            <td>
                                <div v-if="h.interview_date">
                                    <p class="mb-1">{{ h.interview_date }}</p>
                                    <a :href="h.interview_link" target="_blank" class="btn btn-success btn-sm">Join
                                        Interview</a>
                                </div>
                                <span v-else class="text-muted">Not Scheduled</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>


<script setup>
import Navbar from "@/components/navbar.vue";
import { ref, onMounted } from "vue"
import api from "../api/axios"

const profile = ref({})

const drives = ref([])
const history = ref([])

const branches = ref([])

const message = ref("")
const messageType = ref("success")


async function load() {
    try {
        profile.value = (await api.get('/student/get-profile')).data
        drives.value = (await api.get('/student/drives')).data
        history.value = (await api.get('/student/history')).data
        branches.value = (await api.get('/auth/branches')).data
    } catch (error) {
        message.value = error.response?.data?.message || "Error"
        messageType.value = "danger"
    }

}

onMounted(load)

async function updateprofile() {
    try {
        await api.post('/student/update-profile', {
            name: profile.value.name,
            branch: profile.value.branch,
            cgpa: profile.value.cgpa,
            year: profile.value.year
        })
        message.value = "Profile updated successfully"
        messageType.value = "success"
    } catch (error) {
        message.value = error.response?.data?.message || "Error in updating profile"
        messageType.value = "danger"
    }
    await load()
}

const search = ref("")
async function searchdrives() {
    const res = await api.get("/student/search?q=" + search.value)
    drives.value = res.data
}

async function uploadresume(e) {
    try {
        const file = e.target.files[0]

        if (!file) return
        const form = new FormData()
        form.append("resume", e.target.files[0])
        await api.post("/student/upload-resume", form)

        message.value = "Resume uploaded successfully"
        messageType.value = "success"
    }
    catch (error) {
        message.value = error.response?.data?.message || "Error in uploading resume"
        messageType.value = "danger"
    }
    await load()
}

async function Download() {
    try {
        const res = await api.get("/student/export")
        console.log(res.data.message)
        message.value = res.data.message || "File downloaded successfully"
        messageType.value = "success"
    }
    catch (error) {
        message.value = error.response?.data?.message || "Error in downloading file"
        messageType.value = "danger"
    }
    await load()
}

</script>
