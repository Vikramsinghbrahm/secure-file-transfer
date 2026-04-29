import { createRouter, createWebHistory } from "vue-router";

import ActivityView from "../views/ActivityView.vue";
import FilesView from "../views/FilesView.vue";
import OverviewView from "../views/OverviewView.vue";
import WorkspaceView from "../views/WorkspaceView.vue";

const routes = [
  {
    path: "/",
    name: "overview",
    component: OverviewView,
    meta: {
      kicker: "Overview",
      title: "Transfer operations",
      description: "Session status, storage totals, and direct access to the main workflows.",
    },
  },
  {
    path: "/workspace",
    name: "workspace",
    component: WorkspaceView,
    meta: {
      kicker: "Workspace",
      title: "Workspace",
      description: "Authentication, session state, and upload actions.",
    },
  },
  {
    path: "/files",
    name: "files",
    component: FilesView,
    meta: {
      kicker: "Files",
      title: "Files and sharing",
      description: "Review stored artifacts, generate links, and revoke external access.",
    },
  },
  {
    path: "/activity",
    name: "activity",
    component: ActivityView,
    meta: {
      kicker: "Activity",
      title: "Activity",
      description: "Usage metrics and recent transfer events.",
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
