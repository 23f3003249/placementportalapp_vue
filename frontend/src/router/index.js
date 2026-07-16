import { createRouter, createWebHistory } from "vue-router";

import api from "@/api/axios";

import login from "../views/login.vue";
import register from "../views/register.vue";

import admindashboard from "../views/admindashboard.vue";
import companydashboard from "../views/companydashboard.vue";
import studentdashboard from "@/views/studentdashboard.vue";

import details from "@/components/details.vue";

import applicationhistory from "@/views/applicationhistory.vue";
import applicants from "@/views/applicants.vue";

const routes = [
  {
    path: "/",
    redirect: "/login",
  },
  {
    path: "/login",
    name: "Login",
    component: login,
  },
  {
    path: "/register",
    name: "Register",
    component: register,
  },
  {
    path: "/admindashboard",
    name: "Admindashboard",
    component: admindashboard,
    meta: {
      requiresAuth: true,
      role: "admin",
    },
  },
  {
    path: "/companydashboard",
    name: "Companydashboard",
    component: companydashboard,
    meta: {
      requiresAuth: true,
      role: "company",
    },
  },
  {
    path: "/studentdashboard",
    name: "Studentdashboard",
    component: studentdashboard,
    meta: {
      requiresAuth: true,
      role: "student",
    },
  },
  {
    path: "/details/:type/:id",
    name: "Details",
    component: details,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/history",
    name: "Applicationhistory",
    component: applicationhistory,
    meta: {
      requiresAuth: true,
      role: "student",
    },
  },
  {
    path: "/applicants/:id",
    name: "Applicants",
    component: applicants,
    meta: {
      requiresAuth: true,
      role: "company",
    },
  },
  {
    path: "/:pathMatch(.*)*",
    redirect: "/login",
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const ROLE_HOME = {
  admin: "/admindashboard",
  company: "/companydashboard",
  student: "/studentdashboard",
};

router.beforeEach(async (to) => {
  if (!to.meta.requiresAuth) {
    return true;
  }

  try {
    const response = await api.get("/auth/current-user");
    const user = response.data;

    if (!user?.role) {
      return "/login";
    }
    if (to.meta.role && user.role !== to.meta.role) {
      return ROLE_HOME[user.role] || "/login";
    }
    return true;
  } catch (error) {
    return "/login";
  }
});

export default router;
