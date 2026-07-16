<template>
    <Navbar />
    <div class="container mt-4">
        <div v-if="message" class="alert alert-danger">
            {{ message }}
        </div>
        <div v-if="loading" class="text-center mt-5">
            <div class="spinner-border"></div>
            <p class="mt-2">
                Loading details..
            </p>
        </div>

        <div v-else-if="item.title" class="card shadow-sm">
            <div class="card-header bg-primary text-white">
                <h4 class="mb-0">{{ item.title }}</h4>
            </div>
            <div class="card-body">
                <table class="table table-bordered">
                    <tbody>
                        <tr v-for="(value, key) in item.details" :key="key">
                            <th style="width: 35%"> {{ key }}</th>
                            <td>{{ value }}</td>
                        </tr>
                    </tbody>
                </table>
                <div class="d-flex gap-2">
                    <button v-if="
                        currentRole === 'student' &&
                        route.params.type === 'drive'
                    " class="btn btn-success" @click="applyDrive">
                        Apply
                    </button>
                    <button class="btn btn-secondary" @click="goBack">
                        Go Back
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>


<script setup>

import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import Navbar from "@/components/navbar.vue";
import api from "@/api/axios";


const route = useRoute();
const router = useRouter();

const item = ref({});
const currentRole = ref("");
const loading = ref(true);
const message = ref("");

onMounted(load);

async function load() {
    loading.value = true;
    message.value = "";
    item.value = {};
    try {
        const userResponse = await api.get("/auth/current-user");
        currentRole.value = userResponse.data.role;
        let endpoint = "";
        if (currentRole.value === "admin") {
            endpoint = `/admin/details/${route.params.type}/${route.params.id}`;
        }
        else if (
            currentRole.value === "student" &&
            route.params.type === "drive"
        ) {
            endpoint = `/student/drive/${route.params.id}`;
        }

        else {
            throw new Error("Details are not available");
        }

        const response = await api.get(endpoint);
        if (currentRole.value === "admin") {
            item.value = response.data;
        }

        else if (
            route.params.type === "drive"
        ) {
            const drive = response.data;
            item.value = {
                type: "drive",
                title: drive.title,
                details: {
                    "Company": drive.company,
                    "Job Title": drive.title,
                    "Description": drive.description,
                    "Eligible Branch": drive.branch,
                    "Minimum CGPA": drive.cgpa,
                    "Eligible Year": drive.year,
                    "Deadline": drive.deadline,
                    "Status": drive.status || "Approved",
                },
            };
        }
    }

    catch (error) {
        message.value = error.response?.data?.message || error.message || "Unable to load details";
    }
    finally {
        loading.value = false;
    }
}

async function applyDrive() {
    try {
        const response = await api.post(`/student/apply/${route.params.id}`);
        message.value = response.data.message;
        await load();
    }
    catch (error) {
        message.value = error.response?.data?.message || "Unable to apply";
    }
}

function goBack() {
    router.back();
}

</script>