export const useApiFetch = () => {
  const config = useRuntimeConfig();

  const apiFetch = (endpoint, options = {}) => {
    let accessToken = null;
    try {
      const authStore = useAuthStore();
      accessToken = authStore.accessToken;
    } catch (e) { }

    // Fallback 1: Nuxt Cookie Ref
    if (!accessToken) {
      try {
        accessToken = useCookie("cw_access_token").value;
      } catch (e) { }
    }

    // Fallback 2: Direct document.cookie parse
    if (import.meta.client && !accessToken) {
      const match = document.cookie.match(
        /(^|;)\s*cw_access_token\s*=\s*([^;]+)/,
      );
      if (match) {
        accessToken = match[2];
      }
    }

    let baseURL = (import.meta.server && config.apiBaseServer) ? config.apiBaseServer : config.public.apiBase;
    if (import.meta.client && baseURL.startsWith("http")) {
      baseURL = "/api";
    }

    return $fetch(endpoint, {
      baseURL,
      ...options,
      headers: {
        ...options.headers,
        ...(accessToken && { Authorization: `Bearer ${accessToken}` }),
      },
    });
  };

  return { apiFetch };
};
