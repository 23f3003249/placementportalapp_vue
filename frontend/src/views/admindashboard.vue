<template>
    <Navbar />
    <div v-if="message" class="alert alert-dismissible" :class="'alert-' + messageType" role="alert">{{ message }}
        <button type="button" class="btn-close" @click="message = ''">
        </button>
    </div>

    <!-- Admin Dashboard -->
    <div class="container border-dark mt-4">

        <h1>Admin Dashboard</h1>

        <div class="row g-2 mt-4">
            <div class="col-md-3">
                <div class="card p-2 text-center shadow-sm">
                    <div class="card-body"> {{ dashboard.students || "0" }}</div>
                    Students Registered
                </div>
            </div>
            <div class="col-md-3">
                <div class="card p-2 text-center shadow-sm">
                    <div class="card-body"><b>{{ dashboard.companies || "0" }} </b></div>
                    Companies Registered
                </div>
            </div>
            <div class="col-md-3">
                <div class="card  p-2 text-center shadow-sm">
                    <div class="card-body"><b>{{ dashboard.drives || "0" }}</b></div>
                    Drives
                </div>
            </div>
            <div class="col-md-3">
                <div class="card  p-2 text-center shadow-sm">
                    <div class="card-body"><b>{{ dashboard.applications || "0" }}</b></div>
                    Applications
                </div>
            </div>

        </div>

        <hr>


        <div class="card shadow-sm mb-3">
            <div class="card-body">
                <h5>Manage Branches</h5>
                <div class="d-flex gap-2 mb-3">
                    <input v-model="newBranch" type="text" class="form-control" placeholder="Enter branch name">
                    <button class="btn btn-primary" @click="addBranch">
                        Add Branch
                    </button>
                </div>
                <div class="d-flex flex-wrap gap-2">
                    <div v-for="branch in branches" :key="branch.id" class="badge bg-secondary p-2">

                        {{ branch.name }}

                        <button class="btn btn-sm btn-light text-danger py-0 px-1" @click="deleteBranch(branch.id)">
                            X
                        </button>

                    </div>
                </div>
            </div>
        </div>

        <hr>

        <!-- for company views and actions-->

        <div class="card shadow-sm mb-3">
            <div class="card-body">
                <h5>Companies</h5>
                <div class="row mb-3">
                    <div class="col-md-5">
                        <input class="form-control mt-1 my-3" v-model="companysearch" placeholder="Search Company..."
                            @input="searchcompany">
                    </div>
                </div>

                <div class="table-responsive">
                    <table class="table table-bordered align-middle">
                        <thead>
                            <tr>
                                <th>Company</th>
                                <th>Email</th>
                                <th>Status</th>
                                <th>Active</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="c in companies" :key="c.id">
                                <td>{{ c.company_name }}</td>
                                <td>{{ c.email }}</td>
                                <td>
                                    <span v-if="c.approved" class="badge bg-success">Approved</span>
                                    <span v-else class="badge bg-warning">Pending</span>
                                </td>
                                <td>{{ c.active ? "Active" : "Blocked" }}</td>
                                <td>
                                    <div class="d-flex gap-2">
                                        <router-link :to="'/details/company/' + c.id" class="btn btn-primary btn-sm">
                                            View
                                        </router-link>
                                        <button v-if="!c.approved" class="btn btn-success btn-sm"
                                            @click="approvecompany(c.id)">Approve</button>
                                        <button v-if="!c.approved" class="btn btn-danger btn-sm"
                                            @click="rejectcompany(c.id)">Reject</button>
                                        <button v-if="c.active" class="btn btn-danger btn-sm"
                                            @click="blacklistcompany(c.id)">Block</button>
                                    </div>
                                </td>
                            </tr>
                            <tr v-if="companies.length === 0">
                                <td colspan="5" class="text-center">
                                    No companies found
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <hr>

        <!-- for students for view and action-->

        <div class="card shadow-sm mb-3">
            <div class="card-body">
                <h5>Students</h5>
                <div class="row mb-3">
                    <div class="col-md-5">
                        <input class="form-control mt-1 my-3" placeholder="Search Student.." v-model="studentsearch"
                            @input="searchstudent">
                    </div>
                </div>

                <div class="table-responsive">
                    <table class="table table-bordered align-middle">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Email</th>
                                <th>Branch</th>
                                <th>CGPA</th>
                                <th>Year</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="s in students" :key="s.id">
                                <td>{{ s.name }}</td>
                                <td>{{ s.email }}</td>
                                <td>{{ s.branch }}</td>
                                <td>{{ s.cgpa }}</td>
                                <td>{{ s.year }}</td>
                                <td>

                                    <div class="d-flex gap-2 flex-wrap">

                                        <router-link :to="'/details/student/' + s.id" class="btn btn-primary btn-sm">
                                            View
                                        </router-link>

                                        <button v-if="s.active" class="btn btn-danger btn-sm"
                                            @click="blackliststudent(s.id)">
                                            Block
                                        </button>

                                        <span v-else class="badge bg-danger">
                                            Blocked
                                        </span>

                                    </div>

                                </td>
                            </tr>
                            <tr v-if="students.length === 0">
                                <td colspan="6" class="text-center">
                                    No student found
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>


        <hr>

        <!-- for drives -->

        <div class="card shadow-sm mb-3">
            <div class="card-body">
                <h5>Drives</h5>
                <div class="row mb-3">
                    <div class="col-md-5">
                        <input class="form-control mt-1 my-3" placeholder="Serach Drive..." v-model="drivesearch"
                            @input="searchdrive">
                    </div>
                </div>
                <div class="table-responsive">
                    <table class="table table-bordered align-middle">
                        <thead>
                            <tr>
                                <th>Company</th>
                                <th>Title</th>
                                <th>Deadline</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="d in drives" :key="d.id">
                                <td>{{ d.company }} </td>
                                <td>{{ d.title }}</td>
                                <td>{{ d.deadline }}</td>
                                <td>
                                    <span v-if="d.status == 'Approved'" class="badge bg-success">Approved</span>
                                    <span v-else class="badge bg-danger">{{ d.status }}</span>
                                </td>

                                <td>
                                    <router-link :to="'/details/drive/' + d.id" class="btn btn-primary btn-sm me-1">
                                        View
                                    </router-link>
                                    <button v-if="d.status == 'Pending'" class="btn btn-success btn-sm"
                                        @click="approvedrive(d.id)">Approve</button>
                                    <span v-if="d.status == 'Approved'" class="badge bg-success">Approved</span>
                                    <button v-if="d.status == 'Pending'" class="btn btn-danger btn-sm"
                                        @click="rejectdrive(d.id)">Reject</button>
                                    <span v-if="d.status == 'Rejected'" class="badge bg-danger">Rejected</span>
                                </td>
                            </tr>
                            <tr v-if="drives.length === 0">
                                <td colspan="5" class="text-center">
                                    No Drive found
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Applications -->

        <div class="card shadow-sm mb-3">
            <div class="card-body">
                <h5>All students applications</h5>
                <div class="table-responsive">
                    <table class="table table-bordered align-middle">
                        <thead>
                            <tr>
                                <th>Student</th>
                                <th>Company</th>
                                <th>Drive</th>
                                <th>Application Date</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="a in applications" :key="a.student_name + a.drive_title">
                                <td>{{ a.student_name }}</td>
                                <td>{{ a.company_name }}</td>
                                <td>{{ a.drive_title }}</td>
                                <td>{{ a.application_date }}</td>
                                <td>
                                    <span class="badge" :class="statusclass(a.status)">
                                        {{ a.status }}
                                    </span>
                                </td>
                            </tr>
                            <tr v-if="applications.length === 0">
                                <td colspan="5" class="text-center">
                                    No applications found
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import Navbar from "@/components/navbar.vue"
import { ref, onMounted } from "vue"
import api from "../api/axios"

const dashboard = ref({})
const companies = ref([])
const students = ref([])
const drives = ref([])
const applications = ref([])


const branches = ref([])
const newBranch = ref("")

const companysearch = ref("")
const studentsearch = ref("")
const drivesearch = ref("")

const message = ref("")
const messageType = ref("success")

async function load() {
    try {

        dashboard.value = (await api.get("/admin/dashboard")).data
        companies.value = (await api.get("/admin/companies")).data
        students.value = (await api.get("/admin/students")).data
        drives.value = (await api.get("/admin/drives")).data
        applications.value = (await api.get("/admin/applications")).data
        branches.value = (await api.get('/admin/branches')).data
    }
    catch (error) {
        message.value = error.response?.data?.message || "Error in loading data"
        messageType.value = "danger"
    }
}

onMounted(load)

// search company function
async function searchcompany() {
    try {
        if (!companysearch.value.trim()) {
            const res = await api.get("/admin/companies")
            companies.value = res.data
            return
        }
        const res = await api.get("/admin/search/companies?q=" + companysearch.value)

        companies.value = res.data
    } catch (error) {
        console.error(error || "company search failed")
    }
}

//search student function
async function searchstudent() {
    try {
        if (!studentsearch.value.trim()) {
            const res = await api.get("/admin/students")
            students.value = res.data
            return
        }
        const res = await api.get("/admin/search/students?q=" + studentsearch.value)
        students.value = res.data
    }
    catch (error) {
        console.error(error || "student search failed")
    }
}

//searcg drive function 
async function searchdrive() {
    try {
        if (!drivesearch.value.trim()) {
            const res = await api.get("/admin/drives")
            drives.value = res.data
            return
        }
        const res = await api.get("/admin/search/drives?q=" + drivesearch.value)
        drives.value = res.data
    }
    catch (error) {
        console.error(error || "drive search failed")
    }
}

function statusclass(status) {
    if (status == "Applied") return "bg-success"
    if (status == "Shortlisted") return "bg-warning"
    if (status == "Selected") return "bg-info"
    if (status == "Rejected") return "bg-danger"

    return "bg-secondary"
}

async function approvecompany(id) {
    try {

        await api.post("/admin/approve-company/" + id)
        await load()
        message.value = "Company approved successfully"
        messageType.value = "success"
    }
    catch (error) {
        message.value = error.response?.data?.message || "company approval failed"
        messageType.value = "danger"
    }
}

async function approvedrive(id) {
    try {
        await api.post("/admin/approve-drive/" + id)
        await load()
        message.value = "Drive approved successfully"
        messageType.value = "success"
    }
    catch (error) {
        message.value = error.response?.data?.message || "drive approval failed"
        messageType.value = "danger"
    }
}

async function rejectdrive(id) {
    try {
        await api.post('/admin/reject-drive/' + id)
        await load()

        message.value = "Drive rejected successfully"
        messageType.value = "success"
    }
    catch (error) {
        message.value = error.response?.data?.message || "Drive reject failed"
        messageType.value = "danger"
    }

}

async function blacklistcompany(id) {
    try {
        await api.post("/admin/blacklist-company/" + id)
        await load()
        message.value = "Company blacklisteed successfully"
        messageType.value = "success"

    } catch (error) {
        message.value = error.response?.data?.message || "company block failed"
        messageType.value = "danger"
    }
    load()
}

async function rejectcompany(id) {
    try {
        await api.post("/admin/reject-company/" + id)
        await load()
        message.value = "Company rejected successfully"
        messageType.value = "success"
    }
    catch (error) {
        message.value = error.response?.data?.message || "company rejection failed"
        messageType.value = "danger"
    }
}

async function blackliststudent(id) {
    try {
        await api.post("/admin/blacklist-student/" + id)
        await load()
        message.value = "Student blacklisted successfully"
        messageType.value = "success"
    }
    catch (error) {
        message.value = error.response?.data?.message || "student block failed"
        messageType.value = "danger"
    }

}


async function addBranch() {
    try {
        if (!newBranch.value.trim()) {
            message.value = "Branch name cannot be empty"
            messageType.value = "danger"
            return
        }
        const res = await api.post('/admin/branches', {
            name: newBranch.value.trim()
        })

        message.value = res.data.message || "Branch added successfully"
        messageType.value = "success"
        newBranch.value = ""

        await load()
    } catch (error) {
        message.value = error.response?.data?.message || "Failed to add branch"
        messageType.value = "danger"
    }
}

async function deleteBranch(id) {

    try {
        if (!confirm("Delete this branch?"))
            return
        const res = await api.delete("/admin/branches/" + id)
        message.value = res.data.message
        messageType.value = "success"
        await load()
    }
    catch (error) {
        message.value =
            error.response?.data?.message ||
            "Unable to delete branch"
        messageType.value = "danger"
    }

}
</script>