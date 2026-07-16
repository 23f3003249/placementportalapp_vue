<template>
    <Navbar />
    <div v-if="message" class="alert alert-dismissible" :class="'alert-' + messageType" role="alert">{{ message }}
        <button type="button" class="btn-close" @click="message = ''">
        </button>
    </div>
    <div class="container mt-4">
        <h3>Company Dashboard</h3>

        <div class="card shadow-sm mb-4">
            <div class="card-header bg-primary text-white">
                <h5>Company Profile</h5>
            </div>

            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <label>Company Name</label>
                        <input v-model="profile.company_name" class="form-control">
                    </div>

                    <div class="col-md-6">
                        <label>Account Email</label>
                        <input v-model="profile.email" disabled class="form-control">
                    </div>

                    <div class="col-md-6 mt-3">
                        <label>HR Email</label>
                        <input v-model="profile.hr_email" class="form-control">
                    </div>

                    <div class="col-md-6 mt-3">
                        <label>Website</label>
                        <input v-model="profile.website" class="form-control">
                    </div>

                    <div class="col-12 mt-3">
                        <button class="btn btn-primary" @click="updateCompanyProfile">
                            Update Profile
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>


    <div class="container mt-4">
        <div class="row mb-4">
            <div class="col-md-4">
                <div class="card text-center shadow-sm">
                    <h2>{{ dashboard.drives || 0 }}</h2>
                    <h5>Total Drives</h5>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card text-center shadow-sm">
                    <h2>{{ dashboard.applications || 0 }}</h2>
                    <h5>Total Applications</h5>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card text-center shadow-sm">
                    <h2>{{ approveddrives }}</h2>
                    <h5>Approved Drives</h5>
                </div>
            </div>
        </div>
    </div>


    <div class="container mt-4">
        <div class="col-lg-12 ">
            <div class="card ">

                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">
                        {{ editingId ? "Update Placement Drive" : "Create Placement Drive" }}
                    </h4>
                </div>

                <div class="card-body">
                    <form @submit.prevent="createdrive">
                        <div class="mb-2">
                            <input type="text" v-model="title" class="form-control" placeholder="Job title" required>
                        </div>
                        <div class="mb-2">
                            <input type="text" v-model="description" class="form-control" placeholder="Job Description"
                                required>
                        </div>
                        <div class="mb-3">

                            <label class="form-label">
                                Eligible Branch
                            </label>

                            <div class="d-flex flex-wrap gap-3">
                                <div class="form-check">
                                    <input class="form-check-input" type="radio" name="driveBranch" id="branch-all"
                                        value="all" v-model="branch" required>
                                    <label class="form-check-label" for="branch-all">
                                        All Branches
                                    </label>
                                </div>
                                <div v-for="b in branches" :key="b.id" class="form-check">
                                    <input class="form-check-input" type="radio" name="driveBranch"
                                        :id="'drive-branch-' + b.id" :value="b.name" v-model="branch">
                                    <label class="form-check-label" :for="'drive-branch-' + b.id">
                                        {{ b.name }}
                                    </label>
                                </div>
                            </div>
                        </div>
                        <div class="mb-2">
                            <input type="number" v-model="cgpa" class="form-control" placeholder="minimun CGPA"
                                step="0.01" max="10" min="0" required>
                        </div>
                        <div class="mb-2">
                            <input type="number" v-model="year" class="form-control" placeholder="Eligible year"
                                required>
                        </div>
                        <div class="mb-2">
                            <label class="form-label">Application Deadline</label>
                            <input type="date" v-model="deadline" class="form-control" required>
                        </div>
                        <button class="btn btn-success px-3" type="submit">
                            {{ editingId ? "Update Drive" : "Create Drive" }}
                        </button>

                    </form>
                </div>
            </div>
        </div>


        <div class="card mt-2 shadow-sm">
            <div class="card-header bg-primary text-white">

                <h4>My Placement Drives</h4>
            </div>

            <div class="card-body ">

                <table class="table table-bordered align-middle">
                    <thead>
                        <tr>
                            <th>TTitle</th>
                            <th>Status</th>
                            <th>Deadline</th>
                            <th>Applicants</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="d in drives" :key="d.id">
                            <td>{{ d.title }}</td>
                            <td>
                                <span class="badge"
                                    :class="{ 'bg-warning': d.status == 'Pending', 'bg-success': d.status == 'Approved', 'bg-danger': d.status == 'Closed', 'bg-danger': d.status == 'Rejected' }">
                                    {{ d.status }}
                                </span>
                            </td>
                            <td>{{ d.deadline }}</td>
                            <td>{{ d.applicants }}</td>
                            <td>

                                <div class="d-flex gap-2">

                                    <router-link :to='"/applicants/" + d.id' class="btn btn-sm btn-outline-primary">
                                        View Applicants
                                    </router-link>

                                    <button class="btn btn-warning btn-sm" @click="editDrive(d)"
                                        :disabled="d.status == 'Approved'">
                                        Edit
                                    </button>

                                </div>

                            </td>
                        </tr>
                        <tr v-if="drives.length == 0">
                            <td colspan="5" class="text-center text-muted">No drives available</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>


</template>


<script setup>
import Navbar from "@/components/navbar.vue";
import api from "@/api/axios";
import { ref, onMounted, computed } from "vue";


const dashboard = ref({})
const drives = ref([])

const profile = ref({})
const title = ref("")
const description = ref("")
const branch = ref("")
const cgpa = ref("")
const year = ref("")
const deadline = ref("")

const branches = ref([])

const editingId = ref(null)

const message = ref("")
const messageType = ref("success")


const approveddrives = computed(() => { return drives.value.filter(d => d.status == "Approved").length })

async function load() {
    try {
        profile.value = (await api.get('/company/get-profile')).data
        dashboard.value = (await api.get('/company/dashboard')).data
        drives.value = (await api.get('/company/drives')).data
        branches.value = (await api.get('/auth/branches')).data

    }
    catch (error) {
        message.value = error.response?.data?.message || "Error"
        messageType.value = "danger"
    }
}

onMounted(load)


async function createdrive() {

    const isEditing = editingId.value

    try {
        if (isEditing) {
            await api.put(
                "/company/drive/" + editingId.value,
                {
                    title: title.value,
                    description: description.value,
                    branch: branch.value,
                    cgpa: cgpa.value,
                    year: year.value,
                    deadline: deadline.value
                })
        } else {
            await api.post(
                "/company/drive/create",
                {
                    title: title.value,
                    description: description.value,
                    branch: branch.value,
                    cgpa: cgpa.value,
                    year: year.value,
                    deadline: deadline.value
                })
        }

        title.value = ""
        description.value = ""
        branch.value = ""
        cgpa.value = ""
        year.value = ""
        deadline.value = ""

        editingId.value = null

        message.value = isEditing
            ? "Drive updated successfully"
            : "Drive created successfully"

        messageType.value = "success"
        await load()

    }

    catch (error) {
        message.value =
            error.response?.data?.message ||
            "Operation failed"
        messageType.value = "danger"
    }
}

async function updateCompanyProfile() {
    try {
        await api.post('/company/update-profile', {
            company_name: profile.value.company_name,
            hr_email: profile.value.hr_email,
            website: profile.value.website
        })
        message.value = "Profile updated successfully"
        messageType.value = "success"
    } catch (error) {
        message.value = error.response?.data?.message || "Error in updating profile"
        messageType.value = "danger"
    }
    await load()
}

function editDrive(d) {

    editingId.value = d.id

    title.value = d.title
    description.value = d.description
    branch.value = d.branch
    cgpa.value = d.cgpa
    year.value = d.year
    deadline.value = d.deadline

    // Scroll to the form
    window.scrollTo({
        top: 0,
        behavior: "smooth"
    })

    // Optional success message
    message.value = "Editing drive: " + d.title
    messageType.value = "success"
}

</script>

