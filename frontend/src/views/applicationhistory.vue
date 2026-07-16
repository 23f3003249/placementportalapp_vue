<template>
    <Navbar />
    <div class="container mt-4">
        <h4>Application History</h4>
        <table class="table table-bordered align-middle">
            <thead>
                <tr>
                    <td>Company</td>
                    <td>Drive</td>
                    <td>Status</td>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>ABC Pvt Ltd</td>
                    <td>SDE Intern</td>
                    <td>Applied</td>
                </tr>
                <tr>
                    <td>XYZ Pvt Ltd</td>
                    <td>Data Analyst</td>
                    <td>Rejected</td>
                </tr>
            </tbody>


        </table>
    </div>

</template>

<script setup>
import Navbar from '@/components/navbar.vue';

</script>