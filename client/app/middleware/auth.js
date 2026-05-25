export default defineNuxtRouteMiddleware(async (to) => {
  const authStore = useAuthStore();

  if (!authStore.user) {
    await authStore.fetchUser();
  }

  if (!authStore.isAuthenticated) {
    return navigateTo("/login", { replace: true });
  }
});
