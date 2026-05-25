export const usePopup = () => {
    const popups = useState("popups", () => [])

    function showPopup(message, type = "success") {
        const id = Date.now() + Math.random()

        popups.value.unshift({ id, message, type })

        setTimeout(() => {
            popups.value = popups.value.filter(p => p.id !== id)
        }, 4000)
    }

    function showError(err, fallback) {
        const message = Array.isArray(err?.data?.detail)
            ? err.data.detail.map(e => e.msg).join(', ')
            : err?.data?.detail || fallback || "Something went wrong"

        showPopup(message, "error")
    }

    function removePopup(id) {
        popups.value = popups.value.filter(p => p.id !== id)
    }

    return { popups, showPopup, removePopup, showError }
}