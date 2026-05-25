import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", () => {
  const user = ref(null);
  const isLoading = ref(false);

  const accessToken = useCookie("cw_access_token", {
    maxAge: 60 * 300, // 300 minutes — matches backend ACCESS_TOKEN_LIFETIME
    path: "/",
    sameSite: "lax",
    secure: false, // set true in production behind HTTPS
  });

  const refreshToken = useCookie("cw_refresh_token", {
    maxAge: 60 * 60 * 24 * 3, // 3 days — matches backend REFRESH_TOKEN_LIFETIME
    path: "/",
    sameSite: "lax",
    secure: false,
  });

  const isAuthenticated = computed(() => !!accessToken.value && !!user.value);

  const { apiFetch } = useApiFetch();
  const { showPopup, showError } = usePopup();

  /**
   * POST /auth/login — obtain JWT pair and fetch user profile.
   */
  async function login(email, password) {
    isLoading.value = true;
    try {
      const data = await apiFetch("/auth/login", {
        method: "POST",
        body: { email, password },
      });

      accessToken.value = data.access;
      refreshToken.value = data.refresh;

      await fetchUser();
      showPopup("Welcome back!");
      return true;
    } catch (err) {
      showError(err, "Invalid email or password");
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * POST /auth/register — create account then auto-login.
   */
  async function register(email, password, confirmPassword) {
    isLoading.value = true;
    try {
      await apiFetch("/auth/register", {
        method: "POST",
        body: { email, password, confirm_password: confirmPassword },
      });

      // Auto-login: obtain tokens directly after successful registration
      const data = await apiFetch("/auth/login", {
        method: "POST",
        body: { email, password },
      });

      accessToken.value = data.access;
      refreshToken.value = data.refresh;

      await fetchUser();
      showPopup("Account created successfully!");
      return true;
    } catch (err) {
      showError(err, "Registration failed");
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * GET /auth/me — fetch the authenticated user profile.
   */
  async function fetchUser() {
    if (!accessToken.value) return;

    try {
      user.value = await apiFetch("/auth/me");
    } catch {
      // Token expired or invalid — clear everything
      logout();
    }
  }

  /**
   * Clear tokens and user state.
   */
  function logout() {
    accessToken.value = null;
    refreshToken.value = null;
    user.value = null;
    navigateTo("/login");
  }

  return {
    user,
    accessToken,
    refreshToken,
    isLoading,
    isAuthenticated,
    login,
    register,
    fetchUser,
    logout,
  };
});
